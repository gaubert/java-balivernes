
import unittest
import os
import time
import logging
import logging.handlers
import StringIO
import re
from lxml import etree

import ctbto.common.utils as utils
import ctbto.common.xml_utils

from ctbto.db        import DatabaseConnector,DBDataFetcher
from org.ctbto.conf  import Conf

from ctbto.renderers import GenieParticulateRenderer
from ctbto.renderers import SaunaRenderer
from ctbto.transformer import XML2HTMLRenderer


SQL_GETSAMPLEIDS = "select sample_id from RMSMAN.GARDS_SAMPLE_Data where (collect_stop between to_date('%s','YYYY-MM-DD HH24:MI:SS') and to_date('%s','YYYY-MM-DD HH24:MI:SS')) and  spectral_qualifier='%s' and ROWNUM <= %s"

SQL_GETSAUNASAMPLEIDS  = "select SAMPLE_ID from GARDS_SAMPLE_DATA where station_id in (522, 684) and (collect_stop between to_date('%s','YYYY-MM-DD HH24:MI:SS') and to_date('%s','YYYY-MM-DD HH24:MI:SS')) and  spectral_qualifier='%s' and ROWNUM <= %s order by SAMPLE_ID"

SQL_GETSPALAXSAMPLEIDS = "select SAMPLE_ID from GARDS_SAMPLE_DATA where station_id in (600,542,555,566,521,620,685,614,595) and (collect_stop between to_date('%s','YYYY-MM-DD HH24:MI:SS') and to_date('%s','YYYY-MM-DD HH24:MI:SS')) and  spectral_qualifier='%s' and ROWNUM <= %s order by SAMPLE_ID"

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
        log.setLevel(logging.INFO)
        log.info("Start")

