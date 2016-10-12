"""
yieldcalculations.py

Basic interest rate calculations.

Copyright 2016 Brian Romanchuk

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import math


def DF(mat, r):
    """
    DF(mat, r) - Discount factor, for a given maturity (years) and zero rate r.
    :param mat: float
    :param r: float
    :return: float

    May also input equally-sized lists.

    For example, calculate the discount factor for a 5% zero rate after one year
    (rounded to 4 decimal places).
    >>> round(DF(1., .05), 4)
    0.9524

    Example with list inputs. Maturities from 0 - 5 years, flat zero rate of 5%
    >>> mats = []
    >>> zerorates = []
    >>> for i in range(0, 6):
    ...     mats.append(float(i))
    ...     zerorates.append(.05)
    ...
    >>> out = DF(mats, zerorates)
    >>> [round(x, 4) for x in out] # Round to 4 decimal places
    [1.0, 0.9524, 0.907, 0.8638, 0.8227, 0.7835]
    """
    if type(mat) is list:
        out = []
        for m, ZR in zip(mat, r):
            out.append(math.pow(1. + ZR, -m))
    else:
        out = math.pow(1. + r, -mat)
    return out

def ZRfromDF(mat, DF):
    """
    ZRfromDF(mat, DF) - Zero Rate from Discount Factor

    :param mat: float
    :param DF: float
    :return: float
    """
    pass