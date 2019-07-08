import unittest
from webtentacle.splunk.data2splunk import *
from webtentacle.splunk import initialize
from webtentacle.common.config import LoadConfig

class TestData2splunk(unittest.TestCase):
    """
    Test folder, file, different format input to the Splunk
    """
    def setUp(self):
        """
        initialize the connector to splunk
        """
        sg = LoadConfig("webtentacle/config.yml").get_splunk()
        initialize.init(host=sg.get("host"), port=sg.get("port"), username="admin",password="changemeagain", cookie=0)
        
    def tearDown(self):
        """
        disconnect from splunk
        """
        initialize.splunk_service.logout()
    
    @unittest.skip("not now")
    def test_single(self):
        try:
            dump = Data2Splunk(source="test-single-file.json", sourcetype="_json", delete_after=0)
            dump.single("webtentacle/tests/data/test.json")
            self.assertTrue(1) #@todo query from splunk (we need to implement query)
        except Exception as exception:
            self.fail("single json dump to Splunk raised Exception unexpectedly! Error: {}", str(exception))
            
    def test_bulk(self):
        try:
            dump = Data2Splunk(source="test-bulk-file.json", sourcetype="_json", delete_after=0)
            dump.bulk(directory="webtentacle/tests/data/",extension="json")
            self.assertTrue(1) #@todo query from splunk (we need to implement query)
        except Exception as exception:
            self.fail("single json dump to Splunk raised Exception unexpectedly! Error: {}", str(exception))
            
            
if __name__ == '__main__':
    unittest.main()