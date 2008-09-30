import logging
import sqlalchemy
import new
import os
import re
import pprint
import string
import datetime
import time
from StringIO import StringIO

from common.exceptions import CTBTOError
import common.utils
import common.time_utils

""" sql requests """
SQL_GETDETECTORINFO   = "select det.detector_code as detector_code, det.description as detector_description, det.type as detector_type from RMSMAN.GARDS_DETECTORS det, RMSMAN.GARDS_SAMPLE_DATA data where data.sample_id=%s and data.DETECTOR_ID=det.DETECTOR_ID"
SQL_GETSTATIONINFO    = "select sta.station_code as station_code, sta.country_code as station_country_code, sta.type as station_type, sta.description as station_location,to_char(sta.lat)||' '||to_char(sta.lon)||' '||to_char(sta.elevation) as station_coordinates from RMSMAN.GARDS_STATIONS sta, RMSMAN.GARDS_SAMPLE_DATA data where data.sample_id=%s and sta.STATION_ID=data.STATION_ID"
SQL_GETSAMPLETYPE     = "select sta.type as sample_type from RMSMAN.GARDS_STATIONS sta, RMSMAN.GARDS_SAMPLE_DATA data where data.sample_id=%s and sta.STATION_ID=data.STATION_ID"


SQL_GETSAMPLEINFO     = "select sample_id as sample_id, input_file_name as spectrum_filepath, data_type as data_data_type, geometry as sample_geometry, \
                                detector_id as detector_id, spectral_qualifier as data_spectral_qualifier, quantity as sample_quantity, transmit_dtg as data_transmit_dtg , \
                                collect_start as data_collect_start, collect_stop as data_collect_stop, acquisition_start as data_acq_start, \
                                acquisition_stop as data_acq_stop, acquisition_live_sec as data_acq_live_sec, acquisition_real_sec as data_acq_real_sec \
                                from RMSMAN.GARDS_SAMPLE_DATA where sample_id=%s"
                                
""" get SAUNA Sample files : beta and gamma spectrum plus histogram. parameters station and sampleid """
SQL_GETSAUNA_FILES    = "select prod.dir, prod.DFIle,fp.prodtype from idcx.FILEPRODUCT prod,idcx.FPDESCRIPTIoN fp where (fp.typeid=30 or fp.typeid=29 or fp.typeid=34) and prod.chan='%s' and prod.typeID= fp.typeID and sta='%s'"

SQL_GETPARTICULATE_SPECTRUM    = "select prod.dir, prod.DFIle,fp.prodtype from FILEPRODUCT prod,FPDESCRIPTIoN fp where fp.typeid=29 and prod.chan='%s' and prod.typeID= fp.typeID and sta='%s'"

""" Get information regarding all identified nuclides """
SQL_SAUNA_GETIDENTIFIEDNUCLIDES = "select conc.conc as conc, conc.conc_err as conc_err, conc.MDC as MDC, conc.LC as LC, conc.LD as LD, lib.NAME as Nuclide, lib.HALFLIFE as halflife from RMSMAN.GARDS_BG_ISOTOPE_CONCS conc, RMSMAN.GARDS_XE_NUCL_LIB lib where sample_id=%s and conc.NUCLIDE_ID=lib.NUCLIDE_ID and conc.NID_FLAG=1"

""" Get information regarding all nuclides """
SQL_SAUNA_GETALLNUCLIDES = "select conc.conc as conc, conc.conc_err as conc_err, conc.MDC as MDC, conc.LC as LC, conc.LD as LD, lib.NAME as Nuclide, lib.HALFLIFE as halflife from RMSMAN.GARDS_BG_ISOTOPE_CONCS conc, RMSMAN.GARDS_XE_NUCL_LIB lib where sample_id=%s and conc.NUCLIDE_ID=lib.NUCLIDE_ID"

""" get particulate category """
SQL_PARTICULATE_CATEGORY_STATUS ="select entry_date as cat_entry_date, cnf_begin_date as cat_cnf_begin_date,cnf_end_date as cat_cnf_end_date, review_date as cat_review_date, review_time as cat_review_time, analyst as cat_analyst, status as cat_status, category as cat_category, auto_category as cat_auto_category, release_date as cat_release_date from RMSMAN.GARDS_SAMPLE_STATUS where sample_id=%s"

