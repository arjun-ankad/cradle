from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext
import os

ext_modules = [
    Pybind11Extension(
        "asset_models",
        [
            "bindings.cpp",
            "black_scholes.cpp",
            "greeks.cpp",
            "binomial_tree.cpp",
            "monte_carlo.cpp",
            "lsmc.cpp"
        ],
        include_dirs=[
            ".",  # current folder for your own headers
            "/opt/homebrew/include/eigen3"  # <- Add Eigen's include path here
        ],
        cxx_std=17,
    ),
]

setup(
    name="asset_models",
    version="0.1",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)
