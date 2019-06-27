from webtentacle import config
from webtentacle import pool
import os
from multiprocessing import Pool
import logging

if __name__ == '__main__':
    settings = config.LoadConfig('config.yml')
    settings.set_logging()
    logging.debug("loaded settings: {}".format(settings.settings))

    urls = settings.get_urls()
    file_output = settings.get_file_output()
    #exitcode, output, err = pool.run_nikto([one_url], file_output)
    pool.concurrent_pool(urls, file_output)
    