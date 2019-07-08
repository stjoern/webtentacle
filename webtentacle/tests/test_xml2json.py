import unittest
from webtentacle.parser.xml2json import Xml2Json

class TestXml2json(unittest.TestCase):
    """
    Test the xml2json converter
    """
    def test_sanitize_xml(self):
        try:
            xml2json = Xml2Json(filepath="webtentacle/tests/data/test.xml", url="0.0.0.0", xmloutput="test_translated.xml")
            xml2json.sanitize_xml()
            result = Xml2Json.file_exist(xml2json.file_result)
            self.assertTrue(result)
        except Exception as exception:
            self.fail("sanitize_xml() raised Exception unexpectedly!")
            
if __name__ == '__main__':
    unittest.main()