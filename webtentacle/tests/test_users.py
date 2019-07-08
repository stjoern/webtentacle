import unittest
from webtentacle.splunk.users import Users
from webtentacle.splunk import initialize
from webtentacle.common.config import LoadConfig

class TestUsers(unittest.TestCase):
    """
    Test creating, updating, deleting user
    """
    def setUp(self):
        """
        initialize the connector to splunk
        """
        sg = LoadConfig("webtentacle/config.yml").get_splunk()
        initialize.init(host=sg.get("host"), 
                        port=sg.get("port"),
                        username="admin",
                        password="changemeagain",
                        cookie=0)
        
    def tearDown(self):
        """
        disconnect from splunk
        """
        initialize.splunk_service.logout()
        
    def test_create_user(self):
        try:
            users = Users()
            user = users.create_user(username="test", password="blueberry", roles=['power'])
            self.assertEqual(user.name, 'test')
        except Exception as exc:
            self.fail("cannot create user, error: {}".format(str(exc)))
            