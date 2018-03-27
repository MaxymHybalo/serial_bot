import time
from processors import InstructionProcessor
from enhance import Enhancer
from processes.recognizer import Recognizer
from processes.items_handler import ItemsHandler
from processes.click import  Click
from processes.nested_process import NestedProcessor
import utils.cv2_utils as utils
if __name__ == '__main__':
    startTime = time.time()
    # processor = InstructionProcessor(buff.get_buff_instruction(sequence=buff.farm_buff_sequence, reload=True))
    # following object used as example for recognizer
    roi = [80, 20, 340, 515]
    items_find_properties = {
        'roi': roi,
        'color': ((0, 150, 150), (3, 255, 255)),
        'kernel': (2, 2),
        'name': 'items_points',
        'threshold_lower': 130
    }
    grid_shape_find_properties = {
        'roi': roi,
        'color': ((80, 69, 100), (94, 255, 255)),
        'kernel': None,
        'threshold_lower': 30,
        'name': 'grid_points'
    }
    # items = Recognizer(None, None, **items_find_properties, process='find')
    # grid = Recognizer(None, None, **grid_shape_find_properties, process='find')
    # handler = ItemsHandler(items_find_properties['name'], grid_shape_find_properties['name'])
    nested = NestedProcessor([Click(500, 500)])
    processor = InstructionProcessor([Click(200, 200), nested])
    processor.process()
    targets = processor.storage['targets']
    # image = utils.get_image('assets/i5.JPG')
    # image = utils.get_image(roi)
    # for t in targets:
    #     image = utils.draw_rect(image, t, 36,36)
    # utils.show(image)
    # ENHANCEMENT
    # enhancer = Enhancer('configuration.yaml')
    # processor = InstructionProcessor(enhancer.enhance(enhancer.enhancement))
    # processor.process()

    execTime = (time.time() - startTime)

    print("Finished work, time:", execTime,'(sec) ', execTime / 60, '(min)')
