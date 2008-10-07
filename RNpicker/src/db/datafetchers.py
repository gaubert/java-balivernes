import logging
import sqlalchemy
import new
import os
import re
import pickle
import pprint
import string
import datetime
import time
import zlib
import base64
from StringIO import StringIO

import common.utils
import common.time_utils
import db.rndata
from common.exceptions import CTBTOError
# list of requests
from sqlrequests import *


class DBDataFetcher(object):
    """ Base Class used to get data from the IDC Database """
    
    # Class members
    c_log = logging.getLogger("datafetchers.DBDataFetcher")
    c_log.setLevel(logging.DEBUG)
    
   
    def getDataFetcher(cls,aDbConnector=None,aSampleID=None):
       """ Factory method returning the right DBFetcher \
           First it gets the sample type in order to instantiate the right DBFetcher => Particulate or NobleGas
       """
       
       # check preconditions
       if aDbConnector is None: raise CTBTOError(-1,"passed argument aDbConnector is null")
       
       if aSampleID is None : raise CTBTOError(-1,"passed argument aSampleID is null")
       
       # get sampleID type (ARIX or SAUNA or SPALAX or Particulate)
       result = aDbConnector.execute(SQL_GETSAMPLETYPE%(aSampleID))
        
       rows = result.fetchall()
       
       nbResults = len(rows)
       
       if nbResults is not 1:
            raise CTBTOError(-1,"Expecting to have one result but got %d either None or more than one. %s"%(nbResults,rows))
        
       print "Type = %s"%(rows[0]['SAMPLE_TYPE'])
       
       print "Klass = %s"%(SAMPLE_TYPE[rows[0]['SAMPLE_TYPE']])
       
       
       # create object and update its internal dictionary
       inst = object.__new__(SAMPLE_TYPE[rows[0]['SAMPLE_TYPE']])
       
       type = rows[0]['SAMPLE_TYPE']
       if type is None: 
           type = "Particulate"
       
       conf = common.utils.Conf.get_conf()
       
       inst.__dict__.update({'_sampleID':aSampleID,'_connector':aDbConnector,'_dataBag':{u'SAMPLE_TYPE':type},'_conf':conf,'_activateCaching':(True) if conf.get("Options","activateCaching","false") == "true" else False}) 
    
       result.close()
       
       return inst
       
    #class method binding
    getDataFetcher = classmethod(getDataFetcher)
    
     
    def __init__(self,aDbConnector=None,aSampleID=None):
        
        self._connector = aDbConnector
        self._sampleID  = aSampleID
        # dict containing all the data retrieved from the filesystems and DB
        self._dataBag   = {}
        
        # get reference to the conf object
        self._conf              = common.utils.Conf.get_conf()
        
         # get flag indicating if the cache function is activated
        self._activateCaching = (True) if self._conf.get("Options","activateCaching","false") == "true" else False
    
    def getConnector(self):
        return self._connector
    
    def getSampleID(self):
        return self._sampleID
    
    def activateCaching(self):
        return self._activateCaching
    
    def _fetchData(self):
        """ abstract global data fetching method """
        raise CTBTOError(-1,"method not implemented in Base Class. To be defined in children")
    
    def _fetchAnalysisResults(self):
        """ abstract global data fetching method """
        raise CTBTOError(-1,"method not implemented in Base Class. To be defined in children")
    
    def _fetchFlags(self):
        """ abstract global fetching method for getting the flags"""
        raise CTBTOError(-1,"method not implemented in Base Class. To be defined in children")
    
    def _fetchCalibration(self):  
        """ abstract global fetch method for get the Calibration info """
        raise CTBTOError(-1,"method not implemented in Base Class. To be defined in children")

    def asXML(self):
        """ abstract global xmlizer method """
        raise CTBTOError(-1,"method not implemented in Base Class. To be defined in children")
    
    def _fetchStationInfo(self):
       """ get station info. same treatment for all sample types """ 
       print "In fetch Station Info "
       result = self._connector.execute(SQL_GETSTATIONINFO%(self._sampleID))
       
       # only one row in result set
       rows = result.fetchall()
       
       nbResults = len(rows)
       
       if nbResults is not 1:
            raise CTBTOError(-1,"Expecting to have one result but got %d either None or more than one. %s"%(nbResults,rows))
         
       # update data bag
       self._dataBag.update(rows[0].items())
       
       print "dataBag= %s"%(self._dataBag)
       
       result.close()
       
    def _fetchDetectorInfo(self):
       """ get station info. same treatment for all sample types """ 
       print "In fetch Detector Info "
       result = self._connector.execute(SQL_GETDETECTORINFO%(self._sampleID))
       
       # only one row in result set
       rows = result.fetchall()
       
       nbResults = len(rows)
       
       if nbResults is not 1:
            raise CTBTOError(-1,"Expecting to have one result but got %d either None or more than one. %s"%(nbResults,rows))
         
       # update data bag
       self._dataBag.update(rows[0].items())
       
       result.close()
       
    def _formatHalfLife(self,aHalfLife):
        """ transform halflife from the database given in days in an 8601 iso formatted period in seconds """
        
        try:
            
          pattern = "(?P<year>[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)(\s)*Y|(?P<month>[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)(\s)*M|(?P<day>[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)(\s)*D|(?P<hour>[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)(\s)*H|(?P<minute>[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)(\s)*M|(?P<second>[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)(\s)*S"
          
          result = re.match(pattern,aHalfLife)
          
          if result.group('year') != None:
              return float(result.group('year')) 
          elif result.group('month') != None:
              return float(result.group('month'))
          elif result.group('month') != None:
              return float(result.group('day')) 
          elif result.group('month') != None:
              return float(result.group('hour')) 
          elif result.group('month') != None:
              return float(result.group('second'))  
          return float(value)
          
        except Exception, ex:
            raise CTBTOError(-1,"Error when parsing halflife value %s. Exception %s"%(aHalfLife,ex))
            
    
    def _transformResults(self,aDataDict):
        """ transformer that modify the retrieve content from the database in order to be exploited directly by the renderers """
        
        # transform date information
        for (key,value) in aDataDict.items():
          if str(value.__class__) == "<type 'datetime.datetime'>" :
              aDataDict[key]= value.isoformat()
              
        return aDataDict
              
       
    def _fetchSampleInfo(self):
       """ get sample info from sample data """ 
       print "In fetch SampleInfo "
       result = self._connector.execute(SQL_GETSAMPLEINFO%(self._sampleID))
       
       # only one row in result set
       rows = result.fetchall()
       
       nbResults = len(rows)
       
       if nbResults is not 1:
            raise CTBTOError(-1,"Expecting to have one result but got %d either None or more than one. %s"%(nbResults,rows))
         
       # get retrieved data and transform dates
       data = {}
       data.update(rows[0])
       
       # update data bag
       self._dataBag.update(self._transformResults(data).items())
       
       # Work on dates and time
       # add decay time => Collect_Stop - Acq_Start
       dc = rows[0]['DATA_ACQ_STOP'] - rows[0]['DATA_COLLECT_STOP']
       self._dataBag[u'DATA_DECAY_TIME'] = "PT%dS"%(dc.seconds)
       
       # sampling time
       dc =  rows[0]['DATA_COLLECT_STOP'] - rows[0]['DATA_COLLECT_START']
       self._dataBag[u'DATA_SAMPLING_TIME'] = "PT%dS"%(dc.seconds)
       
       self._dataBag[u'DATA_ACQ_LIVE_SEC'] = "PT%dS"%(self._dataBag['DATA_ACQ_LIVE_SEC'])
       self._dataBag[u'DATA_ACQ_REAL_SEC'] = "PT%dS"%(self._dataBag['DATA_ACQ_REAL_SEC'])
        
       result.close()
       
    def _createCachingFile(self,aSampleID):
        """Build a caching file from the config caching dir and the given sampleID.
        
            Args:
               aSampleID: given sampleID
        
            Returns:
              the built hashtable
              
            Raises:
               exception
        """
        
        # create caching dir if it doesn't exist
        dir = self._conf.get("Caching","dir","/tmp")
        
        common.utils.makedirs(dir)
        
        return "%s/sampml_caching_%s.data"%(dir,aSampleID)
        
    def _cache(self):
        
        """pickle the retrieved data in a file for a future usage
        
            Returns:
              
              
            Raises:
               exception if issue when pickling
        """
        
        cachingFilename = self._createCachingFile(self.getSampleID())
        
        if self.activateCaching() and not os.path.exists(cachingFilename):
            
            # only rewrite when file doesn't exist for the moment
            f = open(cachingFilename,"w")
            
            pickle.dump(self._dataBag,f)
            
            f.close()
        
        
    def fetch(self):
        
        # check if the caching function is activated
        # if yes and if the caching file exist load it
        
        cachingFilename = self._createCachingFile(self.getSampleID())
        
        if self.activateCaching() and os.path.exists(cachingFilename):
            
            print "fetch data from the caching file %s.\n"%(cachingFilename)
            
            f = open(cachingFilename,"r")
            
            self._dataBag = pickle.load(f)
            
        else:
            
          print "fetch data from the database.\n"
          
          # get station info
          self._fetchStationInfo()
        
          # get detector info
          self._fetchDetectorInfo()
        
          # get sample info
          self._fetchSampleInfo()
        
          # get Data Files
          self._fetchData()

          # get analysis results
          self._fetchAnalysisResults()
        
          # get parameters
          self._fetchParameters()
        
          self._fetchFlags()
        
          self._fetchCalibration()
          
          self._cache()
    
    def _removeChannelSpan(self,aLine):
        """remove the first column of the matrix of values.
           This is optional and can be remove
        
            Args:
               aLine: line numbers as a line
               
            Returns:
               return string representing the new line
        
        """
        # use curryfication to create the justify func with 11 chars
        justify = common.utils.curry(string.ljust,width=11)
        
        # justify all elements in the list
        list = map(justify,aLine.split()[1:])
        
        # join all that to have a unique string 
        # need to join on an empty string. Strange interface for the join method
        return "%s\n"%("".join(list))
        
        
    def _readDataFile(self,aDir,aFilename,aType):
        """ read a file in a string buffer. This is used for the data files """
        
         # check that the file exists
        path = "%s/%s"%(aDir,aFilename)
        
        # if config says RemoteDataSource is activated then create a remote data source
        if self._conf.getboolean("Options","remoteDataSource") is True:
           input = db.rndata.RemoteFSDataSource(path)
        else:
            # this is a local path so check if it exits and open fd
            if not os.path.exists(path):
               raise CTBTOError(-1,"the file %s does not exits"%(path))
    
            input = open(path,"r")
       
        tok_list = []
        
        energy_span  = 0
        channel_span = 0
        e_max        = 0
        
        # store in a StringIO object
        data = StringIO()
        try:
           for line in input:
                
              # we might also have to add more splitting character
              # get the first column which should always be the last columns (channel span)
              # get also max of value of other columns (energy span)
              l = map(string.atoi,line.split())
              
              #print "line %s"%(l)
              
              
              if l[0] > channel_span:
                 channel_span = l[0]
                 
              e_max = max(l[1:]) 
              
              if energy_span < e_max:
                  energy_span = e_max
              
              # add 16 spaces char for formatting purposes
              if self._conf.getboolean("Options","removeChannelIndex") is True:
                  data.write("                %s"%(self._removeChannelSpan(line)))
              else:
                  data.write("                %s"%(line))
        finally:    
           input.close()
           
        print "channel_span %s"%(channel_span)
        print "energy_span %s"%(energy_span)
         
        self._dataBag["rawdata_%s_channel_span"%(aType)] = channel_span
        self._dataBag["rawdata_%s_energy_span"%(aType)]  = energy_span
        
        
        # check in the conf if we need to compress the data
        if self._conf.getboolean("Options","compressSpectrum") is True:
            # XML need to be 64base encoded
            self._dataBag["rawdata_%s"%(aType)] = base64.b64encode(zlib.compress(data.getvalue()))
            # add a compressed flag in dict
            self._dataBag["rawdata_%s_compressed"%(aType)] = True
        else:
            #add raw data in clear
            self._dataBag["rawdata_%s"%(aType)] = data.getvalue()
             # add a compressed flag in dict
            self._dataBag["rawdata_%s_compressed"%(aType)] = False
        
        # create a unique id for the extract data
        self._dataBag["rawdata_%s_ID"%(aType)] = "%s-%s-%s"%(self._dataBag[u'STATION_CODE'],self._dataBag[u'SAMPLE_ID'],aType.lower())
        
    def get(self,aKey,aDefault=None):
        """ return one of the fetched elements """
        return self._dataBag.get(aKey,aDefault)
    
    def printContent(self,aIostream = None):
       pp = pprint.PrettyPrinter(indent=4,stream=aIostream)
       pp.pprint(self._dataBag)
       
    

        

