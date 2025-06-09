#include <cmath>
#include "black_scholes.h"

double delta(char opt, double S, double K, double T, double r, double sigma) {
    double h = 0.01;
    return (black_scholes_price(opt, S + h, K, T, r, sigma) -
            black_scholes_price(opt, S - h, K, T, r, sigma)) / (2 * h);
}

double gamma(char opt, double S, double K, double T, double r, double sigma) {
    double h = 0.01;
    return (black_scholes_price(opt, S + h, K, T, r, sigma) -
            2 * black_scholes_price(opt, S, K, T, r, sigma) +
            black_scholes_price(opt, S - h, K, T, r, sigma)) / (h * h);
}

double vega(char opt, double S, double K, double T, double r, double sigma) {
    double h = 0.01;
    return (black_scholes_price(opt, S, K, T, r, sigma + h) -
            black_scholes_price(opt, S, K, T, r, sigma - h)) / (2 * h);
}

double theta(char opt, double S, double K, double T, double r, double sigma) {
    double h = 1.0 / 365;  // 1 day
    return (black_scholes_price(opt, S, K, T + h, r, sigma) -
            black_scholes_price(opt, S, K, T - h, r, sigma)) / (2 * h);
}

double rho(char opt, double S, double K, double T, double r, double sigma) {
    double h = 0.01;
    return (black_scholes_price(opt, S, K, T, r + h, sigma) -
            black_scholes_price(opt, S, K, T, r - h, sigma)) / (2 * h);
}