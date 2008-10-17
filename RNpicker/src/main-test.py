import random
import unittest

import logging
import logging.handlers
import StringIO
import re
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
   
        self.conf = common.utils.Conf.get_instance()
        self.mainUrl  = self.conf.get("MainDatabaseAccess","url")
   
        print "Main URL=%s"%(self.mainUrl)
   
        # create DB connector
        self.mainConn = DatabaseConnector(self.mainUrl)
   
        self.mainConn.connect()
        
        self.archiveUrl  = self.conf.get("ArchiveDatabaseAccess","url")
   
        print "URL=%s"%(self.archiveUrl)
   
        # create DB connector
        self.archConn = DatabaseConnector(self.archiveUrl)
   
        self.archConn.connect()
        
    def assertIfNoTagsLeft(self,path):
        """
           Check that no tags are left in the XML
        """
        
        # pattern for looking for tags
        pattern="\${\w*}"
        
        # first read file in memory as the file is small
        f = open(path,"r")
        
        strToCheck = f.read()
        
        f.close()
        
        res = re.findall(pattern, strToCheck)
         
        self.failUnless((len(res) == 0), "Error. the file %s contains the following tags=%s"%(path,res))
            

    def getListOfSampleIDs(self,beginDate='2008-07-01',endDate='2008-07-31',spectralQualif='FULL',nbOfElem='100'):
        
       result = self.mainConn.execute(SQL_GETSAMPLEIDS%(beginDate,endDate,spectralQualif,nbOfElem))
        
       sampleIDs= []
        
       rows = result.fetchall()
       
       for row in rows:
           sampleIDs.append(row[0])
       
       print "samples %s\n"%(sampleIDs)
      
       return sampleIDs
      
    def tesstPrelParticulateSamples(self):
        
        # another recent sample = "0889826" 
        # tanzani 0888997
        # list to run on production 
        #listOfSamplesToTest = ["0892843","0892533","0892630","0892506","0892493"]
        #listOfSamplesToTest = [ "0889826" ]
        
        # get full
        listOfSamplesToTest = self.getListOfSampleIDs('2008-07-01',endDate='2008-07-31',spectralQualif='PREL',nbOfElem='10')
        listOfSamplesToTest = [857991]       
        #transform in numbers and retransform in str to remove the 0 at the beginning of the number"
        #intifiedlist = map(int,listOfSamplesToTest)
        
        #listOfSamplesToTest = map(str,intifiedlist)
        
        print "list of Prel Sample",listOfSamplesToTest
        
        for sampleID in listOfSamplesToTest:
           # fetchnoble particulate
           fetcher = DBDataFetcher.getDataFetcher(self.mainConn,self.archConn,sampleID)
   
           fetcher.fetch()
           
           #fetcher.printContent(open("/tmp/sample_%s_extract.data"%(sampleID),"w"))
       
           renderer = ParticulateRenderer(fetcher)
   
           xmlStr = renderer.asXmlStr()
           
           path = "/tmp/samples/sampml-prel-%s.xml"%(sampleID)
   
           common.xml_utils.pretty_print_xml(StringIO.StringIO(xmlStr),path)
           
           # check if no tags are left
           self.assertIfNoTagsLeft(path)

    def testFullParticulateSamples(self):
        
        # another recent sample = "0889826" 
        # tanzani 0888997
        # list to run on production 
        #listOfSamplesToTest = ["0892843","0892533","0892630","0892506","0892493"]
        
        
        # get full
        listOfSamplesToTest = self.getListOfSampleIDs('2008-07-01',endDate='2008-07-31',spectralQualif='FULL',nbOfElem='10')
        #listOfSamplesToTest = [ "857874" ]
        listOfSamplesToTest = [ "857882" ]
               
        #transform in numbers and retransform in str to remove the 0 at the beginning of the number"
        #intifiedlist = map(int,listOfSamplesToTest)
        
        #listOfSamplesToTest = map(str,intifiedlist)
        
        print "list Full of Sample",listOfSamplesToTest
        
        for sampleID in listOfSamplesToTest:
           # fetchnoble particulate
           fetcher = DBDataFetcher.getDataFetcher(self.mainConn,self.archConn,sampleID)
   
           fetcher.fetch()
           
           fetcher.printContent(open("/tmp/sample_%s_extract.data"%(sampleID),"w"))
       
           renderer = ParticulateRenderer(fetcher)
   
           xmlStr = renderer.asXmlStr()
           
           #print "Non Formatted String [%s]\n"%(xmlStr)
           
           f = open("/tmp/xmlStr.xml","w")
           
           f.write(xmlStr)
           f.close()
   
           path = "/tmp/samples/sampml-full-%s.xml"%(sampleID)
   
           common.xml_utils.pretty_print_xml(StringIO.StringIO(xmlStr),path)
           
           # check if no tags are left
           self.assertIfNoTagsLeft(path)

if __name__ == '__main__':
    unittest.main()
