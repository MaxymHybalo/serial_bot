import time
import buff_instruction as buff
import enhance

from processors import InstructionProcessor
from click import Click
from configurator import Configurator

if __name__ == '__main__':
    startTime = time.time()
    # run()
    # print(buff.getBuffInstruction())
    # processInstruction(enhance.enhance())
    # processInstruction(buff.getBuffInstruction())
    # processor = InstructionProcessor(buff.getBuffInstruction())
    processor = InstructionProcessor(enhance.combination())

    processor.process()
    execTime = (time.time() - startTime)

    print("Finished work, time:", execTime,'(sec) ', execTime / 60, '(min)')
