import unittest

from shapes.window import Window

class TestWindow(unittest.TestCase):

    def setUp(self):
        Window.locate_window = patch_locate_window
        import pyautogui
        pyautogui.screenshot = patch_ui_screenshot

    def test_init(self):
        result = Window()
        self.assertIsInstance(result, Window)

    def test_position(self):
        result = Window().position()
        self.assertEqual(result, (100, 240))

    def test_center(self):
        result = Window().center()
        self.assertEqual(result, (940.0, 765.0))

    def test_relative(self):
        result = Window().relative((100, 100))
        self.assertEqual(result, (200, 340))

def patch_locate_window(self):
    self.windowHead = (100,200, 40, 40)

def patch_ui_screenshot(region):
    return (100, 225, 1920, 1080)