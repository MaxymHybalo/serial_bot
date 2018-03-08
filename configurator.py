import json
from recognizer import Recognizer
from click import Click

class Configurator: 
    
    def __init__(self, filepath):
        self.filepath = filepath
    

    def import_config(self):
        config = open(self.filepath, 'r')
        configuration = config.read()
        config.close()
        return json.loads(configuration)


    def generate_objects(self):
        config = self.import_config()
        generated = dict()
        for key, value in config.items():
            if type(value) is list:
                generated[key] = self._from_list(value)
            else:
                generated[key] = self._get_object(value)
        return generated        

    def _from_list(self, value):
        sub_list = list()
        for e in value:
            sub_list.append(self._get_object(e))
        return sub_list
    
    def _get_object(self, cfg):
        process = cfg['process']
        if process == 'recognize':
            return Recognizer(
                cfg['img'],
                cfg['region'],
                wait=cfg['freq']
            )
        if process == 'center_on':
            return Recognizer(
                cfg['img'], 
                cfg['region'],
                wait=cfg['freq'],
                process=cfg['process']
            )
        if process == 'click':
            return Click(cfg['x'], cfg['y'], delay=cfg['delay'])