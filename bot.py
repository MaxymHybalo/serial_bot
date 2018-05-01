import time
import logging
from jobs.enhancer import Enhancer
from processes.object_processor import ObjectProcessor


def configure_logger():
    log_format = '%(levelname)s : %(name)s %(asctime)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=log_format,
                        datefmt='%d-%m %H:%M:%S')


if __name__ == '__main__':
    startTime = time.time()
    configure_logger()
    logging.getLogger()

    # ENHANCEMENT
    enhancer = Enhancer('enhancer.config.v2.yaml')
    processor = ObjectProcessor(enhancer)

    processor.handle()

    execTime = (time.time() - startTime)
    finalMessage = "Finished work, time: {0} (sec), {1} (min)".format(execTime, execTime / 60)
    logging.info(finalMessage)