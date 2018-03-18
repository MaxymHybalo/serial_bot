import time
import buff_instruction as buff
import enhance

from processors import InstructionProcessor

if __name__ == '__main__':
    startTime = time.time()
    processor = InstructionProcessor(buff.get_buff_instruction(sequence=buff.farm_buff_sequence, reload=True))
    # following object used as example for recognizer
    # kwargs = {
    #     'roi': (0, 0, 280, 480),
    #     'color': ((0, 50, 50), (1, 255, 255)),
    #     'kernel': (2, 2)
    # }
    # rec = Recognizer('assets/inventory.JPG', None, **kwargs, process='find')
    # processor = InstructionProcessor([rec,])
    processor.process()
    execTime = (time.time() - startTime)

    print("Finished work, time:", execTime,'(sec) ', execTime / 60, '(min)')
