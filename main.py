#!/usr/bin/env python3

from webtentacle import config
from webtentacle import pool
import os
from multiprocessing import Pool
import logging
from webtentacle import splunk
from webtentacle import splunk_output

if __name__ == '__main__':
    settings = config.LoadConfig('config.yml')
    settings.set_logging()
    logging.debug("loaded settings: {}".format(settings.settings))

    splunk.echo_installed_apps()
    urls = settings.get_urls()
    nikto = settings.get_nikto()
    file_output = settings.get_file_output()
    pool.concurrent_pool(urls, file_output, nikto)
    print("job nikto finished")
    splunk_output.write_data_to_splunk()
    print("job splunk dumping data finished")
    
    
    