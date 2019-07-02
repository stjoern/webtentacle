import yaml
import logging

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
                print(exc)

    def get_urls(self):
        return self.settings.get('webapps',[])

    def get_nikto(self):
        return self.settings.get('nikto',{})
    
    def url_generator(self):
        for url in self.settings.get('webapps',[]):
            yield url

    def get_file_output(self):
        return self.settings.get("files_output",None)
    
    def set_logging(self):
        log = self.settings.get("logging")
        logging.basicConfig(filename="{}/{}".format(log.get("folder"), log.get("file")), 
                            filemode='w+', 
                            format='%(process)d-%(asctime)s-%(name)s-%(levelname)s-%(message)s', 
                            level=eval("logging.{}".format((log.get("mode")).upper())))
        
    def get_splunk(self):
        return self.settings.get("splunk")