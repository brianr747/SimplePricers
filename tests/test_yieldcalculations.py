"""
test_yieldcalculations.py

Note that sone tests are in doctests. Do not replicate them within unitt tests, as we then have to maintain
the same test twice.
"""

from unittest import TestCase
import doctest

import simplepricers.yieldcalculations as yieldcalculations
from simplepricers.bonds_curves import ZeroCurve


def load_tests(loader, tests, ignore):
    """
    Load doctests, so unittest discovery can find them.
    """
    tests.addTests(doctest.DocTestSuite(yieldcalculations))
    return tests


class TestDF(TestCase):
    def test_DF_list(self):
        mats = []
        rates = []
        for i in range(0, 5):
            mats.append(float(i))
            rates.append(.05)
        out = yieldcalculations.DF(mats, rates)
        out = [round(x, 4) for x in out]
        self.assertEqual(out, [1.0, 0.9524, 0.907, 0.8638, 0.8227])


class TestDFExponential(TestCase):
    def test_DF_exponential_list(self):
        t = [1., 2.]
        r = [.05, .05]
        out = yieldcalculations.DF_exponential(t, r)
        out = [round(x, 4) for x in out]
        self.assertEqual(out, [.9512, .9048])


class TestConvertRate(TestCase):
    def test_ConvertRate_duh(self):
        self.assertEqual(yieldcalculations.ConvertRate(.02, '1', '1'), .02)

    def test_unsupported(self):
        with self.assertRaises(NotImplementedError):
            yieldcalculations.ConvertRate(.02, '5', '1')


class TestZeroCurve(TestCase):
    def test_df1(self):
        obj = ZeroCurve([0., 1.], [.04, .05])
        # At T=1, zero rate = .05, so DF = 1/1.05
        self.assertEqual(1/1.05, obj.GetDF(1,))
        # At T=0.5, zero rate = 4.5%; so = 1/(1.045)^.5
        self.assertEqual(1/pow(1.045, .5), obj.GetDF(.5))