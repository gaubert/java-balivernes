import logging
import sqlalchemy
import new
import os
import pprint
import string
from StringIO import StringIO

from common.exceptions import CTBTOError
import common.utils

""" sql requests """
SQL_GETDETECTORINFO   = "select det.detector_code as detector_code, det.description as detector_description, det.type as detector_type from RMSMAN.GARDS_DETECTORS det, RMSMAN.GARDS_SAMPLE_DATA data where data.sample_id=%s and data.DETECTOR_ID=det.DETECTOR_ID"
SQL_GETSTATIONINFO    = "select sta.station_code as station_code, sta.country_code as station_country_code, sta.type as station_type, sta.description as station_location,to_char(sta.lat)||' '||to_char(sta.lon)||' '||to_char(sta.elevation) as station_coordinates from RMSMAN.GARDS_STATIONS sta, RMSMAN.GARDS_SAMPLE_DATA data where data.sample_id=%s and sta.STATION_ID=data.STATION_ID"
SQL_GETSAMPLETYPE     = "select sta.type as sample_type from RMSMAN.GARDS_STATIONS sta, RMSMAN.GARDS_SAMPLE_DATA data where data.sample_id=%s and sta.STATION_ID=data.STATION_ID"


SQL_GETSAMPLEINFO     = "select sample_id as sample_id, input_file_name as spectrum_filepath, data_type as data_data_type, geometry as sample_geometry, \
                                spectral_qualifier as data_spectral_qualifier, quantity as sample_quantity, transmit_dtg as data_transmit_dtg , \
                                collect_start as data_collect_start, collect_stop as data_collect_stop, acquisition_start as data_acq_start, \
                                acquisition_stop as data_acq_stop, acquisition_live_sec as data_acq_live_sec, acquisition_real_sec as data_acq_real_sec \
                                from RMSMAN.GARDS_SAMPLE_DATA where sample_id=%s"
                                
""" get SAUNA Sample files : beta and gamma spectrum plus histogram. parameters station and sampleid """
SQL_GETSAUNA_FILES    = "select prod.dir, prod.DFIle,fp.prodtype from idcx.FILEPRODUCT prod,idcx.FPDESCRIPTIoN fp where (fp.typeid=30 or fp.typeid=29 or fp.typeid=34) and prod.chan='%s' and prod.typeID= fp.typeID and sta='%s'"

SQL_GETPARTICULATE_SPECTRUM    = "select prod.dir, prod.DFIle,fp.prodtype from idcx.FILEPRODUCT prod,idcx.FPDESCRIPTIoN fp where fp.typeid=29 and prod.chan='%s' and prod.typeID= fp.typeID and sta='%s'"

""" Get information regarding all identified nuclides """
SQL_SAUNA_GETIDENTIFIEDNUCLIDES = "select conc.conc as conc, conc.conc_err as conc_err, conc.MDC as MDC, conc.LC as LC, conc.LD as LD, lib.NAME as Nuclide, lib.HALFLIFE as halflife from RMSMAN.GARDS_BG_ISOTOPE_CONCS conc, RMSMAN.GARDS_XE_NUCL_LIB lib where sample_id=%s and conc.NUCLIDE_ID=lib.NUCLIDE_ID and conc.NID_FLAG=1"

""" Get information regarding all nuclides """
SQL_SAUNA_GETALLNUCLIDES = "select conc.conc as conc, conc.conc_err as conc_err, conc.MDC as MDC, conc.LC as LC, conc.LD as LD, lib.NAME as Nuclide, lib.HALFLIFE as halflife from RMSMAN.GARDS_BG_ISOTOPE_CONCS conc, RMSMAN.GARDS_XE_NUCL_LIB lib where sample_id=%s and conc.NUCLIDE_ID=lib.NUCLIDE_ID"

""" get particulate category """
SQL_PARTICULATE_CATEGORY_STATUS ="select entry_date as cat_entry_date, cnf_begin_date as cat_cnf_begin_date,cnf_end_date as cat_cnf_end_date, review_date as cat_review_date, review_time as cat_review_time, analyst as cat_analyst, status as cat_status, category as cat_category, auto_category as cat_auto_category, release_date as cat_release_date from RMSMAN.GARDS_SAMPLE_STATUS where sample_id=%s"

SQL_PARTICULATE_CATEGORY ="select NAME as CAT_NUCL_NAME, METHOD_ID as CAT_METHOD_ID, CATEGORY as CAT_CATEGORY, UPPER_BOUND as CAT_UPPER_BOUND, LOWER_BOUND as CAT_LOWER_BOUND, CENTRAL_VALUE as CAT_CENTRAL_VALUE, DELTA as CAT_DELTA, ACTIVITY as CAT_ACTIVITY from RMSMAN.GARDS_SAMPLE_CAT where sample_id=%s and hold=0"


""" returned all ided nuclides for a particular sample """
SQL_PARTICULATE_GET_NONQUANTIFIED_NUCLIDES = "select * from RMSMAN.GARDS_NUCL_IDED ided where sample_id=%s and name not in (select name from RMSMAN.GARDS_NUCL2QUANTIFY)"

SQL_PARTICULATE_GET_QUANTIFIED_NUCLIDES = "select * from RMSMAN.GARDS_NUCL_IDED ided where sample_id=%s and name in (select name from RMSMAN.GARDS_NUCL2QUANTIFY)"