##############################################
### class: SaunaNobleGasDataFetcher
###
###
##############################################        
class SaunaNobleGasDataFetcher(DBDataFetcher):
    """ Class for fetching SAUNA-ARIX related data """
    
      # Class members
    c_log = logging.getLogger("datafetchers.SaunaNobleGasDataFetcher")
    c_log.setLevel(logging.DEBUG)


    def __init__(self,aDbConnector=None,aSampleID=None):
        
        super(SaunaNobleGasDataFetcher,self).__init__(aDbConnector,aSampleID)
        
        self._dataBag['SAMPLE_TYPE']="SAUNA"
        
    def _fetchData(self):
        """ get the different raw data info """
        
        # there are 3 components: histogram, beta and gamma spectrum
        
        # first path information from database
        result = self._connector.execute(SQL_GETSAUNA_FILES%(self._sampleID,self._dataBag['STATION_CODE']))
       
        # only one row in result set
        rows = result.fetchall()
       
        nbResults = len(rows)
       
        if nbResults is not 3:
            raise CTBTOError(-1,"Expecting to have 3 products but got %d either None or more than one. %s"%(nbResults,rows))
        
        print "data Rows = %s"%(rows)
        
        for row in rows:
            self._readDataFile(row['DIR'], row['DFile'], row['PRODTYPE'])
        
        result.close()
    
    def _fetchAnalysisResults(self):
        """ get the activity concentration summary for ided nuclides, the activity summary, ROINetCounts results """
        
        # get identified Nuclides
        result = self._connector.execute(SQL_SAUNA_GETIDENTIFIEDNUCLIDES%(self._sampleID))
       
        # only one row in result set
        rows = result.fetchall()
       
        nbResults = len(rows)
       
        if nbResults is 0:
            raise CTBTOError(-1,"Expecting to have n identified nuclides but got 0")
        
        # add results in a list which will become a list of dicts
        res = {}
        
        for row in rows:
            res.update(row.items())
            
        # add in dataBag
        self._dataBag['AR_identifiedNuclides'] = res
        
        result.close()
        
        # get information regarding all Nuclides
        result = self._connector.execute(SQL_SAUNA_GETALLNUCLIDES%(self._sampleID))
       
        # only one row in result set
        rows = result.fetchall()
       
        nbResults = len(rows)
       
        if nbResults is 0:
            raise CTBTOError(-1,"Expecting to have n nuclides but got 0")
        
        # add results in a list which will become a list of dicts
        res = {}
        
        for row in rows:
            res.update(row.items())
            
        # add in dataBag
        self._dataBag['AR_AllNuclides'] = res
        
        result.close()         

