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

SQL_GETSAMPLEIDS = "select sample_id from RMSMAN.GARDS_SAMPLE_Data where (collect_stop between to_date('%s','YYYY-MM-DD HH24:MI:SS') and to_date('%s','YYYY-MM-DD HH24:MI:SS')) and  spectral_qualifier='%s' and ROWNUM <= %s"


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

    def getListOfSampleIDs(self,beginDate='2008-07-01',endDate='2008-07-31',spectralQualif='FULL',nbOfElem='100'):
        
       result = self.conn.execute(SQL_GETSAMPLEIDS%(beginDate,endDate,spectralQualif,nbOfElem))
        
       sampleIDs= []
        
       rows = result.fetchall()
       
       for row in rows:
           sampleIDs.append(row[0])
       
       print "samples %s\n"%(sampleIDs)
      
       return sampleIDs
        

    def testFullParticulateSamples(self):
        
        # another recent sample = "0889826" 
        # tanzani 0888997
        # list to run on production 
        #listOfSamplesToTest = ["0892843","0892533","0892630","0892506","0892493"]
        #listOfSamplesToTest = [ "0889826" ]
        
        # get full
        listOfSamplesToTest = self.getListOfSampleIDs('2008-07-01',endDate='2008-07-31',spectralQualif='FULL',nbOfElem='10')
               
        #transform in numbers and retransform in str to remove the 0 at the beginning of the number"
        #intifiedlist = map(int,listOfSamplesToTest)
        
        #listOfSamplesToTest = map(str,intifiedlist)
        
        print "list of Sample",listOfSamplesToTest
        
        for sampleID in listOfSamplesToTest:
           # fetchnoble particulate
           fetcher = DBDataFetcher.getDataFetcher(self.conn,sampleID)
   
           fetcher.fetch()
           
           fetcher.printContent(open("/tmp/sample_%s_extract.data"%(sampleID),"w"))
       
           renderer = ParticulateRenderer(fetcher)
   
           xmlStr = renderer.asXmlStr()
   
           common.xml_utils.pretty_print_xml(StringIO.StringIO(xmlStr),"/tmp/samples/sampml-%s.xml"%(sampleID))

if __name__ == '__main__':
    unittest.main()
