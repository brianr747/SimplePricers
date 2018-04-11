"""
ex20180411_bootstrapping_problem.py

Generates a plot used to illustrate problems with bootstrapping.

Uses SciPy for convenience, doesn't use any library code.
"""

import scipy.interpolate
import numpy

import simplepricers.Quick2DPlot as Q2D

# First: set up zero curve
t_orig = [0., 1., 2., 2.25, 3.0, 4., 6., 10.]
y_orig = [.019, .019, .023, .0195, .025, .026, .0255, .024]

interp = scipy.interpolate.interp1d(t_orig, y_orig)
t = numpy.linspace(0, 10, num=41)
y = interp(t)

Q2D.Quick2DPlot(t, y, title='Zero Inflation Curve', filename='bootstrapping1.png', marker=None)

# Calculate the discount factors
df = 1. / (1. + y)**t
Q2D.Quick2DPlot(t, df)

# forward factors
f = (df[0:40])/(df[1:41])
Q2D.Quick2DPlot(t[1:41], f)

forward = (f**4) - 1
Q2D.Quick2DPlot(t[1:41], forward, title='Forward Curve', filename='bootstrapping2.png', marker=None)
