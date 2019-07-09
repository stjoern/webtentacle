from webtentacle.splunk import initialize
import logging

class Users(object):
    def __init__(self):
        pass
    
    def get_users(self):
        kwargs = {"sort_key":"username", "sort_dir":"asc"}
        return initialize.splunk_service.users.list(count=-1, **kwargs)
    
    def create_user(self, username, password, roles):
        usernames = map(lambda x: x.name, self.get_users()) 
        if username not in usernames:
            user = initialize.splunk_service.users.create(username=username, password=password, roles=roles) 
            logging.info("New user {} created".format(username))
            return user
        else:
            logging.debug("User {} already created.".format(username))
            return
        
    #@TODO
    # delete_user
    # change roles
    # change password