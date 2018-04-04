import time
from jobs.enhancer import Enhancer
from processes.object_processor import ObjectProcessor

if __name__ == '__main__':
    startTime = time.time()



    # ENHANCEMENT
    enhancer = Enhancer('enhancer.config.v2.yaml')
    processor = ObjectProcessor(enhancer)

    processor.handle()

    execTime = (time.time() - startTime)

    print("Finished work, time:", execTime, '(sec) ', execTime / 60, '(min)')
