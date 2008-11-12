import random
import unittest

import time
import os
import logging
import logging.handlers
import StringIO
import re
from lxml import etree

import ctbto.common.utils
import ctbto.common.xml_utils

from ctbto.common    import Conf
from ctbto.db        import DatabaseConnector,DBDataFetcher

#from ctbto.db        import DBDataFetcher

from ctbto.renderers import GenieParticulateRenderer
from ctbto.renderers import SaunaRenderer


SQL_GETSAMPLEIDS = "select sample_id from RMSMAN.GARDS_SAMPLE_Data where (collect_stop between to_date('%s','YYYY-MM-DD HH24:MI:SS') and to_date('%s','YYYY-MM-DD HH24:MI:SS')) and  spectral_qualifier='%s' and ROWNUM <= %s"

SQL_GETSAUNASAMPLEIDS = "select SAMPLE_ID,STATION_ID,SITE_DET_CODE from GARDS_SAMPLE_DATA where station_id in (522, 684) and (collect_stop between to_date('%s','YYYY-MM-DD HH24:MI:SS') and to_date('%s','YYYY-MM-DD HH24:MI:SS')) and  spectral_qualifier='%s' and ROWNUM <= %s"

def myBasicLoggingConfig():
    """
    Do basic configuration for the logging system by creating a
    StreamHandler with a default Formatter and adding it to the
    root logger.
    """
    if len(logging.root.handlers) == 0:
        hdlr = logging.handlers.RotatingFileHandler("/tmp/logging.log", "a", 5000000, 4)
        console = logging.StreamHandler()
        fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        hdlr.setFormatter(fmt)
        console.setFormatter(fmt)
        logging.root.addHandler(hdlr)
        logging.root.addHandler(console)
        
        log = logging.getLogger("ROOT")
        log.setLevel(logging.DEBUG)
        log.info("Start")


