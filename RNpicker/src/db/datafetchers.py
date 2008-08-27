import logging
import sqlalchemy
import new
import os
from StringIO import StringIO

from common.exceptions import CTBTOError


""" sql requests """
SQL_GETDETECTORINFO   = "select det.detector_code as detector_code, det.description as detector_description, det.type as detector_type from RMSMAN.GARDS_DETECTORS det, RMSMAN.GARDS_SAMPLE_DATA data where data.sample_id=%s and data.DETECTOR_ID=det.DETECTOR_ID"
SQL_GETSTATIONINFO    = "select sta.station_code as station_code, sta.country_code as station_country_code, sta.type as station_type, sta.description as station_description,sta.lat as station_lat, sta.lon as station_lon, sta.elevation as station_elevation from RMSMAN.GARDS_STATIONS sta, RMSMAN.GARDS_SAMPLE_DATA data where data.sample_id=%s and sta.STATION_ID=data.STATION_ID"
SQL_GETSAMPLETYPE     = "select sta.type from RMSMAN.GARDS_STATIONS sta, RMSMAN.GARDS_SAMPLE_DATA data where data.sample_id=%s and sta.STATION_ID=data.STATION_ID"
SQL_GETSAMPLEINFO     = "select sample_id as data_sample_id, input_file_name as spectrum_filepath, data_type as data_data_type, geometry as data_geometry, \
                                spectral_qualifier as data_spectral_qualifier, quantity as data_quantity, transmit_dtg as data_transmit_dtg , \
                                collect_start as data_collect_start, collect_stop as data_collect_stop, acquisition_start as data_acq_start, \
                                acquisition_stop as data_acq_stop, acquisition_live_sec as data_acq_live_sec, acquisition_real_sec as acq_real_sec \
                                from RMSMAN.GARDS_SAMPLE_DATA where sample_id=%s"
                                
""" get SAUNA Sample files : beta and gamma spectrum plus histogram. parameters station and sampleid """
SQL_GETSAUNA_FILES    = "select prod.dir, prod.DFIle,fp.prodtype from idcx.FILEPRODUCT prod,idcx.FPDESCRIPTIoN fp where (fp.typeid=30 or fp.typeid=29 or fp.typeid=34) and prod.chan='%s' and prod.typeID= fp.typeID and sta='%s'"

""" Get information regarding all identified nuclides """
SQL_SAUNA_GETIDENTIFIEDNUCLIDES = "select conc.conc as conc, conc.conc_err as conc_err, conc.MDC as MDC, conc.LC as LC, conc.LD as LD, lib.NAME as Nuclide, lib.HALFLIFE as halflife from RMSMAN.GARDS_BG_ISOTOPE_CONCS conc, RMSMAN.GARDS_XE_NUCL_LIB lib where sample_id=%s and conc.NUCLIDE_ID=lib.NUCLIDE_ID and conc.NID_FLAG=1"

""" Get information regarding all nuclides """
SQL_SAUNA_GETALLNUCLIDES = "select conc.conc as conc, conc.conc_err as conc_err, conc.MDC as MDC, conc.LC as LC, conc.LD as LD, lib.NAME as Nuclide, lib.HALFLIFE as halflife from RMSMAN.GARDS_BG_ISOTOPE_CONCS conc, RMSMAN.GARDS_XE_NUCL_LIB lib where sample_id=%s and conc.NUCLIDE_ID=lib.NUCLIDE_ID"

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
        
       print "Type = %s"%(rows[0]['TYPE'])
       
       print "Klass = %s"%(SAMPLE_TYPE[rows[0]['TYPE']])
       
       
       # create object and update its internal dictionary
       inst = object.__new__(SAMPLE_TYPE[rows[0]['TYPE']])
       inst.__dict__.update({'_sampleID':aSampleID,'_connector':aDbConnector,'_dataBag':{}}) 
       
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
       
       print "dataBag= %s"%(self._dataBag)
       
       result.close()
       
    def _fetchSampleInfo(self):
       """ get sample info from sample data """ 
       print "In fetch SampleInfo "
       result = self._connector.execute(SQL_GETSAMPLEINFO%(self._sampleID))
       
       # only one row in result set
       rows = result.fetchall()
       
       nbResults = len(rows)
       
       if nbResults is not 1:
            raise CTBTOError(-1,"Expecting to have one result but got %d either None or more than one. %s"%(nbResults,rows))
         
       # update data bag
       self._dataBag.update(rows[0].items())
       
       print "dataBag= %s"%(self._dataBag)
       
       result.close()

    def _readDataFile(self,aDir,aFilename,aType):
        """ read a file in a string buffer. This is used for the data files """
        
        # check that the file exists
        path = "%s/%s"%(aDir,aFilename)
        
        if not os.path.exists(path):
            raise CTBTOError(-1,"the file %s does not exits"%(filePath))
        
        # store in a StringIO object
        input = open(path,"r")
        
        data = StringIO()
        
        for line in input:
            data.write(line)
            
        input.close()
        
        self._dataBag["rawdata_%s"%(aType)] = data
        
    
        

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
        
        print "dataBag = %s"%(self._dataBag)
            
            
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

class SpalaxNobleGasDataFetcher:
    """ Class for fetching SPALAX related data """
    
      # Class members
    c_log = logging.getLogger("datafetchers.SpalaxNobleGasDataFetcher")
    c_log.setLevel(logging.DEBUG)


    def __init__(self):
        print "create SpalaxNobleGasDataFetcher"
        

class ParticulateDataFetcher:
    """ Class for fetching particualte related data """
    
      # Class members
    c_log = logging.getLogger("datafetchers.ParticulateDataFetcher")
    c_log.setLevel(logging.DEBUG)


    def __init__(self):
        print "create ParticulateDataFetcher"


""" Dictionary used to map DB Sample type with the right fetcher """
SAMPLE_TYPE = {'SAUNA':SaunaNobleGasDataFetcher, 'ARIX-4':SaunaNobleGasDataFetcher, 'SPALAX':SpalaxNobleGasDataFetcher, None:ParticulateDataFetcher}
        