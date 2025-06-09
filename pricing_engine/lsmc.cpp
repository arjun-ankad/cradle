#include <Eigen/Dense>
#include <vector>
#include <cmath>
#include <random>
#include <algorithm>
#include <numeric>

using std::vector;

double lsmc_price_put( double S0, double K, double r, double sigma, double T, int N, int M ) {
    double dt = T / N;
    std::mt19937_64 rng;
    std::normal_distribution<> norm(0.0, 1.0);

    vector<vector<double>> paths(M, vector<double>(N + 1));
    
    // Simulate the price paths
    for (int i = 0; i < M; ++i) {
        paths[i][0] = S0;
        for (int t = 1; t <= N; ++t) {
            double Z = norm(rng);
            paths[i][t] = paths[i][t - 1] * std::exp((r - 0.5 * sigma * sigma) * dt + sigma * std::sqrt(dt) * Z);
        }
    }

    vector<double> cashflows(M);
    for (int i = 0; i < M; ++i)
        cashflows[i] = std::max(K - paths[i][N], 0.0);

    // Working backwards
    for (int t = N - 1; t >= 1; --t) {
        vector<int> in_the_money;
        vector<double> x, y;

        for (int i = 0; i < M; ++i) {
            double St = paths[i][t];
            double payoff = std::max(K - St, 0.0);
            if (payoff > 0) {
                in_the_money.push_back(i);
                x.push_back(St);
                y.push_back(cashflows[i] * std::exp(-r * dt));
            }
        }

        // Regression: E[continuation value | St]
        int n = x.size();
        if (n > 0) {
            Eigen::MatrixXd A(n, 3);
            Eigen::VectorXd b(n);

            for (int i = 0; i < n; ++i) {
                A(i, 0) = 1.0;
                A(i, 1) = x[i];
                A(i, 2) = x[i] * x[i];
                b(i) = y[i];
            }

            Eigen::VectorXd coeffs = A.colPivHouseholderQr().solve(b);

            for (int i = 0; i < n; ++i) {
                double cont_val = coeffs(0) + coeffs(1) * x[i] + coeffs(2) * x[i] * x[i];
                double immediate = std::max(K - x[i], 0.0);
                if (immediate > cont_val) {
                    cashflows[in_the_money[i]] = immediate;
                } else {
                    cashflows[in_the_money[i]] *= std::exp(-r * dt);
                }
            }
        }
    }

    // Averaging discounted cashflows
    double price = std::accumulate(cashflows.begin(), cashflows.end(), 0.0) / M;
    return price * std::exp(-r * dt);
}
