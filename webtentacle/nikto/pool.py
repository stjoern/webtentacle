from string import Template
import sys
from urllib.parse import urlsplit
import re
from datetime import datetime
import subprocess
from subprocess import Popen, PIPE
import os
import concurrent.futures
from functools import partial
import logging
import sys

logger = logging.getLogger('webtentacle')

def run_nikto(file_output, nikto, ref_url):
    """
    use nikto to start testing web headers
    todo: add more arguments

    Arguments:
        url: url of the website
        filename: the ouptut will be saved to the file
    Returns:
        (filename, return value)
    """
    def get_file_output( ref_url, file_output, nikto, extension):
        if not re.match(r'http(s?)\:',ref_url):
            ref_url = 'http://' + ref_url
        parsed = urlsplit(ref_url)
        host = parsed.netloc
        template = eval(file_output.get('template','Template("$url-$timestamp")'))
        ts = datetime.now().timestamp()
        substituted = template.substitute(url=host, timestamp=datetime.utcfromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S'))
        substituted += '.{}'.format(extension)
        return substituted, ref_url

    extension = file_output.get("extension_used","xml")
    file_name, url = get_file_output(ref_url, file_output, nikto, extension)
    file_output_path = '{}/{}'.format(file_output.get('folder','/tmp'), file_name)
    useragent = nikto.get("useragent","webtentacle")
    

    args = ["nikto", "-useragent", useragent, "-h", url, "-Tuning", "2", "-Format", extension, "-o", file_output_path]
    logging.debug("nikto {}".format(" ".join(args)))
    p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    exitcode = p.returncode
    logger.debug(output)
    return err, exitcode

def concurrent_pool(urls, file_output, nikto):
    starter = partial(run_nikto, file_output, nikto)
    errmsg = 'nikto has failed to run {} web headers testing, return code {}'
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as tp:
        fs = [tp.submit(starter, t) for t in urls]
        for fut in concurrent.futures.as_completed(fs, timeout=None):
            fn, rv = fut.result()
            if rv == 0:
                logging.debug('finished "{}"'.format(fn))
            elif rv < 0:
                logging.debug('problem with file "{}"'.format(fn))
            else:
                logging.debug(errmsg.format(fn, rv))