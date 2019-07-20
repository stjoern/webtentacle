import os, sys
from webtentacle.common.config import config
from subprocess import Popen, PIPE


SPLUNK_HOST=None
SPLUNK_PORT=None
SPLUNK_TOKEN=None
SPLUNK_INDEX=None

PROTOCOL='https'
VERIFY='True'
LEVEL='DEBUG'
RETRY_COUNT=5
FLUSH=15
DEBUG=False
LOG_FILE=None



try:
    args = ['.code/keyring/crypt','decrypt','--username']
    token_name = config.get('splunk','key_name')
    if not token_name:
        raise ValueError("No Splunk API token name in config.yml found.")
    args.append(token_name)
    SPLUNK_PORT = config.get('splunk','port')
    p = Popen(args, stdin=PIPE,stdout=PIPE,stderr=PIPE)
    
    SPLUNK_TOKEN, err = p.communicate()
    SPLUNK_TOKEN=str(SPLUNK_TOKEN, 'utf-8')
    if p.returncode != 0:
        raise ValueError("Problem with decrypting the Splunk API key")
    
    LOG_FILE = os.path.join(config.get('logging','folder'), config.get('logging','file'))
    
    try:
        SPLUNK_HOST = config.get('splunk', 'host')
        SPLUNK_INDEX = config.get('splunk', 'index')
        
        PROTOCOL=config.get('splunk','protocol')
        VERIFY=config.get('splunk','verify')
        LEVEL=config.get('splunk','level')
        RETRY_COUNT=config.get('splunk','retry_count')
        FLUSH=config.get('splunk','flush')  
    except Exception as exc:
        raise ValueError('cannot get value from config.yml, {}'.format(str(exc)))
    
except Exception as exc:
    print("error occurred: {}".format(str(exc)))
    sys.exit(2)
    
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s"
        },
        'standard': {
            "format": "%(levelname)s <PID %(process)d:%(processName)s> %(name)s.%(funcName)s(): %(message)s"
        }
    },
    'handlers': {
        'splunk': {
            'level': LEVEL,
            'class': 'splunk_handler.SplunkHandler',
            'formatter': 'json',
            'host': SPLUNK_HOST,
            'port': SPLUNK_PORT,
            'token': SPLUNK_TOKEN,
            'index': SPLUNK_INDEX,
            'sourcetype': 'json',
            'verify': VERIFY,
            'retry_count': RETRY_COUNT,
            'debug': DEBUG,
            'protocol': PROTOCOL
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'debug_file_handler': {
            'level': DEBUG,
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': LOG_FILE,
            'maxBytes': 10485760, # 10MB
            'backupCount': 20,
            'encoding': 'utf8'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'splunk','debug_file_handler'],
            'level': 'DEBUG'
        }
    }
}
