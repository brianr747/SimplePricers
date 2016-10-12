"""
utils.py

Utility functions for the simplepricers package.

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


def create_grid(start, stop, frequency):
    """
    create_grid - returns an evenly grid in a list, with a number of points per year
    equal to the frequency. For example, frequency = 2 means semiannual.

    For example, create an annual grid from years 0 -> 5 (inclusive)
    >>> create_grid(0., 5., 1)
    [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]

    Create a semi-annual grid with frequency = 2
    >>> create_grid(0., 2., 2)
    [0.0, 0.5, 1.0, 1.5, 2.0]

    Negative time is allowed.
    >>> create_grid(-1., 0, 4)
    [-1.0, -0.75, -0.5, -0.25, 0.0]

    Note that dates are aligned to the start date, and if the end point is not an even number of
    time steps from the start, the interval terminates at the last equally-spaced point before the
    stop point.
    >>> create_grid(10., 11.1, 1)
    [10.0, 11.0]
    >>> create_grid(10., 11.6, 2)
    [10.0, 10.5, 11.0, 11.5]

    Raises a ValueError if the stop point is before the start point.
    >>> create_grid(1., 0., 1)
    Traceback (most recent call last):
    ...
    ValueError: Stop point must be after start

    :param start: float
    :param stop: float
    :param frequency: int
    :return: list
    """
    if stop < start:
        raise ValueError('Stop point must be after start')
    frequency = float(frequency)
    interval = int(frequency * (stop - start))
    #  Generate an integer grid
    out = range(0, interval + 1)
    # return to original time interval as floats
    return [start + float(x) / frequency for x in out]
