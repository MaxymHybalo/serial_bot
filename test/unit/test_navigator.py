import unittest

from jobs.helpers.navigator import start_point, circus_npc_point, \
    is_near_npc, distance

from shapes.window import Window

class TestNavigator(unittest.TestCase):

    def test_start_point(self):
        data = (100, 200, 50, 50)
        result = start_point(data)
        self.assertEqual(result, (150, 225))

    def test_circus_npc_pint(self):
        data = (100, 200, 50, 50)
        result = circus_npc_point(data)
        self.assertEqual(result, (125, 250))

    def test_is_near_npc(self):
        data = ((100, 200, 100, 30), (100, 300, 100, 40))
        result = is_near_npc(data[0], data[1])
        self.assertTrue(result, True)

    def test_distance(self):
        data = ((40, 40), (20, 25))
        result = distance(data[0], data[1])
        self.assertEqual(result, 25.0)
