import time
import logging

from utils.configurator import Configurator
from jobs.enhancer import Enhancer
from jobs.combinator import Combinator
from jobs.buffer import Buffer
from jobs.taming import Taming
from jobs.farming import Farming

from jobs.grid_layout import Grid
from processes.object_processor import ProcessInitializer
from processes.instruction_processor import InstructionProcessor
from utils.serial_controller import SerialController
from utils.config import Config

def load_config():
    return Configurator('config.yml').from_yaml()

def run(external_processor=None):
    start_time = time.time()
    log = logging.getLogger('bot')
    config = load_config()
    if not SerialController().serial:
        SerialController().run_serial(config['serial']) 
    mode = config['mode']
    if mode == 'enhance':
        enhancer = Enhancer(config['enhancer'])
        enhancer.process()
    if mode == 'buff':
        buff_config = Configurator(config['buffer']).from_yaml()
        processor = ProcessInitializer(Buffer(buff_config), config['serial'])
        processor.handle()
    if mode == 'make':
        external_processor.process()
    if mode == 'combination':
        combinate = Combinator(config['enhancer'])
        combinate.process()
    if mode == 'taming':
        Taming().run()
    if mode == 'farming':
        Farming().run()
    if mode == 'test':
        print('nothings')

    exec_time = (time.time() - start_time)
    final_message = "Finished work, time: {0} (sec), {1} (min)".format(exec_time, exec_time / 60)
    log.info(final_message)
    return exec_time

if __name__ == '__main__':
    run()
