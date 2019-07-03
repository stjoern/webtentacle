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



service = client.connect(host=socket.gethostname(),port=conf.get('port'),username='admin',password='changemeagain',cookie=0)

def get_users():
    # get collection of users
    return service.users

def create_user(username, password):
    user = service.users.create(username=username, password=password, roles=['power','user','admin'])
    return user


#create_user('webtentacle','letmeinplease')
#service.logout()

#service = client.connect(host=socket.gethostname(),
#                         port=conf.get('port'),
#                         username='webtentacle',
#                         password='letmeinplease',
#                         cookie=0)


def echo_installed_apps():
    for i, app in enumerate(service.apps):
        print("Installed applications: {}".format(app.name))
