import logging
import os
import re
import pickle
import pprint
import string
import zlib
import base64
from StringIO import StringIO

import ctbto.common.time_utils
import ctbto.db.rndata
import sqlrequests

from ctbto.query import RequestParser
from ctbto.common   import CTBTOError
from org.ctbto.conf import Conf

UNDEFINED="N/A"


class DBDataFetcher(object):
    """ Base Class used to get data from the IDC Database """
    
    # Class members
    c_log = logging.getLogger("datafetchers.DBDataFetcher")
    c_log.setLevel(logging.INFO)
    
    c_nid_translation = {0:"nuclide not identified by automated analysis",1:"nuclide identified by automated analysis",-1:"nuclide identified by automated analysis but rejected"}
    c_fpdescription_type_translation = {"SPHD":"SPHDF","PREL":"SPHDP","":"BLANK","QC":"QCPHD","BK":"DETBKPHD"}
    
    
    def getDataFetcher(cls,aMainDbConnector=None,aArchiveDbConnector=None,aSampleID=None):
        """ Factory method returning the right DBFetcher \
           First it gets the sample type in order to instantiate the right DBFetcher => Particulate or NobleGas
           """
       
        # check preconditions
        if aMainDbConnector is None: raise CTBTOError(-1,"passed argument aMainDbConnector is null")
       
        if aArchiveDbConnector is None: raise CTBTOError(-1,"passed argument aArchiveDbConnector is null")
       
        if aSampleID is None : raise CTBTOError(-1,"passed argument aSampleID is null")
       
        # get sampleID type (ARIX or SAUNA or SPALAX or Particulate)
        result = aMainDbConnector.execute(sqlrequests.SQL_GET_SAMPLE_TYPE%(aSampleID))
        
        rows = result.fetchall()
       
        nbResults = len(rows)
       
        if nbResults != 1:
            raise CTBTOError(-1,"Error, Expecting to have one result for sample_id %s but got %d either None or more than one. %s"%(aSampleID,nbResults,rows))
        
        cls.c_log.debug("sampleID=%s,Type = %s"%(aSampleID,rows[0]['SAMPLE_TYPE']))
       
        cls.c_log.debug("Klass = %s"%(SAMPLE_TYPE[rows[0]['SAMPLE_TYPE']]))
        
        
        
        ty = SAMPLE_TYPE.get(rows[0]['SAMPLE_TYPE'],None)
        if ty is None: 
            raise CTBTOError(-1,"The sample type %s is not supported or unknown"%(rows[0]['SAMPLE_TYPE']))

        inst = ty(aMainDbConnector,aArchiveDbConnector,aSampleID)
    
        result.close()
       
        return inst
       
    #class method binding
    getDataFetcher = classmethod(getDataFetcher)
    
     
    def __init__(self,aMainDbConnector=None,aArchiveDbConnector=None,aSampleID=None,aRemoteHostForAccessingFiles=None):
        
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
        self._conf              = Conf.get_instance() #IGNORE:E1101
        
        # create query parser 
        self._parser            = RequestParser()
        
        # use to support a the same time Particulate that are running on the prod env and the noble gas that runs on the dev env
        self._remoteHost        = aRemoteHostForAccessingFiles
        
         # get flag indicating if the cache function is activated
        self._activateCaching   = (True) if self._conf.get("Caching","activateCaching","false") == "true" else False
    
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
      
    def getRemoteHost(self):
        return self._remoteHost
    
    def setRemoteHost(self,aRemoteHost):
        self._remoteHost = aRemoteHost     
    
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
    
    def _fetchAnalysisResults(self,aParams=None):
        """ abstract global data fetching method """
        raise CTBTOError(-1,"method not implemented in Base Class. To be defined in children")
    
    def _fetchFlags(self,sid,aDataname):
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
        DBDataFetcher.c_log.debug("In fetch Station Info")
        result = self._mainConnector.execute(sqlrequests.SQL_GETSTATIONINFO%(self._sampleID))
       
        # only one row in result set
        rows = result.fetchall()
       
        nbResults = len(rows)
       
        if nbResults != 1:
            raise CTBTOError(-1,"Expecting to have one result for sample_id %s but got %d either None or more than one. %s"%(self._sampleID,nbResults,rows))
         
        # update data bag
        self._dataBag.update(rows[0].items())
       
        result.close()
       
    def _fetchDetectorInfo(self):
        """ get station info. same treatment for all sample types """ 
       
        DBDataFetcher.c_log.debug("In fetch Detector Info ")
       
        result = self._mainConnector.execute(sqlrequests.SQL_GETDETECTORINFO%(self._sampleID))
       
        # only one row in result set
        rows = result.fetchall()
       
        nbResults = len(rows)
       
        if nbResults != 1:
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
            elif result.group('day') != None:
                return float(result.group('day')) 
            elif result.group('hour') != None:
                return float(result.group('hour')) 
            elif result.group('second') != None:
                return float(result.group('second'))  
            return float(aHalfLife)
          
        except Exception, ex:
            raise CTBTOError(-1,"Error when parsing halflife value %s for sample_id %s. Exception %s"%(aHalfLife,self._sampleID,ex))
            
    
    def _transformResults(self,aDataDict):
        """ transformer that modify the retrieve content from the database in order to be exploited directly by the renderers
            - change datetime format to isoformat
            - change None Value to N/A (non available)
        """
        
        # transform date information
        for (key,value) in aDataDict.items():
            if str(value.__class__) == "<type 'datetime.datetime'>" :
                aDataDict[key]= value.isoformat() 
            if value == None:
                aDataDict[key] = UNDEFINED
              
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
    
    def _getCalibrationCheckSum(self,aCoeffs):
        """return the checksum of the calibration coeffs. This is done to create a unique id for the different calibration types.
        
            Args:
               aCoeffs: a list of coeffs
               
            Returns:
               return the transformed hash
        
            Raises:
               exception
        """
        
        coeffsStr = ''.join(map(str,aCoeffs)) #IGNORE:W0141
        
        return ctbto.common.utils.checksum(coeffsStr)
        
          
              
    def _fetchSampleRefId(self):
        """get the reference_id for this sample
        
            Returns: Nothing
              
              
            Raises:
               exception if issue when accesing the database
        """
        result = self._mainConnector.execute(sqlrequests.SQL_PARTICULATE_GET_SAMPLE_REF_ID%(self._sampleID))
       
        # only one row in result set
        rows = result.fetchall()
       
        nbResults = len(rows)
       
        if nbResults != 1:
            raise CTBTOError(-1,"Expecting to have one result for sample_id %s but got %d either None or more than one. %s"%(self._sampleID,nbResults,rows))
         
        self._dataBag[u'REFERENCE_ID'] = rows[0]['SAMPLE_REF_ID']
       
        result.close()
    
    def _findDatanameAndType(self,aSampleID,aDataType="",aSpectralQualifier=""):
        """ Private method used to find the name qualifier of a spectrum.
             This name is used to create keys related to the spectrum in the data dict.
        
            Args:
               params: aDataType. Type returned by the sqlrequests.SQL_GETSAMPLEINFO SQL req,
                       aSpectralQualifier. Spectral Qualifier returned by the sqlrequests.SQL_GETSAMPLEINFO SQL req
               
            Returns:
               return Nothing
        
            Raises:
               exception
        """
        
        # strip the retruned dataname as the database name can contain some funny characters
        if aDataType == 'S' and aSpectralQualifier == 'PREL':
            return (("PREL_%s"%(aSampleID)).strip(),'PREL')
        elif aDataType == 'S' and aSpectralQualifier == 'FULL':
            return (("SPHD_%s"%(aSampleID)).strip(),'SPHD')
        elif aDataType == 'Q':
            return (("QC_%s"%(aSampleID)).strip(),'QC')
        elif aDataType == 'D':
            return (("DETBK_%s"%(aSampleID)).strip(),'DETBK')
        elif aDataType == 'G' and aSpectralQualifier == 'FULL':
            return (("GASBK_%s"%(aSampleID)).strip(),'GASBK')
        elif aDataType == 'B' and aSpectralQualifier == 'FULL':
            return (("BAK_%s"%(aSampleID)).strip(),'BAK')
        else:
            raise CTBTOError(-1,"Unknown spectrum type: DataType = %s and SpectralQualifier = %s\n"%(aDataType,aSpectralQualifier))  
       
    def _fetchGeneralSpectrumInfo(self,aSampleID,aPrefix=""):
        """ get general spectrum info like acq date, sampling time ... """ 
       
        DBDataFetcher.c_log.info("Getting general sample info for %s\n"%(aSampleID))
       
        result = self._mainConnector.execute(sqlrequests.SQL_GETSAMPLEINFO%(aSampleID))
       
        # only one row in result set
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults != 1:
            raise CTBTOError(-1,"Expecting to have one result for sample_id %s but got %d either None or more than one. %s"%(aSampleID,nbResults,rows))
         
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
            data[u'DATA_DECAY_TIME'] = "N/A"
        else:   
            # retrun difference in seconds
            dc = ctbto.common.time_utils.getDifferenceInTime(b,a)
            
            # Handle negative values: check that it is neg or not
            if dc < 0:
                data[u'DATA_DECAY_TIME'] = "-PT%dS"%(abs(dc))
                DBDataFetcher.c_log.error("Decay time for %s is negative: %s !! \n"%(aSampleID,data[u'DATA_DECAY_TIME']))
            else:
                data[u'DATA_DECAY_TIME'] = "PT%dS"%(dc)
       
        a = rows[0][u'DATA_COLLECT_STOP']
        b = rows[0]['DATA_COLLECT_START']
       
        if a is None or b is None:
            data[u'DATA_SAMPLING_TIME'] = "N/A"
        else:
            # sampling time in secondds
            dc =  ctbto.common.time_utils.getDifferenceInTime(b,a)
            if dc < 0:
                data[u'DATA_SAMPLING_TIME'] = "-PT%dS"%(abs(dc))
                DBDataFetcher.c_log.error("Sampling time for %s is negative: %s !! \n"%(aSampleID,data[u'DATA_SAMPLING_TIME']))
            else:
                data[u'DATA_SAMPLING_TIME'] = "PT%dS"%(dc)
       
        data[u'DATA_ACQ_LIVE_SEC'] = "PT%dS"%(data['DATA_ACQ_LIVE_SEC']) if data['DATA_ACQ_LIVE_SEC'] is not None else ""
        data[u'DATA_ACQ_REAL_SEC'] = "PT%dS"%(data['DATA_ACQ_REAL_SEC']) if data['DATA_ACQ_REAL_SEC'] is not None else ""
       
        (dataname,ty) = self._findDatanameAndType(aSampleID,data[u'DATA_DATA_TYPE'],data[u'DATA_SPECTRAL_QUALIFIER'])
       
        # add prefix
        data = self._addKeyPrefix(data,"%s%s"%(dataname,aPrefix))
       
        # update data bag
        self._dataBag.update(data.items())
        
        result.close()
       
        return (dataname,ty)
    
    
       
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
        directory = self._conf.get("Caching","dir","/tmp")
        
        ctbto.common.utils.makedirs(directory)
        
        return "%s/sampml_caching_%s.data"%(directory,aSampleID)
        
    def _cache(self):
        
        """pickle the retrieved data in a file for a future usage.
           Ask to owerwrite the cache
        
            Returns: Nothing
              
              
            Raises:
               exception if issue when pickling
        """
        
        cachingFilename = self._createCachingFile(self.getSampleID())
        
        if self.activateCaching():
            
            # only rewrite when file doesn't exist for the moment
            f = open(cachingFilename,"w")
            
            pickle.dump(self._dataBag,f)
            
            f.close()
        
        
    def fetch(self,aParams="",aType=""):
        """pickle the retrieved data in a file for a future usage
        
            Args:
               aParams: string containing some parameters for each fetching bloc (ex params="specturm=curr/qc/prels/bk")
               aType: GAS or PAR for particulate or gas
            
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
            
            DBDataFetcher.c_log.info("Loading cache data from file %s for sampleID %s.\n"%(cachingFilename,self._sampleID))
            
            f = open(cachingFilename,"r")
            
            self._dataBag = pickle.load(f)
            
            DBDataFetcher.c_log.info("Checking cache consistency\n")
            
            # cache checking : Checks that the request doesn't contain more spectrum than asked
            reqDict = self._parser.parse(aParams,aType)
            
            spectra = reqDict[RequestParser.SPECTRUM]
            
            # do ensemble difference spectra - CONTENT_PRESENT
            rest = spectra.difference(self._dataBag[u'CONTENT_PRESENT'])
            
            # there are more elements passed that the ones in content_present
            if len(rest) > 0:
                # if difference rest - CONTENT_NOT_PRESENT = 0 then we have retrieved everything 
                # So we can use the cache otherwise launch a retrieval for what is missing
                rest = rest.difference(self._dataBag[u'CONTENT_NOT_PRESENT'])
                if len(rest) > 0:
                    # something needs to be looked for: it is in rest
                    # rebuild a spectrum param
                    params         = "spectrum="
                    accessDatabase = True
                    cpt = 1
                    for elem in rest:
                        if cpt != len(rest):
                            params += "%s/"%(elem)  
                        else:
                            params += "%s"%(elem) 
                   
                        cpt += 1          
        else:
            params = aParams 
            accessDatabase = True
         
        if accessDatabase:
            DBDataFetcher.c_log.info("Read missing sample data from the database for %s.\n"%(self._sampleID))
          
            # save sampleID
            self._dataBag[u'SAMPLE_ID'] = self._sampleID
            
            #get refID 
            self._fetchSampleRefId()
          
            # get station info
            self._fetchStationInfo()
        
            # get detector info
            self._fetchDetectorInfo()
          
            # get Data Files
            self._fetchData(params)

            # get analysis results
            self._fetchAnalysisResults(params)
        
            self._fetchCalibration()
          
            self._cache()
        else:
            DBDataFetcher.c_log.info("Entirely rely on the cache for %s\n"%(self._sampleID))
          
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
        justify = ctbto.common.utils.curry(string.ljust,width=11)
        
        # justify all elements in the list
        l = map(justify,aLine.split()[1:]) #IGNORE:W0141
        
        # join all that to have a unique string 
        # need to join on an empty string. Strange interface for the join method
        return "%s\n"%("".join(l))
        
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
        
        # read the spectrum in a StringIO
        data = StringIO()
        hasFoundEOSpectrum = False
        
        for line in aInput:
            if line.find('#') >= 0 or line.find('STOP'):
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
    
    def _extractHistrogramFromHistogramFile(self,aInput):
        
        data = StringIO()
        
        data.writelines(aInput)
        
        # go to the beginning of the Stream
        data.seek(0)
        
        return (data,"0 0")
    
    def _readDataFile(self,aFoundOnArchive,aDir,aFilename,aProdType,aOffset,aSize,aSampleID,aDataname='curr',aSpectrumType='CURR'):  #IGNORE:W0613
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
               return file descriptor (fd) and the extension
        
            Raises:
               exception
        """
         # check that the file exists
        path  = "%s/%s"%(aDir,aFilename)
        ext   = ""
        theInput = None
        
        # if config says RemoteDataSource is activated then create a remote data source
        if self._conf.getboolean("Options","remoteDataSource",True) is True:
            # to be changed as a factory should be used
            if aFoundOnArchive is True:
                theInput = ctbto.db.rndata.RemoteArchiveDataSource(path,aSampleID,aOffset,aSize,self._remoteHost)
                ext   = os.path.splitext(theInput.getLocalFilename())[-1]
            else: 
                theInput = ctbto.db.rndata.RemoteFSDataSource(path,aSampleID,aOffset,aSize,self._remoteHost)
                ext   = os.path.splitext(theInput.getLocalFilename())[-1]
        else:
            # this is a local path so check if it exits and open fd
            if not os.path.exists(path):
                raise CTBTOError(-1,"the file %s does not exits"%(path))
           
            theInput = open(path,"r")
            ext = os.path.splitext(aFilename)[-1] 
        
        return (theInput,ext)
        
    def _processHistogram(self,aData,aToCompress=False):
        """process the histogram and return the data and limites.
           
        
            Args:
               
               aDataname.
               aSpectrumType.
               
            Returns:
               return the data
        
            Raises:
               exception
        """
        data         = None
        
        # store in a StringIO object
        # for the moment just add some spaces to have a nice histogram
       
        parsedHistogram = StringIO()
        try:
            for line in aData:
                parsedHistogram.write("                %s"%(line))
        finally: 
            aData.close()   
     
        # check in the conf if we need to compress the data
        if aToCompress:
            try:
                data = base64.b64encode(zlib.compress(parsedHistogram.getvalue()))
            except Exception, e: #IGNORE:W0703
                DBDataFetcher.c_log.error("Error,%s\n"%(e))
        else:
            data = parsedHistogram.getvalue()
          
        return data
        
    def _processSpectrum(self,aData,aToCompress=False):
        """process the spectrum and return the data and limites.
        
            Args:
               
               aDataname.
               aSpectrumType.
               
            Returns:
               return Nothing
        
            Raises:
               exception
        """
        energy_span  = 0
        channel_span = 0
        e_max        = 0
        data         = None
        
        # store in a StringIO object
        # not very efficient as the spectrum is parsed two times
        # [MAJ] to change
        parsedSpectrum = StringIO()
        try:
            for line in aData:
                
                # we might also have to add more splitting character
                # get the first column which should always be the last columns (channel span)
                # get also max of value of other columns (energy span)
                #use int instread of atoi
                l = map(int,line.split()) #IGNORE:W0141
              
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
            aData.close()   
     
        # check in the conf if we need to compress the data
        if aToCompress:
            try:
                data = base64.b64encode(zlib.compress(parsedSpectrum.getvalue()))
            except Exception, e: #IGNORE:W0703
                DBDataFetcher.c_log.error("Error,%s\n"%(e))
        else:
            data = parsedSpectrum.getvalue()
          
        
        return (data,channel_span,energy_span)
        
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
    c_log.setLevel(logging.INFO)


    def __init__(self,aMainDbConnector=None,aArchiveDbConnector=None,aSampleID=None):
        
        super(SaunaNobleGasDataFetcher,self).__init__(aMainDbConnector,aArchiveDbConnector,aSampleID)
        
        self._dataBag['SAMPLE_TYPE']='SAUNA'
    
    def _fetchDETBKSpectrumData(self):
        """get the Background data.
           If the caching function is activated save the retrieved spectrum on disc.
        
            Args:
               params: None
               
            Returns:
               return Nothing
        
            Raises:
               exception
        """
        
        # precondition do nothing if there the curr sample is a Detector background itself
        prefix = self._dataBag.get(u'CURRENT_CURR',"")
        if self._dataBag.get(u"%s_DATA_DATA_TYPE"%(prefix),'') == 'D':
            return
        
        SaunaNobleGasDataFetcher.c_log.info("Getting Detector Background Spectrum for %s\n"%(self._sampleID))
        
        # follow the same method as the one defined in bg_analyse
        # first look for the gas bk id in gards_sample_aux and then try to get the corresponding id.
        # if no sample_id is found look use the mrp method
        (rows,nbResults,_) = self.execute(sqlrequests.SQL_GET_SAUNA_AUX_DETBK_ID%(self._sampleID))
        id_found = False
        if nbResults == 1:
            # get ID from the measurement ID
            mid = rows[0]['mid']
            
            (rows,nbResults,_) = self.execute(sqlrequests.SQL_GET_SAUNA_DETBK_SAMPLEID_FROM_MID%(mid))
            
            if nbResults >= 1:
                sid =  rows[0]['sid']
                id_found = True
            else:
                SaunaNobleGasDataFetcher.c_log.info("Warning. Could not find a Detector Background sample_id from the measurement id %s. For more details regarding the request, see the log file"%(mid))

        if not id_found:
            #go in MRP method 
            SaunaNobleGasDataFetcher.c_log.info("Warning. Use MRP method to find the detector background associated to %s\n"%(self._sampleID))
            # need to get the latest BK sample_id
            (rows,nbResults,_) = self.execute(sqlrequests.SQL_GET_SAUNA_MRP_DETBK_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'])) 
       
            if nbResults == 0:
                SaunaNobleGasDataFetcher.c_log.info("Warning. There is no Detector Background for %s.\n request %s \n Database query result %s"%(self._sampleID,sqlrequests.SQL_GET_SAUNA_MRP_DETBK_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID']),rows))
                self._dataBag[u'CONTENT_NOT_PRESENT'].add('DETBK')
                return
       
            if nbResults > 1:
                SaunaNobleGasDataFetcher.c_log.info("There is more than one Detector Background for %s. Take the first result.\n request %s \n Database query result %s"%(self._sampleID,sqlrequests.SQL_GET_SAUNA_MRP_DETBK_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID']),rows))
           
            sid = rows[0]['SAMPLE_ID']
        
        
        DBDataFetcher.c_log.debug("sid = %s\n"%(sid))
          
        # now fetch the spectrum
        try:
            (dataname,_) = self._fetchAllData(sid)
           
            self._dataBag[u'CURRENT_DETBK'] = dataname
           
            self._dataBag[u'CONTENT_PRESENT'].add('DETBK') 
           
        except Exception, e: #IGNORE:W0703
            SaunaNobleGasDataFetcher.c_log.info("Warning. No Data File found for a Detector Background %s\n.Exception e = %s\n"%(sid,e))
            self._dataBag[u'CONTENT_NOT_PRESENT'].add('DETBK')
    
    def _fetchGASBKSpectrumData(self):
        """get the Background data.
           If the caching function is activated save the retrieved spectrum on disc.
        
            Args:
               params: None
               
            Returns:
               return Nothing
        
            Raises:
               exception
        """
        
        # precondition do nothing if there the curr sample is a Detector background itself
        prefix = self._dataBag.get(u'CURRENT_CURR',"")
        if self._dataBag.get(u"%s_DATA_DATA_TYPE"%(prefix),'') == 'G':
            return
        
        SaunaNobleGasDataFetcher.c_log.info("Getting Gas Background Spectrum for %s\n"%(self._sampleID))
        
         # follow the same method as the one defined in bg_analyse
        # first look for the gas bk id in gards_sample_aux and then try to get the corresponding id.
        # if no sample_id is found look use the mrp method
        (rows,nbResults,_) = self.execute(sqlrequests.SQL_GET_SAUNA_AUX_GASBK_ID%(self._sampleID))
        id_found = False
        if nbResults == 1:
            # get ID from the measurement ID
            mid = rows[0]['mid']
            
            (rows,nbResults,_) = self.execute(sqlrequests.SQL_GET_SAUNA_GASBK_SAMPLEID_FROM_MID%(mid))
            
            if nbResults >= 1:
                sid =  rows[0]['sid']
                id_found = True
            else:
                SaunaNobleGasDataFetcher.c_log.info("Warning. Could not find a Gas Background sample_id from the measurement id %s. For more details regarding the request, see the log file"%(mid))

        if not id_found:
            # need to get the latest GAS BK sample_id
            (rows,nbResults,_) = self.execute(sqlrequests.SQL_GET_SAUNA_MRP_GASBK_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'])) 
       
            if nbResults == 0:
                SaunaNobleGasDataFetcher.c_log.info("Warning. There is no Background for %s.\n request %s \n Database query result %s"%(self._sampleID,sqlrequests.SQL_GET_SAUNA_MRP_GASBK_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID']),rows))
                self._dataBag[u'CONTENT_NOT_PRESENT'].add('GASBK')
                return
       
            if nbResults > 1:
                SaunaNobleGasDataFetcher.c_log.info("There is more than one Background for %s. Take the first result.\n request %s \n Database query result %s"%(self._sampleID,sqlrequests.SQL_GET_SAUNA_MRP_GASBK_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID']),rows))
           
            sid = rows[0]['SAMPLE_ID']
        
        DBDataFetcher.c_log.debug("sid = %s\n"%(sid))
          
        # now fetch the spectrum
        try:
            (dataname,_) = self._fetchAllData(sid) 
           
            self._dataBag[u'CURRENT_GASBK'] = dataname
           
            self._dataBag[u'CONTENT_PRESENT'].add('GASBK') 
           
        except Exception, e: #IGNORE:W0703
            SaunaNobleGasDataFetcher.c_log.error("Warning. No Data File found for background %s\n.Exception e = %s\n"%(sid,e))
            self._dataBag[u'CONTENT_NOT_PRESENT'].add('GASBK')
    
    def _fetchPrelsSpectrumData(self):
        """get the preliminary data.
           If the caching function is activated save the retrieved specturm on disc.
        
            Args:
               params: None
               
            Returns:
               return Nothing
        
            Raises:
               exception
        """
        
        # precondition do nothing if there the curr sample is a prel itself
        prefix = self._dataBag.get(u'CURRENT_CURR',"")
        if self._dataBag.get(u"%s_DATA_DATA_TYPE"%(prefix),'') == 'S' and self._dataBag.get(u"%s_DATA_SPECTRAL_QUALIFIER"%(prefix),'') == 'PREL':
            return
    
        SaunaNobleGasDataFetcher.c_log.info("Getting Prels Spectrum for %s\n"%(self._sampleID))
         
        # need to get the latest BK sample_id
        (rows,nbResults,_) = self.execute(sqlrequests.SQL_GET_SAUNA_PREL_SAMPLEIDS%(self._sampleID,self._dataBag[u'DETECTOR_ID'])) 
        
        if nbResults == 0:
            SaunaNobleGasDataFetcher.c_log.info("There is no PREL spectrum for %s."%(self._sampleID))
            self._dataBag[u'CONTENT_NOT_PRESENT'].add('PREL')
            return
        
        listOfPrel = []
          
        for row in rows:
            sid = row['SAMPLE_ID']
             
            # now fetch the spectrum with the a PREL_cpt id
            (dataname,_) = self._fetchAllData(sid) 
            # update list of prels
            listOfPrel.append(dataname)
         
        self._dataBag['CURR_List_OF_PRELS']  =  listOfPrel
        self._dataBag[u'CONTENT_PRESENT'].add('PREL') 
    
    def _fetchQCSpectrumData(self):
        """get the QC data.
           If the caching function is activated save the retrieved specturm on disc.
        
            Args:
               params: aDataname prefix in the dict
               
            Returns:
               return Nothing
        
            Raises:
               exception
        """
        
        #self.printContent(open("/tmp/sample_%s_extract.data"%(self._sampleID),"w"))
        
        # precondition do nothing if there the curr sample is a Detector background itself
        prefix = self._dataBag.get(u'CURRENT_CURR',"")
        if self._dataBag.get(u"%s_DATA_DATA_TYPE"%(prefix),'') == 'Q':
            return
        
        SaunaNobleGasDataFetcher.c_log.info("Getting QC Spectrum of %s\n"%(self._sampleID))
        
        # need to get the latest BK sample_id
        (rows,nbResults,_) = self.execute(sqlrequests.SQL_GET_SAUNA_QC_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'])) 
        
        nbResults = len(rows)
        
        if nbResults == 0:
            SaunaNobleGasDataFetcher.c_log.info("Warning. There is no QC for %s.\n request %s \n Database query result %s"%(self._sampleID,sqlrequests.SQL_GETPARTICULATE_QC_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID']),rows)) 
            # add in CONTENT_NOT_PRESENT this is used by the cache
            self._dataBag[u'CONTENT_NOT_PRESENT'].add('QC')
            return
       
        if nbResults > 1:
            SaunaNobleGasDataFetcher.c_log.info("There is more than one QC for %s. Take the first result.\n request %s \n Database query result %s"%(self._sampleID,sqlrequests.SQL_GETPARTICULATE_QC_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID']),rows))
           
        sid = rows[0]['SAMPLE_ID']
        
        try:
            # now fetch the spectrum
            (dataname,_) = self._fetchAllData(sid) 
        
            self._dataBag[u'CURRENT_QC'] = dataname
           
            self._dataBag[u'CONTENT_PRESENT'].add('QC') 
        
        except Exception, e: #IGNORE:W0703
            SaunaNobleGasDataFetcher.c_log.info("Warning. No Data File found for QC %s\n.Exception e = %s\n"%(sid,e))
            self._dataBag[u'CONTENT_NOT_PRESENT'].add('QC')
    
    def _fetchCURRSpectrumData(self):
        """ fetch the current spectrum identified by the current sampleID
        
            Args:
               params: aDataname
               
            Returns:
               return Nothing
        
            Raises:
               exception
        """
        
        (dataname,_) = self._fetchAllData(self._sampleID) 
        
        self._dataBag[u'CURRENT_CURR'] = dataname
        
        if'CURR' not in self._dataBag[u'CONTENT_PRESENT']:
            self._dataBag[u'CONTENT_PRESENT'].add('CURR') 
        
    def _fetchAuxiliarySampleInfo(self,aSampleID,aDataname):
        """ Get auxiliary information
        
            Args:
               aSampleID: sampleID
               
        """
        SaunaNobleGasDataFetcher.c_log.info("Getting auxiliary sample info for %s\n"%(aSampleID))
       
        result = self._mainConnector.execute(sqlrequests.SQL_GET_AUX_SAMPLE_INFO%(aSampleID))
       
        # only one row in result set
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults != 1:
            SaunaNobleGasDataFetcher.c_log.info("Warning. No auxiliary info for sample %s\n"%(aSampleID))
         
        # get retrieved data and transform dates
        data = {}
        data.update(rows[0])
        
        self._dataBag["%s_AUXILIARY_INFO"%(aDataname)] = data
           
    
        
    def _fetchAllData(self,aSampleID):
        """Fetch the two spectra (beta and gamma) and histogram
           If the caching function is activated save the retrieved specturm on disc.
           Try to find an extracted spectrum on OPS and Archive and if there is none of them look for the raw message (typeid)
        
            Args:
               aDataname: Name of the data. This will be used to create the name in the persistent hashtable and in the data spectrum filename
               
            Returns: (dataname,type)
                     where dataname = ID of the spectrum info in the data dict
                     where type     = type of the spectrum (SPHD, PREL, QC, BK)
        
            Raises:
               exception
        """
           
        SaunaNobleGasDataFetcher.c_log.info("Getting Spectra and Histogram for %s\n"%(aSampleID))
           
        # get sample info related to this sampleID
        (dataname,ty) = self._fetchGeneralSpectrumInfo(aSampleID)
           
        self._fetchAuxiliarySampleInfo(aSampleID,dataname)
         
        (rows,nbResults,foundOnArchive) = self.execute(sqlrequests.SQL_SAUNA_GET_FILES%(aSampleID,self._dataBag['STATION_CODE']),aTryOnArchive=True,aRaiseExceptionOnError=False)
         
        if nbResults == 0:
            SaunaNobleGasDataFetcher.c_log.warning("WARNING: sample_id %s has no extracted spectrum.Try to find a raw message.\n"%(aSampleID))
            arch_type = DBDataFetcher.c_fpdescription_type_translation.get(ty,"")
            (rows,nbResults,foundOnArchive) = self.execute(sqlrequests.SQL_SAUNA_GET_RAW_FILE%(arch_type,aSampleID,self._dataBag['STATION_CODE']),aTryOnArchive=True,aRaiseExceptionOnError=False) 
        elif nbResults != 3:
            SaunaNobleGasDataFetcher.c_log.warning("WARNING: found %d data file for %s when exactly 3 should be found\n"%(nbResults,aSampleID))
            
        data = {}
        
        self._dataBag[u"%s_DATA_NAME"%(dataname)]   = "%s-%s-%s"%(self._dataBag[u'STATION_CODE'],aSampleID,ty)

        for row in rows:
            (theInput,ext) = self._readDataFile(foundOnArchive,row['DIR'], row['DFile'],row['PRODTYPE'],row['FOFF'],row['DSIZE'],aSampleID,dataname,ty)
            
            compressed = self._conf.getboolean("Options","compressSpectrum")
            filename   = row['DFile']
            
             # check the message type and do the necessary.
            # here we expect a .msg or .s
            # we can also have .h coming from noble gaz histogram
            if filename.endswith("b.s") or filename.endswith("b.archs"):
               
                spec_id = "%s_DATA_B"%(dataname)
               
                (data,_) = self._extractSpectrumFromSpectrumFile(theInput) 
             
                theInput.close()
           
                (data,channel_span,energy_span) = self._processSpectrum(data,compressed) #IGNORE:W0612
               
                self._dataBag[u"%s_COMPRESSED"%(spec_id)]     = compressed
                self._dataBag[u"%s"%(spec_id)]                = data
                # create a unique id for the extract data
                self._dataBag[u"%s_ID"%(spec_id)]   = "%s-%s-%s-B"%(self._dataBag[u'STATION_CODE'],aSampleID,ty)
                self._dataBag[u"%s_TY"%(spec_id)]   = "%s-B"%(ty)
                  
            elif filename.endswith("g.s") or filename.endswith("g.archs"):
                spec_id = "%s_DATA_G"%(dataname)
               
                (data,_) = self._extractSpectrumFromSpectrumFile(theInput)
             
                theInput.close()
           
                (data,channel_span,energy_span) = self._processSpectrum(data,compressed)
               
                self._dataBag[u"%s_COMPRESSED"%(spec_id)]     = compressed
                self._dataBag[u"%s"%(spec_id)]                = data
                # create a unique id for the extract data
                self._dataBag[u"%s_ID"%(spec_id)]   = "%s-%s-%s-G"%(self._dataBag[u'STATION_CODE'],aSampleID,ty)
                self._dataBag[u"%s_TY"%(spec_id)]   = "%s-G"%(ty)
               
            elif filename.endswith(".h") or filename.endswith(".archhist"):
                spec_id = "%s_DATA_H"%(dataname)
               
                (data,_) = self._extractHistrogramFromHistogramFile(theInput)
               
                theInput.close()
               
                data = self._processHistogram(data,compressed)
               
                self._dataBag[u"%s_COMPRESSED"%(spec_id)]     = compressed
                self._dataBag[u"%s"%(spec_id)]                = data
               
                (r,n,foundOnArchive) = self.execute(sqlrequests.SQL_SAUNA_GET_HISTOGRAM_INFO%(aSampleID),aTryOnArchive=True,aRaiseExceptionOnError=False) #IGNORE:W0612
                if nbResults == 0:
                    SaunaNobleGasDataFetcher.c_log.warning("WARNING: Cannot find histogram information for sample_id %s in the database.\n"%(aSampleID))
                else:
                    # get energy and channel span from the table
                    self._dataBag[u"%s_DATA_G_CHANNEL_SPAN"%(dataname)] = r[0]['G_CHANNELS']
                    self._dataBag[u"%s_DATA_G_ENERGY_SPAN"%(dataname)]  = r[0]['G_ENERGY_SPAN']
                    self._dataBag[u"%s_DATA_B_CHANNEL_SPAN"%(dataname)] = r[0]['B_CHANNELS']
                    self._dataBag[u"%s_DATA_B_ENERGY_SPAN"%(dataname)]  = r[0]['B_ENERGY_SPAN']
               
                # create a unique id for the extracted data
                self._dataBag[u"%s_ID"%(spec_id)] = "%s-%s-%s-H"%(self._dataBag[u'STATION_CODE'],aSampleID,ty)
                self._dataBag[u"%s_TY"%(spec_id)]   = "%s-H"%(ty)
               
            elif filename.endswith(".msg") or filename.endswith(".archmsg"):
                # Here whe should extract the 3 components
                #TO BE DONE
                CTBTOError(-1,"To be developed\n")
            # remove it for the moment
            else:
                raise CTBTOError(-1,"Error unknown extension %s. Do not know how to read the file %s for aSampleID %s"%(ext,filename,aSampleID))
        
        # the global prefix BK_SID or CURR_SID and the ty (PREL, BK, CURR)
        return (dataname,ty)
        
    def _fetchData(self,aParams=None):
        """ get the different raw data info """
        
        spectrums = self._parser.parse(aParams,RequestParser.GAS).get(RequestParser.SPECTRUM,set())
        
        if ('None' in spectrums):
            # None is in there so do not include data
            return
        
        #fetch current spectrum
        if ('CURR' in spectrums):
            self._fetchCURRSpectrumData()
        
        if ('QC' in spectrums):
            self._fetchQCSpectrumData()
        
        # this is detector BK
        # to be changed in DETBK
        if ('DETBK' in spectrums):
            self._fetchDETBKSpectrumData()
           
        # get Gas BK
        # to be change in GASBK
        if ('GASBK' in spectrums):
            self._fetchGASBKSpectrumData()
        
        if ('PREL' in spectrums):
            self._fetchPrelsSpectrumData()
    
    def _fetchNuclidesToQuantify(self):
        
        # return all gards_XE_NUCL_LIB
        result = self._mainConnector.execute(sqlrequests.SQL_GET_NOBLEGAS_XE_NUCL_LIB)
        
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
        self._dataBag[u'XE_NUCL_LIB'] = res
        
        result.close() 
              
    def _fetchAnalysisResults(self,aParams=None):
        """ get the  sample categorization, activityConcentrationSummary, peaks results, parameters, flags"""
        
        # get static info necessary for the analysis
        self._fetchNuclidesToQuantify()
        
           
        analyses = self._parser.parse(aParams,RequestParser.GAS).get(RequestParser.ANALYSIS,set())
       
        if ('None' in analyses):
            # None is in there so do not include data
            return
        
        for analysis in analyses:
        
            # for the moment ignore Analysis for PREL
            if analysis == 'PREL' :
                continue
        
            # check if there is some data regarding this type of analysis
            # get the dataname of the current spectrum (it is the main spectrum)
            dataname = self._dataBag.get('CURRENT_%s'%(analysis),None)
          
            if dataname is not None:
                DBDataFetcher.c_log.info("Getting Analysis Results for CURRENT_%s\n"%(analysis))
          
                # extract id from dataname
                [pre,sid] = dataname.split('_') #IGNORE:W0612
          
                #self._fetchCategoryResults(sid,dataname)
        
                self._fetchNuclidesResults(sid,dataname)
             
                self._fetchROIResults(sid,dataname)
                 
                self._fetchFlags(sid,dataname)
        
                self._fetchParameters(sid,dataname)
   
   
    def _fetchNuclidesResults(self,sid,dataname):
        """fetch all the nuclides information regading the passed sampleID (sid).
            
                Args:
                   sid:sample_id
                   dataname: prefix used to store the data in the database
                   
                Returns:
                   return
            
                Raises:
                   exception"""
        
        # get identified Nuclides
        result = self._mainConnector.execute(sqlrequests.SQL_SAUNA_GET_IDENTIFIED_NUCLIDES%(sid))
       
        # only one row in result set
        rows = result.fetchall()   
       
        # get the volume of mesured xenon to compute activities from concentration
        # it is in m3 and in the AUXILIARY_INFO
        aux = self._dataBag.get('%s_AUXILIARY_INFO'%(dataname),{})
        # we need to a correction coefficient 0.087 according to Matthias
        corr_volume = aux.get('XE_VOLUME',0) / 0.087
        
        # add results in a list which will become a list of dicts
        res = []
        data = {}
        
        for row in rows:
            data.update(row.items())  
            
            nidflag = data.get(u'NID_FLAG',None)

            # check if there is NID key
            if nidflag is not None:
                val = DBDataFetcher.c_nid_translation.get(nidflag,nidflag)
                data[u'NID_FLAG']     = val
                data[u'NID_FLAG_NUM'] = nidflag
        
          
            # get activity. If no volume or no activity results are 0
            data[u'ACTIVITY'] = data.get(u'CONC',0)*corr_volume
            data[u'ACTIVITY_ERR'] = data.get(u'CONC_ERR',0)*corr_volume
            
            SaunaNobleGasDataFetcher.c_log.debug("Vol = %s, corr_vol = %s, activity = %s, concentration = %s \n"%(aux.get('XE_VOLUME',0), corr_volume, data.get(u'CONC',0)*corr_volume, data.get(u'CONC',0)))
          
            # to avoid div by 0 check that quotient is not nul
            if data[u'ACTIVITY'] != 0:
                data[u'ACTIVITY_ERR_PERC'] = abs((data.get(u'ACTIVITY_ERR',0)*100)/data.get(u'ACTIVITY'))
          
            # add concentration error in percent
            if data.get(u'CONC',0) != 0:
                data[u'CONC_ERR_PERC'] = abs((data.get(u'CONC_ERR',0)*100)/data.get(u'CONC'))
          
            data[u'LC_ACTIVITY'] = data.get(u'LC',0)* corr_volume 
            data[u'LD_ACTIVITY'] = data.get(u'LD',0)* corr_volume
          
            res.append(data)
            data = {}

        # add in dataBag
        self._dataBag[u'%s_IDED_NUCLIDES'%(dataname)] = res
            
        result.close()
    
    def _fetchFlags(self,sid,aDataname):
        """ get the different flags """
        
        self._fetchTimelinessFlags(sid,aDataname)
        
        self._fetchdataQualityFlags(sid,aDataname)
        
    def _fetchdataQualityFlags(self,sid,aDataname):
        """ Check Volume Flags """
        
        # check Xenon Volume
        volMin = 0.43
        
        aux = self._dataBag.get('%s_AUXILIARY_INFO'%(aDataname),None)
        
        if aux is not None:
            vol     = aux[u'XE_VOLUME']
            vol_err = aux[u'XE_VOLUME_ERR']
            
            # check that vol + err > VolMin
            if (vol + vol_err) < volMin:
                #NOK
                self._dataBag[u'%s_VOLUME_FLAG'%(aDataname)] = 'Fail'
               
            else:
                # OK
                self._dataBag[u'%s_VOLUME_FLAG'%(aDataname)] = 'Pass'
            
            self._dataBag[u'%s_VOLUME_VAL'%(aDataname)]  = vol
            self._dataBag[u'%s_VOLUME_TEST'%(aDataname)] = 'x superior or equal to 0.43 ml' 
    
    def _fetchTimelinessFlags(self,sid,aDataname):
        """ prepare timeliness checking info """
        
        # precondition check that there is COLLECT_START 
        # otherwise quit
        if (self._dataBag.get("%s_DATA_COLLECT_START"%(aDataname),None) is None) or (self._dataBag.get("%s_DATA_COLLECT_STOP"%(aDataname),None) is None):
            SaunaNobleGasDataFetcher.c_log.warning("Warnings. Cannot compute the timeliness flags missing information for %s\n"%(sid))
            return
       
        # check collection flag
        # check that collection time with CollMin = 0.1 H < Collection Stop - Collection Start < CollMax = 25H
        # min is 4 H = 14400 seconds and max is 25 h = 90 000 seconds
        coll_min  = 14400
        coll_max  = 90000
        collect_start  = ctbto.common.time_utils.getDateTimeFromISO8601(self._dataBag["%s_DATA_COLLECT_START"%(aDataname)])
        collect_stop   = ctbto.common.time_utils.getDateTimeFromISO8601(self._dataBag["%s_DATA_COLLECT_STOP"%(aDataname)])
    
        diff_in_sec = ctbto.common.time_utils.getDifferenceInTime(collect_start, collect_stop)
        
        # check time collection 
        # if 4 within 24 hours
        if diff_in_sec < coll_min or diff_in_sec > coll_max:
            # not ok add the diff
            self._dataBag[u'%s_TIME_FLAGS_COLLECTION_FLAG'%(aDataname)] = 'Fail'
        else:
            # ok
            self._dataBag[u'%s_TIME_FLAGS_COLLECTION_FLAG'%(aDataname)] = 'Pass'
        
        self._dataBag[u'%s_TIME_FLAGS_COLLECTION_VAL'%(aDataname)]   = diff_in_sec
        self._dataBag[u'%s_TIME_FLAGS_COLLECTION_TEST'%(aDataname)] = 'x between 4h and 25h'
        
        # check decay flag
        # decay time = ['DATA_ACQ_STOP'] - ['DATA_COLLECT_STOP']
        # check that acq time with PauseMin = 0.1 H (360) < Acq Start - Coll Stop < CollMax = 24H (86 400 sec)
        pause_min  = 360
        pause_max  = 86400
        
        acq_start  = ctbto.common.time_utils.getDateTimeFromISO8601(self._dataBag["%s_DATA_ACQ_START"%(aDataname)])
        
        acq_stop   = ctbto.common.time_utils.getDateTimeFromISO8601(self._dataBag["%s_DATA_ACQ_STOP"%(aDataname)])
    
        diff_in_sec = ctbto.common.time_utils.getDifferenceInTime(collect_stop,acq_start)
          
        # check pause time or decay time
        if diff_in_sec > pause_max or diff_in_sec < pause_min:
            # NOK
            self._dataBag[u'%s_TIME_FLAGS_DECAY_FLAG'%(aDataname)] = 'Fail'
        else:
            # OK
            self._dataBag[u'%s_TIME_FLAGS_DECAY_FLAG'%(aDataname)] = 'Pass' 
        
        self._dataBag[u'%s_TIME_FLAGS_DECAY_VAL'%(aDataname)]   = diff_in_sec
        self._dataBag[u'%s_TIME_FLAGS_DECAY_TEST'%(aDataname)]  = 'x between 0.1h and 24h'
        
       
        # check acquisition flag
        # acqMin = 4 H (14400 s) < Acquisition Time < acqMax 25H (90000 s)
        acq_min = 14400
        acq_max = 90000
        
        diff_in_sec   = ctbto.common.time_utils.getDifferenceInTime(acq_start,acq_stop)
        
        if diff_in_sec > acq_max and diff_in_sec < acq_min:
            # NOK
            self._dataBag[u'%s_TIME_FLAGS_ACQUISITION_FLAG'%(aDataname)] = 'Fail'
        else:
            # OK
            self._dataBag[u'%s_TIME_FLAGS_ACQUISITION_FLAG'%(aDataname)] = 'Pass'
        
        self._dataBag[u'%s_TIME_FLAGS_ACQUISITION_VAL'%(aDataname)]   = diff_in_sec
        self._dataBag[u'%s_TIME_FLAGS_ACQUISITION_TEST'%(aDataname)]  = 'x between 4h and 25h'
        
        # response time 48 h (302400 sec) tramsit_dtg - collect_start
        max_respond_time = 302400
        transmit_time = ctbto.common.time_utils.getDateTimeFromISO8601(self._dataBag[u'%s_DATA_TRANSMIT_DTG'%(aDataname)])
        diff_in_sec = ctbto.common.time_utils.getDifferenceInTime(collect_start,transmit_time)
        
        if diff_in_sec > max_respond_time:
            self._dataBag[u'%s_TIME_FLAGS_RESPOND_TIME_FLAG'%(aDataname)] = 'Fail'
        else:
            self._dataBag[u'%s_TIME_FLAGS_RESPOND_TIME_FLAG'%(aDataname)] = 'Pass'
        
        self._dataBag[u'%s_TIME_FLAGS_RESPOND_TIME_VAL'%(aDataname)]   = diff_in_sec
        self._dataBag[u'%s_TIME_FLAGS_RESPOND_TIME_TEST'%(aDataname)]  = 'no more than 48h'
    
           
    def _fetchParameters(self,sid,dataname):
        """fetch all the analysis parameters for the passed sampleID (sid).
            
                Args:
                   sid:sample_id
                   dataname: prefix used to store the data in the database
                   
                Returns:
                   return
            
                Raises:
                   exception"""
        
        # get processing params and flags
        result = self._mainConnector.execute(sqlrequests.SQL_SAUNA_GET_PROCESSING_PARAMS%(sid))
       
        # only one row in result set
        rows = result.fetchall()    
        
        # add results in a list which will become a list of dicts
        res = []
        data = {}
        
        for row in rows:
            data.update(row.items())  
          
            res.append(data)
            data = {}

        # add in dataBag
        self._dataBag[u'%s_PROC_PARAMS'%(dataname)] = res
        
        result.close()
        
        # get ROI params
        result = self._mainConnector.execute(sqlrequests.SQL_SAUNA_GET_ROI_PARAMS%(sid))
       
        # only one row in result set
        rows = result.fetchall()    
        
        # add results in a list which will become a list of dicts
        res = []
        data = {}
        
        for row in rows:
            data.update(row.items())  
          
            res.append(data)
            data = {}

        # add in dataBag
        self._dataBag[u'%s_ROI_PARAMS'%(dataname)] = res
        
        result.close()
      
      
    def _fetchNuclideNamePerROI(self,sid):
        """fetch the nuclide names for a given ROI.
            
                Args:
                   sid:sample_id
                   
                Returns:
                   return
            
                Raises:
                   exception
        """ 
        # get ROI Concs
        result = self._mainConnector.execute(sqlrequests.SQL_SAUNA_GET_NUCLIDE_FOR_ROI%(sid))
       
        # only one row in result set
        rows = result.fetchall()
   
        # add results in a dict
        data = {}
        for row in rows:
            data[row['ROI']] = row['NAME']
       
        # region 1 always PB-214
        data[1] = "PB-214"
        
        return data
   
    def _fetchROIEfficiency(self,sid):
        """fetch all the ROI Efficiency info.
            
                Args:
                   sid:sample_id
                   
                Returns:
                   return a dict where the key is the ROI number and the value is (efficiency,efficiency_err)
            
                Raises:
                   exception
           """ 
        # GET ROI INFO
        result = self._mainConnector.execute(sqlrequests.SQL_SAUNA_GET_ROI_EFFICIENCY%(sid))
       
        # only one row in result set
        rows = result.fetchall()
   
        # add results in a dict
        data = {} 
       
        for row in rows:
            data[row['ROI']]=(row['BG_EFFICIENCY'],row['BG_EFFIC_ERROR'])
    
        return data
           
    def _fetchROIResults(self,sid,dataname):
        """fetch all the ROI information for the passed sampleID (sid).
            
                Args:
                   sid:sample_id
                   dataname: prefix used to store the data in the database
                   
                Returns:
                   return
            
                Raises:
                   exception
        """
       
        # first game the Nuclide for the corresponding ROI
        ROI_2_Nuclides = self._fetchNuclideNamePerROI(sid)
       
        efficiency = self._fetchROIEfficiency(sid)
    
        # GET ROI INFO
        result = self._mainConnector.execute(sqlrequests.SQL_SAUNA_GET_ROI_INFO%(sid))
       
        # only one row in result set
        rows = result.fetchall()
   
        # add results in a list which will become a list of dicts
        res = []
        data = {}
        
        for row in rows:
            data.update(row.items()) 
          
            # add related nuclide
            data[u'Nuclide'] = ROI_2_Nuclides.get(data['ROI'],"NoName")
          
            # add efficiency
            eff = efficiency.get(data['ROI'],None)
            if eff != None:
                (e,e_err) = eff
                data[u'EFFICIENCY'] = e
                data[u'EFFICIENCY_ERROR'] = e_err
              
                # get relative error
                if e != 0:
                    data[u'EFFICIENCY_ERROR_PERC'] = abs((e_err*100)/e)
              
            
            res.append(data)
            data = {}

        # add in dataBag
        self._dataBag[u'%s_ROI_INFO'%(dataname)] = res  
        result.close()
       
        # get ROI Boundaries
        # GET ROI INFO
        result = self._mainConnector.execute(sqlrequests.SQL_SAUNA_GET_ROI_BOUNDARIES%(sid))
       
        # only one row in result set
        rows = result.fetchall()
   
        # add results in a list which will become a list of dicts
        res = []
        data = {}
        
        for row in rows:
            data.update(row.items()) 
            res.append(data)
            data = {}

        # add in dataBag
        self._dataBag[u'%s_ROI_BOUNDARIES'%(dataname)] = res  
        result.close()
     
    def _fetchCalibration(self):  
        """ Fetch the calibration info for all the different spectrums """
        
        for present in self._dataBag.get('CONTENT_PRESENT',[]):
            
            # treat preliminary samples differently
            if present == 'PREL':
                
                for prel in self._dataBag.get('CURR_List_OF_PRELS',[]):
                    
                    if prel is None:
                        raise CTBTOError(-1,"Error when fetching Calibration info for prefix %s, There is no CURRENT_%s in the dataBag\n"%(present,present))
                    
                    self._fetchCalibrationCoeffs(prel)
            else:    
            
                prefix = self._dataBag.get(u'CURRENT_%s'%(present),None)
                if prefix is None:
                    raise CTBTOError(-1,"Error when fetching Calibration info for prefix %s, There is no CURRENT_%s in the dataBag\n"%(present,present))
               
                self._fetchCalibrationCoeffs(prefix)
          
                        
    def _fetchCalibrationCoeffs(self,prefix):
        
        # get the sampleID 
        # extract id from dataname
        
        [pre,sid] = prefix.split('_') #IGNORE:W0612
    
        if sid is None:
            raise CTBTOError(-1,"Error when fetching Calibration Info. No sampleID found in dataBag for %s"%(prefix))
        
        calIDs_list = []
        
        # get energy calibration info
        result = self._mainConnector.execute(sqlrequests.SQL_GET_SAUNA_ENERGY_CAL%(sid))
        
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults != 1:
            DBDataFetcher.c_log.warning("Warning no energy calibration coefficient for %s\n"%(sid))
            return
        
        # create a list of dicts
        data = {}

        data.update(rows[0].items())
        
        
        # Beta Cal Info
        checksum = self._getCalibrationCheckSum([data[u'BETA_COEFF1'],data[u'BETA_COEFF2'],data[u'BETA_COEFF3']])
        
        cal_id = 'EN-B-%s'%(checksum)
        
        # add in dataBag as EN-checksumif not already in the dataBag
        if cal_id not in self._dataBag:
            self._dataBag[cal_id] = {'BETA_COEFF1':data[u'BETA_COEFF1'],'BETA_COEFF2':data[u'BETA_COEFF2'],'BETA_COEFF3':data[u'BETA_COEFF3']}
        
        # prefix_ENERGY_CAL now refers to this calibration ID
        self._dataBag[u'%s_B_ENERGY_CAL'%(prefix)] = cal_id
        
        # add in list of calibration info for this particular sample
        calIDs_list.append(cal_id)
        
        # Gamma Cal Info
        checksum = self._getCalibrationCheckSum([data[u'GAMMA_COEFF1'],data[u'GAMMA_COEFF2'],data[u'GAMMA_COEFF3']])
        
        cal_id = 'EN-G-%s'%(checksum)
        
        # add in dataBag as EN-checksumif not already in the dataBag
        if cal_id not in self._dataBag:
            self._dataBag[cal_id] = {'GAMMA_COEFF1':data[u'GAMMA_COEFF1'],'GAMMA_COEFF2':data[u'GAMMA_COEFF2'],'GAMMA_COEFF3':data[u'GAMMA_COEFF3']}
        
        # prefix_ENERGY_CAL now refers to this calibration ID
        self._dataBag[u'%s_G_ENERGY_CAL'%(prefix)] = cal_id
        
        # add in list of calibration info for this particular sample
        calIDs_list.append(cal_id)
        
        # add the list of calib_infos in the bag
        self._dataBag[u'%s_G_DATA_ALL_CALS'%(prefix)] = calIDs_list
        
        result.close()     

class SpalaxNobleGasDataFetcher(DBDataFetcher):
    """ Class for fetching SPALAX related data """
    
    # Class members
    c_log = logging.getLogger("datafetchers.SpalaxNobleGasDataFetcher")
    c_log.setLevel(logging.INFO)
    
    c_method_translation = { 11: 'Peak Fit Method', 12:'Decay Analysis Method'}


    def __init__(self,aMainDbConnector=None,aArchiveDbConnector=None,aSampleID=None):
        
        super(SpalaxNobleGasDataFetcher,self).__init__(aMainDbConnector,aArchiveDbConnector,aSampleID)
        
        self._dataBag['SAMPLE_TYPE']= 'SPALAX'
    
    def _fetchData(self,aParams=None):
        """ get the different raw data info """
        
        spectrums = self._parser.parse(aParams,RequestParser.GAS).get(RequestParser.SPECTRUM,set())
        
        if ('None' in spectrums):
            # None is in there so do not include data
            return
        
        #fetch current spectrum
        if ('CURR' in spectrums):
            self._fetchCURRSpectrumData()
        
        #if ('QC' in spectrums):
        #    self._fetchQCSpectrumData()
        
        if ('DETBK' in spectrums):
            self._fetchDETBKSpectrumData()
        
        if ('PREL' in spectrums):
            self._fetchPrelsSpectrumData()
      
    def _fetchDETBKSpectrumData(self):
        """get the Background spectrum.
           If the caching function is activated save the retrieved spectrum on disc.
        
            Args:
               params: None
               
            Returns:
               return Nothing
        
            Raises:
               exception
        """
        
        # precondition do nothing if there the curr sample is a Detector background itself
        prefix = self._dataBag.get(u'CURRENT_CURR',"")
        if self._dataBag.get(u"%s_DATA_DATA_TYPE"%(prefix),'') == 'D':
            return
        
        SpalaxNobleGasDataFetcher.c_log.info("Getting Background Spectrum for %s\n"%(self._sampleID))
        
        # need to get the latest BK sample_id
        result = self._mainConnector.execute(sqlrequests.SQL_SPALAX_GET_DETBK_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID']))
        
        # only one row in result set
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults == 0:
            SpalaxNobleGasDataFetcher.c_log.warning("There is no Background for %s.\n request %s \n Database query result %s"%(self._sampleID,sqlrequests.SQL_GETPARTICULATE_BK_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID']),rows))
            self._dataBag[u'CONTENT_NOT_PRESENT'].add('BK')
            return
       
        if nbResults > 1:
            SpalaxNobleGasDataFetcher.c_log.warning("There is more than one Background for %s. Take the first result.\n request %s \n Database query result %s"%(self._sampleID,sqlrequests.SQL_GETPARTICULATE_BK_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID']),rows))
           
        sid = rows[0]['SAMPLE_ID']
        
        DBDataFetcher.c_log.debug("sid = %s\n"%(sid))
        
        result.close()
        
        # now fetch the spectrum
        try:
            (dataname,ty) = self._fetchSpectrumData(sid) #IGNORE:W0612
           
            self._dataBag[u'CURRENT_BK'] = dataname
           
            self._dataBag[u'CONTENT_PRESENT'].add('BK') 
           
        except Exception, e: #IGNORE:W0703
            SpalaxNobleGasDataFetcher.c_log.warning("Warning. No Data File found for background %s.Exception : %s\n"%(sid,e))
            self._dataBag[u'CONTENT_NOT_PRESENT'].add('BK')
            
    
    def _fetchQCSpectrumData(self):
        """get the QC spectrum.
           If the caching function is activated save the retrieved specturm on disc.
        
            Args:
               params: aDataname prefix in the dict
               
            Returns:
               return Nothing
        
            Raises:
               exception
        """  
        # precondition do nothing if there the curr sample is a Detector background itself
        prefix = self._dataBag.get(u'CURRENT_CURR',"")
        if self._dataBag.get(u"%s_DATA_DATA_TYPE"%(prefix),'') == 'Q':
            return
        
        SpalaxNobleGasDataFetcher.c_log.info("Getting QC Spectrum of %s\n"%(self._sampleID))
        
        # need to get the latest BK sample_id
        (rows,nbResults,foundOnArchive) = self.execute(sqlrequests.SQL_SPALAX_GET_QC_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'])) #IGNORE:W0612
        
        nbResults = len(rows)
        
        if nbResults == 0:
            SpalaxNobleGasDataFetcher.c_log.warning("Warning. There is no QC for %s.\n request %s \n Database query result %s"%(self._sampleID,sqlrequests.SQL_GETPARTICULATE_QC_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID']),rows)) 
            # add in CONTENT_NOT_PRESENT this is used by the cache
            self._dataBag[u'CONTENT_NOT_PRESENT'].add('QC')
            return
       
        if nbResults > 1:
            SpalaxNobleGasDataFetcher.c_log.warning("There is more than one QC for %s. Take the first result.\n request %s \n Database query result %s"%(self._sampleID,sqlrequests.SQL_GETPARTICULATE_QC_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID']),rows))
           
        sid = rows[0]['SAMPLE_ID']
        
        try:
            # now fetch the spectrum
            (dataname,ty) = self._fetchSpectrumData(sid) #IGNORE:W0612
        
            self._dataBag[u'CURRENT_QC'] = dataname
           
            self._dataBag[u'CONTENT_PRESENT'].add('QC') 
        
        except Exception, e: #IGNORE:W0703
            SpalaxNobleGasDataFetcher.c_log.warning("Warning. No Data File found for QC %s. Exception: %s\n"%(sid,e))
            self._dataBag[u'CONTENT_NOT_PRESENT'].add('QC')
        
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
        
        # precondition do nothing if there the curr sample is a prel itself
        prefix = self._dataBag.get(u'CURRENT_CURR',"")
        if self._dataBag.get(u"%s_DATA_DATA_TYPE"%(prefix),'') == 'S' and self._dataBag.get(u"%s_DATA_SPECTRAL_QUALIFIER"%(prefix),'') == 'PREL':
            return
    
        SpalaxNobleGasDataFetcher.c_log.info("Getting Prels Spectrum for %s\n"%(self._sampleID))
        
        # need to get the latest BK sample_id
        result = self._mainConnector.execute(sqlrequests.SQL_SPALAX_GET_PREL_SAMPLEIDS%(self._sampleID,self._dataBag[u'DETECTOR_ID']))
        
        # only one row in result set
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults == 0:
            SpalaxNobleGasDataFetcher.c_log.warning("There is no PREL spectrum for %s."%(self._sampleID))
            self._dataBag[u'CONTENT_NOT_PRESENT'].add('PREL')
            return
        
        listOfPrel = []
          
        for row in rows:
            sid = row['SAMPLE_ID']
             
            # now fetch the spectrum with the a PREL_cpt id
            (dataname,ty) = self._fetchSpectrumData(sid) #IGNORE:W0612
            # update list of prels
            listOfPrel.append(dataname)
        
        self._dataBag['CURR_List_OF_PRELS']  =  listOfPrel
        self._dataBag[u'CONTENT_PRESENT'].add('PREL') 
           
        
        result.close()
        
    def _fetchCURRSpectrumData(self):
        """ fetch the current spectrum identified by the current sampleID
        
            Args:
               params: aDataname
               
            Returns:
               return Nothing
        
            Raises:
               exception
        """
        
        (dataname,ty) = self._fetchSpectrumData(self._sampleID) #IGNORE:W0612
        
        self._dataBag[u'CURRENT_CURR'] = dataname
        
        if'CURR' not in self._dataBag[u'CONTENT_PRESENT']:
            self._dataBag[u'CONTENT_PRESENT'].add('CURR')  
    
    def _fetchAuxiliarySampleInfo(self,aSampleID,aDataname):
        """ Get auxiliary information
        
            Args:
               aSampleID: sampleID
               
        """
        SpalaxNobleGasDataFetcher.c_log.info("Getting auxiliary sample info for %s\n"%(aSampleID))
       
        result = self._mainConnector.execute(sqlrequests.SQL_GET_AUX_SAMPLE_INFO%(aSampleID))
       
        # only one row in result set
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults != 1:
            SpalaxNobleGasDataFetcher.c_log.info("Warning. No auxiliary info for sample %s\n"%(aSampleID))
         
        # get retrieved data and transform dates
        data = {}
        data.update(rows[0])
        
        self._dataBag["%s_AUXILIARY_INFO"%(aDataname)] = data
    
    def _fetchSpectrumData(self,aSampleID):
        """get the any spectrum data.
           If the caching function is activated save the retrieved specturm on disc.
           Try to find an extracted spectrum on OPS and Archive and if there is none of them look for the raw message (typeid)
        
            Args:
               aDataname: Name of the data. This will be used to create the name in the persistent hashtable and in the data spectrum filename
               
            Returns: (dataname,type)
                     where dataname = ID of the spectrum info in the data dict
                     where type     = type of the spectrum (SPHD, PREL, QC, BK)
        
            Raises:
               exception
        """
           
        SpalaxNobleGasDataFetcher.c_log.info("Getting Spectrum for %s\n"%(aSampleID))
           
        # get sample info related to this sampleID
        # pass the gamma prefix
        (dataname,ty) = self._fetchGeneralSpectrumInfo(aSampleID,"_G")
        
        # fetch auxiliary data
        self._fetchAuxiliarySampleInfo(aSampleID,dataname)
        
        SpalaxNobleGasDataFetcher.c_log.info("Its name will be %s and its type is %s"%(dataname,ty))
         
        (rows,nbResults,foundOnArchive) = self.execute(sqlrequests.SQL_SPALAX_GET_SPECTRUM%(aSampleID,self._dataBag['STATION_CODE']),aTryOnArchive=True,aRaiseExceptionOnError=False)
        
        if nbResults == 0:
            SpalaxNobleGasDataFetcher.c_log.warning("WARNING: sample_id %s has no extracted spectrum.Try to find a raw message.\n"%(aSampleID))
            arch_type = DBDataFetcher.c_fpdescription_type_translation.get(ty,"")
            (rows,nbResults,foundOnArchive) = self.execute(sqlrequests.SQL_SPALAX_GET_RAW_SPECTRUM%(arch_type,aSampleID,self._dataBag['STATION_CODE']),aTryOnArchive=True,aRaiseExceptionOnError=True) 
        elif nbResults > 1:
            ParticulateDataFetcher.c_log.warning("WARNING: found more than one spectrum for sample_id %s\n"%(aSampleID))
            
        # add spectrum group name
        self._dataBag[u"%s_DATA_NAME"%(dataname)]   = "%s-%s-%s"%(self._dataBag[u'STATION_CODE'],aSampleID,ty)
        
        for row in rows:
            (anInput,ext) = self._readDataFile(foundOnArchive,row['DIR'], row['DFile'],row['PRODTYPE'],row['FOFF'],row['DSIZE'],aSampleID,dataname,ty)
           
            # check if it has to be compressed
            compressed = self._conf.getboolean("Options","compressSpectrum")
            sid = "%s_G_DATA"%(dataname)
                
            # check the message type and do the necessary.
            # here we expect a .msg or .s
            # we can also have .h coming from noble gaz histogram
            if ext == '.msg' or ext == '.archmsg':
              
                (data,limits)  =  self._extractSpectrumFromMessageFile(anInput) #IGNORE:W0612
              
                anInput.close()
              
                (data,channel_span,energy_span) = self._processSpectrum(data,compressed)
            # '.archs' given for an archived sample
            elif ext == '.s' or ext == '.archs':
            
                (data,limits) = self._extractSpectrumFromSpectrumFile(anInput)
             
                anInput.close()
           
                (data,channel_span,energy_span) = self._processSpectrum(data,compressed)
            else:
                raise CTBTOError(-1,"Error unknown extension %s. Do not know how to read the file %s for aSampleID %s"%(ext,row['DFile'],aSampleID))
         
            self._dataBag[u"%s_COMPRESSED"%(sid)]     = compressed
            self._dataBag[u"%s"%(sid)]                = data
            self._dataBag[u"%s_CHANNEL_SPAN"%(sid)]   = channel_span
            self._dataBag[u"%s_ENERGY_SPAN"%(sid)]    = energy_span
            # create a unique id for the extract data
            self._dataBag[u"%s_ID"%(sid)] = "%s-%s-%s"%(self._dataBag[u'STATION_CODE'],aSampleID,ty)
            self._dataBag[u"%s_TY"%(sid)]   = "%s-G"%(ty)
        
        return (dataname,ty)
    
    def _fetchNuclidesToQuantify(self):
        """ get the Xe nuclides to quantify """
        # return all gards_XE_NUCL_LIB
        result = self._mainConnector.execute(sqlrequests.SQL_GET_NOBLEGAS_XE_NUCL_LIB)
        
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
        self._dataBag[u'XE_NUCL_LIB'] = res
        
        result.close()  
    
    def _fetchXeRefLines(self):  
        """ get the Xe reference lines"""
        
        # return all gards_XE_NUCL_LIB
        result = self._mainConnector.execute(sqlrequests.SQL_SPALAX_GET_XE_REF_LINES)
        
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
        self._dataBag[u'XE_REF_LINES_LIB'] = res
        
        result.close()
        
    def _fetchXeNuclideLinesLib(self):
        """ get the lib of nuclides lines"""
        
        # return all gards_XE_NUCL_LIB
        result = self._mainConnector.execute(sqlrequests.SQL_GET_NOBLEGAS_XE_NUCL_LINES_LIB)
        
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
        self._dataBag[u'XE_NUCLIDE_LINES_LIB'] = res
        
        result.close()

    def _fetchAutoSaintDefaultParams(self):
        """ get the default params used by autosaint to run the analysis"""
        
        # return all gards_XE_NUCL_LIB
        result = self._mainConnector.execute(sqlrequests.SQL_GET_AUTOSAINT_DEFAULT_PARAMS)
        
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
        self._dataBag[u'AUTOSAINT_DEFAULT_PARAMS'] = res
        
        result.close()
           
    def _fetchAnalysisResults(self,aParams=None):
        """ get the  sample categorization, activityConcentrationSummary, peaks results, parameters, flags"""
        
        # get static info necessary for the analysis
        self._fetchNuclidesToQuantify()
        
        self._fetchXeNuclideLinesLib()
        
        self._fetchXeRefLines()
        
        self._fetchAutoSaintDefaultParams()
           
        analyses = self._parser.parse(aParams,RequestParser.GAS).get(RequestParser.ANALYSIS,set())
       
        if ('None' in analyses):
            # None is in there so do not include data
            return
        
        for analysis in analyses:
        
            # for the moment ignore Analysis for PREL
            if analysis == 'PREL' :
                continue
        
            # check if there is some data regarding this type of analysis
            # get the dataname of the current spectrum (it is the main spectrum)
            dataname = self._dataBag.get('CURRENT_%s'%(analysis),None)
          
            if dataname is not None:
                DBDataFetcher.c_log.info("Getting Analysis Results for CURRENT_%s\n"%(analysis))
          
                # extract id from dataname
                [pre,sid] = dataname.split('_') #IGNORE:W0612
          
                self._fetchCategoryResults(sid,dataname)
        
                self._fetchXeResults(sid,dataname)
             
                self._fetchFlags(sid,dataname)
        
                self._fetchParameters(sid,dataname)
    
    def _fetchParameters(self,a_sid,a_dataname):
        """ 
           Get the parameters for a particular sample
           
            Args:
               
            Returns:  
        
            Raises:
               exception
        """
        # get processing params and flags
        result = self._mainConnector.execute(sqlrequests.SQL_SPALAX_GET_PROCESSING_PARAMETERS%(a_sid))
       
        # only one row in result set
        rows = result.fetchall()    
        
        # add results in a list which will become a list of dicts
        res = []
        data = {}
        
        for row in rows:
            data.update(row.items())  
          
            res.append(data)
            data = {}

        # add in dataBag
        self._dataBag[u'%s_PROC_PARAMS'%(a_dataname)] = res
        
        result.close()  
    
    def _fetchCategoryResults(self,a_sid,a_dataname):
        """ 
           Get the category results
           
            Args:
               
            Returns:   = type of the spectrum (SPHD, PREL, QC, BK)
        
            Raises:
               exception
        """
        
        # to be done when the category scheme is established
        
    def _fetchFlags(self,a_sid,a_dataname):
        """ 
           Get the different kind of flags (QC flags from GARDS_QC_RESULTS and Quality flags from GARDS_FLAGS)
           
            Args:
                a_sid : the sample_id
                a_dataname: name used to qualify the related sample in the data dict.
               
            Returns:   
        
            Raises:
               exception
        """
        self._fetchdataQualityFlags(a_sid,a_dataname)
        
        self._fetchQCFlags(a_sid, a_dataname)
    
    def _fetchQCFlags(self,sid,dataname):
        """ 
           Get the QC flags as they have been stored in the DB by autoSaintXe
           
            Args:
               
            Returns:   = type of the spectrum (SPHD, PREL, QC, BK)
        
            Raises:
               exception
        """
         # get MDA nuclides
        result = self._mainConnector.execute(sqlrequests.SQL_SPALAX_GET_QC_FLAGS%(sid))
        
        rows = result.fetchall()
        
        if len(rows):
            data = {}
        
            res = []
        
            for row in rows:
                # copy row in a normal dict
                data.update(row)
            
                res.append(data)
                data = {}
               
            # add in dataBag
            # R is for Red and G for Green
            self._dataBag[u'%s_QC_FLAGS'%(dataname)] = res    
        
        
    def _fetchdataQualityFlags(self,sid,dataname):
        """ 
           Get the category results
           
            Args:
               
            Returns:   = type of the spectrum (SPHD, PREL, QC, BK)
        
            Raises:
               exception
        """
        
         # get MDA nuclides
        result = self._mainConnector.execute(sqlrequests.SQL_SPALAX_GET_DATA_QUALITY_FLAGS%(sid))
        
        rows = result.fetchall()
        
        if len(rows):
            data = {}
        
            res = []
        
            for row in rows:
                # copy row in a normal dict
                data.update(row)
            
                res.append(data)
                data = {}
               
            # add in dataBag
            self._dataBag[u'%s_DATA_QUALITY_FLAGS'%(dataname)] = res
    
    def _fetchXeResults(self,sid,dataname):
        """ 
           Get the XE results
           
            Args:
               
            Returns:
        
            Raises:
               exception
        """
        # get identified Nuclides
        result = self._mainConnector.execute(sqlrequests.SQL_SPALAX_GET_XE_RESULTS %(sid))
       
        # only one row in result set
        rows = result.fetchall()   
        
        # get the volume of mesured xenon to compute activities from concentration
        # it is in m3 and in the AUXILIARY_INFO
        aux = self._dataBag.get('%s_AUXILIARY_INFO'%(dataname),{})
        # we need a vol in l
        corr_volume = aux.get('XE_VOLUME',0)/(1000)
       
        # add results in a list which will become a list of dicts
        res = []
        data = {}
        
        for row in rows:
            data.update(row.items())  
            
            # translate NID_FLAG to something humanely understandable
            nidflag = data.get(u'NID_FLAG',None)
            # check if there is NID key
            if nidflag is not None:
                val = DBDataFetcher.c_nid_translation.get(nidflag,nidflag)
                data[u'NID_FLAG']     = val
                data[u'NID_FLAG_NUM'] = nidflag
            
            # translate METHOD_ID to something humanely understandable
            method_id = data.get(u'METHOD_ID',UNDEFINED)
            # check if there is NID key
            if nidflag is not None:
                val = SpalaxNobleGasDataFetcher.c_method_translation.get(method_id,method_id)
                data[u'METHOD']    = val
                data[u'METHOD_ID'] = nidflag
                
            # translate NUCLIDE_ID into a string
            # use nuclide lib for translation
            # beware the list index start at 0 and the nuclide_id start at 1
            nuclide_id = data.get(u'NUCLIDE_ID',None)
            nuclide_id = nuclide_id - 1
            nuclide_lib = self._dataBag[u'XE_NUCL_LIB']
            if nuclide_id is not None:
                nucl = nuclide_lib[nuclide_id] if (nuclide_id < len(nuclide_lib)) and (nuclide_id >=0) else UNDEFINED
                data[u'NUCLIDE'] =  nucl[u'NAME']
        
            # add concentration error in percent
            if data.get(u'CONC',0) != 0:
                data[u'CONC_ERR_PERC'] = (data.get(u'CONC_ERR',0)*100)/data.get(u'CONC')
                
            # calculate volumes and concentration (need vol for that)
            # get activity. If no volume or no activity results are 0
            # if volume = 0 (I think that 1 m3 means nothing)
            if corr_volume >= 0:
                data[u'ACTIVITY']     = data.get(u'CONC',0)*corr_volume if data.get(u'CONC',0) != 0 else UNDEFINED
                data[u'ACTIVITY_ERR'] = data.get(u'CONC_ERR',0)*corr_volume
                data[u'LC_ACTIVITY']  = data.get(u'LC',0)*corr_volume
                data[u'LD_ACTIVITY']  = data.get(u'LD',0)*corr_volume
            else:
                data[u'ACTIVITY']     = UNDEFINED
                data[u'ACTIVITY_ERR'] = UNDEFINED
                data[u'LC_ACTIVITY']  = UNDEFINED  
                data[u'LD_ACTIVITY']  = UNDEFINED
          
            # to avoid div by 0 check that quotient is not nul
            if data[u'ACTIVITY'] != UNDEFINED:
                data[u'ACTIVITY_ERR_PERC'] = (data.get(u'ACTIVITY_ERR',0)*100)/data.get(u'ACTIVITY')
          
            res.append(data)
            data = {}

        # add in dataBag
        self._dataBag[u'%s_XE_RESULTS'%(dataname)] = res
            
        result.close() 
    
    
    def _fetchCalibrationCoeffs(self,prefix):
        
        # get the sampleID 
        # extract id from dataname
        
        [pre,sid] = prefix.split('_') #IGNORE:W0612
    
        if sid is None:
            raise CTBTOError(-1,"Error when fetching Calibration Info. No sampleID found in dataBag for %s"%(prefix))
        
        calIDs_list = []
        
        # get energy calibration info
        result = self._mainConnector.execute(sqlrequests.SQL_SPALAX_GET_ENERGY_CAL%(sid))
        
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults != 1:
            raise CTBTOError(-1,"Expecting to have 1 energy calibration row for sample_id %s but got %d either None or more than one. %s"%(self._sampleID,nbResults,rows))
        
        # create a list of dicts
        data = {}

        data.update(rows[0].items())
        
        checksum = self._getCalibrationCheckSum([data[u'COEFF1'],data[u'COEFF2'],data[u'COEFF3'],data[u'COEFF4'],data[u'COEFF5'],data[u'COEFF6'],data[u'COEFF7'],data[u'COEFF8']])
        
        cal_id = 'EN-%s'%(checksum)
        
        # add in dataBag as EN-checksumif not already in the dataBag
        if cal_id not in self._dataBag:
            self._dataBag[cal_id] = data
        
        # prefix_ENERGY_CAL now refers to this calibration ID
        self._dataBag[u'%s_G_ENERGY_CAL'%(prefix)] = cal_id
        
        # add in list of calibration info for this particular sample
        calIDs_list.append(cal_id)
        
        # get resolution Calibration
        result = self._mainConnector.execute(sqlrequests.SQL_SPALAX_GET_RESOLUTION_CAL%(sid))
        
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults != 1:
            raise CTBTOError(-1,"Expecting to have 1 resolution calibration row for sample_id %s but got %d either None or more than one. %s"%(self._sampleID,nbResults,rows))
        
        # init list of dicts
        data = {}

        data.update(rows[0].items())
        
        checksum = self._getCalibrationCheckSum([data[u'COEFF1'],data[u'COEFF2'],data[u'COEFF3'],data[u'COEFF4'],data[u'COEFF5'],data[u'COEFF6'],data[u'COEFF7'],data[u'COEFF8']])
        
        cal_id = 'RE-%s'%(checksum)
        
        # add in dataBag as EN-checksumif not already in the dataBag
        if cal_id not in self._dataBag:
            self._dataBag[cal_id] = data
        
        # add in dataBag
        self._dataBag[u'%s_G_RESOLUTION_CAL'%(prefix)] = cal_id
        
        # add in list of calibration info for this particular sample
        calIDs_list.append(cal_id)
        
        result = self._mainConnector.execute(sqlrequests.SQL_SPALAX_GET_EFFICIENCY_CAL%(sid))
        
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults != 1:
            raise CTBTOError(-1,"Expecting to have 1 efficiency calibration row for sample_id %s but got %d either None or more than one. %s"%(self._sampleID,nbResults,rows))
        
        # create a list of dicts
        data = {}

        data.update(rows[0].items())
        
        checksum = self._getCalibrationCheckSum([data[u'COEFF1'],data[u'COEFF2'],data[u'COEFF3'],data[u'COEFF4'],data[u'COEFF5'],data[u'COEFF6'],data[u'COEFF7'],data[u'COEFF8']])
       
        cal_id = 'EF-%s'%(checksum)
        
        # add in dataBag as EN-checksumif not already in the dataBag
        if cal_id not in self._dataBag:
            self._dataBag[cal_id] = data
        
        # add in dataBag
        self._dataBag[u'%s_G_EFFICIENCY_CAL'%(prefix)] = cal_id
        
        # add in list of calibration info for this particular sample
        calIDs_list.append(cal_id)
        
        # add the list of calib_infos in the bag
        self._dataBag[u'%s_G_DATA_ALL_CALS' % (prefix)] = calIDs_list
        
        result.close()
        
    def _fetchCalibration(self):  
        """ Fetch the calibration info for all the different spectrums """
        
        for present in self._dataBag.get('CONTENT_PRESENT',[]):
            
            # treat preliminary samples differently
            if present == 'PREL':
                
                for prel in self._dataBag.get('CURR_List_OF_PRELS',[]):
                    
                    if prel is None:
                        raise CTBTOError(-1,"Error when fetching Calibration info for prefix %s, There is no CURRENT_%s in the dataBag\n"%(present,present))
                    
                    self._fetchCalibrationCoeffs(prel)
            else:    
            
                prefix = self._dataBag.get(u'CURRENT_%s'%(present),None)
                if prefix is None:
                    raise CTBTOError(-1,"Error when fetching Calibration info for prefix %s, There is no CURRENT_%s in the dataBag\n"%(present,present))
               
                self._fetchCalibrationCoeffs(prefix)
                        
        
              
        

class ParticulateDataFetcher(DBDataFetcher):
    """ Class for fetching particulate related data """
    
      # Class members
    c_log = logging.getLogger("datafetchers.ParticulateDataFetcher")
    #c_log.setLevel(logging.DEBUG)
    
    
    def __init__(self,aMainDbConnector=None,aArchiveDbConnector=None,aSampleID=None):
        
        super(ParticulateDataFetcher,self).__init__(aMainDbConnector,aArchiveDbConnector,aSampleID)
       
        self._dataBag['SAMPLE_TYPE']= 'PARTICULATE'
    
    def _fetchSpectrumData(self,aSampleID):
        """get the any spectrum data.
           If the caching function is activated save the retrieved specturm on disc.
           Try to find an extracted spectrum on OPS and Archive and if there is none of them look for the raw message (typeid)
        
            Args:
               aDataname: Name of the data. This will be used to create the name in the persistent hashtable and in the data spectrum filename
               
            Returns: (dataname,type)
                     where dataname = ID of the spectrum info in the data dict
                     where type     = type of the spectrum (SPHD, PREL, QC, BK)
        
            Raises:
               exception
        """
           
        ParticulateDataFetcher.c_log.info("Getting Spectrum for %s\n"%(aSampleID))
           
        # get sample info related to this sampleID
        # pass the gamma prefix
        (dataname,ty) = self._fetchGeneralSpectrumInfo(aSampleID,"_G")
        
        ParticulateDataFetcher.c_log.info("Its name will be %s and its type is %s"%(dataname,ty))
         
        (rows,nbResults,foundOnArchive) = self.execute(sqlrequests.SQL_GETPARTICULATE_SPECTRUM%(aSampleID,self._dataBag['STATION_CODE']),aTryOnArchive=True,aRaiseExceptionOnError=False)
        
        if nbResults == 0:
            ParticulateDataFetcher.c_log.warning("WARNING: sample_id %s has no extracted spectrum.Try to find a raw message.\n"%(aSampleID))
            arch_type = DBDataFetcher.c_fpdescription_type_translation.get(ty,"")
            (rows,nbResults,foundOnArchive) = self.execute(sqlrequests.SQL_GETPARTICULATE_RAW_SPECTRUM%(arch_type,aSampleID,self._dataBag['STATION_CODE']),aTryOnArchive=True,aRaiseExceptionOnError=True) 
        elif nbResults > 1:
            ParticulateDataFetcher.c_log.warning("WARNING: found more than one spectrum for sample_id %s\n"%(aSampleID))
        
        for row in rows:
            (anInput,ext) = self._readDataFile(foundOnArchive,row['DIR'], row['DFile'],row['PRODTYPE'],row['FOFF'],row['DSIZE'],aSampleID,dataname,ty)
           
            # check if it has to be compressed
            compressed = self._conf.getboolean("Options","compressSpectrum")
            sid = "%s_G_DATA"%(dataname)
                
            # check the message type and do the necessary.
            # here we expect a .msg or .s
            # we can also have .h coming from noble gaz histogram
            if ext == '.msg' or ext == '.archmsg':
              
                (data,limits)  =  self._extractSpectrumFromMessageFile(anInput) #IGNORE:W0612
              
                anInput.close()
              
                (data,channel_span,energy_span) = self._processSpectrum(data,compressed)
            # '.archs' given for an archived sample
            elif ext == '.s' or ext == '.archs':
            
                (data,limits) = self._extractSpectrumFromSpectrumFile(anInput)
             
                anInput.close()
           
                (data,channel_span,energy_span) = self._processSpectrum(data,compressed)
            else:
                raise CTBTOError(-1,"Error unknown extension %s. Do not know how to read the file %s for aSampleID %s"%(ext,row['DFile'],aSampleID))
         
            self._dataBag[u"%s_COMPRESSED"%(sid)]     = compressed
            self._dataBag[u"%s"%(sid)]                = data
            self._dataBag[u"%s_CHANNEL_SPAN"%(sid)]   = channel_span
            self._dataBag[u"%s_ENERGY_SPAN"%(sid)]    = energy_span
            # create a unique id for the extract data
            self._dataBag[u"%s_ID"%(sid)] = "%s-%s-%s"%(self._dataBag[u'STATION_CODE'],aSampleID,ty)
            self._dataBag[u"%s_TY"%(sid)]   = "%s-G"%(ty)
        
        return (dataname,ty)
        
        
    def _fetchBKSpectrumData(self):
        """get the Background spectrum.
           If the caching function is activated save the retrieved spectrum on disc.
        
            Args:
               params: None
               
            Returns:
               return Nothing
        
            Raises:
               exception
        """
        
        # precondition do nothing if there the curr sample is a Detector background itself
        prefix = self._dataBag.get(u'CURRENT_CURR',"")
        if self._dataBag.get(u"%s_DATA_DATA_TYPE"%(prefix),'') == 'D':
            return
        
        ParticulateDataFetcher.c_log.info("Getting Background Spectrum for %s\n"%(self._sampleID))
        
        # need to get the latest BK sample_id
        result = self._mainConnector.execute(sqlrequests.SQL_GETPARTICULATE_BK_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID']))
        
        # only one row in result set
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults == 0:
            ParticulateDataFetcher.c_log.warning("There is no Background for %s.\n request %s \n Database query result %s"%(self._sampleID,sqlrequests.SQL_GETPARTICULATE_BK_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID']),rows))
            self._dataBag[u'CONTENT_NOT_PRESENT'].add('BK')
            return
       
        if nbResults > 1:
            ParticulateDataFetcher.c_log.warning("There is more than one Background for %s. Take the first result.\n request %s \n Database query result %s"%(self._sampleID,sqlrequests.SQL_GETPARTICULATE_BK_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID']),rows))
           
        sid = rows[0]['SAMPLE_ID']
        
        DBDataFetcher.c_log.debug("sid = %s\n"%(sid))
        
        result.close()
        
        # now fetch the spectrum
        try:
            (dataname,ty) = self._fetchSpectrumData(sid) #IGNORE:W0612
           
            self._dataBag[u'CURRENT_BK'] = dataname
           
            self._dataBag[u'CONTENT_PRESENT'].add('BK') 
           
        except Exception, e: #IGNORE:W0703
            ParticulateDataFetcher.c_log.warning("Warning. No Data File found for background %s.Exception : %s\n"%(sid,e))
            self._dataBag[u'CONTENT_NOT_PRESENT'].add('BK')
            
    
    def _fetchQCSpectrumData(self):
        """get the QC spectrum.
           If the caching function is activated save the retrieved specturm on disc.
        
            Args:
               params: aDataname prefix in the dict
               
            Returns:
               return Nothing
        
            Raises:
               exception
        """  
        # precondition do nothing if there the curr sample is a Detector background itself
        prefix = self._dataBag.get(u'CURRENT_CURR',"")
        if self._dataBag.get(u"%s_DATA_DATA_TYPE"%(prefix),'') == 'Q':
            return
        
        ParticulateDataFetcher.c_log.info("Getting QC Spectrum of %s\n"%(self._sampleID))
        
        # need to get the latest BK sample_id
        (rows,nbResults,foundOnArchive) = self.execute(sqlrequests.SQL_GETPARTICULATE_QC_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'])) #IGNORE:W0612
        
        nbResults = len(rows)
        
        if nbResults == 0:
            ParticulateDataFetcher.c_log.warning("Warning. There is no QC for %s.\n request %s \n Database query result %s"%(self._sampleID,sqlrequests.SQL_GETPARTICULATE_QC_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID']),rows)) 
            # add in CONTENT_NOT_PRESENT this is used by the cache
            self._dataBag[u'CONTENT_NOT_PRESENT'].add('QC')
            return
       
        if nbResults > 1:
            ParticulateDataFetcher.c_log.warning("There is more than one QC for %s. Take the first result.\n request %s \n Database query result %s"%(self._sampleID,sqlrequests.SQL_GETPARTICULATE_QC_SAMPLEID%(self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID'],self._sampleID,self._dataBag[u'STATION_ID'],self._dataBag[u'DETECTOR_ID']),rows))
           
        sid = rows[0]['SAMPLE_ID']
        
        try:
            # now fetch the spectrum
            (dataname,ty) = self._fetchSpectrumData(sid) #IGNORE:W0612
        
            self._dataBag[u'CURRENT_QC'] = dataname
           
            self._dataBag[u'CONTENT_PRESENT'].add('QC') 
        
        except Exception, e: #IGNORE:W0703
            ParticulateDataFetcher.c_log.warning("Warning. No Data File found for QC %s. Exception: %s\n"%(sid,e))
            self._dataBag[u'CONTENT_NOT_PRESENT'].add('QC')
        
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
        
        # precondition do nothing if there the curr sample is a prel itself
        prefix = self._dataBag.get(u'CURRENT_CURR',"")
        if self._dataBag.get(u"%s_DATA_DATA_TYPE"%(prefix),'') == 'S' and self._dataBag.get(u"%s_DATA_SPECTRAL_QUALIFIER"%(prefix),'') == 'PREL':
            return
    
        ParticulateDataFetcher.c_log.info("Getting Prels Spectrum for %s\n"%(self._sampleID))
        
        # need to get the latest BK sample_id
        result = self._mainConnector.execute(sqlrequests.SQL_GETPARTICULATE_PREL_SAMPLEIDS%(self._sampleID,self._dataBag[u'DETECTOR_ID']))
        
        # only one row in result set
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults == 0:
            ParticulateDataFetcher.c_log.warning("There is no PREL spectrum for %s."%(self._sampleID))
            self._dataBag[u'CONTENT_NOT_PRESENT'].add('PREL')
            return
        
        listOfPrel = []
          
        for row in rows:
            sid = row['SAMPLE_ID']
             
            # now fetch the spectrum with the a PREL_cpt id
            (dataname,ty) = self._fetchSpectrumData(sid) #IGNORE:W0612
            # update list of prels
            listOfPrel.append(dataname)
        
        self._dataBag['CURR_List_OF_PRELS']  =  listOfPrel
        self._dataBag[u'CONTENT_PRESENT'].add('PREL') 
           
        
        result.close()
    
    
    def _fetchCURRSpectrumData(self):
        """ fetch the current spectrum identified by the current sampleID
        
            Args:
               params: aDataname
               
            Returns:
               return Nothing
        
            Raises:
               exception
        """
        
        (dataname,ty) = self._fetchSpectrumData(self._sampleID) #IGNORE:W0612
        
        self._dataBag[u'CURRENT_CURR'] = dataname
        
        if'CURR' not in self._dataBag[u'CONTENT_PRESENT']:
            self._dataBag[u'CONTENT_PRESENT'].add('CURR') 
    
    def _fetchData(self,aParams=""):
        """ get the different raw data info """
        
        spectrums = self._parser.parse(aParams,RequestParser.PAR).get(RequestParser.SPECTRUM,set())
        
        if ('None' in spectrums):
            # None is in there so do not include data
            return
        
        #fetch current spectrum
        if ('CURR' in spectrums):
            self._fetchCURRSpectrumData()
        
        if ('QC' in spectrums):
            self._fetchQCSpectrumData()
        
        if ('BK' in spectrums):
            self._fetchBKSpectrumData()
        
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
       
    def _fetchCategoryResults(self,sid,dataname):
        
        """sub method of _fetchAnalysisResults. Get the Category info from the database.
           First get the category status which is the global category defined for a particular sampleID.
           Then get the details for all nuclides
        
            Args:
               params: sid: Look for an analysis for the following sid
                       dataname: prefix of the analysis
               
            Returns:
               return Nothing
        
            Raises:
               exception CTBTOError if any issue
        """
            
        # get category status
        result = self._mainConnector.execute(sqlrequests.SQL_PARTICULATE_CATEGORY_STATUS%(sid))
       
        # do something only if there is some information
        
        rows = result.fetchall()
        
        if len(rows) > 0:
        
            data = {}
            data.update(rows[0])
    
            self._dataBag[u'%s_CAT_INFOS'%(dataname)] = self._transformResults(data)
          
            result = self._mainConnector.execute(sqlrequests.SQL_PARTICULATE_CATEGORY%(sid))
       
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
            self._dataBag[u'%s_CATEGORIES'%(dataname)] = res
        
        result.close()
        
    def _fetchPeaksResults(self,sid,dataname):
        """ Get info regarding the found peaks """
        
        # get peaks
        result = self._mainConnector.execute(sqlrequests.SQL_PARTICULATE_GET_PEAKS%(sid))
        
        rows = result.fetchall()
        
        if len(rows) > 0:
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
            self._dataBag[u'%s_PEAKS'%(dataname)] = res
        
        result.close()
        
    def _fetchNuclideLines(self,sid,dataname):
        """Get all info regarding the Nuclide Lines for a particualr sample .
         
        """
         
        # get the data from the DB
        result = self._mainConnector.execute(sqlrequests.SQL_PARTICULATE_GET_NUCLIDE_LINES_INFO%(sid))

        rows = result.fetchall()
        
        if len(rows) > 0:
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
            self._dataBag[u'%s_IDED_NUCLIDE_LINES'%(dataname)] = res
        
        result.close()
    
    def _fetchNuclidesToQuantify(self):
        
        # return all nucl2quantify this is kind of static table
        result = self._mainConnector.execute(sqlrequests.SQL_PARTICULATE_GET_NUCL2QUANTIFY)
        
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
        
    def _fetchNuclidesResults(self,sid,dataname):
        """ Get all info regarding the nuclides related to this sample """
         # get non quantified nuclides
        
        # to distinguish quantified and non quantified nuclide there is a table called GARDS_NUCL2QUANTIFY => static table of the nucl to treat
        result = self._mainConnector.execute(sqlrequests.SQL_PARTICULATE_GET_NUCLIDES_INFO%(sid))
        
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
                val = DBDataFetcher.c_nid_translation.get(nidflag,nidflag)
                data[u'NID_FLAG']     = val
                data[u'NID_FLAG_NUM'] = nidflag
            
            res.append(data)
            data = {}

        # add in dataBag
        self._dataBag[u'%s_IDED_NUCLIDES'%(dataname)] = res
        
        result.close()
        
        
        
    
    def _fetchAnalysisResults(self,aParams=None):
        """ get the  sample categorization, activityConcentrationSummary, peaks results, parameters, flags"""
           
        # get static info necessary for the analysis
        self._fetchNuclidesToQuantify()
        
        analyses = self._parser.parse(aParams,RequestParser.PAR).get(RequestParser.ANALYSIS,set())
       
        if ('None' in analyses):
            # None is in there so do not include data
            return
        
        for analysis in analyses:
        
            # for the moment ignore Analysis for PREL
            if analysis == 'PREL' :
                continue
        
            # check if there is some data regarding this type of analysis
            # get the dataname of the current spectrum (it is the main spectrum)
            dataname = self._dataBag.get('CURRENT_%s'%(analysis),None)
          
            if dataname is not None:
                ParticulateDataFetcher.c_log.info("Getting Analysis Results for CURRENT_%s\n"%(analysis))
          
                # extract id from dataname
                [pre,sid] = dataname.split('_') #IGNORE:W0612
          
                self._fetchCategoryResults(sid,dataname)
        
                self._fetchNuclidesResults(sid,dataname)
        
                self._fetchNuclideLines(sid,dataname)
        
                self._fetchPeaksResults(sid,dataname)
          
                self._fetchFlags(sid,dataname)
        
                self._fetchParameters(sid,dataname)
        
        
    def _getMRP(self,aDataname):
        """ get the most recent prior """
        
        data_type    = self._dataBag["%s_DATA_DATA_TYPE"%(aDataname)]
        
        detector_id  = self._dataBag['DETECTOR_ID']
        
        sample_type  = self._dataBag['SAMPLE_TYPE']
        
        collect_stop = self._dataBag["%s_DATA_COLLECT_STOP"%(aDataname)].replace("T"," ")
        
        ParticulateDataFetcher.c_log.debug("Executed request %s\n"%(sqlrequests.SQL_PARTICULATE_GET_MRP%(collect_stop,collect_stop,data_type,detector_id,sample_type)))
    
        # get MDA nuclides
        result = self._mainConnector.execute(sqlrequests.SQL_PARTICULATE_GET_MRP%(collect_stop,collect_stop,data_type,detector_id,sample_type))
        
        rows = result.fetchall()
        
        if len(rows) > 0:
            
            row = rows[0]
             
            mrp_sid   = row['mrp_sample_id']
            hoursDiff = row['mrp_collect_stop_diff']*24 
            
            self._dataBag[u'TIME_FLAGS_PREVIOUS_SAMPLE']  = True 
            self._dataBag[u'TIME_FLAGS_MRP_SAMPLE_ID']    = mrp_sid
            self._dataBag[u'TIME_FLAGS_MRP_HOURS_DIFF']   = hoursDiff
            
            ParticulateDataFetcher.c_log.info("There is a mrp and it is %d\n"%(mrp_sid))
            
        else:
            
            ParticulateDataFetcher.c_log.info("No MRP found\n")
            self._dataBag[u'TIME_FLAGS_PREVIOUS_SAMPLE']  = False 
        
        
    def _fetchFlags(self,sid,aDataname):
        """ get the different flags """
        
        self._fetchTimelinessFlags(sid,aDataname)
        
        self._fetchdataQualityFlags(sid,aDataname)
        
    
    def _fetchdataQualityFlags(self,sid,dataname):
        """ data quality flags"""
        
         # get MDA nuclides
        result = self._mainConnector.execute(sqlrequests.SQL_PARTICULATE_GET_DATA_QUALITY_FLAGS%(sid))
        
        rows = result.fetchall()
        
        if len(rows):
            data = {}
        
            res = []
        
            for row in rows:
                # copy row in a normal dict
                data.update(row)
            
                res.append(data)
                data = {}
               
            # add in dataBag
            self._dataBag[u'%s_DATA_QUALITY_FLAGS'%(dataname)] = res
        
    def _fetchTimelinessFlags(self,sid,aDataname):
        """ prepare timeliness checking info """
        
        # precondition check that there is COLLECT_START 
        # otherwise quit
        if (self._dataBag.get("%s_DATA_COLLECT_START"%(aDataname),None) is None) or (self._dataBag.get("%s_DATA_COLLECT_STOP"%(aDataname),None) is None):
            ParticulateDataFetcher.c_log.warning("Warnings. Cannot compute the timeliness flags missing information for %s\n"%(sid))
            return
       
        # get the timeliness flag
         
        self._getMRP(aDataname)
        
        # check collection flag
        
        # check that collection time with 24 Hours
        collect_start  = ctbto.common.time_utils.getDateTimeFromISO8601(self._dataBag["%s_DATA_COLLECT_START"%(aDataname)])
        collect_stop   = ctbto.common.time_utils.getDateTimeFromISO8601(self._dataBag["%s_DATA_COLLECT_STOP"%(aDataname)])
    
        diff_in_sec = ctbto.common.time_utils.getDifferenceInTime(collect_start, collect_stop)
        
        # check time collection within 24 hours +/- 10 % => 3hrs
        # between 21.6 and 26.4
        # if 0 within 24 hours
        if diff_in_sec > 95040 or diff_in_sec < 77760:
            self._dataBag[u'%s_TIME_FLAGS_COLLECTION_WITHIN_24'%(aDataname)] = diff_in_sec
        else:
            self._dataBag[u'%s_TIME_FLAGS_COLLECTION_WITHIN_24'%(aDataname)] = 0 
        
        
        # check acquisition flag
        # need to be done within 3 hours
        
        # check that collection time with 24 Hours
        acq_start  = ctbto.common.time_utils.getDateTimeFromISO8601(self._dataBag["%s_DATA_ACQ_START"%(aDataname)])
        acq_stop   = ctbto.common.time_utils.getDateTimeFromISO8601(self._dataBag["%s_DATA_ACQ_STOP"%(aDataname)])
    
        diff_in_sec = ctbto.common.time_utils.getDifferenceInTime(acq_start, acq_stop)
          
        # acquisition diff with 3 hours
        if diff_in_sec < (20*60*60):
            self._dataBag[u'%s_TIME_FLAGS_ACQUISITION_FLAG'%(aDataname)] = diff_in_sec
        else:
            self._dataBag[u'%s_TIME_FLAGS_ACQUISITION_FLAG'%(aDataname)] = 0 
        
        # check decay flag
        # decay time = ['DATA_ACQ_STOP'] - ['DATA_COLLECT_STOP']
        
        # check that collection time with 24 Hours
        decay_time_in_sec   = ctbto.common.time_utils.getDifferenceInTime(collect_stop,acq_start)
        
        if (decay_time_in_sec > 24*60*60):
            self._dataBag[u'%s_TIME_FLAGS_DECAY_FLAG'%(aDataname)] = decay_time_in_sec
        else:
            self._dataBag[u'%s_TIME_FLAGS_DECAY_FLAG'%(aDataname)] = 0
            
        #  check sample_arrival_delay
        
        # get cat info dict
        cat_info = self._dataBag['%s_CAT_INFOS'%(aDataname)]
        
        entry_date_time      = ctbto.common.time_utils.getDateTimeFromISO8601(cat_info['CAT_ENTRY_DATE'])
        sample_arrival_delay = ctbto.common.time_utils.getDifferenceInTime(entry_date_time,collect_start)
        
        # check that sample_arrival_delay is within 72 hours or 72*60*60 seconds
        if sample_arrival_delay > (72*60*60):
            self._dataBag[u'%s_TIME_FLAGS_SAMPLE_ARRIVAL_FLAG'%(aDataname)] = entry_date_time
        else:
            self._dataBag[u'%s_TIME_FLAGS_SAMPLE_ARRIVAL_FLAG'%(aDataname)] = 0 
           
        
    def _fetchParameters(self,sid,dataname):
        """ get the different parameters used for the analysis """
        
        ParticulateDataFetcher.c_log.info("Getting Analysis parameters for %s\n"%(sid))
         
        result = self._mainConnector.execute(sqlrequests.SQL_PARTICULATE_GET_PROCESSING_PARAMETERS%(self._sampleID))
        
        rows = result.fetchall()
        
        nbResults = len(rows)
        
        # do nothing if no results
        if nbResults >0:
            # do some sanity checkings
            if nbResults != 1:
                ParticulateDataFetcher.c_log.warning("sample_id %s is a %s sample and no processing parameters has been found\n"%(self._sampleID,self._dataBag.get(u"%s_DATA_SPECTRAL_QUALIFIER"%(dataname),"(undefined)")))
         
            # create a list of dicts
            data = {}
        
            data.update((rows[0].items()) if len(rows) > 0 else {})
    
            # add in dataBag
            self._dataBag[u'%s_PROCESSING_PARAMETERS'%(dataname)] = data
        
            result.close()  
        
            result = self._mainConnector.execute(sqlrequests.SQL_PARTICULATE_GET_UPDATE_PARAMETERS%(sid))
        
            rows = result.fetchall()
        
            nbResults = len(rows)
            
            # do nothing if no results
            if nbResults >0:
                # do some sanity checkings
                if nbResults != 1:
                    ParticulateDataFetcher.c_log.warning("%s sample and no update parameters found\n"%(self._dataBag[u"%s_DATA_SPECTRAL_QUALIFIER"%(dataname)]))
            
         
                # create a list of dicts
                data = {}

                data.update((rows[0].items()) if len(rows) > 0 else {})
        
                # add in dataBag
                self._dataBag[u'%s_UPDATE_PARAMETERS'%(dataname)] = data
        
    def _fetchCalibrationCoeffs(self,prefix):
        
        # get the sampleID 
        # extract id from dataname
        
        [pre,sid] = prefix.split('_') #IGNORE:W0612
    
        if sid is None:
            raise CTBTOError(-1,"Error when fetching Calibration Info. No sampleID found in dataBag for %s"%(prefix))
        
        calIDs_list = []
        
        # get energy calibration info
        result = self._mainConnector.execute(sqlrequests.SQL_PARTICULATE_GET_ENERGY_CAL%(sid))
        
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults != 1:
            raise CTBTOError(-1,"Expecting to have 1 energy calibration row for sample_id %s but got %d either None or more than one. %s"%(self._sampleID,nbResults,rows))
        
        # create a list of dicts
        data = {}

        data.update(rows[0].items())
        
        checksum = self._getCalibrationCheckSum([data[u'COEFF1'],data[u'COEFF2'],data[u'COEFF3'],data[u'COEFF4'],data[u'COEFF5'],data[u'COEFF6'],data[u'COEFF7'],data[u'COEFF8']])
        
        cal_id = 'EN-%s'%(checksum)
        
        # add in dataBag as EN-checksumif not already in the dataBag
        if cal_id not in self._dataBag:
            self._dataBag[cal_id] = data
        
        # prefix_ENERGY_CAL now refers to this calibration ID
        self._dataBag[u'%s_G_ENERGY_CAL'%(prefix)] = cal_id
        
        # add in list of calibration info for this particular sample
        calIDs_list.append(cal_id)
        
        # get resolution Calibration
        result = self._mainConnector.execute(sqlrequests.SQL_PARTICULATE_GET_RESOLUTION_CAL%(sid))
        
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults != 1:
            raise CTBTOError(-1,"Expecting to have 1 resolution calibration row for sample_id %s but got %d either None or more than one. %s"%(self._sampleID,nbResults,rows))
        
        # init list of dicts
        data = {}

        data.update(rows[0].items())
        
        checksum = self._getCalibrationCheckSum([data[u'COEFF1'],data[u'COEFF2'],data[u'COEFF3'],data[u'COEFF4'],data[u'COEFF5'],data[u'COEFF6'],data[u'COEFF7'],data[u'COEFF8']])
        
        cal_id = 'RE-%s'%(checksum)
        
        # add in dataBag as EN-checksumif not already in the dataBag
        if cal_id not in self._dataBag:
            self._dataBag[cal_id] = data
        
        # add in dataBag
        self._dataBag[u'%s_G_RESOLUTION_CAL'%(prefix)] = cal_id
        
        # add in list of calibration info for this particular sample
        calIDs_list.append(cal_id)
        
        result = self._mainConnector.execute(sqlrequests.SQL_PARTICULATE_GET_EFFICIENCY_CAL%(sid))
        
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults != 1:
            raise CTBTOError(-1,"Expecting to have 1 efficiency calibration row for sample_id %s but got %d either None or more than one. %s"%(self._sampleID,nbResults,rows))
        
        # create a list of dicts
        data = {}

        data.update(rows[0].items())
        
        checksum = self._getCalibrationCheckSum([data[u'COEFF1'],data[u'COEFF2'],data[u'COEFF3'],data[u'COEFF4'],data[u'COEFF5'],data[u'COEFF6'],data[u'COEFF7'],data[u'COEFF8']])
       
        cal_id = 'EF-%s'%(checksum)
        
        # add in dataBag as EN-checksumif not already in the dataBag
        if cal_id not in self._dataBag:
            self._dataBag[cal_id] = data
        
        # add in dataBag
        self._dataBag[u'%s_G_EFFICIENCY_CAL'%(prefix)] = cal_id
        
        # add in list of calibration info for this particular sample
        calIDs_list.append(cal_id)
        
        # add the list of calib_infos in the bag
        self._dataBag[u'%s_G_DATA_ALL_CALS'%(prefix)] = calIDs_list
        
        result.close()
        
    def _fetchCalibration(self):  
        """ Fetch the calibration info for all the different spectrums """
        
        for present in self._dataBag.get('CONTENT_PRESENT',[]):
            
            # treat preliminary samples differently
            if present == 'PREL':
                
                for prel in self._dataBag.get('CURR_List_OF_PRELS',[]):
                    
                    if prel is None:
                        raise CTBTOError(-1,"Error when fetching Calibration info for prefix %s, There is no CURRENT_%s in the dataBag\n"%(present,present))
                    
                    self._fetchCalibrationCoeffs(prel)
            else:    
            
                prefix = self._dataBag.get(u'CURRENT_%s'%(present),None)
                if prefix is None:
                    raise CTBTOError(-1,"Error when fetching Calibration info for prefix %s, There is no CURRENT_%s in the dataBag\n"%(present,present))
               
                self._fetchCalibrationCoeffs(prefix)
                        
        
                   





""" Dictionary used to map DB Sample type with the right fetcher """ #IGNORE:W0105
SAMPLE_TYPE = {'SAUNA':SaunaNobleGasDataFetcher, 'ARIX-4':SaunaNobleGasDataFetcher, 'SPALAX':SpalaxNobleGasDataFetcher, 'RASA':ParticulateDataFetcher,'CINDER':ParticulateDataFetcher, 'LAB':ParticulateDataFetcher, None:ParticulateDataFetcher,'Gas':None}
        