SQL_PARTICULATE_GET_MDA_NUCLIDES = "select * from RMSMAN.GARDS_NUCL_IDED ided where sample_id=%s and report_mda=1"

SQL_PARTICULATE_GET_PEAKS = "select * from RMSMAN.GARDS_PEAKS where sample_id=%s"


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
        
        print "dataBag = %s"%(self._dataBag)
       

    def _readDataFile(self,aDir,aFilename,aType):
        """ read a file in a string buffer. This is used for the data files """
        
        # check that the file exists
        path = "%s/%s"%(aDir,aFilename)
        
        if not os.path.exists(path):
            raise CTBTOError(-1,"the file %s does not exits"%(filePath))
        
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
      
        """if(sample_cat[i].category != 1)
{
  /* Guillaume: correct Array out of bounds read when i = 0. Added (i==0) ||  */
  if((i == 0) || (sample_cat[i-1].category != 1)&&(sample_cat[i-1].category != sample_cat[i].category)) printf("\n");
   rptBuffer += sprintf(rptBuffer, "%-13s %-8d ", sample_cat[i].name, sample_cat[i].category);

fprintf(stderr,"n = %s  act = %g  upp = %g\n", sample_cat[i].name, sample_cat[i].activity,sample_cat[i].upper_bound);

  if(sample_cat[i].upper_bound == sample_cat[i].lower_bound)
   {
     rptBuffer += sprintf(rptBuffer, "%-25s\n", "Not Regularly Measured");
   }
  else if(sample_cat[i].activity > sample_cat[i].upper_bound)
   {
     rptBuffer += sprintf(rptBuffer, "%-25s\n", "Above Statistical Range");
   }
  else if(sample_cat[i].activity < sample_cat[i].lower_bound)
   {
     rptBuffer += sprintf(rptBuffer, "%-25s\n", "Below Statistical Range");
   }
  else  rptBuffer += sprintf(rptBuffer, "%-25s\n", "Within Statistical Range");"""

        
        
    def _fetchCategoryResults(self):
        """ sub method of _fetchAnalysisResults. Get the Category info from the database """
        
        result = self._connector.execute(SQL_PARTICULATE_CATEGORY%(self._sampleID))
       
        # only one row in result set
        rows = result.fetchall()
         
        # add results in a list which will become a list of dicts
        res = []
        
        # first row is metadata
        #res.append(rows[0].keys())
        data = {}
        i = 0
        
        for row in rows:
            data.update(row)
            # transform dates if necessary
            newRow = self._transformResults(data)
            # add Comment
            self._addCategoryComments(newRow)
            print "newRow %s"%(newRow)
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
        
        # first row is metadata
        res.append(rows[0].keys())
        
        for row in rows:
            res.append(row.values())
               
        # add in dataBag
        self._dataBag['peaks'] = res
        
        result.close()
        
        
    def _fetchNuclidesResults(self):
        """ Get info regarding the ided, non ided, MDAed nuclides """
         # get non quantified nuclides
        
        # to distinguish quantified and non quantified nuclide there is a table called GARDS_NUCL2QUANTIFY => static table of the nucl to treat
        result = self._connector.execute(SQL_PARTICULATE_GET_NONQUANTIFIED_NUCLIDES%(self._sampleID))
        
        rows = result.fetchall()
        
         # add results in a list which will become a list of dicts
        res = []
        
        # first row is metadata
        res.append(rows[0].keys())
        
        for row in rows:
            res.append(row.values())
                
        # add in dataBag
        self._dataBag['non_quantified_nuclides'] = res
        
        result.close()  
      
        # get quantified nuclides
      
        result = self._connector.execute(SQL_PARTICULATE_GET_QUANTIFIED_NUCLIDES%(self._sampleID))
        
        rows = result.fetchall()
        
         # add results in a list which will become a list of dicts
        res = []
        
        # first row is metadata
        res.append(rows[0].keys())
        
        for row in rows:
            res.append(row.values())
                
        # add in dataBag
        self._dataBag['quantified_nuclides'] = res
        
        result.close()  
        
        # get MDA nuclides
        result = self._connector.execute(SQL_PARTICULATE_GET_MDA_NUCLIDES%(self._sampleID))
        
        rows = result.fetchall()
        
         # add results in a list which will become a list of dicts
        res = []
        
        # first row is metadata
        res.append(rows[0].keys())
        
        for row in rows:
            res.append(row.values())
               
        # add in dataBag
        self._dataBag['quantified_nuclides'] = res
        
        result.close()  
        
    
    def _fetchAnalysisResults(self):
        """ get the  sample categorization, activityConcentrationSummary, peaks results, parameters, flags"""
        
        print "into Fetch Analysis Results"
        self._fetchCategoryResults()
        
        self._fetchNuclidesResults()
        
        self._fetchPeaksResults()
        
            
        
                   


""" Dictionary used to map DB Sample type with the right fetcher """
SAMPLE_TYPE = {'SAUNA':SaunaNobleGasDataFetcher, 'ARIX-4':SaunaNobleGasDataFetcher, 'SPALAX':SpalaxNobleGasDataFetcher, None:ParticulateDataFetcher}
        