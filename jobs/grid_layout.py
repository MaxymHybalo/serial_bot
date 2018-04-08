from processes.recognizer import Recognizer
import utils.cv2_utils as utils


class Grid:

    def __init__(self, identifier):
        self.identifier = identifier
        start = self.__find_grid_entry()

    def __find_grid_entry(self):
        rect = Recognizer(self.identifier, None).recognize()
        start = (rect[0], rect[1] + rect[3], 3)
        end = (rect[0] + rect[2], rect[1] + rect[3], 3)
        utils.log_image(**{
            'rect': rect,
            'circle': [start, end],
            'multi': 'circle'
            })
        return start, end
