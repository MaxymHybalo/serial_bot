import unittest
from jobs.farming import Farming
from shapes.window import Window
class TestFarming(unittest.TestCase):
    
    def setUp(self):
        Window.locate_window = patch_locate_window
        import pyautogui
        pyautogui.screenshot = patch_ui_screenshot

        freq = [2, 1, 3]
        actions = ['1', '2', ['c', '5']]
        self.farming = Farming(actions, freq)

    def test_init_actions_time(self):
        self.farming.init_actions_time()
        self.assertEqual(len(self.farming.skills_state), 3)
    
    def test_generate_actions(self):
        self.farming.generate_actions()
        self.assertEqual(self.farming.actions, ['key', 'key', 'key'])
    
    def test_generate_actions_with_turn(self):
        farming = Farming(['1', '2', '_'], [1,2,3])
        farming.generate_actions()
        self.assertEqual(farming.actions, ['key', 'key', 'turn'])
    
    def test_get_method_name_key(self):
        self.assertEqual(self.farming.get_method_name('4'), 'key')

    def test_get_method_name_turn(self):
        self.assertEqual(self.farming.get_method_name('_'), 'turn')

def patch_locate_window(self):
    self.windowHead = (100,200, 40, 40)

def patch_ui_screenshot(region):
    return (100, 225, 1920, 1080)