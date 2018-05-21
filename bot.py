import time
import logging
from utils.configurator import Configurator
from jobs.enhancer import Enhancer
from processes.object_processor import ObjectProcessor


def configure_logger():
    log_format = '%(levelname)s : %(name)s %(asctime)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=log_format,
                        datefmt='%d-%m %H:%M:%S')


def load_config():
    return Configurator('config.yml').from_yaml()


if __name__ == '__main__':
    startTime = time.time()
    configure_logger()
    logging.getLogger()

    config = load_config()

    if config['mode'] == 'enhance':
        enhancer = Enhancer(config['enhancer'] + '.yml')
        processor = ObjectProcessor(enhancer, config['serial'])
        processor.handle()

    # ENHANCEMENT

    execTime = (time.time() - startTime)
    finalMessage = "Finished work, time: {0} (sec), {1} (min)".format(execTime, execTime / 60)
    logging.info(finalMessage)


