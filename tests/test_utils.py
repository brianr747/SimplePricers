from unittest import TestCase
import doctest

import simplepricers.utils as utils
from simplepricers.utils import create_grid


class TestCreateGrid(TestCase):
    """
    These tests seem self-explanatory... The doc string notes some
    of the behaviour to watch out for.
    """

    def test_create_grid(self):
        self.assertEqual(utils.create_grid(0., 1., 1), [0., 1.])

    def test_create_grid2(self):
        self.assertEqual(utils.create_grid(0., .99, 1), [0., ])

    def test_create_grid_3(self):
        self.assertEqual(utils.create_grid(0., 1., 2), [0., .5, 1.])

    def test_create_grid_4(self):
        self.assertEqual(utils.create_grid(.3, 1.3, 2), [0.3, .8, 1.3])

    def test_create_grid_5(self):
        self.assertEqual(create_grid(100., 105., 1), [100., 101., 102., 103., 104., 105.])


# Add in doctests
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(utils))
    return tests
