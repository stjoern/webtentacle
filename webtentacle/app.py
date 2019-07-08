
from webtentacle.common import config
from webtentacle.nikto import pool
import os
from multiprocessing import Pool
import logging
from webtentacle.splunk import initialize
from webtentacle.splunk.users import Users
from webtentacle.splunk.data2splunk import *
from webtentacle.parser.xml2json import Xml2Json
import socket

def run():
    settings = config.LoadConfig('webtentacle/config.yml')
    settings.set_logging()
    logging.debug("loaded settings: {}".format(settings.settings))

    urls = settings.get_urls()
    nikto = settings.get_nikto()
    file_output = settings.get_file_output()
    pool.concurrent_pool(urls, file_output, nikto)
    print("job nikto finished")
    
    #create user
    try:
        splunk_conf = settings.get_splunk()
        initialize.init(host=os.getenv('MOTHER_HOSTNAME'),
                        port=int(splunk_conf.get('port')),
                        username='admin',
                        password=os.getenv('SPLUNK_INITIAL_PASSWORD'),
                        cookie=0)
        user = Users()
        user.create_user(username=os.getenv('SPLUNK_USERNAME'),
                        password=os.getenv('SPLUNK_PASSWORD'),
                        roles=['power','user','admin'])
        initialize.splunk_service.logout()
        initialize.init(host=os.getenv('MOTHER_HOSTNAME'),
                        port=int(splunk_conf.get('port')),
                        username=os.getenv('SPLUNK_USERNAME'),
                        password=os.getenv('SPLUNK_PASSWORD'),
                        cookie=0)
        
        # user authenticated
        print("job webtentacle user authenticated")
        
        for item in glob.glob("{}/*.{}".format(file_output.get('folder'), file_output.get('extension.used'))):
            xmlparser = Xml2Json(filepath=item, url="todo")
            xmlparser.sanitize_xml()
            
        dump = Data2Splunk(host=socket.gethostname(), source='webtentacle', sourcetype="_json", backup=0, delete_after=0)
        dump.bulk(directory=file_output.get("folder"), extension=file_output.get('extension_used'))
        print("job splunk dumping data finished")
    except Exception as exc:
        logging.error("Error occurred, error: {}".format(str(exc)))
        exit(-1)