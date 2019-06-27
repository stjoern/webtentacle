from webtentacle import config
from webtentacle import pool
import os
from multiprocessing import Pool


if __name__ == '__main__':
    settings = config.LoadConfig('config.yml')
    print(settings.settings)
    urls = settings.get_urls()
    #one_url = next(urls)
    file_output = settings.get_file_output()
    #exitcode, output, err = pool.run_nikto([one_url], file_output)
    pool.concurrent_pool(urls, file_output)
    