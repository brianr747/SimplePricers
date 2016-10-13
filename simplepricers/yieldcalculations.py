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


def DF_exponential(mat, r):
    """
    DF_exponential(mat, r) - Discount factor, for a given maturity (years) and exponential zero rate r.
    :param mat: float
    :param r: float
    :return: float

    For example, calculate the exponential discount factor for a 5% zero rate after one year
    (rounded to 4 decimal places).
    >>> round(DF_exponential(1., .05), 4)
    0.9512
    """
    if type(mat) is list:
        out = [None, ] * len(mat)
        for i in range(0, len(mat)):
            out[i] = math.exp(-r[i] * mat[i])
    else:
        out = math.exp(-r * mat)
    return out


def ConvertRate(r_in, in_convention, out_convention):
    """
    ConvertRate - convert a rate from one convention to another

    Conventions specified by str. Supported:
    '1': Annual simple
    '2': Semiannual
    Under construction, only supports one conversion type for now!

    For example, convert 4% semiannual to annual.
    >>> round(ConvertRate(.04, '2', '1'), 4)
    0.0404

    :param r_in: float
    :param in_convention: str
    :param out_convention: str
    :return: float
    """
    if in_convention == '1':
        r_ann = r_in
    elif in_convention == '2':
        r_ann = pow(1 + r_in / 2., 2) - 1
    else:
        raise NotImplementedError('Unsupported rate convention')
    # Always convert to annual simple, then convert to target out
    # Currently, only support annual
    assert (out_convention == '1')
    return r_ann


def ZRfromDF(mat, df):
    """
    ZRfromDF(mat, df) - Zero Rate from Discount Factor

    Not implemented yet!

    >>> out = ZRfromDF(1., .95)
    Traceback (most recent call last):
    ...
    NotImplementedError: Under construction!

    :param mat: float
    :param DF: float
    :return: float
    """
    raise NotImplementedError('Under construction!')
