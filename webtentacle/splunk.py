#!/usr/bin/env python3

import splunklib.client as client
import splunklib.results as results
import logging
import os
import sys
import socket
from . import config

global service

settings = config.LoadConfig('./config.yml')
conf = settings.get_splunk()

service = client.connect(host=conf.get('host'),port=conf.get('port'),username=conf.get('username'),password=conf.get('password'),cookie=0)


def echo_installed_apps():
    for i, app in enumerate(service.apps):
        print("Installed applications: {}".format(app.name))