SQL_PARTICULATE_CATEGORY ="select NAME as CAT_NUCL_NAME, METHOD_ID as CAT_METHOD_ID, CATEGORY as CAT_CATEGORY, UPPER_BOUND as CAT_UPPER_BOUND, LOWER_BOUND as CAT_LOWER_BOUND, CENTRAL_VALUE as CAT_CENTRAL_VALUE, DELTA as CAT_DELTA, ACTIVITY as CAT_ACTIVITY from RMSMAN.GARDS_SAMPLE_CAT where sample_id=%s and hold=0"

""" returned all ided nuclides for a particular sample """
SQL_PARTICULATE_GET_NUCL2QUANTIFY="select name from RMSMAN.GARDS_NUCL2QUANTIFY"

SQL_PARTICULATE_GET_NUCLIDES_INFO="select * from RMSMAN.GARDS_NUCL_IDED ided where sample_id=%s"

SQL_PARTICULATE_GET_NONQUANTIFIED_NUCLIDES = "select * from RMSMAN.GARDS_NUCL_IDED ided where sample_id=%s and name not in (select name from RMSMAN.GARDS_NUCL2QUANTIFY)"

SQL_PARTICULATE_GET_QUANTIFIED_NUCLIDES = "select * from RMSMAN.GARDS_NUCL_IDED ided where sample_id=%s and name in (select name from RMSMAN.GARDS_NUCL2QUANTIFY)"

SQL_PARTICULATE_GET_MDA_NUCLIDES = "select * from RMSMAN.GARDS_NUCL_IDED ided where sample_id=%s and report_mda=1"

SQL_PARTICULATE_GET_PEAKS = "select * from RMSMAN.GARDS_PEAKS where sample_id=%s"

SQL_PARTICULATE_GET_PROCESSING_PARAMETERS = "select * from RMSMAN.GARDS_SAMPLE_PROC_PARAMS where sample_id=%s"

SQL_PARTICULATE_GET_UPDATE_PARAMETERS = "select * from RMSMAN.GARDS_SAMPLE_UPDATE_PARAMS where sample_id=%s"

SQL_PARTICULATE_GET_MRP = "select gsd.sample_id as mrp_sample_id, to_char (gsd.collect_stop, 'YYYY-MM-DD HH24:MI:SS')  as mrp_collect_stop, gsd.collect_stop - to_date('%s', 'YYYY-MM-DD HH24:MI:SS') as mrp_collect_stop_diff from gards_sample_data gsd \
                           where gsd.collect_stop < to_date ('%s','YYYY-MM-DD HH24:MI:SS') \
                             and gsd.data_type = '%s' \
                             and gsd.detector_id = %s \
                             and gsd.sample_type = '%s' \
                             and gsd.spectral_qualifier = 'FULL' \
                           order by collect_stop desc"

SQL_PARTICULATE_GET_DATA_QUALITY_FLAGS = "select gflags.flag_id as dq_flag_id, result as dq_result, value as dq_value, name as dq_name, threshold as dq_threshold, units as dq_units, test as dq_test from RMSMAN.GARDS_SAMPLE_FLAGS sflags,RMSMAN.GARDS_FLAGS gflags where sample_id=%s and sflags.FLAG_ID = gflags.FLAG_ID"

SQL_PARTICULATE_GET_ENERGY_CAL         = "select * from RMSMAN.GARDS_ENERGY_CAL where sample_id=%s"

SQL_PARTICULATE_GET_RESOLUTION_CAL     = "select * from RMSMAN.GARDS_RESOLUTION_CAL where sample_id=%s"

