import time

from processors import InstructionProcessor
from processes.recognizer import Recognizer

if __name__ == '__main__':
    startTime = time.time()
    # processor = InstructionProcessor(buff.get_buff_instruction(sequence=buff.farm_buff_sequence, reload=True))
    # following object used as example for recognizer
    items_find_properties = {
        'roi': (0, 0, 280, 480),
        'color': ((0, 50, 50), (1, 255, 255)),
        'kernel': (2, 2),
        'name': 'items_points',
        'threshold_lower': 120
    }
    grid_shape_find_properties = {
        'roi': (0, 0, 280, 480),
        'color': ((80, 69, 100), (94, 255, 255)),
        'kernel': None,
        'threshold_lower': 30,
        'name': 'grid_points'
    }
    items = Recognizer('assets/inventory.JPG', None, **items_find_properties, process='find')
    grid = Recognizer('assets/inventory.JPG', None, **grid_shape_find_properties, process='find')
    processor = InstructionProcessor([grid, items])
    processor.process()
    processor.show_storage_at('assets/inventory.JPG')
    execTime = (time.time() - startTime)

    print("Finished work, time:", execTime,'(sec) ', execTime / 60, '(min)')
