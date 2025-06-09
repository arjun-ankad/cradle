#include <cmath>
#include <vector>
#include <algorithm>

// using the Coxx-Ross-Rubinstein binomial tree model for option pricing
double binomial_tree_price(
    char option_type, bool is_american,
    double S, double K, double T, double r, double sigma, int steps
) {
    double dt = T / steps;
    double u = std::exp(sigma * std::sqrt(dt));
    double d = 1.0 / u;
    double p = (std::exp(r * dt) - d) / (u - d);
    double discount = std::exp(-r * dt);

    std::vector<double> prices(steps + 1);
    std::vector<double> values(steps + 1);

    // Terminal payoffs
    for (int i = 0; i <= steps; ++i) {
        double ST = S * std::pow(u, steps - i) * std::pow(d, i);
        prices[i] = ST;
        values[i] = (option_type == 'C') ?
            std::max(0.0, ST - K) :
            std::max(0.0, K - ST);
    }

    // Backward induction
    for (int t = steps - 1; t >= 0; --t) {
        for (int i = 0; i <= t; ++i) {
            prices[i] = prices[i] / u;  // go back one step
            double cont_val = discount * (p * values[i] + (1 - p) * values[i + 1]);
            if (is_american) {
                double early_ex = (option_type == 'C') ?
                    std::max(0.0, prices[i] - K) :
                    std::max(0.0, K - prices[i]);
                values[i] = std::max(cont_val, early_ex);
            } else {
                values[i] = cont_val;
            }
        }
    }

    return values[0];
}
