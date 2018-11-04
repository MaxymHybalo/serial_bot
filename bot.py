import time
import logging
from utils.configurator import Configurator
from jobs.enhancer import Enhancer
from jobs.buffer import Buffer
from processes.object_processor import ProcessInitializer
from enhance import Enhancer as Combinator
from processes.instruction_processor import InstructionProcessor

from utils.serial_controller import SerialController

from jobs.grid_layout import Grid

def load_config():
    return Configurator('config.yml').from_yaml()

def run(external_processor=None):
    start_time = time.time()
    log = logging.getLogger('bot')
    config = load_config()
    if not SerialController().serial:
        SerialController().run_serial(config['serial']) 

    if config['mode'] == 'enhance':
        enhancer = Enhancer(config['enhancer'])
        enhancer.process()
    if config['mode'] == 'buff':
        processor = ProcessInitializer(Buffer(config['buffer']), config['serial'])
        processor.handle()
    if config['mode'] == 'make':
        external_processor.process()
    if config['mode'] == 'combination':
        combinate = Combinator('configuration.yaml')
        processor = InstructionProcessor(config['serial'], combinate.enhance(combinate.combination))
        processor.process()
    if config['mode'] == 'test':
        grid = Grid(debug=True)

    exec_time = (time.time() - start_time)
    final_message = "Finished work, time: {0} (sec), {1} (min)".format(exec_time, exec_time / 60)
    log.info(final_message)
    return exec_time

if __name__ == '__main__':
    run()