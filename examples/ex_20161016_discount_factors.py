"""
ex_20161016_discount_factors.py

Example code for discount factors.
"""
try:
    from simplepricers.utils import create_grid
except ImportError:
    import sys
    sys.path.append('..')
    from simplepricers.utils import create_grid

from plot_for_examples import Quick2DPlot


Quick2DPlot(create_grid(0., 2., 1), [1., 3., 2.])

opt = input('hit return to quit')
