#include <cmath>
#include <random>

double monte_carlo_price(char option_type, double S, double K, double T, double r, double sigma, int num_sims) {
    std::mt19937_64 rng;
    std::normal_distribution<> norm(0.0, 1.0);

    double payoff_sum = 0.0;
    for (int i = 0; i < num_sims; ++i) {
        double Z = norm(rng);
        double ST = S * std::exp((r - 0.5 * sigma * sigma) * T + sigma * std::sqrt(T) * Z);
        // Calculate the payoff based on the option type
        if (option_type == 'C') {
            payoff_sum += std::max(0.0, ST - K);
        } else {
            payoff_sum += std::max(0.0, K - ST);
        }
    }

    double discounted_payoff = (payoff_sum / num_sims) * std::exp(-r * T);
    return discounted_payoff;
}
