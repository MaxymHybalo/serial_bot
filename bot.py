import time
from processors import InstructionProcessor
from enhance import Enhancer
from processes.recognizer import Recognizer
from processes.items_handler import ItemsHandler
import utils.cv2_utils as utils
if __name__ == '__main__':
    startTime = time.time()
    # processor = InstructionProcessor(buff.get_buff_instruction(sequence=buff.farm_buff_sequence, reload=True))
    # following object used as example for recognizer
    items_find_properties = {
        'roi': (0, 0, 330, 480),
        'color': ((0, 50, 50), (2, 255, 255)),
        'kernel': (2, 2),
        'name': 'items_points',
        'threshold_lower': 120
    }
    grid_shape_find_properties = {
        'roi': (0, 0, 330, 480),
        'color': ((80, 69, 100), (94, 255, 255)),
        'kernel': None,
        'threshold_lower': 30,
        'name': 'grid_points'
    }
    items = Recognizer('assets/inventory.JPG', None, **items_find_properties, process='find')
    grid = Recognizer('assets/inventory.JPG', None, **grid_shape_find_properties, process='find')
    handler = ItemsHandler(items_find_properties['name'], grid_shape_find_properties['name'])
    enhancer = Enhancer('configuration.yaml')
    matix = enhancer.get_matrix()
    enhancement = enhancer.enhancement()
    image = utils.get_image('assets/inventory.JPG')
    for i in matix:
        image = utils.draw_corners(image, i, (0, 255, 0))

    for i in enhancement:
        image = utils.draw_corners(image, i, (0, 0, 255))

    utils.show(image)
    # print(enhancer.get_matrix())

    # processor = InstructionProcessor([grid, items, handler])
    # processor.process()

    execTime = (time.time() - startTime)

    print("Finished work, time:", execTime,'(sec) ', execTime / 60, '(min)')
