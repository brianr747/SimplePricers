"""
test_bonds.py

Note that some tests are done as doctests.
"""

from unittest import TestCase
import doctest

from simplepricers.bonds_curves import Consol, ZeroCurve
from simplepricers.bonds_curves import CouponBond
import simplepricers.bonds_curves as bonds
from simplepricers.bonds_curves import ZeroCurve


def load_tests(loader, tests, ignore):
    """
    Load doctests, so unittest discovery can find them.
    """
    tests.addTests(doctest.DocTestSuite(bonds))
    return tests


class TestConsol(TestCase):
    def test_ctor(self):
        obj = Consol(.05)
        self.assertEqual(.05, obj.Coupon)

    def test_GetPrice_no_coupon(self):
        with self.assertRaises(NotImplementedError):
            obj = Consol(.05)
            obj.GetPrice(.04, yield_convention='semiannual')

    def test_GetPrice_NoCoupon(self):
        with self.assertRaises(ValueError):
            obj = Consol(.05)
            obj.Coupon = None
            obj.GetPrice(.05)


class TestCouponBond(TestCase):
    def test_GenerateCashFlows(self):
        # 2-year 5% coupon - annual
        obj = CouponBond(2., .05, coupon_freq=1)
        obj.GenerateCashFlows(now=0.)
        self.assertEqual(obj.CashFlowDates, [1., 2.])
        self.assertEqual(obj.CashFlows, [5., 105.])

    def test_GenerateCashFlows_now_set(self):
        # 2-year 5% coupon - annual
        obj = CouponBond(2., .05, coupon_freq=1)
        obj.Now = None
        with self.assertRaises(ValueError):
            obj.GenerateCashFlows()

    def test_GenerateCashFlows_future(self):
        # 2-year 5% coupon - annual
        obj = CouponBond(2., .05, coupon_freq=1)
        obj.GenerateCashFlows(now=2.)
        self.assertEqual(obj.CashFlowDates, [])
        self.assertEqual(obj.CashFlows, [])

    def test_GetPrice_fail_yield(self):
        obj = CouponBond(2., .05, coupon_freq=1)
        with self.assertRaises(NotImplementedError):
            obj.GetPrice(.02, price_type='dirty', yield_convention='semiannual')

    def test_GetPrice_fail_price(self):
        obj = CouponBond(2., .05, coupon_freq=1)
        with self.assertRaises(NotImplementedError):
            obj.GetPrice(.02, price_type='clean')

    def test_yield1(self):
        obj = CouponBond(2., .05, coupon_freq=1)
        self.assertAlmostEqual(.05, obj.GetYield(0, 100., 'dirty', 'bond'), places=4)
        obj = CouponBond(2., .05, coupon_freq=2)
        self.assertAlmostEqual(.05, obj.GetYield(0, 100., 'dirty', 'bond'), places=4)


    def test_ZeroCurvePrice(self):
        obj = CouponBond(2., .05, coupon_freq=1)
        ZC = ZeroCurve([0., 3.], [.05, .05])
        self.assertAlmostEqual(100., obj.GetPriceFromZeroCurve(0., ZC, price_type='dirty'))
