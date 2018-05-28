import json
import yaml

from processes.recognizer import Recognizer
from processes.click import Click


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

    def from_yaml(self):
        data = {}
        with open(self.filepath, 'r') as stream:
            data= yaml.load(stream)
        return data

    @staticmethod
    def pretty_print(message, type='json'):
        parse = str(message)
        parse = parse.replace('\'', '\"')
        parse = parse.replace('None', '\"None\"')
        parse = parse.replace('False', '\"False\"')
        parse = parse.replace('True', '\"True\"')
        parse = json.loads(parse)
        print(json.dumps(parse, indent=4, sort_keys=True))
