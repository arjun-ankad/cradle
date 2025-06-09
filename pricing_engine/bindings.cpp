#include <pybind11/pybind11.h>
#include "black_scholes.h"


double monte_carlo_price(char, double, double, double, double, double, int);
double binomial_tree_price(char, bool, double, double, double, double, double, int);
double lsmc_price_put(double, double, double, double, double, int, int);

double delta(char, double, double, double, double, double);
double gamma(char, double, double, double, double, double);
double vega(char, double, double, double, double, double);
double theta(char, double, double, double, double, double);
double rho(char, double, double, double, double, double);

namespace py = pybind11;

PYBIND11_MODULE(asset_models, m) {
    m.def("black_scholes_price", &black_scholes_price);
    m.def("monte_carlo_price", &monte_carlo_price);
    m.def("binomial_tree_price", &binomial_tree_price);
    m.def("lsmc_price_put", &lsmc_price_put);

    m.def("delta", &delta);
    m.def("gamma", &gamma);
    m.def("vega", &vega);
    m.def("theta", &theta);
    m.def("rho", &rho);
}