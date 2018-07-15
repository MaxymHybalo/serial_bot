import time
import logging
from utils.configurator import Configurator
from jobs.enhancer import Enhancer
from processes.object_processor import ProcessInitializer
from enhance import Enhancer as Combinator
from processors import InstructionProcessor
import buff_instruction as buff


def load_config():
    return Configurator('config.yml').from_yaml()


def run(external_processor=None):
    start_time = time.time()
    log = logging.getLogger('bot')
    config = load_config()

    if config['mode'] == 'enhance':
        enhancer = Enhancer(config['enhancer'])
        processor = ProcessInitializer(enhancer, config['serial'])
        processor.handle()

    if config['mode'] == 'buff':
        processor = InstructionProcessor(buff.get_buff_instruction(sequence=buff.full_buff_sequence, reload=True))
        processor.process()
    if config['mode'] == 'make':
        external_processor.process()
    if config['mode'] == 'combination':
        combinate = Combinator('configuration.yaml')
        processor = InstructionProcessor(combinate.enhance(combinate.combination))
        processor.process()
    if config['mode'] == 'return':
        processor = InstructionProcessor(buff.to_reload(is_return=True))
        processor.process()

    exec_time = (time.time() - start_time)
    final_message = "Finished work, time: {0} (sec), {1} (min)".format(exec_time, exec_time / 60)
    log.info(final_message)
    return exec_time


if __name__ == '__main__':
    run()
