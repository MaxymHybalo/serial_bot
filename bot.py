import time
import logging
from utils.configurator import Configurator
from jobs.enhancer import Enhancer
from processes.object_processor import ProcessInitializer
from processors import InstructionProcessor
import buff_instruction as buff


def configure_logger():
    log_format = '%(levelname)s : %(name)s %(asctime)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=log_format,
                        datefmt='%d-%m %H:%M:%S')


def load_config():
    return Configurator('config.yml').from_yaml()


def run():
    start_time = time.time()
    configure_logger()
    logging.getLogger()

    config = load_config()

    if config['mode'] == 'enhance':
        enhancer = Enhancer(config['enhancer'] + '.yml')
        processor = ProcessInitializer(enhancer, config['serial'])
        processor.proc
        processor.handle()

    if config['mode'] == 'buff':
        processor = InstructionProcessor(buff.get_buff_instruction(sequence=buff.farm_buff_sequence, reload=True))
        processor.process()

    exec_time = (time.time() - start_time)
    final_message = "Finished work, time: {0} (sec), {1} (min)".format(exec_time, exec_time / 60)
    logging.info(final_message)


if __name__ == '__main__':
    run()