import ctbto.tests
class TestSAMPMLCreator(unittest.TestCase):
    
    # Class members
    c_log = logging.getLogger("main_tests.TestSAMPMLCreator")
    c_log.setLevel(logging.INFO)
    
    def _get_tests_dir_path(self):
        """ get the ctbto.tests path depending on where it is defined """
        
        fmod_path = ctbto.tests.__path__
        
        test_dir = "%s/conf_tests"%fmod_path[0]
        
        return test_dir
    
    def __init__(self,stuff):
        super(TestSAMPMLCreator,self).__init__(stuff)
        
        myBasicLoggingConfig()  
        
        os.environ['RNPICKER_CONF_DIR'] = self._get_tests_dir_path()
        
        os.environ[Conf.ENVNAME] = '%s/%s'%(self._get_tests_dir_path(),'rnpicker.config')
        
        # create an empty shell Conf object
        self.conf = Conf.get_instance()
    
        self.mainDatabase      = None
        self.mainUser          = None
        self.mainPassword      = None
        self.mainConn          = None
        self.mainActivateTimer = False
        
        self.ParticulateArchiveDatabaseAccess      = None
        self.archiveUser          = None
        self.archivePassword      = None
        self.archiveActivateTimer = False
        self.archConn             = None
        
        self.xpath_calIDs      = None
        self.xpath_specalIDs   = None
        
        self.nbDatabase        = None
        self.nbUser            = None
        self.nbPassword        = None
        self.nbActivateTimer   = False
        self.nbConn            = None
        
        TestSAMPMLCreator.c_log.info("\n********************************************************************************\n  rnpicker modules are loaded from %s\n********************************************************************************\n"%(self._get_tests_dir_path()))
    
    def _setUpGenieParticulate(self):
        
        
        self.mainDatabase  = self.conf.get("ParticulateDatabaseAccess","hostname")
        self.mainUser      = self.conf.get("ParticulateDatabaseAccess","user")
        self.mainPassword  = self.conf.get("ParticulateDatabaseAccess","password")
        self.mainActivateTimer = self.conf.getboolean("ParticulateDatabaseAccess","activateTimer",True)
   
        TestSAMPMLCreator.c_log.info("")
        TestSAMPMLCreator.c_log.info("Particulate Database=%s"%(self.mainDatabase))
   
        # create DB connector
        self.mainConn = DatabaseConnector(self.mainDatabase,self.mainUser,self.mainPassword,self.mainActivateTimer)
   
        self.mainConn.connect()
        
        self.ParticulateArchiveDatabaseAccess  = self.conf.get("ParticulateArchiveDatabaseAccess","hostname")
        self.archiveUser      = self.conf.get("ParticulateArchiveDatabaseAccess","user")
        self.archivePassword  = self.conf.get("ParticulateArchiveDatabaseAccess","password")
        self.archiveActivateTimer    = self.conf.getboolean("ParticulateArchiveDatabaseAccess","activateTimer",True)
   
   
        TestSAMPMLCreator.c_log.info("Archive Database=%s"%(self.ParticulateArchiveDatabaseAccess))
   
        # create DB connector
        self.archConn = DatabaseConnector(self.ParticulateArchiveDatabaseAccess,self.archiveUser,self.archivePassword,self.archiveActivateTimer)
   
        self.archConn.connect()
        
        # compile xpath expressions used to check final product
        self.xpath_calIDs      = etree.XPath("//*[local-name(.)='CalibrationInformation']/*[local-name(.)='Calibration']/@ID")
        self.xpath_specalIDs   = etree.XPath("//*[local-name(.)='MeasuredInformation']/*[local-name(.)='Spectrum']/@calibrationIDs")
    
    def _setUpNobleGaz(self):
           
        self.nbDatabase        = self.conf.get("NobleGazDatabaseAccess","hostname")
        self.nbUser            = self.conf.get("NobleGazDatabaseAccess","user")
        self.nbPassword        = self.conf.get("NobleGazDatabaseAccess","password")
        self.nbActivateTimer   = self.conf.getboolean("NobleGazDatabaseAccess","activateTimer",True)
   
   
        TestSAMPMLCreator.c_log.info("Noble Gaz Database=%s"%(self.nbDatabase))
   
        # create DB connector
        self.nbConn = DatabaseConnector(self.nbDatabase,self.nbUser,self.nbPassword,self.nbActivateTimer)
   
        self.nbConn.connect()
    
    
    def setUp(self):
   
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
           Check that the calibration info is there
        """
        
        tree = etree.parse(open(path,"r"))
        
        #xpath1 = etree.XPath("//CalibrationInformation/Calibration[@ID]")
        
        calibrationIDs    = self.xpath_calIDs(tree)
        specCalIDs        = self.xpath_specalIDs(tree)

        TestSAMPMLCreator.c_log.debug("spec cal = %s\n"%(specCalIDs))
        TestSAMPMLCreator.c_log.debug("calibrationIDs =%s\n"%(calibrationIDs))
        
        for cals in specCalIDs:
            # split string
            clist = cals.split(' ')
            for elem in clist:
                self.failUnless((elem in calibrationIDs), "Error the following calibration info %s is not defined in the <Calibration> Tag. Xml file produced %s\n"%(elem,path))
        
   
    def assertFileContentEquals(self,a_master_path,a_tocheck_path):
        """
           check at the string level that the two files are identical otherwise fail
        """
        TestSAMPMLCreator.c_log.info("Start bit checking")
        
        linenum = 1
        master  = open(a_master_path,'r')
        tocheck = open(a_tocheck_path,'r')
        
        for m_line in master:
            c_line = tocheck.readline()
            
            if m_line != c_line:
                self.fail("line num %d is different on the master %s and on the file to check %s.\n master line:[%s]\n tcheck line:[%s]"%(linenum,a_master_path,a_tocheck_path,m_line,c_line))
          
        TestSAMPMLCreator.c_log.info("End of bit checking") 
        
    def getListOfSampleIDs(self,beginDate='2008-07-01',endDate='2008-07-31',spectralQualif='FULL',nbOfElem='100'):
        
        result = self.mainConn.execute(SQL_GETSAMPLEIDS%(beginDate,endDate,spectralQualif,nbOfElem))
        
        sampleIDs= []
        
        rows = result.fetchall()
       
        for row in rows:
            sampleIDs.append(row[0])
       
        TestSAMPMLCreator.c_log.info("samples %s\n"%(sampleIDs))
      
        return sampleIDs
   
    def getListOfSaunaSampleIDs(self,beginDate='2008-07-01',endDate='2008-07-31',spectralQualif='FULL',nbOfElem='100'):
        
        result = self.nbConn.execute(SQL_GETSAUNASAMPLEIDS%(beginDate,endDate,spectralQualif,nbOfElem))
        
        sampleIDs= []
        
        rows = result.fetchall()
       
        for row in rows:
            sampleIDs.append(row[0])
       
        TestSAMPMLCreator.c_log.info("sauna samples %s\n"%(sampleIDs))
      
        return sampleIDs
    
    def getListOfSpalaxSampleIDs(self,beginDate='2008-07-01',endDate='2008-07-31',spectralQualif='FULL',nbOfElem='100'):
        
        result = self.nbConn.execute(SQL_GETSPALAXSAMPLEIDS%(beginDate,endDate,spectralQualif,nbOfElem))
        
        sampleIDs= []
        
        rows = result.fetchall()
       
        for row in rows:
            sampleIDs.append(row[0])
       
        TestSAMPMLCreator.c_log.info("spalax samples %s\n"%(sampleIDs))
      
        return sampleIDs
    
          
    def ztestGetOneParticulateSampleAndDoBitChecking(self):
        """
           get a unique particulate sample and do a bit checking against a registered existing sample
        """
        
        request="spectrum=CURR, analysis=CURR"
        cpt = 0
        total_t0 = time.time()
        
        #listOfSamplesToTest = self.getListOfSampleIDs('2008-12-24',endDate='2008-12-25',spectralQualif='FULL',nbOfElem='1')
        
        #sampleID = listOfSamplesToTest[0]
        sampleID = 967273
        
        # fetchnoble particulate
        fetcher = DBDataFetcher.getDataFetcher(self.mainConn,self.archConn,sampleID)
            
        fetcher.fetch(request,'PAR')
                 
        renderer = GenieParticulateRenderer(fetcher)
   
        xmlStr = renderer.asXmlStr(request)
           
        path = "/tmp/samples/sampml-full-%s.xml"%(sampleID)
   
        ctbto.common.xml_utils.pretty_print_xml(StringIO.StringIO(xmlStr),path)
           
        # check if no tags are left
        self.assertIfNoTagsLeft(path)
           
        self.assertAllCalibrationInfo(path)
        
        self.assertFileContentEquals("%s/samples/sampml-full-%s.xml.master"%(self._get_tests_dir_path(),sampleID),path)
                           
        cpt +=1
        
        total_t1 = time.time()
        
        TestSAMPMLCreator.c_log.info("\n****************************************************************************\n****************************************************************************\n****** EXECUTED %d FULL SAMPLE RETRIEVALS in %s seconds   ********\n****************************************************************************\n****************************************************************************\n"%(cpt,total_t1-total_t0))



    def ztestFullGenieParticulateSamples(self):
        """ 
           test Genie Particulate samples 
        """
         
        request="spectrum=ALL, analysis=ALL"
        
        # get full 2003-10-24 to 2003-10-26
        listOfSamplesToTest = self.getListOfSampleIDs('2007-10-24',endDate='2008-10-26',spectralQualif='FULL',nbOfElem='2')
        
        # error
        #listOfSamplesToTest = [ "700637" ]
               
        #transform in numbers and retransform in str to remove the 0 at the beginning of the number"
        #intifiedlist = map(int,listOfSamplesToTest)
        
        #listOfSamplesToTest = map(str,intifiedlist)
        
        TestSAMPMLCreator.c_log.info("list samples: %s"%listOfSamplesToTest)
        
        cpt = 0
        total_t0 = time.time()
        
        for sampleID in listOfSamplesToTest:
            
            TestSAMPMLCreator.c_log.info("\n********************************************************************************\n    Start Test %d for SampleID %s.\n********************************************************************************\n"%(cpt,sampleID))
           
            t0 = time.time()
           
            # fetchnoble particulate
            fetcher = DBDataFetcher.getDataFetcher(self.mainConn,self.archConn,sampleID)
            
            fetcher.fetch(request,'PAR')
                 
            renderer = GenieParticulateRenderer(fetcher)
   
            xmlStr = renderer.asXmlStr(request)
           
            path = "/tmp/samples/sampml-full-%s.xml"%(sampleID)
   
            ctbto.common.xml_utils.pretty_print_xml(StringIO.StringIO(xmlStr),path)
           
            # check if no tags are left
            self.assertIfNoTagsLeft(path)
           
            self.assertAllCalibrationInfo(path)
           
            t1 = time.time()
           
            TestSAMPMLCreator.c_log.info("\n********************************************************************************\n    End of Test %d for SampleID %s. Test executed in %s seconds.\n********************************************************************************\n"%(cpt,sampleID,(t1-t0)))
                       
            cpt +=1
        
        total_t1 = time.time()
        
        TestSAMPMLCreator.c_log.info("\n****************************************************************************\n****************************************************************************\n****** EXECUTED %d FULL SAMPLE RETRIEVALS in %s seconds   ********\n****************************************************************************\n****************************************************************************\n"%(cpt,total_t1-total_t0))

    def ztestFullNobleGazSamples(self):
        """ 
           Get Full Noble Gaz samples.
        """
         
        request="spectrum=CURR/DETBK/GASBK/QC, analysis=CURR"
        
        # get full
        listOfSamplesToTest = self.getListOfSaunaSampleIDs('2008-08-11',endDate='2008-12-12',spectralQualif='FULL',nbOfElem='2')
               
        # remove sampleID for which data isn't available
        if "141372" in listOfSamplesToTest:
            listOfSamplesToTest.remove("141372")
               
        TestSAMPMLCreator.c_log.info("list samples :%s"%(listOfSamplesToTest))
        
        cpt = 0
        total_t0 = time.time()
        
        for sampleID in listOfSamplesToTest:
            
            TestSAMPMLCreator.c_log.info("Start Test %d for SampleID %s.\n"%(cpt,sampleID))
           
            t0 = time.time()
           
            # fetchnoble particulate
            fetcher = DBDataFetcher.getDataFetcher(self.nbConn,self.archConn,sampleID)
            
            #modify remoteHost
            fetcher.setRemoteHost(self.conf.get('RemoteAccess','nobleGazRemoteHost','dls007'))
   
            fetcher.fetch(request,'GAS')
                 
            renderer = SaunaRenderer(fetcher)
   
            xmlStr = renderer.asXmlStr(request)
           
           #print "Non Formatted String [%s]\n"%(xmlStr)
           
           #f = open("/tmp/xmlStr.xml","w")
           
           #f.write(xmlStr)
           #f.close()
   
            path = "/tmp/samples/sampml-full-%s.xml"%(sampleID)
   
            ctbto.common.xml_utils.pretty_print_xml(StringIO.StringIO(xmlStr),path)
           
            # check if no tags are left
            self.assertIfNoTagsLeft(path)
           
           #self.assertAllCalibrationInfo(path)
           
            t1 = time.time()
           
            #TestSAMPMLCreator.c_log.info("End of Test %d for SampleID %s.\nTest executed in %s seconds.\n\n**************************************************************** \n**************************************************************** \n"%(cpt,sampleID,(t1-t0)))
            TestSAMPMLCreator.c_log.info("\n********************************************************************************\n    End of Test %d for SampleID %s. Test executed in %s seconds.\n********************************************************************************\n"%(cpt,sampleID,(t1-t0)))
           
            cpt +=1
        
        total_t1 = time.time()
        
        TestSAMPMLCreator.c_log.info("\n****************************************************************************\n****************************************************************************\n****** EXECUTED %d FULL SAMPLE RETRIEVALS in %s seconds   ********\n****************************************************************************\n****************************************************************************\n"%(cpt,total_t1-total_t0))
    
    def testSpalaxFullNobleGazSamples(self):
        """ 
           Get Full Noble Gaz samples.
        """
         
        request="spectrum=ALL, analysis=CURR"
        
        # get full
        listOfSamplesToTest = self.getListOfSpalaxSampleIDs('2009-01-01',endDate='2009-12-12',spectralQualif='FULL',nbOfElem='2')
               
        # remove sampleID for which data isn't available
        #if "141372" in listOfSamplesToTest:
        #    listOfSamplesToTest.remove("141372")
        #PREL 211385
        listOfSamplesToTest = ['263003']
        TestSAMPMLCreator.c_log.info("list samples :%s"%(listOfSamplesToTest))
        
        cpt = 0
        total_t0 = time.time()
        
        for sampleID in listOfSamplesToTest:
            
            TestSAMPMLCreator.c_log.info("Start Test %d for SampleID %s.\n"%(cpt,sampleID))
           
            t0 = time.time()
           
            # fetchnoble particulate
            fetcher = DBDataFetcher.getDataFetcher(self.nbConn,self.archConn,sampleID)
            
            #modify remoteHost
            fetcher.setRemoteHost(self.conf.get('RemoteAccess','nobleGazRemoteHost','dls007'))
   
            fetcher.fetch(request,'GAS')
                 
            renderer = SaunaRenderer(fetcher)
   
            xmlStr = renderer.asXmlStr(request)
           
           #print "Non Formatted String [%s]\n"%(xmlStr)
           
           #f = open("/tmp/xmlStr.xml","w")
           
           #f.write(xmlStr)
           #f.close()
   
            path = "/tmp/samples/sampml-full-%s.xml"%(sampleID)
   
            ctbto.common.xml_utils.pretty_print_xml(StringIO.StringIO(xmlStr),path)
           
            # check if no tags are left
            self.assertIfNoTagsLeft(path)
           
           #self.assertAllCalibrationInfo(path)
           
            t1 = time.time()
           
            #TestSAMPMLCreator.c_log.info("End of Test %d for SampleID %s.\nTest executed in %s seconds.\n\n**************************************************************** \n**************************************************************** \n"%(cpt,sampleID,(t1-t0)))
            TestSAMPMLCreator.c_log.info("\n********************************************************************************\n    End of Test %d for SampleID %s. Test executed in %s seconds.\n********************************************************************************\n"%(cpt,sampleID,(t1-t0)))
           
            cpt +=1
        
        total_t1 = time.time()
        
        TestSAMPMLCreator.c_log.info("\n****************************************************************************\n****************************************************************************\n****** EXECUTED %d FULL SAMPLE RETRIEVALS in %s seconds   ********\n****************************************************************************\n****************************************************************************\n"%(cpt,total_t1-total_t0))
    
    
    
    def ztestGenerateNobleGasARR(self):
        """ 
           Generate a Noble Gaz ARR.
        """
        
        request="spectrum=CURR/DETBK/GASBK/QC, analysis=CURR"
        
        # get full
        listOfSamplesToTest = self.getListOfSaunaSampleIDs('2007-11-25',endDate='2008-11-26',spectralQualif='FULL',nbOfElem='5')
              
        # remove sampleID for which data isn't available
        # 206975: No Calibration Available
        toRemove = [141372,206975]
        
        for id in toRemove:
            if id in listOfSamplesToTest:
                listOfSamplesToTest.remove(id)
                
        #listOfSamplesToTest = [206975]
               
        TestSAMPMLCreator.c_log.info("list samples %s"%listOfSamplesToTest)
        
        cpt = 1
        total_t0 = time.time()
        
        
        for sampleID in listOfSamplesToTest:
           
            TestSAMPMLCreator.c_log.info("Start Test %d for SampleID %s.\n"%(cpt,sampleID))
           
            t0 = time.time()
           
            # fetch noble gaz or particulate
            fetcher = DBDataFetcher.getDataFetcher(self.nbConn,self.archConn,sampleID)
   
            #modify remoteHost
            fetcher.setRemoteHost(self.conf.get('RemoteAccess','nobleGazRemoteHost','dls007'))
            
            fetcher.fetch(request,'GAS')
                 
            renderer = SaunaRenderer(fetcher)
   
            xmlStr = renderer.asXmlStr(request)
           
            path = "/tmp/samples/sampml-full-%s.xml"%(sampleID)
   
            ctbto.common.xml_utils.pretty_print_xml(StringIO.StringIO(xmlStr),path)
           
            # check if no tags are left
            self.assertIfNoTagsLeft(path)
           
            self.assertAllCalibrationInfo(path)
           
            t1 = time.time()
           
            TestSAMPMLCreator.c_log.info("Fetch sample nb %d with SampleID %s.\nTest executed in %s seconds.\n\n**************************************************************** \n**************************************************************** \n"%(cpt,sampleID,(t1-t0)))
           
            cpt +=1
        
            r = XML2HTMLRenderer('%s/%s'%(self._get_tests_dir_path(),'templates'),'ArrHtml.html')
    
            result = r.render(path)
    
            utils.printInFile(result,"/tmp/ARR-%s.html"%(sampleID))
           
        total_t1 = time.time()
        
        TestSAMPMLCreator.c_log.info("\n****************************************************************************\n****************************************************************************\n****** EXECUTED %d FULL SAMPLE RETRIEVALS in %s seconds   ********\n****************************************************************************\n****************************************************************************\n"%(cpt,total_t1-total_t0))
  
def tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSAMPMLCreator)
    unittest.TextTestRunner(verbosity=2).run(suite)    

if __name__ == '__main__':
    
    tests()
    
    
