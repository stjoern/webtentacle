import logging
from os import path, rename
import xmltodict
import json
import pickle
import glob
import os

class Xml2Json(object):
    def __init__(self, filepath, url, xmloutput=None):
        self.file = path.abspath(filepath)
        self.file_result = None
        self.url = url
        self.xmloutput_file = xmloutput
        self.dir = Xml2Json.get_absolute_path_dir(filepath)
        self.__file = None
    
    @staticmethod
    def get_absolute_path_dir(relative_filepath):
        abspath = path.abspath(relative_filepath)
        return path.dirname(abspath)
        
    @staticmethod
    def file_exist(filepath):
        return True if path.exists(filepath) else False

    
    #@TODO: split sanitize and file writer
    
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
            data[0] = '<event>\n'
            # replace the last line with end tag root </webtentacle>
            data[-1] = '</event>'
            if len(data) < 1:
                logging.error('the xml output file is empty for scanned {} and file {}'.format(self.url, path.basename(self.file)))
                raise ValueError('Error in sanitizing xml file result') 
            # convert to xml
            # send it back to xml
            parse2file = "{}/{}".format(self.dir, self.xmloutput_file) if self.xmloutput_file is not None else self.file
            with open(parse2file, 'w') as fp:
                for row in data:
                    fp.write("{}\n".format(row))
            try:
                with open(parse2file) as fd:
                    doc = xmltodict.parse(fd.read())
            except Exception as error:
                logging.error('sanitize_xml: {}'.format(error)) 
                raise          # not to loose stack
            # write back to json file
            # replace xml extension to json
            pre, ext = path.splitext(self.file)
            json_file = pre + '.json'
            # todo take it away and make function
            old_file = self.file
            os.remove(old_file)
            logging.debug("deleted {} file".format(old_file))
            
            with open(json_file, 'w') as f:
                json.dump(doc, f)
            self.file_result = json_file
        else:
            logging.error("the file {} doesn't exist.".format(self.file))
            raise ValueError('No result file for {}'.format(self.url))
        

        
