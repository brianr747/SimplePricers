"""
test_bonds.py

Note that some tests are done as doctests.
"""

from unittest import TestCase
import doctest

from simplepricers.bonds import Consol
from simplepricers.bonds import CouponBond
import simplepricers.bonds as bonds


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