SQL_PARTICULATE_GET_EFFICIENCY_CAL     = "select * from RMSMAN.GARDS_EFFICIENCY_CAL where sample_id=%s"

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
       
       inst.__dict__.update({'_sampleID':aSampleID,'_connector':aDbConnector,'_dataBag':{u'SAMPLE_TYPE':type}}) 
    
       result.close()
       
       return inst
       
    #class method binding
    getDataFetcher = classmethod(getDataFetcher)
    
     
    def __init__(self,aDbConnector=None,aSampleID=None):
        
        self._connector = aDbConnector
        self._sampleID  = aSampleID
        # dict containing all the data retrieved from the filesystems and DB
        self._dataBag   = {}
    
    def getConnector(self):
        return self._connector
    
    def getSampleID(self):
        return self._sampleID
    
    def fetch(self):
        """ abstract global data fetching method """
        raise CTBTOError(-1,"method not implemented in Base Class. To be defined in children")
    
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
       
    def fetch(self):
        
        # get station info
        self._fetchStationInfo()
        
        # get station info
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
        
    def _readDataFile(self,aDir,aFilename,aType):
        """ read a file in a string buffer. This is used for the data files """
        
        # check that the file exists
        path = "%s/%s"%(aDir,aFilename)
        
        if not os.path.exists(path):
            raise CTBTOError(-1,"the file %s does not exits"%(path))
        
        # store in a StringIO object
        input = open(path,"r")
        
        tok_list = []
        
        energy_span  = 0
        channel_span = 0
        e_max        = 0
        
        data = StringIO()
        try:
           for line in input:
              # we might also have to add more splitting character
              # get of first column which should always be the last columns (channel span)
              # get also max of value of other columns (energy span)
              l = map(string.atoi,line.split())
              
              if l[0] > channel_span:
                 channel_span = l[0]
                 
              e_max = max(l[1:]) 
              
              if energy_span < e_max:
                  energy_span = e_max
              
              # add 16 spaces char for formatting purposes
              data.write("                %s"%(line))
        finally:    
           input.close()
           
        print "channel_span %s"%(channel_span)
        print "energy_span %s"%(energy_span)
         
        self._dataBag["rawdata_%s_channel_span"%(aType)] = channel_span
        self._dataBag["rawdata_%s_energy_span"%(aType)]  = energy_span
        self._dataBag["rawdata_%s"%(aType)] = data.getvalue()
        
    def get(self,aKey,aDefault=None):
        """ return one of the fetched elements """
        
        #print "data Bag %s"%(self._dataBag)
        
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
        
        print "Get Particulate spectrum %s"%(SQL_GETPARTICULATE_SPECTRUM%(self._sampleID,self._dataBag['STATION_CODE']))
        
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
        
        resutl.close()
        
        # return all nucl2quantify this is kind of static table
        result = self._connector.execute(SQL_PARTICULATE_GET_NUCL2QUANTIFY%(self._sampleID))
        
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
        
        self._fetchPeaksResults()
        
        self._fetchFlags()
        
    def _getMRP(self):
        """ get the most recent prior """
        
        collect_stop = self._dataBag['DATA_COLLECT_STOP'].replace("T"," ")
        
        data_type    = self._dataBag['DATA_DATA_TYPE']
        
        detector_id  = self._dataBag['DETECTOR_ID']
        
        sample_type  = self._dataBag['SAMPLE_TYPE']
    
        # get MDA nuclides
        result = self._connector.execute(SQL_PARTICULATE_GET_MRP%(collect_stop,collect_stop,data_type,detector_id,sample_type))
        
        rows = result.fetchall()
        
        if len(rows) > 0:
            
            row = rows[0]
            
            mrp_sid   = row['mrp_sample_id']
            hoursDiff = row['mrp_collect_stop_diff']*24 
            
            self._dataBag[u'TIME_FLAGS_PREVIOUS_SAMPLE']  = True 
            self._dataBag[u'TIME_FLAGS_MRP_SAMPLE_ID']    = mrp_sid
            self._dataBag[u'TIME_FLAGS_MRP_HOURS_DIFF']   = hoursDiff
             
        else:
            
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
        result = self._connector.execute(SQL_PARTICULATE_GET_PROCESSING_PARAMETERS%(self._sampleID))
        
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults is not 1:
            raise CTBTOError(-1,"Expecting to have 1 set of processing parameters but got %d either None or more than one. %s"%(nbResults,rows))
         
        # create a list of dicts
        data = {}

        data.update(rows[0].items())
    
        # add in dataBag
        self._dataBag[u'PROCESSING_PARAMETERS'] = data
        
        result.close()  
        
        result = self._connector.execute(SQL_PARTICULATE_GET_UPDATE_PARAMETERS%(self._sampleID))
        
        rows = result.fetchall()
        
        nbResults = len(rows)
       
        if nbResults is not 1:
            raise CTBTOError(-1,"Expecting to have 1 set of processing parameters but got %d either None or more than one. %s"%(nbResults,rows))
         
        # create a list of dicts
        data = {}

        data.update(rows[0].items())
        
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
        