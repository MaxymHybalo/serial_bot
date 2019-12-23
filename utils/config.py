from utils.singleton import Singleton

class Config(metaclass=Singleton):
    
    def __init__(self, *args, **kwargs):
        self.mode = 'test'
    
    def isWorks(self):
        return self.mode == 'enabled'
    
    def disable(self):
        self.mode = 'disabled'

    def enable(self):
        self.mode = 'enabled'

    def initialize_configs(self, config):
        import jobs.helpers.configs as markers
        from utils.configurator import Configurator
        import sys
        
        config = Configurator(config).from_yaml()

        for c in config['templates']:
            setattr(self, c['name'], getattr(sys.modules['jobs.helpers.configs'], c['name']))
            for field, value in c.items():
                if field is not 'name':
                    setattr(getattr(self, c['name']), field, value)
