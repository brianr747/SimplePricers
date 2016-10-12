from unittest import TestCase
import doctest

import simplepricers.yieldcalculations as yieldcalculations


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


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(yieldcalculations))
    return tests
