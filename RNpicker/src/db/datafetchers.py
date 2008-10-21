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
    
    # spectrum types
    c_spectrum_types = set(['SPHD','QC','PREL','BK'])
    
    # regular expression stuff for spectrum param
    c_pattern        ="(?P<command>\s*spectrum\s*=\s*)(?P<values>[\w+\s*/\s*]*\w)\s*"
    c_spectrum_rex   = re.compile(c_pattern, re.IGNORECASE)
    
    def getDataFetcher(cls,aMainDbConnector=None,aArchiveDbConnector=None,aSampleID=None):
       """ Factory method returning the right DBFetcher \
           First it gets the sample type in order to instantiate the right DBFetcher => Particulate or NobleGas
       """
       
       # check preconditions
       if aMainDbConnector is None: raise CTBTOError(-1,"passed argument aMainDbConnector is null")
       
       if aArchiveDbConnector is None: raise CTBTOError(-1,"passed argument aArchiveDbConnector is null")
       
       if aSampleID is None : raise CTBTOError(-1,"passed argument aSampleID is null")
       
       # get sampleID type (ARIX or SAUNA or SPALAX or Particulate)
       result = aMainDbConnector.execute(SQL_GETSAMPLETYPE%(aSampleID))
        
       rows = result.fetchall()
       
       nbResults = len(rows)
       
       if nbResults is not 1:
            raise CTBTOError(-1,"Error, Expecting to have one result for sample_id %s but got %d either None or more than one. %s"%(aSampleID,nbResults,rows))
        
       cls.c_log.debug("sampleID=%s,Type = %s"%(aSampleID,rows[0]['SAMPLE_TYPE']))
       
       cls.c_log.debug("Klass = %s"%(SAMPLE_TYPE[rows[0]['SAMPLE_TYPE']]))
       
       
       # create object and update its internal dictionary
       inst = object.__new__(SAMPLE_TYPE[rows[0]['SAMPLE_TYPE']])
       
       type = rows[0]['SAMPLE_TYPE']
       if type is None: 
           type = "Particulate"
       
       conf = common.utils.Conf.get_instance()
       
       inst.__dict__.update({'_sampleID':aSampleID,'_mainConnector':aMainDbConnector,'_archiveConnector':aArchiveDbConnector,'_dataBag':{u'CONTENT_NOT_PRESENT':set(),u'CONTENT_PRESENT':set(),u'SAMPLE_TYPE':type},'_conf':conf,'_activateCaching':(True) if conf.get("Options","activateCaching","false") == "true" else False}) 
    
       result.close()
       
       return inst
       
    #class method binding
    getDataFetcher = classmethod(getDataFetcher)
    
     
    def __init__(self,aMainDbConnector=None,aArchiveDbConnector=None,aSampleID=None):
        
        self._mainConnector    = aMainDbConnector
        self._archiveConnector = aArchiveDbConnector
        
        self._sampleID  = aSampleID
        # dict containing all the data retrieved from the filesystems and DB
        self._dataBag   = {}
        
        # this part will contain all the retrieved elements
        # this can be used for consistency checking
        self._dataBag[u'CONTENT_PRESENT']    = set()
        # to flag what cannot be found for the DB
        self._dataBag[u'CONTENT_NOT_PRESENT'] = set()
        
        # get reference to the conf object
        self._conf              = common.utils.Conf.get_instance()
        
         # get flag indicating if the cache function is activated
        self._activateCaching = (True) if self._conf.get("Options","activateCaching","false") == "true" else False
    
    def _parseSpectrumParams(self,aParams=""):
       
        """ parse the spectrum part of the params string. It should be something like spectrum=FULL/QC/BK.
            This is used to specify which of the spectra related to the current spectrum must be retrieved
            The different values:
            - ALL all the spectrum. This is the default,
            - FULL if the associated FULL spectrum should be retrieved,
            - QC the QC Spectrum
            - BK the Background Spectrum
        
            Args:
               aParams: string of parameters in the form of param=values,param=values ....
                        From this string the spectrum=ALL or spectrum=QC/FULL is searched. 
                        The found values will be used to retrieved the related associated samples
               
            Returns:
               return List of spectrum types to fetch
        
            Raises:
               exception CTBTOError if the syntax of the aParams string is incorrect
        """
        
        result = set()
        
        # try to match the spectrum param
        m = DBDataFetcher.c_spectrum_rex.match(aParams)
    
    
        if m is None:
            print("Warning, Cannot find the spectrum=val1/val2 in param string %s\nUse default spectrum=ALL"%(aParams))
            result.update(DBDataFetcher.c_spectrum_types)
            return result
        
        values = m.group('values')
      
        vals = values.split('|')
      
        if len(vals) == 0:
          raise CTBTOError(-1,"Cannot find values for the spectrum params in parameters string %s"%(aParams))
        
        for val in vals:
          dummy = val.strip().upper()
          
          if dummy == 'ALL':
             #ALL superseeds everything and add all the different types
             result.update(DBDataFetcher.c_spectrum_types)
             # leave loop
             break
                
          if dummy not in DBDataFetcher.c_spectrum_types:
              raise CTBTOError(-1,"Unknown spectrum type %s. The spectrum type can only be one of the following %s"%(dummy,DBDataFetcher.c_spectrum_types))
          
          result.add(dummy)
          
        return result
    
    def execute(self,aRequest,aTryOnArchive=False,aRaiseExceptionOnError=True):
       """execute a sql request on the main connection and on the archive connection if necessary.
       
           Args:
              aTryOnArchive: boolean for looking on the archive if no data has been retrieved
              aRaiseExceptionOnError: raise an exception on error.
              
           Returns:
              return a tuple containing (rows,nbOfResults,foundOnArchive)
       
           Raises:
              exception CTBTOError if the aRaiseExceptionOnError flag is activated
       """
       # on main connection
       # try on the main connection
       result = self._mainConnector.execute(aRequest)
       
       # fetch all rows and check if there is a least one
       rows = result.fetchall()
       nbResults = len(rows)
       
       if nbResults <= 0:
           #no results found so if flag is activated look into archive
           if aTryOnArchive:
              result.close()
              result = self._archiveConnector.execute(aRequest)
              
              rows = result.fetchall()
              nbResults = len(rows)
              
              if nbResults == 0 and aRaiseExceptionOnError is True:
                  result.close()
                  raise CTBTOError(-1,"Error in Execute().Expecting to have one result for request %s but got %d either None or more than one. %s"%(aRequest,nbResults,rows))
              else:
                  return (rows,nbResults,True)
              
       result.close()
       return (rows,nbResults,False)
           
    
    def getMainConnector(self):
        return self._mainConnector
    
    def getArchiveConnector(self):
        return self._archiveConnector
    
    def getSampleID(self):
        return self._sampleID
    
    def activateCaching(self):
        return self._activateCaching
    
    def _fetchData(self,aParams=None):
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
       result = self._mainConnector.execute(SQL_GETSTATIONINFO%(self._sampleID))
       
       # only one row in result set
       rows = result.fetchall()
       
       nbResults = len(rows)
       
       if nbResults is not 1:
            raise CTBTOError(-1,"Expecting to have one result for sample_id %s but got %d either None or more than one. %s"%(self._sampleID,nbResults,rows))
         
       # update data bag
       self._dataBag.update(rows[0].items())
       
       #print "dataBag= %s"%(self._dataBag)
       
       result.close()
       
    def _fetchDetectorInfo(self):
       """ get station info. same treatment for all sample types """ 
       print "In fetch Detector Info "
       result = self._mainConnector.execute(SQL_GETDETECTORINFO%(self._sampleID))
       
       # only one row in result set
       rows = result.fetchall()
       
       nbResults = len(rows)
       
       if nbResults is not 1:
            raise CTBTOError(-1,"Expecting to have one result for sample_id %s but got %d either None or more than one. %s"%(self._sampleID,nbResults,rows))
         
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
            raise CTBTOError(-1,"Error when parsing halflife value %s for sample_id %s. Exception %s"%(aHalfLife,self._sampleID,ex))
            
    
    def _transformResults(self,aDataDict):
        """ transformer that modify the retrieve content from the database in order to be exploited directly by the renderers """
        
        # transform date information
        for (key,value) in aDataDict.items():
          if str(value.__class__) == "<type 'datetime.datetime'>" :
              aDataDict[key]= value.isoformat()
              
        return aDataDict
    
    def _addKeyPrefix(self,aDict,aPrefix):
        """add a prefix in the key.
        
            Args:
               aDict  : dict to transform
               aPrefix: the prefix to be added    
               
            Returns:
               return the transformed hash
        
            Raises:
               exception
        """
        transformedDict = {}
        
        # transform date information
        for (key,value) in aDict.items():
            transformedDict["%s_%s"%(aPrefix,key)] = value
              
        return transformedDict
            
              
    def _fetchSampleRefId(self):
        """get the reference_id for this sample
        
            Returns: Nothing
              
              
            Raises:
               exception if issue when accesing the database
        """
        result = self._mainConnector.execute(SQL_PARTICULATE_GET_SAMPLE_REF_ID%(self._sampleID))
       
        # only one row in result set
        rows = result.fetchall()
       
        nbResults = len(rows)
       
        if nbResults is not 1:
            raise CTBTOError(-1,"Expecting to have one result for sample_id %s but got %d either None or more than one. %s"%(self._sampleID,nbResults,rows))
         
        self._dataBag[u'REFERENCE_ID'] = rows[0]['SAMPLE_REF_ID']
       
        result.close()
       
    def _fetchSampleInfo(self,aSampleID,aDataname='current'):
       """ get sample info from sample data """ 
       
       print "Getting general sample info for %s\n"%(aSampleID)
       
       result = self._mainConnector.execute(SQL_GETSAMPLEINFO%(aSampleID))
       
       # only one row in result set
       rows = result.fetchall()
        
       nbResults = len(rows)
       
       if nbResults is not 1:
            raise CTBTOError(-1,"Expecting to have one result for sample_id %s but got %d either None or more than one. %s"%(self._sampleID,nbResults,rows))
         
       # get retrieved data and transform dates
       data = {}
       data.update(rows[0])
       
       # transform dates in data
       self._transformResults(data)
       
       # Work on dates and time
       # add decay time => Acq_Start - Coll_Stop
       
       #take the two operands
       
       a = rows[0]['DATA_ACQ_START']
       b = rows[0]['DATA_COLLECT_STOP']
       
       if a is None or b is None:
         data[u'DATA_DECAY_TIME'] = "Unknown"
       else:   
         # retrun difference in seconds
         dc = common.time_utils.getDifferenceInTime(b,a)
         data[u'DATA_DECAY_TIME'] = "PT%dS"%(dc)
       
       a = rows[0][u'DATA_COLLECT_STOP']
       b = rows[0]['DATA_COLLECT_START']
       
       if a is None or b is None:
         data[u'DATA_SAMPLING_TIME'] = "Unknown"
       else:
         # sampling time in secondds
         dc =  common.time_utils.getDifferenceInTime(b,a)
         data[u'DATA_SAMPLING_TIME'] = "PT%dS"%(dc)
       
       data[u'DATA_ACQ_LIVE_SEC'] = "PT%dS"%(data['DATA_ACQ_LIVE_SEC']) if data['DATA_ACQ_LIVE_SEC'] is not None else ""
       data[u'DATA_ACQ_REAL_SEC'] = "PT%dS"%(data['DATA_ACQ_REAL_SEC']) if data['DATA_ACQ_REAL_SEC'] is not None else ""
       
       # add prefix
       data = self._addKeyPrefix(data,aDataname)
       
       # update data bag
       self._dataBag.update(data.items())
        
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
        
        
    def fetch(self,aParams=""):
        """pickle the retrieved data in a file for a future usage
        
            Args:
               aParams: string containing some parameters for each fetching bloc (ex params="specturm=current/qc/prels/background")
            
            Returns: Nothing
              
              
            Raises:
               exception if issue fetching data (CTBTOError)
        """
        
        params         = None
        # when the cache is not sufficient
        accessDatabase = False
        
        
        # check if the caching function is activated
        # if yes and if the caching file exist load it
        cachingFilename = self._createCachingFile(self._sampleID)
        
        if self.activateCaching() and os.path.exists(cachingFilename):
            
            print "Read sample data for %s from the caching file %s.\n"%(self._sampleID,cachingFilename)
            
            f = open(cachingFilename,"r")
            
            self._dataBag = pickle.load(f)
            
            print "Checking cache consistency\n"
            
            # cache checking : Checks that the request doesn't contain more spectrum than asked
            spectra = self._parseSpectrumParams(aParams)
            
            # do ensemble difference spectra - CONTENT_PRESENT
            rest = spectra.difference(self._dataBag[u'CONTENT_PRESENT'])
            
            # there are more elements passed that the ones in content_present
            if len(rest) > 0:
                # if difference rest - CONTENT_NOT_PRESENT = 0 then we have retrieved everything 
                # So we can use the cache otherwise launch a retrieval for what is missing
                rest = rest.diffence(self._dataBag[u'CONTENT_NOT_PRESENT'])
                if len(rest) > 0:
                 # something needs to be looked for: it is in rest
                 # rebuild a spectrum param
                 params         = "spectrum="
                 accessDatabase = True
                 cpt = 0
                 for elem in rest:
                   if cpt-1 != len(rest):
                     params += "%s\\"%(elem)  
                   else:
                     params += "%s"           
        else:
          params = aParams 
          accessDatabase = True
         
        if accessDatabase:
          print "Read sample data for %s from the database.\n"%(self._sampleID)
          
          #get refID
          self._fetchSampleRefId()
          
          # get station info
          self._fetchStationInfo()
        
          # get detector info
          self._fetchDetectorInfo()
          
          # get Data Files
          self._fetchData(params)

          # get analysis results
          self._fetchAnalysisResults()
        
          # get parameters
          self._fetchParameters()
        
          self._fetchFlags()
        
          self._fetchCalibration()
          
          self._cache()
          
        # create human readable Hash in /tmp if option activated
        if self._conf.getboolean("Options","writeHumanReadableData") is True:
           self.printContent(open("/tmp/sample_%s_extract.data"%(self._sampleID),"w"))
    
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
        
    def _extractSpectrumFromMessageFile(self,aInput):
        """read a station message and extract the spectrum from it.
        
            Args:
               params:
               
            Returns:
               return
        
            Raises:
               exception
        """
        
        hasFoundSpectrum = False
        
        # look for #g_Spectrum
        for line in aInput:
             if line.find('#g_Spectrum') >= 0:
                 # quit the loop
                 hasFoundSpectrum = True
                 break
        
        if hasFoundSpectrum is False:
            raise CTBTOError(-1,"No spectrum tag #g_Spectrum found in file "%(aInput))
            
        # get the next line
        limits = aInput.next()
        
        print "read limits %s"%(limits)
        
        # read the spectrum in a StringIO
        data = StringIO()
        hasFoundEOSpectrum = False
        
        for line in aInput:
            if line.find('#') >= 0:
                # we have reached the end leave
                hasFoundEOSpectrum = True
                break
            else:
                data.write(line)
        
        if hasFoundEOSpectrum is False:
            raise CTBTOError(-1,"No end of spectrum tag # found in file "%(aInput))
        
        # go to the beginning of the Stream
        data.seek(0)
        
        return (data,limits)

    def _extractSpectrumFromSpectrumFile(self,aInput):
        
        data = StringIO()
        
        data.writelines(aInput)
        
        # go to the beginning of the Stream
        data.seek(0)
        
        return (data,"0 0")
    
    def _readDataFile(self,aFoundOnArchive,aDir,aFilename,aProdType,aOffset,aSize,aSampleID,aDataname='current',aSpectrumType='SPHD'):
        """read data from the main connection which is not archived.
           The data dict will be populated accordingly to the data found.
        
            Args:
               aFoundOnArchive. True if found on archive,
               aDir. Dir where to get the data,
               aFile. File name,
               aProdType. Type of product to extract,
               aOffset. Offset from where to read the data in the file,
               aSize. Size to read in the file,
               aSampeID. sampleID to read,
               aDataname.
               aSpectrumType.
               
            Returns:
               return Nothing
        
            Raises:
               exception
        """
         # check that the file exists
        path = "%s/%s"%(aDir,aFilename)
        ext  = ""
        
        # if config says RemoteDataSource is activated then create a remote data source
        if self._conf.getboolean("Options","remoteDataSource") is True:
           # to be changed as a factory should be used
           if aFoundOnArchive is True:
              input = db.rndata.RemoteArchiveDataSource(path,aSampleID,aOffset,aSize)
              ext   = os.path.splitext(input.getLocalFilename())[-1]
           else: 
              input = db.rndata.RemoteFSDataSource(path,aSampleID,aOffset,aSize)
              ext   = os.path.splitext(input.getLocalFilename())[-1]
        else:
            # this is a local path so check if it exits and open fd
            if not os.path.exists(path):
               raise CTBTOError(-1,"the file %s does not exits"%(path))
           
            input = open(path,"r")
            ext = os.path.splitext(aFilename)[-1] 
        
        # check the message type and do the necessary.
        # here we expect a .msg or .s
        if ext == '.msg' or ext == '.archmsg':
           (data,limits)  =  self._extractSpectrumFromMessageFile(input)
        # '.archs' given for an archived sample
        elif ext == '.s' or ext == '.archs':
           (data,limits) = self._extractSpectrumFromSpectrumFile(input)
        # remove it for the moment
        else:
           raise CTBTOError(-1,"Error unknown extension %s. Do not know how to read the file %s for aSampleID %s"%(ext,path,aSampleID))
        
        tok_list = []
        
        energy_span  = 0
        channel_span = 0
        e_max        = 0
        
        # store in a StringIO object
        # not very efficient as the spectrum is parsed two times
        # [MAJ] to change
        parsedSpectrum = StringIO()
        try:
           for line in data:
                
              # we might also have to add more splitting character
              # get the first column which should always be the last columns (channel span)
              # get also max of value of other columns (energy span)
              l = map(string.atoi,line.split())
              
              if l[0] > channel_span:
                 channel_span = l[0]
                 
              e_max = max(l[1:]) 
              
              if energy_span < e_max:
                  energy_span = e_max
              
              # add 16 spaces char for formatting purposes
              if self._conf.getboolean("Options","removeChannelIndex") is True:
                  parsedSpectrum.write("                %s"%(self._removeChannelSpan(line)))
              else:
                  parsedSpectrum.write("                %s"%(line))
        finally: 
           data.close()   
           input.close()
           
        DBDataFetcher.c_log.debug("channel_span %s"%(channel_span))
        DBDataFetcher.c_log.debug("energy_span %s"%(energy_span))
         
        self._dataBag[u"%s_DATA_CHANNEL_SPAN"%(aDataname)] = channel_span
        self._dataBag[u"%s_DATA_ENERGY_SPAN"%(aDataname)]  = energy_span
        
        
        # check in the conf if we need to compress the data
        if self._conf.getboolean("Options","compressSpectrum") is True:
            # XML need to be 64base encoded
            self._dataBag[u"%s_DATA"%(aDataname)] = base64.b64encode(zlib.compress(parsedSpectrum.getvalue()))
            # add a compressed flag in dict
            self._dataBag[u"%_DATA_COMPRESSED"%(aDataname)] = True
        else:
            #add raw data in clear
            self._dataBag[u"%s_DATA"%(aDataname)] = parsedSpectrum.getvalue()
             # add a compressed flag in dict
            self._dataBag[u"%s_DATA_COMPRESSED"%(aDataname)] = False
        
        # create a unique id for the extract data
        self._dataBag[u"%s_DATA_ID"%(aDataname)] = "%s-%s-%s"%(self._dataBag[u'STATION_CODE'],aSampleID,aSpectrumType)
        
        if aSpectrumType not in self._dataBag[u'CONTENT_PRESENT']:
           self._dataBag[u'CONTENT_PRESENT'].add(aSpectrumType) 
        
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
        
    def _fetchData(self,aParams=None):
        """ get the different raw data info """
        
        # there are 3 components: histogram, beta and gamma spectrum
        
        # first path information from database
        result = self._mainConnector.execute(SQL_GETSAUNA_FILES%(self._sampleID,self._dataBag['STATION_CODE']))
       
        # only one row in result set
        rows = result.fetchall()
       
        nbResults = len(rows)
       
        if nbResults is not 3:
            raise CTBTOError(-1,"Expecting to have 3 products for sample_id %s but got %d either None or more than one. %s"%(self._sampleID,nbResults,rows))
        
        print "data Rows = %s"%(rows)
        
        for row in rows:
            self._readDataFile(row['DIR'], row['DFile'], row['PRODTYPE'],self._sampleID)
        
        result.close()
    
    def _fetchAnalysisResults(self):
        """ get the activity concentration summary for ided nuclides, the activity summary, ROINetCounts results """
        
        # get identified Nuclides
        result = self._mainConnector.execute(SQL_SAUNA_GETIDENTIFIEDNUCLIDES%(self._sampleID))
       
        # only one row in result set
        rows = result.fetchall()
       
        nbResults = len(rows)
       
        if nbResults is 0:
            raise CTBTOError(-1,"Expecting to have n identified nuclides for sample_id %s but got 0"%(self._sampleID))
        
        # add results in a list which will become a list of dicts
        res = {}
        
        for row in rows:
            res.update(row.items())
            
        # add in dataBag
        self._dataBag['AR_identifiedNuclides'] = res
        
        result.close()
        
        # get information regarding all Nuclides
        result = self._mainConnector.execute(SQL_SAUNA_GETALLNUCLIDES%(self._sampleID))
       
        # only one row in result set
        rows = result.fetchall()
       
        nbResults = len(rows)
       
        if nbResults is 0:
            raise CTBTOError(-1,"Expecting to have n nuclides for sample_id but got 0"%(self._sampleID))
        
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
    
    c_nid_translation = {0:"nuclide not identifided by automated analysis",1:"nuclide identified by automated analysis",-1:"nuclide identified by automated analysis but rejected"}
    
    c_fpdescription_type_translation = {"SPHD":"SPHDF","PREL":"SPHDP","":"BLANK","QC":"QCPHD","BK":"DETBKPHD"}
    
   
   

    def __init__(self):
        print "create ParticulateDataFetcher"
        
        super(ParticulateDataFetcher,self).__init__(aDbConnector,aSampleID)
       
        self._dataBag['SAMPLE_TYPE']="PARTICULATE"
    
    def _fetchSpectrumData(self,aSampleID,aDataname,aType):
        """get the any spectrum data.
           If the caching function is activated save the retrieved specturm on disc.
           Try to find an extracted spectrum on OPS and Archive and if there is none of them look for the raw message (typeid)
        
            Args:
               aDataname: Name of the data. This will be used to create the name in the persistent hashtable and in the data spectrum filename
               
            Returns:
               return Nothing
        
            Raises:
               exception
        """
           
        print "Getting %s Spectrum for %s\n"%(aDataname,aSampleID)
           
        # get sample info related to this sampleID
        self._fetchSampleInfo(aSampleID,aDataname)
         
         
        (rows,nbResults,foundOnArchive) = self.execute(SQL_GETPARTICULATE_SPECTRUM%(aSampleID,self._dataBag['STATION_CODE']),aTryOnArchive=True,aRaiseExceptionOnError=False)
         
        if nbResults is 0:
            print("WARNING: sample_id %s has no extracted spectrum.Try to find a raw message.\n"%(aSampleID))
            type = ParticulateDataFetcher.c_fpdescription_type_translation.get(aType,"")
            (rows,nbResults,foundOnArchive) = self.execute(SQL_GETPARTICULATE_RAW_SPECTRUM%(type,aSampleID,self._dataBag['STATION_CODE']),aTryOnArchive=True,aRaiseExceptionOnError=True) 
        elif nbResults > 1:
            print("WARNING: found more than one spectrum for sample_id %s\n"%(aSampleID))
        
        for row in rows:
            self._readDataFile(foundOnArchive,row['DIR'], row['DFile'],row['PRODTYPE'],row['FOFF'],row['DSIZE'],aSampleID,aDataname,aType)
        
        
    def _fetchBKSpectrumData(self,aDataname):
        """get the Background spectrum.
           If the caching function is activated save the retrieved spectrum on disc.
        
            Args:
               params: None
               
            Returns:
               return Nothing
        
            Raises:
               exception
        """
        
        # precondition do nothing if there the current sample is a Detector background itself
        if self._dataBag[u'CURRENT_DATA_DATA_TYPE'] == 'D':
            return
        
        print "Getting Background Spectrum for %s\n"%(self._sampleID)
        
        # need to get the latest BK sample_id
        result = self._mainConnector.execute(SQL_GETPARTICULATE_BK_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID']))
        
        # only one row in result set
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults is 0:
           print("Warning. There is no Background for %s.\n request %s \n Database query result %s"%(self._sampleID,SQL_GETPARTICULATE_BK_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID']),rows))
           self._dataBag[u'CONTENT_NOT_PRESENT'].add('BK')
           return
       
        if nbResults > 1:
            print("There is more than one Background for %s. Take the first result.\n request %s \n Database query result %s"%(self._sampleID,SQL_GETPARTICULATE_BK_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID']),rows))
           
        sid = rows[0]['SAMPLE_ID']
        
        DBDataFetcher.c_log.debug("sid = %s\n"%(sid))
        
        result.close()
        
        # now fetch the spectrum
        try:
           self._fetchSpectrumData(sid,aDataname,'BK')
        except Exception, e:
           print "Warning. No Data File found for background %s\n"%(sid)
            
    
    def _fetchQCSpectrumData(self,aDataname):
        """get the QC spectrum.
           If the caching function is activated save the retrieved specturm on disc.
        
            Args:
               params: None
               
            Returns:
               return Nothing
        
            Raises:
               exception
        """
        
        # precondition do nothing if there the current sample is a Detector background itself
        if self._dataBag[u'CURRENT_DATA_DATA_TYPE'] == 'Q':
            return
        
        print "Getting QC Spectrum for %s\n"%(self._sampleID)
        
        # need to get the latest BK sample_id
        (rows,nbResults,foundOnArchive) = self.execute(SQL_GETPARTICULATE_QC_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID']))
        
        nbResults = len(rows)
        
        if nbResults is 0:
           print("Warning. There is no QC for %s.\n request %s \n Database query result %s"%(self._sampleID,SQL_GETPARTICULATE_QC_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID']),rows)) 
           # add in CONTENT_NOT_PRESENT this is used by the cache
           self._dataBag[u'CONTENT_NOT_PRESENT'].add('QC')
           return
       
        if nbResults > 1:
            print("There is more than one QC for %s. Take the first result.\n request %s \n Database query result %s"%(self._sampleID,SQL_GETPARTICULATE_QC_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID']),rows))
           
        sid = rows[0]['SAMPLE_ID']
        
        
        # now fetch the spectrum
        self._fetchSpectrumData(sid,aDataname,'QC')
        
    def _fetchPrelsSpectrumData(self):
        """get the preliminary spectrums.
           If the caching function is activated save the retrieved specturm on disc.
        
            Args:
               params: None
               
            Returns:
               return Nothing
        
            Raises:
               exception
        """
        
        # precondition do nothing if there the current sample is a Detector background itself
        if self._dataBag[u'CURRENT_DATA_DATA_TYPE'] == 'S' and self._dataBag[u'CURRENT_DATA_SPECTRAL_QUALIFIER'] == 'PREL':
            return
        
        print "Getting Prels Spectrum for %s\n"%(self._sampleID)
        
        #print "request %s\n"%(SQL_GETPARTICULATE_BK_SAMPLEID%(self._dataBag[u'DETECTOR_ID']))
        
        # need to get the latest BK sample_id
        result = self._mainConnector.execute(SQL_GETPARTICULATE_PREL_SAMPLEIDS%(self._sampleID,self._dataBag[u'DETECTOR_ID']))
        
        # only one row in result set
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults is 0:
            print("There is no PREL spectrum for %s."%(self._sampleID))
            self._dataBag[u'CONTENT_NOT_PRESENT'].add('PREL')
            return
        
        listOfPrel = []
          
        for row in rows:
            sid = row['SAMPLE_ID']
            
            print "sid = %s\n"%(sid)
            
            prelID = 'PREL_%d'%(sid)
            # now fetch the spectrum with the a PREL_cpt id
            self._fetchSpectrumData(sid,prelID,'PREL')
            # update list of prels
            listOfPrel.append(prelID)
         
        self._dataBag['CURRENT_List_OF_PRELS']  =  listOfPrel
           
        
        result.close()
    
    
    
    def _fetchData(self,aParams=""):
        """ get the different raw data info """
        
        spectrums = self._parseSpectrumParams(aParams)
        
        #fetch current spectrum
        if ('SPHD' in spectrums):
           self._fetchSpectrumData(self._sampleID,'CURRENT','SPHD')
        
        if ('QC' in spectrums):
           self._fetchQCSpectrumData('QC')
        
        if ('BK' in spectrums):
           self._fetchBKSpectrumData('BACKGROUND')
        
        if ('PREL' in spectrums):
          self._fetchPrelsSpectrumData()
        
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
        result = self._mainConnector.execute(SQL_PARTICULATE_CATEGORY_STATUS%(self._sampleID))
       
        # only one row in result set
        rows = result.fetchall()
        
        data = {}
        data.update(rows[0])
    
        self._dataBag.update(self._transformResults(data))
        
        result = self._mainConnector.execute(SQL_PARTICULATE_CATEGORY%(self._sampleID))
       
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
        
        #print "res = %s"%(self._dataBag[u'CATEGORIES'])
       
        result.close()
        
    def _fetchPeaksResults(self):
        """ Get info regarding the found peaks """
        
        # get peaks
        result = self._mainConnector.execute(SQL_PARTICULATE_GET_PEAKS%(self._sampleID))
        
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
        result = self._mainConnector.execute(SQL_PARTICULATE_GET_NUCLIDE_LINES_INFO%(self._sampleID))

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
        result = self._mainConnector.execute(SQL_PARTICULATE_GET_NUCLIDES_INFO%(self._sampleID))
        
        rows = result.fetchall()
        
         # add results in a list which will become a list of dicts
        res = []
        
        # create a list of dicts
        data = {}

        for row in rows:
            # copy row in a normal dict
            data.update(row)
            
            nidflag = data.get(u'NID_FLAG',None)

            # check if there is NID key
            if nidflag is not None:
                val = ParticulateDataFetcher.c_nid_translation.get(nidflag,nidflag)
                data[u'NID_FLAG']=val
            
            res.append(data)
            data = {}

        # add in dataBag
        self._dataBag[u'IDED_NUCLIDES'] = res
        
        result.close()
        
        # return all nucl2quantify this is kind of static table
        result = self._mainConnector.execute(SQL_PARTICULATE_GET_NUCL2QUANTIFY)
        
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
        
        print "Getting Analysis Results for %s\n"%(self._sampleID)
        
        self._fetchCategoryResults()
        
        self._fetchNuclidesResults()
        
        self._fetchNuclideLines()
        
        self._fetchPeaksResults()
        
        self._fetchFlags()
        
    def _getMRP(self):
        """ get the most recent prior """
        
        data_type    = self._dataBag['CURRENT_DATA_DATA_TYPE']
        
        detector_id  = self._dataBag['DETECTOR_ID']
        
        sample_type  = self._dataBag['SAMPLE_TYPE']
        
        collect_stop = self._dataBag['CURRENT_DATA_COLLECT_STOP'].replace("T"," ")
        
        ParticulateDataFetcher.c_log.debug("Executed request %s\n"%(SQL_PARTICULATE_GET_MRP%(collect_stop,collect_stop,data_type,detector_id,sample_type)))
    
        # get MDA nuclides
        result = self._mainConnector.execute(SQL_PARTICULATE_GET_MRP%(collect_stop,collect_stop,data_type,detector_id,sample_type))
        
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
        result = self._mainConnector.execute(SQL_PARTICULATE_GET_DATA_QUALITY_FLAGS%(self._sampleID))
        
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
        
        # precondition check that there is COLLECT_START 
        # otherwise quit
        if (self._dataBag['CURRENT_DATA_COLLECT_START'] is None) or (self._dataBag['CURRENT_DATA_COLLECT_STOP'] is None):
            print "Warnings. Cannot compute the timeliness flags missing information for %s\n"%(self._sampleID)
            return
       
        # get the timeliness flag
         
        self._getMRP()
        
        # check collection flag
        
        # check that collection time with 24 Hours
        collect_start  = common.time_utils.getDateTimeFromISO8601(self._dataBag['CURRENT_DATA_COLLECT_START'])
        collect_stop   = common.time_utils.getDateTimeFromISO8601(self._dataBag['CURRENT_DATA_COLLECT_STOP'])
    
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
        acq_start  = common.time_utils.getDateTimeFromISO8601(self._dataBag['CURRENT_DATA_ACQ_START'])
        acq_stop   = common.time_utils.getDateTimeFromISO8601(self._dataBag['CURRENT_DATA_ACQ_STOP'])
    
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
        
        print "Getting Analysis parameters for %s\n"%(self._sampleID)
        
        #print "request = %s\n"%(SQL_PARTICULATE_GET_PROCESSING_PARAMETERS%(self._sampleID))
        
        result = self._mainConnector.execute(SQL_PARTICULATE_GET_PROCESSING_PARAMETERS%(self._sampleID))
        
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults is not 1:
            if self._dataBag[u'CURRENT_DATA_SPECTRAL_QUALIFIER'] == 'FULL':
               #raise CTBTOError(-1,"Expecting to have 1 set of processing parameters for sample_id %s but got %d either None or more than one. %s"%(self._sampleID,nbResults,rows))
               print("sample_id %s is a %s sample and no processing parameters has been found\n"%(self._sampleID,self._dataBag[u'CURRENT_DATA_SPECTRAL_QUALIFIER']))
            else:
               print("sample_id %s is a %s sample and no processing parameters has been found\n"%(self._sampleID,self._dataBag[u'CURRENT_DATA_SPECTRAL_QUALIFIER']))
         
        # create a list of dicts
        data = {}
        
        
        data.update((rows[0].items()) if len(rows) > 0 else {})
    
        # add in dataBag
        self._dataBag[u'PROCESSING_PARAMETERS'] = data
        
        result.close()  
        
        result = self._mainConnector.execute(SQL_PARTICULATE_GET_UPDATE_PARAMETERS%(self._sampleID))
        
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults is not 1:
            if self._dataBag[u'CURRENT_DATA_SPECTRAL_QUALIFIER'] == 'FULL':
               #raise CTBTOError(-1,"Expecting to have 1 set of update parameters for sample_id %s but got %d either None or more than one. %s"%(self._sampleID,nbResults,rows))
               print("%s sample and no update parameters found\n"%(self._dataBag[u'CURRENT_DATA_SPECTRAL_QUALIFIER']))
            else:
               print("%s sample and no update parameters found\n"%(self._dataBag[u'CURRENT_DATA_SPECTRAL_QUALIFIER']))
         
        # create a list of dicts
        data = {}

        data.update((rows[0].items()) if len(rows) > 0 else {})
        
        # add in dataBag
        self._dataBag[u'UPDATE_PARAMETERS'] = data
        
    def _fetchCalibration(self):  
        """ Fetch the calibration info for particulate """
        
        # get energy calibration info
        result = self._mainConnector.execute(SQL_PARTICULATE_GET_ENERGY_CAL%(self._sampleID))
        
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults is not 1:
            raise CTBTOError(-1,"Expecting to have 1 energy calibration row for sample_id %s but got %d either None or more than one. %s"%(self._sampleID,nbResults,rows))
        
         # create a list of dicts
        data = {}

        data.update(rows[0].items())
        
        # add in dataBag
        self._dataBag[u'ENERGY_CAL'] = data
        
        result = self._mainConnector.execute(SQL_PARTICULATE_GET_RESOLUTION_CAL%(self._sampleID))
        
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults is not 1:
            raise CTBTOError(-1,"Expecting to have 1 resolution calibration row for sample_id %s but got %d either None or more than one. %s"%(self._sampleID,nbResults,rows))
        
         # create a list of dicts
        data = {}

        data.update(rows[0].items())
        
        # add in dataBag
        self._dataBag[u'RESOLUTION_CAL'] = data
        
        result = self._mainConnector.execute(SQL_PARTICULATE_GET_EFFICIENCY_CAL%(self._sampleID))
        
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults is not 1:
            raise CTBTOError(-1,"Expecting to have 1 efficiency calibration row for sample_id %s but got %d either None or more than one. %s"%(self._sampleID,nbResults,rows))
        
         # create a list of dicts
        data = {}

        data.update(rows[0].items())
        
        # add in dataBag
        self._dataBag[u'EFFICIENCY_CAL'] = data
        
        result.close()            
        
                   





""" Dictionary used to map DB Sample type with the right fetcher """
SAMPLE_TYPE = {'SAUNA':SaunaNobleGasDataFetcher, 'ARIX-4':SaunaNobleGasDataFetcher, 'SPALAX':SpalaxNobleGasDataFetcher, 'RASA':ParticulateDataFetcher,'CINDER':ParticulateDataFetcher, 'LAB':ParticulateDataFetcher, None:ParticulateDataFetcher}
        