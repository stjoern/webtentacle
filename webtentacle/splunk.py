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



service = client.connect(host=os.getenv('MOTHER_HOSTNAME'),
                         port=conf.get('port'),
                         username='admin',
                         password=os.getenv('SPLUNK_INITIAL_PASSWORD'),
                         cookie=0)

def get_users():
    # get collection of users
    kwargs = {"sort_key":"username","sort_dir":"asc"}
    return service.users.list(count=-1, **kwargs)


users = get_users()
print("Users:")
for user in users:
    print("{} {}".format(user.realname, user.name))
    for role in user.role_entities:
        print(" - ", role.name)
        
def create_user(username, password):
    user = service.users.create(username=username, password=password, roles=['power','user','admin'])
    return user


usernames = map(lambda x: x.name, users)
if os.getenv('SPLUNK_WEBTENTACLE_USER') not in usernames:
    create_user(os.getenv('SPLUNK_WEBTENTACLE_USER'),os.getenv('SPLUNK_WEBTENTACLE_PASSWORD'))
service.logout()

service = client.connect(host='splunkenterprise',
                         port=int(conf.get('port')),
                         username=os.getenv('SPLUNK_WEBTENTACLE_USER'),
                         password=os.getenv('SPLUNK_WEBTENTACLE_PASSWORD'))


def echo_installed_apps():
    for i, app in enumerate(service.apps):
        print("Installed applications: {}".format(app.name))
