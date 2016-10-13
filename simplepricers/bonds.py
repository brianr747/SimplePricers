"""
bonds.py

Bond calculations.

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

from simplepricers.utils import create_grid


class Bond(object):
    """
    Bond - Abstract base class for bonds.
    """

    def __init__(self, mat=None, coupon=None, coupon_freq=None, now=None):
        """
        Set parameters for the bond.

        Coupon convention: .04 = 4% coupon.
        (Which is a lousy match against the $100 price convention.)
        This potential convention consistency may need to be looked at.

        Only expect to support coupon_freq equal to 1 or two.

        :param mat: float
        :param coupon: float
        :param coupon_freq: int
        :param now: float
        """
        self.Maturity = mat
        self.Coupon = coupon
        self.CouponFrequency = coupon_freq
        self.Now = now
        self.PriceBase = 100.
        self.CashFlows = None
        self.CashFlowDates = None

    def GetPrice(self, yld, now=None, price_type='dirty', yield_convention='bond'):  # pragma: no cover
        """
        Get the price. If now is None (default), uses the existing 'now' setting.

        :param yld: float
        :param now: float
        :param price_type: str
        :param yield_convention: str
        :return: float
        """
        pass


class Consol(Bond):
    """
    Consol - Perpetual bond. Can only support a couple operations.
    Only supports annual coupon.

    Assumes that coupons are paid exactly at the beginning of year (now has no
    fractional part). So now = 0. or 2016, is OK, but 2016.5 will blow up.
    >>> Consol(.05, now=2016.5)
    Traceback (most recent call last):
    ...
    ValueError: Consol calculations assume that we are on a coupon payment date.
    """

    def __init__(self, coupon, now=0.):
        self.CheckCouponDate(now)
        Bond.__init__(self, mat='InfinityAndBeyond!', coupon=coupon, coupon_freq=1, now=now)

    @staticmethod
    def CheckCouponDate(now):
        """CheckCouponDate - are we on a coupon date. Throws an exception if false."""
        if math.floor(now) != now:
            raise ValueError('Consol calculations assume that we are on a coupon payment date.')

    def GetPrice(self, yld, now=None, price_type='dirty', yield_convention='bond'):
        """
        Get the price. If now is None (default), uses the existing 'now' setting.

        Price is based on face value of 100.

        Currently assumes that we are on a coupon date, and so the dirty price equals
        the clean price.

        Get the price of a 2% consol at a yield of 4%. (Bond yield convention, which matches
        the coupon frequency - annual.)
        >>> obj = Consol(.02)
        >>> price = obj.GetPrice(.04)
        >>> "%.2f" % (price,)  # display to 2 decimal places
        '50.00'

        :param yld: float
        :param now: float
        :param price_type: str
        :param yield_convention: str
        :return: float
        """
        if now is None:
            now = self.Now
        self.CheckCouponDate(now)
        if yield_convention != 'bond':
            raise NotImplementedError('Unsupported yield convention!')
        if self.Coupon is None:
            raise ValueError('Must set the coupon before calling GetPrice()')
        return self.PriceBase * self.Coupon / yld


class CouponBond(Bond):
    def GenerateCashFlows(self, now=None):
        """
        Generate the cash flow vector.
        TODO: Optimise this so that recalculation only occurs if 'now' changes.

        :param now: float
        :return: None
        """
        if now is None:
            now = self.Now
        # TODO: Do an optimisation to skip recalculation.
        self.Now = now
        if self.Now is None:
            raise ValueError('Must set ''now'' to calculate cash flows.')
        # deal with corner case of being beyond maturity date.
        if self.Now >= self.Maturity:
            self.CashFlows = []
            self.CashFlowDates = []
            return
        # Generate the time axis with create_grid. The trick is that create_grid aligns the
        # grid to the start date. We need to align the grid to maturity. We accomplish this by
        # multiplying by -1.  (Try doing that with calendar dates!)
        minus_t = create_grid(-self.Maturity, -self.Now, self.CouponFrequency)
        # Go back to positive time...
        self.CashFlowDates = [-x for x in minus_t]
        self.CashFlowDates.reverse()
        # if on top of a payment, pop it out.
        if self.Now == self.CashFlowDates[0]:
            self.CashFlowDates.pop(0)
        coupon_payment = self.PriceBase * self.Coupon / self.CouponFrequency
        # This creates an empty list if we only have a single payment
        self.CashFlows = [coupon_payment] * (len(self.CashFlowDates) - 1)
        self.CashFlows.append(self.PriceBase + coupon_payment)

    def GetPrice(self, yld, now=None, price_type='dirty', yield_convention='bond'):
        self.GenerateCashFlows(now)
