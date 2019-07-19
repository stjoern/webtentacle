import logging
from os import path, rename
import xmltodict
import json
import pickle
import glob
import os

logger = logging.getLogger('webtentacle')
    
class Xml2Json(object):
    def __init__(self, filepath, url, xmloutput):
        self.file = path.abspath(filepath)
        self.file_result = None
        self.url = url
        self.xmloutput = xmloutput
        self.dir = Xml2Json.get_absolute_path_dir(filepath)
        self.__file = None
    
    @staticmethod
    def get_absolute_path_dir(relative_filepath):
        abspath = path.abspath(relative_filepath)
        return path.dirname(abspath)
        
    @staticmethod
    def file_exist(filepath):
        return True if path.exists(filepath) else False


    def sanitize_xml(self):
        if Xml2Json.file_exist(self.file):
            data = None
            with open(self.file) as malformed_xml_file:
                data = malformed_xml_file.readlines()
            if not data:
                logging.error('no output data can be read from scanning {} with file {}'.format(self.url, path.basename(self.file))) 
                raise ValueError('Error in sanitizing xml file result')  
            # delete first two lines
            del data[0:1+1]
            # replace now the new first line with one root <webtentacle>
            data[0] = '<scan>\n'
            # replace the last line with end tag root </webtentacle>
            data[-1] = '</scan>'
            if len(data) < 1:
                logging.error('the xml output file is empty for scanned {} and file {}'.format(self.url, path.basename(self.file)))
                raise ValueError('Error in sanitizing xml file result') 
            # convert to xml
            # send it back to xml
            with open(self.xmloutput, 'w') as fp:
                for row in data:
                    fp.write("{}\n".format(row))
            try:
                with open(self.xmloutput) as fd:
                    doc = xmltodict.parse(fd.read())
                    if doc:
                        logger.info(self.url, extra=doc)
                    else:
                        raise ValueError("No parsed data {}".format("todo IP"))
            except Exception as error:
                logging.debug('Problem in sanitizing xml: {}'.format(error)) 
                raise          # not to loose stack
            # write back to json file
            # replace xml extension to json
            pre, ext = path.splitext(self.file)
            json_file = pre + '.json'
            
            with open(json_file, 'w') as f:
                json.dump(doc, f)
        else:
            logging.debug("Cannot parse scanning result, the file {file} doesn't exist for {url}".format(file=self.file, url=self.url))
            raise ValueError('Cannot parse scanning result for {url}'.format(self.url))
        

        
