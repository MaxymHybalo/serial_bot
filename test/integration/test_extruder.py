import unittest
import numpy as np

from jobs.helpers.extruder import Extruder
from utils.cv2_utils import get_image

class TestExtruder(unittest.TestCase):
    
    testimage = 'test/fixtures/testslice.png'
    
    def setUp(self):
        self.extruder = Extruder(get_image(self.testimage))

    def test_set_image(self):
        data = 'test/fixtures/testslice.png'
        data = get_image(data)
        result = Extruder(data)
        self.assertIsInstance(result.image, np.ndarray)