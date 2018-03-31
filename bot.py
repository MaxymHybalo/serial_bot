import time
from enhance import Enhancer
from processors import InstructionProcessor
import buff_instruction as buff
if __name__ == '__main__':
    startTime = time.time()
    # processor = InstructionProcessor(buff.get_buff_instruction(sequence=buff.farm_buff_sequence, reload=True))

    # ENHANCEMENT
    enhancer = Enhancer('configuration.yaml')
    processor = InstructionProcessor(enhancer.enhance(enhancer.combination))

    processor.process()

    execTime = (time.time() - startTime)

    print("Finished work, time:", execTime, '(sec) ', execTime / 60, '(min)')
