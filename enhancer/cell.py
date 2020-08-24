import logging

# import utils.cv2_utils as utils # used for drawing images

class Cell:
    def __init__(self):
        self.log = logging.getLogger('cell')
    
    def call(self):
        self.log.warn('New cell created')
        print('try to print something')
# 