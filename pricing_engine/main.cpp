#include <iostream>
#include "black_scholes.h"
#include "monte_carlo.cpp"
#include "lsmc.cpp"
#include "binomial_tree.cpp"
#include "greeks.cpp"

int main() {
    // Sample input for European Call
    double S = 100.0;      // Spot price
    double K = 100.0;      // Strike price
    double T = 1.0;        // Time to maturity (1 year)
    double r = 0.05;       // Risk-free rate
    double sigma = 0.2;    // Volatility
    double num_sims = 100000; // Number of simulations for Monte Carlo
    int num_steps = 100; // Number of time steps for LSMC
    

    double call_price = black_scholes_price('C', S, K, T, r, sigma);
    // double put_price = black_scholes_price('P', S, K, T, r, sigma);
    double monte_carlo_call_price = monte_carlo_price('C', S, K, T, r, sigma, num_sims);
    // double monte_carlo_put_price = monte_carlo_price('P', S, K, T, r, sigma, num_sims);
    double lsmc_put_price = lsmc_price_put(S, K, r, sigma, T, num_steps, num_sims);

    std::cout << "Black-Scholes Call Price: " << call_price << std::endl;
    // std::cout << "Black-Scholes Put Price: " << put_price << std::endl; 
    std::cout << "Monte Carlo Call Price: " << monte_carlo_call_price << std::endl;
    // std::cout << "Monte Carlo Put Price: " << monte_carlo_put_price << std::endl;
    std::cout << "LSMC American Put Price: " << lsmc_put_price << std::endl;
       
    std::cout << "Binomial Tree Call (European): " << binomial_tree_price('C', false, S, K, T, r, sigma, 100) << "\n";
    std::cout << "Binomial Tree Put (American):  " << binomial_tree_price('P', true, S, K, T, r, sigma, 100) << "\n";

    return 0;
}