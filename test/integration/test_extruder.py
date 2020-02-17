import unittest

from jobs.helpers.extruder import Extruder

class TestExtruder(unittest.TestCase):
    
    def test_set_image(self):
        data = 'test/fixtures/testslice.png'
        result = Extruder(data)
        print(result.image)
        result = result.image
        self.assertEqual(result, None)