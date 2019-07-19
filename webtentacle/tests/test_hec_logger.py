import unittest
from webtentacle.splunk.hec_handler import hec_logger
from webtentacle.common.config import config
import string
import random
from subprocess import Popen, PIPE


class TestHecLogger(unittest.TestCase):
    
    def test_initialize(self):
        try:
            hec_logger.initialize()
        except Exception as exception:
            self.fail("During hec logger initialization an exception raised. Error: {}".format(str(exception)))
        