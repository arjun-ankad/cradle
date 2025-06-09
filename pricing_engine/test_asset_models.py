import asset_models

# Black-Scholes Call
price = asset_models.black_scholes_price('C', 100, 100, 1.0, 0.05, 0.2)
print("Black-Scholes Call:", price)

# Greeks
print("Delta:", asset_models.delta('C', 100, 100, 1.0, 0.05, 0.2))
print("Vega:", asset_models.vega('C', 100, 100, 1.0, 0.05, 0.2))

# Monte Carlo Call
print("Monte Carlo Call:", asset_models.monte_carlo_price('C', 100, 100, 1.0, 0.05, 0.2, 100000))

# Binomial Tree
print("Binomial Tree Put (American):", asset_models.binomial_tree_price('P', True, 100, 100, 1.0, 0.05, 0.2, 100))

# LSMC (American Put)
print("LSMC American Put:", asset_models.lsmc_price_put(100, 100, 0.05, 0.2, 1.0, 50, 10000))