class TestSAMPMLCreator(unittest.TestCase):
    
    def _setUpGenieParticulate(self):
        
        activateTimer = True
        
        self.mainDatabase  = self.conf.get("MainDatabaseAccess","hostname")
        self.mainUser      = self.conf.get("MainDatabaseAccess","user")
        self.mainPassword  = self.conf.get("MainDatabaseAccess","password")
   
        print "Main Database=%s"%(self.mainDatabase)
   
        # create DB connector
        self.mainConn = DatabaseConnector(self.mainDatabase,self.mainUser,self.mainPassword,activateTimer)
   
        self.mainConn.connect()
        
        self.archiveDatabase  = self.conf.get("ArchiveDatabaseAccess","hostname")
        self.archiveUser      = self.conf.get("ArchiveDatabaseAccess","user")
        self.archivePassword  = self.conf.get("ArchiveDatabaseAccess","password")
   
        print "Archive Database=%s"%(self.archiveDatabase)
   
        # create DB connector
        self.archConn = DatabaseConnector(self.archiveDatabase,self.archiveUser,self.archivePassword,activateTimer)
   
        self.archConn.connect()
        
        # compile xpath expressions used to check final product
        self.xpath_calIDs      = etree.XPath("//*[local-name(.)='CalibrationInformation']/*[local-name(.)='Calibration']/@ID")
        self.xpath_specalIDs   = etree.XPath("//*[local-name(.)='MeasuredInformation']/*[local-name(.)='Spectrum']/@calibrationIDs")
    
    
    
    def _setUpNobleGaz(self):
        
        activateTimer = True
        
        self.conf = Conf.get_instance()
        self.nbDatabase  = self.conf.get("NobleGazDatabaseAccess","hostname")
        self.nbUser      = self.conf.get("NobleGazDatabaseAccess","user")
        self.nbPassword  = self.conf.get("NobleGazDatabaseAccess","password")
   
        print "NB Database=%s"%(self.nbDatabase)
   
        # create DB connector
        self.nbConn = DatabaseConnector(self.nbDatabase,self.nbUser,self.nbPassword,activateTimer)
   
        self.nbConn.connect()
    
    
    def setUp(self):
         
        myBasicLoggingConfig()  
        
        # need to setup the ENV containing the the path to the conf file:
        os.environ[Conf._ENVNAME] = "/home/aubert/dev/src-reps/java-balivernes/RNpicker/etc/conf/rnpicker.config"
   
        self.conf = Conf.get_instance()
   
        self._setUpGenieParticulate()
        
        self._setUpNobleGaz()
        
        
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
        
    def assertAllCalibrationInfo(self,path):
        """
           check that the calibration info is there
        """
        
        tree = etree.parse(open(path,"r"))
        
        #xpath1 = etree.XPath("//CalibrationInformation/Calibration[@ID]")
        
        calibrationIDs    = self.xpath_calIDs(tree)
        specCalIDs        = self.xpath_specalIDs(tree)

        print "spec cal = %s\n"%(specCalIDs)
        print "calibrationIDs =%s\n"%(calibrationIDs)
        
        for cals in specCalIDs:
            # split string
            clist = cals.split(' ')
            for elem in clist:
                self.failUnless((elem in calibrationIDs), "Error the following calibration info %s is not defined in the <Calibration> Tag. Xml file produced %s\n"%(elem,path))
        
   
           

    def getListOfSampleIDs(self,beginDate='2008-07-01',endDate='2008-07-31',spectralQualif='FULL',nbOfElem='100'):
        
       result = self.mainConn.execute(SQL_GETSAMPLEIDS%(beginDate,endDate,spectralQualif,nbOfElem))
        
       sampleIDs= []
        
       rows = result.fetchall()
       
       for row in rows:
           sampleIDs.append(row[0])
       
       print "samples %s\n"%(sampleIDs)
      
       return sampleIDs
   
    def getListOfSaunaSampleIDs(self,beginDate='2008-07-01',endDate='2008-07-31',spectralQualif='FULL',nbOfElem='100'):
        
       result = self.nbConn.execute(SQL_GETSAUNASAMPLEIDS%(beginDate,endDate,spectralQualif,nbOfElem))
        
       sampleIDs= []
        
       rows = result.fetchall()
       
       for row in rows:
           sampleIDs.append(row[0])
       
       print "sauna samples %s\n"%(sampleIDs)
      
       return sampleIDs
      
    def tesstPrelParticulateSamples(self):
        
        # another recent sample = "0889826" 
        # tanzani 0888997
        # list to run on production 
        #listOfSamplesToTest = ["0892843","0892533","0892630","0892506","0892493"]
        #listOfSamplesToTest = [ "0889826" ]
        
        # get full
        listOfSamplesToTest = self.getListOfSampleIDs('2008-07-01',endDate='2008-07-31',spectralQualif='PREL',nbOfElem='1')
        #listOfSamplesToTest = [857991]       
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

    def tesstFullGenieParticulateSamples(self):
        
        # another recent sample = "0889826" 
        # tanzani 0888997
        # list to run on production 
        #listOfSamplesToTest = ["0892843","0892533","0892630","0892506","0892493"]
        
        request="spectrum=ALL, analysis=ALL"
        
        # get full
        listOfSamplesToTest = self.getListOfSampleIDs('2008-10-24',endDate='2008-10-26',spectralQualif='FULL',nbOfElem='1')
        
        # error
        #listOfSamplesToTest = [ "700637" ]
               
        #transform in numbers and retransform in str to remove the 0 at the beginning of the number"
        #intifiedlist = map(int,listOfSamplesToTest)
        
        #listOfSamplesToTest = map(str,intifiedlist)
        
        print "list Full of Sample",listOfSamplesToTest
        
        cpt = 0
        total_t0 = time.time()
        
        for sampleID in listOfSamplesToTest:
            
           print "Start Test %d for SampleID %s.\n"%(cpt,sampleID)
           
           t0 = time.time()
           
           # fetchnoble particulate
           fetcher = DBDataFetcher.getDataFetcher(self.mainConn,self.archConn,sampleID)
   
           fetcher.fetch(request)
                 
           renderer = GenieParticulateRenderer(fetcher)
   
           xmlStr = renderer.asXmlStr(request)
           
           #print "Non Formatted String [%s]\n"%(xmlStr)
           
           f = open("/tmp/xmlStr.xml","w")
           
           f.write(xmlStr)
           f.close()
   
           path = "/tmp/samples/sampml-full-%s.xml"%(sampleID)
   
           ctbto.common.xml_utils.pretty_print_xml(StringIO.StringIO(xmlStr),path)
           
           # check if no tags are left
           self.assertIfNoTagsLeft(path)
           
           self.assertAllCalibrationInfo(path)
           
           t1 = time.time()
           
           print "End of Test %d for SampleID %s.\nTest executed in %s seconds.\n\n**************************************************************** \n**************************************************************** \n"%(cpt,sampleID,(t1-t0))
           
           cpt +=1
        
        total_t1 = time.time()
        
        print "****************************************************************************\n"
        print "****************************************************************************\n"
        print "****** EXECUTED %d FULL SAMPLE RETRIEVALS in %s seconds   ******************\n"%(cpt,total_t1-total_t0)
        print "****************************************************************************\n"
        print "****************************************************************************\n"
        
    def testFullNobleGazSamples(self):
        
        # another recent sample = "0889826" 
        # tanzani 0888997
        # list to run on production 
        #listOfSamplesToTest = ["0892843","0892533","0892630","0892506","0892493"]
        
        request="spectrum=ALL, analysis=ALL"
        
        # get full
        listOfSamplesToTest = self.getListOfSaunaSampleIDs('2007-10-24',endDate='2008-10-30',spectralQualif='FULL',nbOfElem='1000')
        
        # error
        # 103729,241116     
        listOfSamplesToTest = [ "206975" ]
        
        #print "list of samples %s\n"%(listOfSamplesToTest)
              
        # remove sampleID for which data isn't available
        if "141372" in listOfSamplesToTest:
           listOfSamplesToTest.remove("141372")
               
        #transform in numbers and retransform in str to remove the 0 at the beginning of the number"
        #intifiedlist = map(int,listOfSamplesToTest)
        
        #listOfSamplesToTest = map(str,intifiedlist)
        
        print "list Full of Sample",listOfSamplesToTest
        
        cpt = 0
        total_t0 = time.time()
        
        for sampleID in listOfSamplesToTest:
            
           print "Start Test %d for SampleID %s.\n"%(cpt,sampleID)
           
           t0 = time.time()
           
           # fetchnoble particulate
           fetcher = DBDataFetcher.getDataFetcher(self.nbConn,self.archConn,sampleID)
   
           fetcher.fetch(request)
                 
           renderer = SaunaRenderer(fetcher)
   
           xmlStr = renderer.asXmlStr(request)
           
           #print "Non Formatted String [%s]\n"%(xmlStr)
           
           #f = open("/tmp/xmlStr.xml","w")
           
           #f.write(xmlStr)
           #f.close()
   
           path = "/tmp/samples/sampml-full-%s.xml"%(sampleID)
   
           ctbto.common.xml_utils.pretty_print_xml(StringIO.StringIO(xmlStr),path)
           
           # check if no tags are left
           #self.assertIfNoTagsLeft(path)
           
           #self.assertAllCalibrationInfo(path)
           
           t1 = time.time()
           
           print "End of Test %d for SampleID %s.\nTest executed in %s seconds.\n\n**************************************************************** \n**************************************************************** \n"%(cpt,sampleID,(t1-t0))
           
           cpt +=1
        
        total_t1 = time.time()
        
        print "****************************************************************************\n"
        print "****************************************************************************\n"
        print "****** EXECUTED %d FULL SAMPLE RETRIEVALS in %s seconds   ******************\n"%(cpt,total_t1-total_t0)
        print "****************************************************************************\n"
        print "****************************************************************************\n"
        

if __name__ == '__main__':
    unittest.main()
