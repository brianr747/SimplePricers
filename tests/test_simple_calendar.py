from unittest import TestCase

from simplepricers.simple_calendar import SimpleCalendar360, Indexation

class TestSimpleCalendar360(TestCase):
    def test_GetDate(self):
        obj = SimpleCalendar360()
        self.assertEqual(1976.0, obj.GetDate(1976))
        self.assertEqual(1976.0, obj.GetDate(1976, 1))
        self.assertEqual(1976.0, obj.GetDate(1976, 1, 1))
        self.assertEqual(1976.5, obj.GetDate(1976, 7))
        self.assertEqual(1976.0 + (4./360.), obj.GetDate(1976, 1, 5))

    def test_AddMonths(self):
        obj = SimpleCalendar360()
        self.assertEqual(obj.GetDate(1976, 3, 1), obj.AddMonths(1976.0, 2))


class TestIndexation(TestCase):
    def test_Set1(self):
        obj = Indexation()
        with self.assertRaises(ValueError):
            obj.SetIndexValues([1., 2.], [100.])

    def test_Set2(self):
        obj = Indexation()
        obj.SetIndexValues([0., 1.], [100., 101.])
        self.assertEqual([(0., 100.), (1., 101.)], obj.IndexDateValues)

    def test_Set3(self):
        obj = Indexation()
        obj.SetIndexValues([2., 1.], [100., 101.])
        self.assertEqual([(1., 101.), (2., 100.)], obj.IndexDateValues)

