import unittest

from hashlib import sha1
from utils.cv2_utils import get_image, screenshot
from PIL.Image import Image

TEST_SLICE_HASH = '299f24df480dcccc383d55904577cfac87fd8362'

class TestCV2Utils(unittest.TestCase):

    def test_get_image(self):
        data = 'test/fixtures/testslice.png'
        result = get_image(data)
        result = sha1(result).hexdigest()
        self.assertEqual(result, TEST_SLICE_HASH)

    def test_screenshot(self):
        data = [100, 100, 1000, 200]
        result = screenshot(data)
        self.assertIsInstance(result, Image)