"""
simple_calendar.py

This is an utterly hopeless calendar system, that in no way should be let near real-world pricing
applications.

Although we could later define a date object, dates for internal calculations are real numbers, with 1.0
equalling one year. This is good enough for really simple yield and price calculations.

We fall flat on our faces once we start to interact with index-linked bonds. So I am creating a simple
calendar to simulate the principles of index-linked calculations -- without doing them correctly (oops).

Copyright 2018 Brian Romanchuk

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

class SimpleCalendar360(object):
    """
    This class holds the functions for a calendar that consists of:
    (1) 12 months
    (2) 30 days per month.
    The day/month determines the fractional offset from the year.

    Day/month are "1-based," like the real world.

    "January 1" is associated with an offset of zero. So the date 1976.0 is "January 1, 1976."

    """
    def __init__(self):
        self.NumMonths = 12.
        self.NumDaysPerMonth = 30.
        self.NumDaysPerYear = self.NumMonths * self.NumDaysPerMonth

    def GetDate(self, year, month=1, day=1):
        """
        Returns the
        :param year: int
        :param month: int
        :param day: int
        :return: float
        """
        return float(year) + (float(month-1)/self.NumMonths) + (float(day-1) / self.NumDaysPerYear)

    def AddMonths(self, date, num_months):
        """
        Shift a date by a number of months
        :param date: float
        :param num_months: int
        :return: float
        """
        # NOTE: If we get rounding issues, could do modulo-12.
        return date + (float(num_months)/self.NumMonths)


class Indexation(object):
    """
    Class that manages simple indexation calculations.

    Probably should be done with numeric array objects, but stick with lists for now.

    I want this code to be very easy to understand, with no worries about performance.
    """

    def __init__(self):
        self.Calendar = SimpleCalendar360()
        self.IndexDateValues = []

    def SetIndexValues(self, dates, values):
        """
        Add two lists of dates/values to the
        :param dates: list
        :param values: list
        :return:
        """
        if not len(dates) == len(values):
            raise ValueError('dates and values vectors not the same size')
        # Not sure how to do this efficiently, do it brute force style
        self.IndexDateValues = []
        # Save the data as tuples
        for d,v in zip(dates, values):
            self.IndexDateValues.append((d, v))
        self.IndexDateValues.sort()

    def GetValue(self, date):
        """
        Return the index value for a date
        :param date: float
        :return: float
        """
        if len(self.IndexDateValues) == 0:
            raise ValueError('No index data in object')
        if date < self.IndexDateValues[0][0]:
            raise ValueError('Date before start of index data')
        prev_d, prev_v = self.IndexDateValues[0]
        # Go through the index points, which we assume are ordered.
        for d,v in self.IndexDateValues:
            # Special case, we hit the new point exactly.
            # This also covers the special case where the date matches the first index date exactly
            if d == date:
                return v
            # Is date in the interval [prev_d, d]?
            if date < d:
                # Interpolate
                fac = (date - prev_d)/(d - prev_d)
                return prev_v + fac*(v - prev_v)
            # Otherwise, keep going
            prev_d = d
            prev_v = v
        # If we get here, we are outside the interval
        # TODO: Add an extrapolation feature.
        raise ValueError('Date greater than index data')



