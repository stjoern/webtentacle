import logging
from splunk_hec_handler import SplunkHecHandler
from subprocess import Popen, PIPE
from webtentacle.common.config import config

logger = logging.getLogger('webtentacle')
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.level = logging.INFO
logger.addHandler(stream_handler)
splunk_handler = None

def initialize():
    try:
        args = ['.code/keyring/crypt','decrypt','--username']
        token = config.get('splunk','key_name')
        port = config.get('splunk','port')
        if not token:
            raise ValueError("no Splunk API token name found")
        args.append(token)
        print("args called: {}".format(args))
        p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        if p.returncode != 0:
            raise ValueError("Error occurred: {}".format(output))
        splunk_handler = SplunkHecHandler('localhost',
                                          token,
                                          port=port,
                                          proto='http',
                                          ssl_verify=False,
                                          source="webtentacle",
                                          sourcetype='webtentacle_json')
        logger.addHandler(splunk_handler)
        logger.info("Testing splunk HEC info message")
        
    except Exception as exc:
        print("error {}".format(str(exc)))

https://github.com/zach-taylor/splunk_handler
s = SplunkHandler(host='localhost',port='8088',token=token,index='main',verify=False,debug=True)
