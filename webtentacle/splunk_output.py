from . splunk import service
import glob
from . config import LoadConfig
import socket
import os

def write_data_to_splunk():
    myindex=service.indexes['main']
    host = socket.gethostname()
    mysocket = myindex.attach(sourcetype='myfile',host=socket.gethostname())
    settings = LoadConfig('config.yml')
    mm = glob.glob("{}/*.txt".format(settings.get_file_output()))
    for item in glob.glob("{}/*.txt".format(settings.get_file_output().get("folder"))):
        file_data = ''
        with open(item, 'r') as lines:
            for line in lines:
                if line.isspace(): 
                    line = ' '
                file_data += line      
                file_data += '\r\n'
            mysocket.send(str.encode(file_data))
    mysocket.close()
    
    #os.remove(item)