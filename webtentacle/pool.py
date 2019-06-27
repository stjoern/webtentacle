from string import Template
from urllib.parse import urlsplit
import re
from datetime import datetime
import subprocess
from subprocess import Popen, PIPE
import os
import concurrent
from functools import partial

def run_nikto(file_output, ref_url, ):
    """
    use nikto to start testing web headers
    todo: add more arguments

    Arguments:
        url: url of the website
        filename: the ouptut will be saved to the file
    Returns:
        (filename, return value)
    """
    def get_file_output(ref_url, file_output):
        if not re.match(r'http(s?)\:',ref_url):
            ref_url = 'http://' + ref_url
        parsed = urlsplit(ref_url)
        host = parsed.netloc
        template = eval(file_output.get('template',''))
        ts = datetime.now().timestamp()
        substituted = template.substitute(url=host, timestamp=datetime.utcfromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S'))
        substituted += '.txt'
        print(substituted)
        return substituted, ref_url

    file_name, url = get_file_output(ref_url, file_output)
    file_output_path = '{}/{}'.format(file_output.get('folder','/tmp'), file_name)

    args = ["/usr/bin/nikto", "-h", url]#,'-Plugins "apache_expect"']#, '-Format xml']
   # p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
   # output, err = p.communicate()
   # exitcode = p.returncode
    f = open(file_output_path, "w")
    rv = subprocess.call(args, stdout=f, stderr=PIPE, shell=False)
    return file_name, rv
   # return exitcode, output, err

def concurrent_pool(urls, file_output):
    starter = partial(run_nikto, file_output)
    errmsg = 'nikto has failed to run {} web headers testing, return code {}'
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as tp:
        fs = [tp.submit(starter, t) for t in urls]
        for fut in concurrent.futures.as_completed(fs, timeout=None):
            fn, rv = fut.result()
            if rv == 0:
                print('finished "{}"'.format(fn))
            elif rv < 0:
                print('warning')
            else:
                print('error')