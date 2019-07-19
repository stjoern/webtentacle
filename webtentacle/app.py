
from webtentacle.common import config
from webtentacle.nikto import pool
import os
from multiprocessing import Pool
import logging
import logging.config
from webtentacle.splunk import initialize
from webtentacle.splunk.users import Users
from webtentacle.splunk.data2splunk import *
from webtentacle.parser.xml2json import Xml2Json
import socket
from webtentacle.splunk.hec_handler.hec_logging import LOGGING
from webtentacle.common.config import config

def run():
    
    
    logging.config.dictConfig(LOGGING)
    logger = logging.getLogger('webtentacle')
    '''
    try:
        urls = config.get('webapps')
        file_output = config.get('files_output')
        nikto = config.get('nikto')
        pool.concurrent_pool(urls, file_output, nikto)
    except Exception as exc:
        logging.error(str(exc))
        
    logger.debug('job Scanning -> finished')
    '''
    try:
        reg_exp = os.path.join(config.get('files_output','folder'),'*.{}'.format(config.get('files_output','extension_used')))
        for item in glob.glob(reg_exp):
            base = os.path.basename(item)
            to_be_sanitized_to = os.path.join(config.get('files_output','sanitized'), base)
            parsed_url = base.split('-')[0] or 'FQDN'
            xmlparser = Xml2Json(filepath=item, url=parsed_url, xmloutput=to_be_sanitized_to)
            xmlparser.sanitize_xml()
            
        #dump = Data2Splunk(host=socket.gethostname(), source='webtentacle', sourcetype="_json", backup=0, delete_after=1)
        #dump.bulk(directory=file_output.get("folder"), extension='json')
        #logging.info("job splunk 'dumping data' finished")
        print("job splunk dumping data finished")
    except Exception as exc:
        logging.error("Error occurred, error: {}".format(str(exc)))
        exit(-1)