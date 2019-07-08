from webtentacle.splunk.initialize import splunk_service
import glob
from webtentacle.common.config import LoadConfig
import socket
import os
from webtentacle.common import helper
import logging
import shutil
from webtentacle.splunk import initialize

class Data2Splunk(object):
    def __init__(self, index='main', host=None, source=None, sourcetype=None, backup=0, delete_after=1):
        self.index = index
        self.host = socket.gethostname() if not host else host
        self.source = source
        self.sourcetype = sourcetype
        self.backup = backup
        self.delete_after = delete_after
        self.index = initialize.splunk_service.indexes[index]
        self.__file = None
      
         
    def single(self, file):
        self.__file = file
        try:
            if helper.file_exist(file):
                with self.index.attached_socket(source=self.source, sourcetype=self.sourcetype) as sock:
                    file_data = ''
                    with open(file, 'r') as lines:
                        for line in lines:
                            if line.isspace():
                                line = ' '
                            line.replace("'","\\'")
                            file_data+=line
                            file_data+='\r\n'
                    sock.send(str.encode(file_data))
            if self.delete_after:
                self.__delete()
        except Exception as exc:
            logging.error('Error occurred while saving data to Splunk for file {}, error: {}'.format(file, exc))
            raise
        
    def bulk(self, directory, extension):
        for item in glob.glob("{}/*.{}".format(directory, extension)):
            self.__file = item
            self.single(item)
        
      
    def __delete(self):
        remove = lambda f: os.remove(f)
        if self.__file:
            remove(self.__file)
        #elif self.__folder :
        #    for root, dirs, files in os.walk(self.__folder):
        #        for f in files:
        #            os.unlink(os.path.join(root, f))
        #        for d in dirs:
        #            shutil.rmtree(os.path.join(root, d))
        else:
            pass
        self.__file = None
             

               
    
def write_data_to_splunk():
    index = initialize.splunk_service.indexes['main']
    settings = LoadConfig('webtentacle/config.yml')
    with index.attached_socket(source='webtentacle', sourcetype='_json') as sock:
            for item in glob.glob("{}/*.txt".format(settings.get_file_output().get("folder")))[:]:
                file_data = ''
                with open(item, 'r') as lines:
                    for line in lines:
                        if line.isspace(): 
                            line = ' '
                            line.replace("'","\\'")
                        file_data += line      
                        file_data += '\r\n'
                sock.send(str.encode(file_data))
