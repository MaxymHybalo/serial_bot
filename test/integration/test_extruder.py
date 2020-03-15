import unittest
import numpy as np

from jobs.helpers.extruder import Extruder
from utils.cv2_utils import get_image

class TestExtruder(unittest.TestCase):
    
    testimage = 'test/fixtures/testslice.png'
    
    def setUp(self):
        self.extruder = Extruder(get_image(self.testimage))

    def test_set_image(self):
        data = get_image(self.testimage)
        result = Extruder(data)
        self.assertIsInstance(result.image, np.ndarray)

    def test_filter_by_color(self):
        result = self.extruder.filterByColor(self.extruder.image, TestExtruderConfig)
        self.assertIsInstance(result, np.ndarray)

    def test_filter_img_by_color(self):
        data = TestExtruderConfig()
        result = self.extruder.filtredImgByColor(data)
        self.assertIsInstance(result, np.ndarray)
    
    def test_match_by_template_no_roi_minmax(self):
        template = get_image(TestExtruderConfig.template)
        data = self.extruder.match_by_template(template)
        self.assertEqual(data, (5, 46, 22, 19))
    
    def test_match_by_template_roi_minmax(self):
        template = get_image(TestExtruderConfig.template)
        data = self.extruder.match_by_template(template, roi=(0,40, 30, 30))
        self.assertEqual(data, (5, 46, 22, 19))

    def test_match_by_template_threshold(self):
        template = get_image(TestExtruderConfig.template)
        data = self.extruder.match_by_template(template, method ='threshold')
        self.assertEqual(data, (5, 46, 22, 19))


class TestExtruderConfig:
    light = [11, 140, 0]
    dark = [18, 255, 255]
    template = 'test/fixtures/template.png'

