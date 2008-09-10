import random
import unittest

import logging
import logging.handlers
import StringIO
import common.utils
import common.xml_utils
from db.datafetchers import DBDataFetcher
from db.connections import DatabaseConnector
from renderers.SAMPMLrendererv1 import ParticulateRenderer


def myBasicLoggingConfig():
    """
    Do basic configuration for the logging system by creating a
    StreamHandler with a default Formatter and adding it to the
    root logger.
    """
    if len(logging.root.handlers) == 0:
        hdlr = logging.handlers.RotatingFileHandler("/tmp/logging.log", "a", 5000000, 4)
        # fmt = logging.Formatter(logging.BASIC_FORMAT)
        fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        hdlr.setFormatter(fmt)
        logging.root.addHandler(hdlr)


class TestSAMPMLCreator(unittest.TestCase):
    
    def setUp(self):
         
        myBasicLoggingConfig()  
        log = logging.getLogger("ROOT")
        log.setLevel(logging.DEBUG)
        log.info("Start")
   
        self.conf = common.utils.Conf.get_conf()
        self.url  = self.conf.get("DatabaseAccess","url")
   
        print "URL=%s"%(self.url)
   
        # create DB connector
        self.conn = DatabaseConnector(self.url)
   
        self.conn.connect()

    def testParticulateSamples(self):
        
        
        
        # another recent sample = "0889826" 
        # tanzani 0888997
        listOfSamplesToTest = [ "0889826" ]
        
        #transform in numbers and retransform in str to remove the 0 at the beginning of the number"
        intifiedlist = map(int,listOfSamplesToTest)
        
        listOfSamplesToTest = map(str,intifiedlist)
        
        print "list of Sample",listOfSamplesToTest
        
        for sampleID in listOfSamplesToTest:
           # fetchnoble particulate
           fetcher = DBDataFetcher.getDataFetcher(self.conn,sampleID)
   
           fetcher.fetch()
   
           renderer = ParticulateRenderer(fetcher)
   
           xmlStr = renderer.asXmlStr()
   
           common.xml_utils.pretty_print_xml(StringIO.StringIO(xmlStr),"/tmp/sampml-%s.xml"%(sampleID))

if __name__ == '__main__':
    unittest.main()
