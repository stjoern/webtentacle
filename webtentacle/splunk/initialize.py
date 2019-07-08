import splunklib.client as client

splunk_service = None

def init(host, port, username, password, cookie=1):
    global splunk_service
    splunk_service = client.connect(host=host, port=port, timeout=None, username=username, password=password, cookie=cookie)
    print("splunk connected..")
    
def get_installed_apps():
    for i, app in enumerate(splunk_service.apps):
        print("Installed application: {} - {}".format(i, app.name))