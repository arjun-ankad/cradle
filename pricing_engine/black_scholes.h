// black_scholes.h
#ifndef BLACK_SCHOLES_H
#define BLACK_SCHOLES_H

// Computes the cumulative distribution function of the standard normal distribution
double normal_cdf(double x);

// Computes the Black-Scholes price for European call ('C') or put ('P') options
// Parameters:
// option_type: 'C' for Call, 'P' for Put
// S: Spot price of the underlying asset
// K: Strike price
// T: Time to expiration in years
// r: Risk-free interest rate
// sigma: Volatility of the underlying asset
double black_scholes_price(char option_type, double S, double K, double T, double r, double sigma);

#endif // BLACK_SCHOLES_H