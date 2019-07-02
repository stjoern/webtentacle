#!/usr/bin/env python3

import splunklib.client as client
import logging
from  . config import LoadConfig

settings = config.LoadConfig('./config.yml')
conf = settings.get_splunk()

service = client.connect(
    host=conf.get('host','localhost'), 
    port=conf.get('port',8089), 
    timeout=None, 
    username=conf.get('username','admin'),
    password=conf.get('password','changeme'))

def echo_installed_apps():
    for i, app in enumerate(service.apps):
        print("Installed applications: {}".format(app.name))


if __name__ == '__main__':
    print("splunk instance ...")
    echo_installed_apps()