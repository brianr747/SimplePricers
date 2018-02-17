"""
bonds_curves.py

Bond and curve calculations.

Documentation comments refer to:

[Faboozzi 2000] "Fixed Income Analysis for the Chartered Financial Analyst Program,
        2000, ISBN 1-883249-83-X.


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
import simplepricers.yieldcalculations as yc
from simplepricers.yieldcalculations import DF
from simplepricers.simple_calendar import Indexation


class Bond(object):
    """
    Bond - Abstract base class for bonds.
    """

    def __init__(self, mat=None, coupon=None, coupon_freq=None, now=0.):
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

    def CalcDuration(self, yld, now=None, yield_convention='bond'):
        """
        CalcDuration - Calculate the duration with yield shocks.

        For example, calculate for a 9% 20-year bond at 6%. Based on [Fabozzi2000, page 256]
        >>> obj = CouponBond(20., .09, 2)
        >>> dur = obj.CalcDuration(.06)
        >>> round(dur,2)
        10.66

        :param yld: float
        :param now: float
        :param yield_convention: str
        :return: float
        """
        bp = .0001
        p_orig = self.GetPrice(yld, now, price_type='dirty', yield_convention=yield_convention)
        p_up = self.GetPrice(yld + bp, now, price_type='dirty', yield_convention=yield_convention)
        p_dn = self.GetPrice(yld - bp, now, price_type='dirty', yield_convention=yield_convention)
        return (p_dn - p_up) / (2. * p_orig * bp)


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

    def GetPrice(self, yld, now=None, price_type='clean', yield_convention='bond'):
        """
        GetPrice - Returns the price.

        Under construction, only supports: price_type='dirty', yield_convention='bond'
        Note: that this forces you to specify price='dirty', even though clean prices
        are not yet supported! (This way we future-proof code.)

        A 4-year 10% coupon bond, at a 8% yield
        (From  [Fabozzi2000] pages 155-6.)
        >>> obj = CouponBond(4., .10, coupon_freq=2)
        >>> price = obj.GetPrice(.08, price_type='dirty')
        >>> round(price, 4)
        106.7327

        A 4 year, 10% annual coupon bond, with 12% yield.
        (Also from Fabozzi, pages 150-151.)
        >>> obj = CouponBond(4., .10, coupon_freq=1)
        >>> price = obj.GetPrice(.12, price_type='dirty')
        >>> round(price, 4)
        93.9253

        :param yld: float
        :param now: float
        :param price_type: str
        :param yield_convention: str
        :return: float
        """
        if yield_convention != 'bond':
            raise NotImplementedError('Unsupported yield_convention')
        if price_type != 'dirty':
            raise NotImplementedError('Unsupported price_type convention')
        if self.CouponFrequency == 2:
            yld = yc.ConvertRate(yld, '2', '1')
        self.GenerateCashFlows(now)
        NPV = 0.
        df = yc.DF(self.CashFlowDates, [yld, ] * len(self.CashFlowDates))
        for i in range(0, len(self.CashFlows)):
            NPV += df[i] * self.CashFlows[i]
        return NPV

    def GetYield(self, now, price, price_type='clean', yield_convention='bond', guess=(0., .25), toler=1e-6):
        """
        Ugly yield calculation...
        :param now: float
        :param price: float
        :param price_type: str
        :param yield_convention: str
        :param guess: tuple
        :return: float
        """
        if yield_convention != 'bond':
            raise NotImplementedError('Unsupported yield_convention')
        if price_type != 'dirty':
            raise NotImplementedError('Unsupported price_type convention')

        self.GenerateCashFlows(now)

        def get_price(y):
            NPV = 0.
            df = yc.DF(self.CashFlowDates, [y, ] * len(self.CashFlowDates))
            for i in range(0, len(self.CashFlows)):
                NPV += df[i] * self.CashFlows[i]
            return NPV

        low, high = guess[0:2]
        price_lo = get_price(low)
        price_hi = get_price(high)
        # Yield downn, price up!
        if not (price < price_lo) and (price > price_hi):
            raise ValueError('Answer not bracketed by guess!')
        yld = (low + high) / 2.
        while (high-low) > toler:
            yld = (low + high) / 2.
            estimate = get_price(yld)
            if price > estimate:
                # Estimated price is too low -> yield too high
                high = yld
            else:
                low = yld
        if self.CouponFrequency == 2:
            yld = yc.ConvertRate(yld, '1', '2')
        return yld


    def GetPriceFromZeroCurve(self, now, ZC, price_type='clean'):
        """
        Get the fair value off of a ZeroCurve object.

        Although price_type only supports 'dirty' for now. Left this way to future-proof code.

        :param now: float
        :param ZC: ZeroCurve
        :param price_type: str
        :return: float
        """
        if price_type != 'dirty':
            raise NotImplementedError('Unsupported price_type convention')
        self.GenerateCashFlows(now)
        NPV = 0.
        df = [ZC.GetDF(x) for x in self.CashFlowDates]
        for i in range(0, len(self.CashFlows)):
            NPV += df[i] * self.CashFlows[i]
        return NPV


class InflationLinkedBond(CouponBond):
    def __init__(self, mat=None, coupon=None, coupon_freq=1, now=0., issue_date=0.):
        super().__init__(mat, coupon, coupon_freq, now)
        self.InflationCurve = Indexation()
        self.InflationCurve.SetIndexValues([issue_date], [1.])

    def CalcEconomicBreakeven(self, now, price, ZC, price_type='clean', toler=.00001, guess=(-.05,.1)):
        if not price_type=='dirty':
            raise NotImplementedError('Only dirty price supported')
        lo, hi = guess[0:2]
        self.GenerateCashFlows(now)

        DF = [ZC.GetDF(x) for x in self.CashFlowDates]

        def get_NPV(inf):
            self.InflationCurve.ExtrapolationRate = inf
            NPV = 0.0
            for d, cf, d_df in zip(self.CashFlowDates, self.CashFlows, DF):
                NPV += d_df * cf * self.InflationCurve.GetValue(d)
            return NPV

        mid = (hi + lo)/2.
        if lo >= hi:
            raise ValueError('Invalid initial guess!')
        while (hi-lo) > toler:
            mid = (hi + lo) / 2.
            NPV = get_NPV(mid)
            if NPV > price:
                # NPV too high -> guess too high -> hi=mid
                hi = mid
            else:
                lo = mid
        return mid




class ZeroCurve(object):
    """
    ZeroCurve object - handles basic nominal discounting

    Uses the simple interest rate convention.
    """
    def __init__(self, mats=(), ZC=()):
        """
        Initialise the ZeroCurve
        :param ZC: list
        :param mats: list
        """
        if not len(ZC) == len(mats):
            raise ValueError('Zero curve and maturities must be equal length')
        self.ZC = list(ZC)
        self.Maturities = list(mats)

    def GetZeroRate(self, mat):
        """
        Get the zero rate at a particular maturity point, must be interior.
        Note that if shortest maturity > 0, we use it for all maturities up to that point as well.

        Note that we assume that the maturity list is sorted
        :param mat: float
        :return: float
        """
        if mat < 0:
            raise ValueError('Negative maturity - fail')
        if mat > self.Maturities[-1]:
            raise ValueError('Maturity longer than longest zero maturity')
        if mat <= self.Maturities[0]:
            return self.Maturities[0]
        prev_mat = self.Maturities[0]
        prev_zero = self.ZC[0]
        # We already tested for the shortest maturity
        for pos in range(1, len(self.Maturities)):
            if self.Maturities[pos] == mat:
                return self.ZC[pos]
            if self.Maturities[pos] > mat:
                fac = (mat - prev_mat)/(self.Maturities[pos] - prev_mat)
                return ((1-fac)*prev_zero) + (fac*self.ZC[pos])
            prev_mat = self.Maturities[pos]
            prev_zero = self.ZC[pos]

    def GetDF(self, mat):
        """
        Return the associated discount factor for a maturity.
        Assumes that the maturity list is sorted.
        :param mat: float
        :return: float
        """
        r = self.GetZeroRate(mat)
        return DF(mat, r)

    def CalcParCoupon(self, mat, coupon_freq=1, toler=.000001, guess=(None,None)):
        if not(mat==round(mat)):
            raise NotImplementedError('Non-integer maturities not supported yet')
        # Set bounds; hopefully conservative enough
        lo, hi = guess[0:2]
        if lo is None:
            lo = min(self.ZC)-.01
        if hi is None:
            hi = max(self.ZC)+.01
        if lo > hi:
            raise ValueError('Bad Guess')
        # Assume bounds are OK. TODO: validate guess
        # This line is redundant, but the code validation is unhappy if it missing
        mid = (lo + hi)/2.
        price = 0.
        bond = CouponBond(mat, coupon=mid, coupon_freq=coupon_freq)
        while (hi-lo)>toler:
            mid = (lo+hi)/2.
            bond.Coupon = mid
            # Since we only have dirty prices, that is why we assume an integer number of years
            price = bond.GetPriceFromZeroCurve(0, self, price_type='dirty')
            if price > 100.:
                # coupon is too high, so mid becomes upper bound
                hi = mid
            else:
                lo = mid
        if abs(price-100.) > .001:
            raise ValueError('Initial guess range does not cover actual value')
        return mid