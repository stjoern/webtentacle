
from webtentacle.common import config
from webtentacle.nikto import pool
import os
import sys
from multiprocessing import Pool
import logging
import logging.config
from webtentacle.parser.xml2json import Xml2Json
from webtentacle.splunk.hec_handler.hec_logging import LOGGING
from webtentacle.common.config import config
from webtentacle.common.cleaner import delete_files_top_down
import glob

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('webtentacle')
        
def run():

    try:
        urls = config.get('webapps')
        file_output = config.get('files_output')
        nikto = config.get('nikto')
        pool.concurrent_pool(urls, file_output, nikto)
    except Exception as exc:
        logging.error("cannot scan the webapps", extra={'error_detail': str(exc)})
        sys.exit(os.EX_DATAERR)
    else:
        logging.debug("job <webapp scanning> finished successfully")
    
    # parse and dump data to splunk
    try:
        reg_exp = os.path.join(config.get('files_output','folder'),'*.{}'.format(config.get('files_output','extension_used')))
        for item in glob.glob(reg_exp):
            base = os.path.basename(item)
            to_be_sanitized_to = os.path.join(config.get('files_output','sanitized'), base)
            parsed_url = base.split('-')[0] or 'FQDN'
            xmlparser = Xml2Json(filepath=item, url=parsed_url, xmloutput=to_be_sanitized_to)
            xmlparser.sanitize_xml()
        print("job splunk dumping data finished")
    except Exception as exc:
        logging.error("cannot parse the scanner result.", extra={'error_detail': str(exc)})
        sys.exit(os.EX_DATAERR)
    else:
        logging.debug("job <parsing, splunk dump> finished successfully")
        
    # clean after dumping data to splunk
    try:
        delete_files_top_down(config.get('files_output','folder'), 'json', 'xml')      
    except Exception as exc:
        logger.error("cannot clean files after parsing", extra={'error_detail': str(exc)})
        sys.exit(os.EX_DATAERR)
    else:
        logging.debug("job <cleaning> finished successfully")
        
    sys.exit(os.EX_OK)