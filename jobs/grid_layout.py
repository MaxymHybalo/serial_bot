from processes.recognizer import Recognizer
import utils.cv2_utils as utils

class Grid:

    def __init__(self, identifier):
        self.identifier = identifier
        start = self.__find_grid_entry()
        utils.log_image({'rect': start})

    def __find_grid_entry(self):
        return Recognizer(self.identifier, None).recognize()
