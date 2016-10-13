"""
ex_20161016_discount_factors.py

Example code for discount factors.
"""

from simplepricers.utils import create_grid

from plot_for_examples import Quick2DPlot


Quick2DPlot(create_grid(0., 2., 1), [1., 3., 2.])