class SpalaxNobleGasDataFetcher(DBDataFetcher):
    """ Class for fetching SPALAX related data """
    
      # Class members
    c_log = logging.getLogger("datafetchers.SpalaxNobleGasDataFetcher")
    c_log.setLevel(logging.DEBUG)


    def __init__(self):
        
        print "create SpalaxNobleGasDataFetcher"
        
        super(SpalaxNobleGasDataFetcher,self).__init__(aDbConnector,aSampleID)
       
        self._dataBag['SAMPLE_TYPE']="SPALAX"
        

class ParticulateDataFetcher(DBDataFetcher):
    """ Class for fetching particualte related data """
    
      # Class members
    c_log = logging.getLogger("datafetchers.ParticulateDataFetcher")
    c_log.setLevel(logging.DEBUG)


    def __init__(self):
        print "create ParticulateDataFetcher"
        
        super(ParticulateDataFetcher,self).__init__(aDbConnector,aSampleID)
       
        self._dataBag['SAMPLE_TYPE']="PARTICULATE"
    
    def _fetchData(self):
        """ get the different raw data info """
        
        # need to get the gamma spectrum 
        # first path information from database
        result = self._connector.execute(SQL_GETPARTICULATE_SPECTRUM%(self._sampleID,self._dataBag['STATION_CODE']))
       
        # only one row in result set
        rows = result.fetchall()
       
        nbResults = len(rows)
       
        if nbResults is not 1:
            raise CTBTOError(-1,"Expecting to have 1 product for particulate but got %d either None or more than one. %s"%(nbResults,rows))
         
        for row in rows:
            self._readDataFile(row['DIR'], row['DFile'], row['PRODTYPE'])
        
        result.close()
        
    def _addCategoryComments(self,aData):
        """ Add the comments as it was defined in the RRR """
        
        if aData['CAT_CATEGORY'] != 1:
            if aData['CAT_UPPER_BOUND'] == aData['CAT_LOWER_BOUND']:
                aData['CAT_COMMENT'] = "Not Regularly Measured"
            elif aData['CAT_ACTIVITY'] > aData['CAT_UPPER_BOUND']:
                aData['CAT_COMMENT'] = "Above Statistical Range"
            elif aData['CAT_ACTIVITY'] < aData['CAT_LOWER_BOUND']:
                aData['CAT_COMMENT'] = "Below Statistical Range"
            else:
                aData['CAT_COMMENT'] = "Within Statistical Range"
       
    def _fetchCategoryResults(self):
        """ sub method of _fetchAnalysisResults. Get the Category info from the database """
        
        # get category status
        result = self._connector.execute(SQL_PARTICULATE_CATEGORY_STATUS%(self._sampleID))
       
        # only one row in result set
        rows = result.fetchall()
        
        data = {}
        data.update(rows[0])
    
        self._dataBag.update(self._transformResults(data))
        
        result = self._connector.execute(SQL_PARTICULATE_CATEGORY%(self._sampleID))
       
        # only one row in result set
        rows = result.fetchall()
         
        # add results in a list which will become a list of dicts
        res = []
        
        # create a list of dicts
        data = {}
        
        for row in rows:
            data.update(row)
            # transform dates if necessary
            newRow = self._transformResults(data)
            # add Comment
            self._addCategoryComments(newRow)
            res.append(newRow)
            data = {}
       
        # update data bag
        self._dataBag[u'CATEGORIES'] = res
        
        print "res = %s"%(self._dataBag[u'CATEGORIES'])
       
        result.close()
        
    def _fetchPeaksResults(self):
        """ Get info regarding the found peaks """
        
        # get peaks
        result = self._connector.execute(SQL_PARTICULATE_GET_PEAKS%(self._sampleID))
        
        rows = result.fetchall()
        
         # add results in a list which will become a list of dicts
        res = []
        
        data = {}
        
        for row in rows:
            data.update(row)
            # transform dates if necessary
            newRow = self._transformResults(data)
            
            res.append(newRow)
            data = {}
               
        # add in dataBag
        self._dataBag[u'PEAKS'] = res
        
        result.close()
        
    def _fetchNuclideLines(self):
        """Get all info regarding the Nuclide Lines for a particualr sample .
         
        """
         
        # get the data from the DB
        result = self._connector.execute(SQL_PARTICULATE_GET_NUCLIDE_LINES_INFO%(self._sampleID))

        rows = result.fetchall()
        
         # add results in a list which will become a list of dicts
        res = []
        
        # create a list of dicts
        data = {}

        for row in rows:
            # copy row in a normal dict
            data.update(row)
            res.append(data)
            data = {}
        
        # add in dataBag
        self._dataBag[u'IDED_NUCLIDE_LINES'] = res
        
        
    def _fetchNuclidesResults(self):
        """ Get all info regarding the nuclides related to this sample """
         # get non quantified nuclides
        
        # to distinguish quantified and non quantified nuclide there is a table called GARDS_NUCL2QUANTIFY => static table of the nucl to treat
        result = self._connector.execute(SQL_PARTICULATE_GET_NUCLIDES_INFO%(self._sampleID))
        
        rows = result.fetchall()
        
         # add results in a list which will become a list of dicts
        res = []
        
        # create a list of dicts
        data = {}

        for row in rows:
            # copy row in a normal dict
            data.update(row)
            res.append(data)
            data = {}
        
        # add in dataBag
        self._dataBag[u'IDED_NUCLIDES'] = res
        
        result.close()
        
        # return all nucl2quantify this is kind of static table
        result = self._connector.execute(SQL_PARTICULATE_GET_NUCL2QUANTIFY)
        
        rows = result.fetchall()
        
         # add results in a list which will become a list of dicts
        res = []
        
        # create a list of dicts
        data = {}

        for row in rows:
            # copy row in a normal dict
            data.update(row)
            res.append(data)
            data = {}
        
        # add in dataBag
        self._dataBag[u'NUCLIDES_2_QUANTIFY'] = res
        
        result.close()  
        
    
    def _fetchAnalysisResults(self):
        """ get the  sample categorization, activityConcentrationSummary, peaks results, parameters, flags"""
        
        print "into Fetch Analysis Results"
        self._fetchCategoryResults()
        
        self._fetchNuclidesResults()
        
        self._fetchNuclideLines()
        
        self._fetchPeaksResults()
        
        self._fetchFlags()
        
    def _getMRP(self):
        """ get the most recent prior """
        
        collect_stop = self._dataBag['DATA_COLLECT_STOP'].replace("T"," ")
        
        data_type    = self._dataBag['DATA_DATA_TYPE']
        
        detector_id  = self._dataBag['DETECTOR_ID']
        
        sample_type  = self._dataBag['SAMPLE_TYPE']
        
        print "Executed request %s\n"%(SQL_PARTICULATE_GET_MRP%(collect_stop,collect_stop,data_type,detector_id,sample_type))
    
        # get MDA nuclides
        result = self._connector.execute(SQL_PARTICULATE_GET_MRP%(collect_stop,collect_stop,data_type,detector_id,sample_type))
        
        rows = result.fetchall()
        
        if len(rows) > 0:
            
            row = rows[0]
            
            print "There is a mrp and it is %d\n"%(mrp_sid)
            
            mrp_sid   = row['mrp_sample_id']
            hoursDiff = row['mrp_collect_stop_diff']*24 
            
            self._dataBag[u'TIME_FLAGS_PREVIOUS_SAMPLE']  = True 
            self._dataBag[u'TIME_FLAGS_MRP_SAMPLE_ID']    = mrp_sid
            self._dataBag[u'TIME_FLAGS_MRP_HOURS_DIFF']   = hoursDiff
             
        else:
            
           print "No MRP found\n"
           self._dataBag[u'TIME_FLAGS_PREVIOUS_SAMPLE']  = False 
        
        
    def _fetchFlags(self):
        """ get the different flags """
        
        self._fetchTimelinessFlags()
        
        self._fetchdataQualityFlags()
        
        # we miss event screening flags to be added
        
    
    def _fetchdataQualityFlags(self):
        """ data quality flags"""
        
         # get MDA nuclides
        result = self._connector.execute(SQL_PARTICULATE_GET_DATA_QUALITY_FLAGS%(self._sampleID))
        
        rows = result.fetchall()
        
        data = {}
        
        res = []
        
        for row in rows:
            # copy row in a normal dict
            data.update(row)
            
            res.append(data)
            data = {}
               
        # add in dataBag
        self._dataBag[u'DATA_QUALITY_FLAGS'] = res
        
        
        
        
    def _fetchTimelinessFlags(self):
        """ prepare timeliness checking info """
        # get the timeliness flag
        self._getMRP()
        
        # check collection flag
        
        # check that collection time with 24 Hours
        collect_start  = common.time_utils.getDateTimeFromISO8601(self._dataBag['DATA_COLLECT_START'])
        collect_stop   = common.time_utils.getDateTimeFromISO8601(self._dataBag['DATA_COLLECT_STOP'])
    
        diff_in_sec = common.time_utils.getDifferenceInTime(collect_start, collect_stop)
        
        # check time collection within 24 hours +/- 10 % => 3hrs
        # between 21.6 and 26.4
        # if 0 within 24 hours
        if diff_in_sec > 95040 or diff_in_sec < 77760:
           self._dataBag[u'TIME_FLAGS_COLLECTION_WITHIN_24'] = diff_in_sec
        else:
           self._dataBag[u'TIME_FLAGS_COLLECTION_WITHIN_24'] = 0 
        
        
        # check acquisition flag
        # need to be done within 3 hours
        
        # check that collection time with 24 Hours
        acq_start  = common.time_utils.getDateTimeFromISO8601(self._dataBag['DATA_ACQ_START'])
        acq_stop   = common.time_utils.getDateTimeFromISO8601(self._dataBag['DATA_ACQ_STOP'])
    
        diff_in_sec = common.time_utils.getDifferenceInTime(collect_start, collect_stop)
          
        # acquisition diff with 3 hours
        if diff_in_sec < (20*60*60):
           self._dataBag[u'TIME_FLAGS_ACQUISITION_FLAG'] = diff_in_sec
        else:
           self._dataBag[u'TIME_FLAGS_ACQUISITION_FLAG'] = 0 
        
        # check decay flag
        # decay time = ['DATA_ACQ_STOP'] - ['DATA_COLLECT_STOP']
        
        # check that collection time with 24 Hours
        decay_time_in_sec   = common.time_utils.getDifferenceInTime(collect_stop,acq_start)
        
        if (decay_time_in_sec > 24*60*60):
            self._dataBag[u'TIME_FLAGS_DECAY_FLAG'] = decay_time_in_sec
        else:
            self._dataBag[u'TIME_FLAGS_DECAY_FLAG'] = 0
            
        #  check sample_arrival_delay
        entry_date_time      = common.time_utils.getDateTimeFromISO8601(self._dataBag['CAT_ENTRY_DATE'])
        sample_arrival_delay = common.time_utils.getDifferenceInTime(entry_date_time,collect_start)
        
        # check that sample_arrival_delay is within 72 hours or 72*60*60 seconds
        if sample_arrival_delay > (72*60*60):
           self._dataBag[u'TIME_FLAGS_SAMPLE_ARRIVAL_FLAG'] = entry_date_time
        else:
           self._dataBag[u'TIME_FLAGS_SAMPLE_ARRIVAL_FLAG'] = 0 

        
    def _fetchParameters(self):
        """ get the different parameters used for the analysis """
        
        print "into fetch Parameters"
        print "request = %s\n"%(SQL_PARTICULATE_GET_PROCESSING_PARAMETERS%(self._sampleID))
        result = self._connector.execute(SQL_PARTICULATE_GET_PROCESSING_PARAMETERS%(self._sampleID))
        
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults is not 1:
            if self._dataBag[u'DATA_SPECTRAL_QUALIFIER'] == 'FULL':
               raise CTBTOError(-1,"Expecting to have 1 set of processing parameters but got %d either None or more than one. %s"%(nbResults,rows))
            else:
               print("%s sample and no processing parameters found\n"%(self._dataBag[u'DATA_SPECTRAL_QUALIFIER']))
         
        # create a list of dicts
        data = {}
        
        
        data.update((rows[0].items()) if len(rows) > 0 else {})
    
        # add in dataBag
        self._dataBag[u'PROCESSING_PARAMETERS'] = data
        
        result.close()  
        
        result = self._connector.execute(SQL_PARTICULATE_GET_UPDATE_PARAMETERS%(self._sampleID))
        
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults is not 1:
            if self._dataBag[u'DATA_SPECTRAL_QUALIFIER'] == 'FULL':
               raise CTBTOError(-1,"Expecting to have 1 set of update parameters but got %d either None or more than one. %s"%(nbResults,rows))
            else:
               print("%s sample and no update parameters found\n"%(self._dataBag[u'DATA_SPECTRAL_QUALIFIER']))
         
        # create a list of dicts
        data = {}

        data.update((rows[0].items()) if len(rows) > 0 else {})
        
        # add in dataBag
        self._dataBag[u'UPDATE_PARAMETERS'] = data
        
    def _fetchCalibration(self):  
        """ Fetch the calibration info for particulate """
        
        # get energy calibration info
        result = self._connector.execute(SQL_PARTICULATE_GET_ENERGY_CAL%(self._sampleID))
        
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults is not 1:
            raise CTBTOError(-1,"Expecting to have 1 energy calibration row  but got %d either None or more than one. %s"%(nbResults,rows))
        
         # create a list of dicts
        data = {}

        data.update(rows[0].items())
        
        # add in dataBag
        self._dataBag[u'ENERGY_CAL'] = data
        
        result = self._connector.execute(SQL_PARTICULATE_GET_RESOLUTION_CAL%(self._sampleID))
        
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults is not 1:
            raise CTBTOError(-1,"Expecting to have 1 resolution calibration row  but got %d either None or more than one. %s"%(nbResults,rows))
        
         # create a list of dicts
        data = {}

        data.update(rows[0].items())
        
        # add in dataBag
        self._dataBag[u'RESOLUTION_CAL'] = data
        
        result = self._connector.execute(SQL_PARTICULATE_GET_EFFICIENCY_CAL%(self._sampleID))
        
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults is not 1:
            raise CTBTOError(-1,"Expecting to have 1 efficiency calibration row  but got %d either None or more than one. %s"%(nbResults,rows))
        
         # create a list of dicts
        data = {}

        data.update(rows[0].items())
        
        # add in dataBag
        self._dataBag[u'EFFICIENCY_CAL'] = data
        
        result.close()            
        
                   





""" Dictionary used to map DB Sample type with the right fetcher """
SAMPLE_TYPE = {'SAUNA':SaunaNobleGasDataFetcher, 'ARIX-4':SaunaNobleGasDataFetcher, 'SPALAX':SpalaxNobleGasDataFetcher, None:ParticulateDataFetcher}
        