import yaml
import logging
from webtentacle.common.helper import get_nested

logger = logging.getLogger('webtentacle-config')

class SingletonMetaClass(type):
    def __init__(cls, name, bases, dict):
        super(SingletonMetaClass, cls).__init__(name, bases, dict)
        original_new = cls.__new__
        def my_new(cls, *args, **kwds):
            if cls.instance == None:
                cls.instance = original_new(cls, *args, **kwds)
            return cls.instance
        cls.instance = None
        cls.__new__ = staticmethod(my_new)

class LoadConfig(object):
    __metaclass__ = SingletonMetaClass
    def __init__(self, config_file):
        self.config_file = config_file
        self.settings =self.load_config(self.config_file)
    def __str__(self):
        return "LoadConfig: config_file<" + self.config_file + ">, settings<" + str(self.settings) + ">"
        
    def load_config(self, config_file):
        with open(config_file, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                logger.debug("problem redading config.ymll, {}".format(str(exc)))
    
    def get(self, *args):
        return get_nested(self.settings, *args)
    
config = LoadConfig('webtentacle/config.yml')