"""
recession_random_walk.py

This file has nothing to do with pricing applications, it's just code that generates charts
for a random walk simulation of recessions. The explanation of what I am doing will appear in an
article on my website, and in my upcoming book on recessions.
"""

import random
from statistics import mean
import math

from examples.plot_for_examples import Quick2DPlot

N = 240
t = list(range(0,N))

t_float = [float(x)/12. for x in t]

# force the seed to always give the same results
seed = input('Choose seed value (plotted example uses 0) > ')

random.seed(float(seed))


# FIRST: We generate a state variable that transitions between a "high growth" and a "low growth" state.
# 1 = high growth
# 0 = low growth

def state_transition(state):
    if state == 1:
        if random.random() < .98:
            return 1
        else:
            return 0
    if state == 0:
        if random.random() < .96:
            return 0
        else:
            return 1


# Generate the state transition series
state = [1]
for i in range(1,N):
    state.append(state_transition(state[-1]))

#-----------------------------------
# Generate "GDP growth"
# g = current month GDP growth, annualised. Start at 2.5%
g = 2.5
# Create a vector that will be the time series.
growth = [g]

for i in range(1,N):
    # Set the reversion level based on the current state.
    if state[i] == 1:
        revert = 2.5
    else:
        revert = .75
    # New growth = old growth + .25* (deviation from reversion level) + normally distributed noise.
    g = g + .25*(revert - g) + random.normalvariate(0,.8)
    growth.append(g)

def cheating_MA(ser):
    """
    DO a six-month MA, cheat on the first six months.
    :param ser:
    :return:
    """
    out = []
    for i in range(0, len(ser)):
        if i <= 5:
            out.append(mean(ser[0:i+1]))
        else:
            cut = ser[i-5:i+1]
            if not len(cut) == 6:
                print(cut)
                raise ValueError('Coding problem')
            out.append(mean(cut))
    return out


# Quick2DPlot(t_float,state)
# Plot the moving average, since the raw growth rate is very noisy.
# Since we are used to looking at year-on-year growth rates, this looks more
# plausible.
p = Quick2DPlot([t_float, t_float], [cheating_MA(growth), state], 'Random Walk Growth', run_now=False)
p.Legend = ['Growth(6-mo MA)', 'State']
p.OutputDirectory = 'figures'
p.DPI = 300
p.FileName = 'recession_random_walk.png'

p.DoPlot()

for x,y,z in zip(t_float, state, cheating_MA(growth)):
    print(x, y, z)



