import logging
import re

import ctbto.common.utils

from ctbto.common   import CTBTOError

from org.ctbto.conf import Conf
from ctbto.query    import RequestParser
from ctbto.db       import UNDEFINED

class BaseRenderer(object):
    """ Base Class used to transform the fetcher content into XML """
    
    # Class members
    c_log = logging.getLogger("SAMPMLrendererv1.BaseRenderer")
    c_log.setLevel(logging.INFO)
    
    def getRenderer(cls,aDataFetcher):
        """ Factory method returning the right Renderer \
            First it gets the sample type in order to instantiate the right DataFetcher => SAUNA, SPALAX, GenieParticulate, ...
           """
       
        # check preconditions
        if aDataFetcher is None: raise CTBTOError(-1,"passed argument aDataFetcher is null")
       
        # use the sample type to create the right renderer for the moment
        type = aDataFetcher.get('SAMPLE_TYPE')
       
        cls.c_log.debug("Type = %s"%(type))
       
        cls.c_log.debug("Klass = %s"%(RENDERER_TYPE.get(type,None)))
        
        klass = RENDERER_TYPE.get(type,None)
        if klass is None: 
            raise CTBTOError(-1,"There is no renderer for the following type"%(type))

        inst = klass(aDataFetcher)
    
        return inst
       
    #class method binding
    getRenderer = classmethod(getRenderer)
    
    def __init__(self, aDataFetcher):
        
        self._conf = Conf.get_instance()
        self._fetcher = aDataFetcher
        self._quantifiable = set()
        self._template = None
        self._populatedTemplate = None
        self._analysisCounter = 0
        
        # create query parser 
        self._parser = RequestParser()
        
        # dict used to substitute values in fetcher with template values
        self._substitutionDict = {  "SAMPLEID"           :   "SAMPLE_ID",
                                    "REFERENCEID"        :   "REFERENCE_ID",
                                    "STATION_LOCATION"   :   "STATION_LOCATION",
                                    "STATION_CODE"       :   "STATION_CODE",
                                    "COUNTRY_CODE"       :   "STATION_COUNTRY_CODE",
                                    "COORDINATES"        :   "STATION_COORDINATES",
                                    "DET_CODE"           :   "DETECTOR_CODE",
                                    "DET_TYPE"           :   "DETECTOR_TYPE",
                                    "DET_DESCRIPTION"    :   "DETECTOR_DESCRIPTION",
                                    "SAMPLE_TYPE"        :   "SAMPLE_TYPE",
                                    "REMARK"             :   "TEMPLATE_COMMAND_NOTHING",
                                 }
                                  
        self._createTemplate()
        
    def _createTemplate(self):
        """ Read XML template from a file and store it in a String 
            Read main template from a file because do not know how to setup the encoding.
            When open(...) is used, the encoding is read properly
        """
       
    def _sortSpectrumsSet(self, aSpectrums):
        
        results = []
        
        if 'CURR' in aSpectrums:
            id = self._fetcher.get(u'CURRENT_CURR', None)
            if id != None:
                results.append(id)
                
            aSpectrums.remove('CURR')
        
        if 'DETBK' in aSpectrums:
            id = self._fetcher.get(u'CURRENT_BK', None)
            if id != None:
                results.append(id)
                
            aSpectrums.remove('DETBK')
        
        if 'GASBK' in aSpectrums:
            id = self._fetcher.get(u'CURRENT_GASBK', None)
            if id != None:
                results.append(id)
            aSpectrums.remove('GASBK')
        
        if 'QC' in aSpectrums:
            if id != None:
                results.append(self._fetcher.get(u'CURRENT_QC', None))
            aSpectrums.remove('QC')
            
        # for the rest alphabetical order sorting
        l = []
        for e in aSpectrums:
            l.append(e)
        
        l.sort()
        results.extend(l)
        
        return results
     
    def _generateAnalysisID(self):
        """ simple counter incremented """
     
        self._analysisCounter += 1
     
        return "analysis-%d" % (self._analysisCounter)
    
    def _substituteValues(self):
        """ substitue values """
        
        for (key, val) in self._substitutionDict.items():
            pattern = "\${%s}" % (key)
            
            if val == "TEMPLATE_COMMAND_NOTHING":
                self._populatedTemplate = re.sub(pattern, "", self._populatedTemplate)
            
            self._populatedTemplate = re.sub(pattern, str(self._fetcher.get(val, UNDEFINED)), self._populatedTemplate)
            
    def asXml(self):
        """  """
        
    def asXmlStr(self, aRequest): #IGNORE:W0613
        """ return the xml product according to the passed request
        
            Args:
               aRequest: string containing some parameters for each fetching bloc (ex params="specturm=curr/qc/prels/bk")
            
            Returns: the populated template
              
              
            Raises:
               exception if issue fetching data (CTBTOError)
        """
        
        self._substituteValues()
        
        return self._populatedTemplate
        
class SpalaxRenderer(BaseRenderer):
    
    # Class members
    c_log = logging.getLogger("SAMPMLrendererv1.SpalaxRenderer")
    c_log.setLevel(logging.INFO)
    
      
    def __init__(self, aDataFetcher):
        
        super(SpalaxRenderer, self).__init__(aDataFetcher)
        
        # add values specific to Spalax
        dummy_dict = {  
                        # to be changed as only one analysis is supported at the moment
                        "SPECTRUM_ID"                    :   "CURR_DATA_ID"
                      }
        # add specific particulate keys
        self._substitutionDict.update(dummy_dict)
        
        self._xe_lib = set()
    
    def _createTemplate(self):
        """ Read the template from a file. Old method now everything is read from the conf """
        
        # get template path from conf
        self._template = self._conf.get("SpalaxTemplatingSystem", "spalaxBaseTemplate")
        
        self._populatedTemplate = self._template
    
    def asXmlStr(self, aRequest=""):
        """ return the xml particulate product according to the passed request
        
            Args:
               aRequest: string containing some parameters for each fetching bloc (ex params="specturm=curr/qc/prels/bk"). Default = ""
            
            Returns: the populated template
              
              
            Raises:
               exception if issue fetching data (CTBTOError)
         """
       
        # parse request to know what need to be added in the product
        # [Parsing could be done for once and shared between fetcher and renderer]
        reqDict = self._parser.parse(aRequest, RequestParser.GAS)
         
        self._fillData(reqDict)
       
        self._fillAnalysisResults(reqDict)
       
        self._fillCalibration()
       
        # father 
        BaseRenderer.asXmlStr(self, aRequest)
       
        return self._populatedTemplate 
    
    def _getCategory(self, id): #IGNORE:W0613
        """ return Categorization for the passed sample_id. Do nothing for the moment """
        return ""
    
    def _build_xml_from_table_representation(self,table):
        """ dynamically build the xml adding the parameters """
        
        xml=''
        # add technical stuff to ignore_list
        ignore_list = ['DBDefault','DBFile','DBPassword','DBServer','DBString','DBUser','Help','ManualDB','ManualDBUser','ManualDBPassword','RmsHome',]
        # add calibration info as it is somewhere else in the file
        ignore_list.extend(['EfficiencyCalibrationCoeffs','EfficiencyCalPolyDegree','EfficiencyCoeffs','EnergyCalibrationCoeffs','EnergyCalPolyDegree','EnergyCoeffs','ResolutionCalibrationCoeffs','ResolutionCalPolyDegree','ResolutionCoeffs'])
        
        name = ''
        value  = None
        
        for line in table:
            name   = line['NAME']
            value  = line['VALUE']
            if name not in ignore_list and value != None:
                xml += '<%s>%s</%s>'%(name,value,name)

        return xml
    
    def _getParameters(self, id): #IGNORE:W0613
        """ return the processing paramters
        
            Args:
               id: Analysis id
            
            Returns: the populated template
              
              
            Raises:
               exception if issue fetching data (CTBTOError)
        """
        
        # first add Quantified Nuclides
        template = self._conf.get("SpalaxTemplatingSystem", "spalaxProcessingParametersTemplate")

        return re.sub("\${PARAMETERS}",self._build_xml_from_table_representation(self._fetcher.get("%s_PROC_PARAMS" % (id), None)), template)

    def _getNuclides(self, id):
        """ fill the information regarding the analysed nuclides
        
            Args:
               id: Analysis id
            
            Returns: the populated template
              
              
            Raises:
               exception if issue fetching data (CTBTOError)
        """
        result_str = ""
        
         # first get the template
        nuclide_template          = self._conf.get("SpalaxTemplatingSystem", "spalaxNuclideTemplate")
        
        xeresults = self._fetcher.get("%s_XE_RESULTS"%(id),None)
        
        matrix_results = {}
        
        if xeresults is not None:
            for result in xeresults:
                method = result[u'METHOD']
                # if the matrix doesn't exist add it in the results
                if method not in matrix_results:
                    matrix_results[method] = ""
                
                dummy_template = re.sub("\${METHOD}",result[u'METHOD'],nuclide_template)
                dummy_template = re.sub("\${NAME}",result[u'NUCLIDE'],dummy_template)
                dummy_template = re.sub("\${CONCENTRATION}", str(result['CONC']), dummy_template)
                dummy_template = re.sub("\${CONCENTRATION_ERROR}", str(result['CONC_ERR']), dummy_template)
                dummy_template = re.sub("\${CONCENTRATION_ERROR_PERC}", str(result.get('CONC_ERR_PERC', 'N/A')), dummy_template)
                dummy_template = re.sub("\${MDI}", str(result['MDI']) if (result['MDI'] != None) else UNDEFINED, dummy_template)
                dummy_template = re.sub("\${MDC}", str(result['MDC']) if (result['MDC'] != None) else UNDEFINED, dummy_template)
                # LC and LD in concentration
                dummy_template = re.sub("\${LC}", str(result['LC']), dummy_template)
                dummy_template = re.sub("\${LD}", str(result['LD']), dummy_template)
                dummy_template = re.sub("\${ACTIVITY}", str(result['ACTIVITY']), dummy_template)
                dummy_template = re.sub("\${ACTIVITY_ERROR}", str(result['ACTIVITY_ERR']), dummy_template)
                dummy_template = re.sub("\${ACTIVITY_ERROR_PERC}", str(result.get('ACTIVITY_ERR_PERC', 'N/A')), dummy_template)
                dummy_template = re.sub("\${LC_ACTIVITY}", str(result['LC_ACTIVITY']), dummy_template)
                dummy_template = re.sub("\${LD_ACTIVITY}", str(result['LD_ACTIVITY']), dummy_template)
            
                dummy_template = re.sub("\${IDENTIFICATION_INDICATOR}", str(result['NID_FLAG']), dummy_template)
                dummy_template = re.sub("\${IDENTIFICATION_NUM}", str(result['NID_FLAG_NUM']), dummy_template)
            
                matrix_results[method] += dummy_template
        
        # hopefully we should get two matrixes in matrix_results
        for (method,nuclides) in matrix_results.items():
            result_str += nuclides
                
        return result_str
    
    def _getXECovMatrix(self,id):
        """ fill the covariance matrix results
        
            Args:
               id: Analysis id
            
            Returns: the populated template
              
              
            Raises:
               exception if issue fetching data (CTBTOError)
        """
        
        result_str = ""
        
         # first get the template
        cell_template          = self._conf.get("SpalaxTemplatingSystem", "spalaxCovMatrixCellTemplate")
        method_matrix_template = self._conf.get("SpalaxTemplatingSystem", "spalaxMethodMatrixTemplate")
        
        matrix_results = {}
        
        xeresults = self._fetcher.get("%s_XE_RESULTS"%(id),None)
        
        if xeresults is not None:
            for result in xeresults:
                method = result[u'METHOD']
                # if the matrix doesn't exist add it in the results
                if method not in matrix_results:
                    matrix_results[method] = ""
               
                cells = matrix_results[method]
               
                row     = re.sub("\${ROW}",str(result.get(u'NUCLIDE','Error')) , cell_template)
                
                one_row = re.sub("\${COL}"  ,'XE_131M', row)
                one_row = re.sub("\${VALUE}",str(result.get(u'COV_XE_131M','Error')) , one_row)
                cells  += one_row
                
                one_row = re.sub("\${COL}"  ,'XE_133M', row)
                one_row = re.sub("\${VALUE}",str(result.get(u'COV_XE_133M','Error')) , one_row)
                cells  += one_row
                
                one_row = re.sub("\${COL}"  ,'XE_133', row)
                one_row = re.sub("\${VALUE}",str(result.get(u'COV_XE_133','Error')) , one_row)
                cells  += one_row
                
                one_row = re.sub("\${COL}"  ,'XE_135', row)
                one_row = re.sub("\${VALUE}",str(result.get(u'COV_XE_135','Error')) , one_row)
                cells  += one_row
                
                # put cells in matrix_results for the found method
                matrix_results[method] = cells
        
        # hopefully we should get two matrixes in matrix_results
        for (method,cells) in matrix_results.items():
            m = re.sub("\${METHOD}",method, method_matrix_template)
            m = re.sub("\${CELLS}",cells, m)
            
            result_str += m
            
                
        return result_str
    
    def _getDataQualityFlags(self,id):
        """ Add the data quality flags
        
            Args:
               id: Analysis id
            
            Returns: the populated template
              
              
            Raises:
               exception if issue fetching data (CTBTOError)
        """
        template = self._conf.get("SpalaxTemplatingSystem", "spalaxDataQualityFlagsTemplate")
        
        # add Data Quality Flags
        dataQFlags = self._fetcher.get('%s_DATA_QUALITY_FLAGS' % (id), [])
        
        # list of all flags found
        dq_xml = ""
        
        if len(dataQFlags) > 0:
            for flag in dataQFlags:
                name = flag['DQ_NAME']
              
                # check if it has a template if not ignore.
                dummy_template = self._conf.get("SpalaxTemplatingSystem", "dataQFlags_%s_Template" % (name), None)
                if dummy_template != None:
                    dummy_template = re.sub("\${%s_VAL}" % (name), str(flag['DQ_VALUE']), dummy_template)
                    dummy_template = re.sub("\${%s_PASS}" % (name), "true" if flag['DQ_RESULT'] == 0 else "false", dummy_template)
                    dummy_template = re.sub("\${%s_THRESOLD}" % (name), str(flag['DQ_THRESHOLD']), dummy_template)
                 
                    # add non empty template to data flags
                    dq_xml += dummy_template
              
        return re.sub("\${DQ_FLAGS}", dq_xml, template)
    
    def _getQCFlags(self,id):
        """ Add the QC flags
        
            Args:
               id: Analysis id
            
            Returns: the populated template
              
              
            Raises:
               exception if issue fetching data (CTBTOError)
        """
        template = self._conf.get("SpalaxTemplatingSystem", "spalaxQCFlagsTemplate")
        
        # add Data Quality Flags
        dataQFlags = self._fetcher.get('%s_QC_FLAGS' % (id), [])
        
        xml = ''
        
        # get the template for a unique flag
        one_flag = self._conf.get("SpalaxTemplatingSystem", "spalaxQCFlagTemplate")
        
        for dFlag in dataQFlags:
            xml_f = re.sub("\${NAME}", dFlag[u'TEST_NAME'], one_flag)
            xml_f = re.sub("\${COMMENT}",dFlag[u'QC_COMMENT'], xml_f)
            xml_f = re.sub("\${PASS}","true" if dFlag[u'FLAG'] == 'G' else "false", xml_f)
            xml += xml_f
        
        return  re.sub("\${QC_FLAGS}",xml,template)   
    
    def _getFlags(self, id):
        """ create xml part with the flag info
        
            Args:
               id: Analysis id
            
            Returns: the populated template
              
              
            Raises:
               exception if issue fetching data (CTBTOError)
        """
        xml = self._getDataQualityFlags(id)
        
        xml += self._getQCFlags(id)
        
        return xml
    
    def _fillAnalysisResults(self, requestDict):
        """ fill the analysis results for each result
        
            Args:
               aRequest: string containing some parameters for each fetching bloc (ex params="specturm=curr/qc/prels/bk"). Default = ""
            
            Returns: the populated template
              
              
            Raises:
               exception if issue fetching data (CTBTOError)
        """
        # check if there is a spectrum in the hashtable. If not replace ${SPECTRUM} by an empty string ""
        requestedTypes = requestDict[RequestParser.ANALYSIS]
        
        all_analyses_xml = ""
      
        for ty in requestedTypes:
           
            #identifier in the dict for this analysis  
            sindict_id = self._fetcher.get("CURRENT_%s" % (ty), None)
           
            if sindict_id is not None:
        
                # first get the template
                template = self._conf.get("SpalaxTemplatingSystem", "spalaxAnalysisTemplate")
                dummy_template = ""
        
                # for the moment only one result
                dummy_template += template
    
                #spectrum_id = self._fetcher.get("%s_G_DATA_ID" % (self._fetcher.get("CURRENT_%s" % (ty), '')), "n/a")
                # get the spectrum gid
                spectrum_gid = self._fetcher.get("%s_DATA_NAME" % (self._fetcher.get("CURRENT_%s" % (ty), '')), "n/a")
                
                # Add analysis identifier => SpectrumID prefixed by AN
                dummy_template = re.sub("\${ANALYSISID}", "AN-%s" % (spectrum_gid), dummy_template)
        
                dummy_template = re.sub("\${SPECTRUM_ID}", spectrum_gid, dummy_template)
        
                dummy_template = re.sub("\${CATEGORY}", self._getCategory(sindict_id), dummy_template)
        
                dummy_template = re.sub("\${NUCLIDES}", self._getNuclides(sindict_id), dummy_template)
             
                dummy_template = re.sub("\${XECOVMATRIX}", self._getXECovMatrix(sindict_id), dummy_template)
                
                dummy_template = re.sub("\${PARAMETERS}", self._getParameters(sindict_id), dummy_template)
        
                dummy_template = re.sub("\${FLAGS}", self._getFlags(sindict_id), dummy_template)
             
                #add Calibration references
                l = self._fetcher.get("%s_G_DATA_ALL_CALS" % (sindict_id))
                if l is None :
                    SaunaRenderer.c_log.warning("No calibration information for sample %s" % (ty))
                    l = []
                else:
                    # add calibration info
                    dummy_template = re.sub("\${CAL_INFOS}", ' '.join(map(str, l)), dummy_template) #IGNORE:W0141
        
                # add software method version info
                dummy_template = re.sub("\${SOFTWARE}", "bg_analyse", dummy_template)
                dummy_template = re.sub("\${METHOD}", "standard", dummy_template)
                dummy_template = re.sub("\${VERSION}", "1.0", dummy_template)
                dummy_template = re.sub("\${SOFTCOMMENTS}", "Old version", dummy_template)
             
                all_analyses_xml += dummy_template
        
            # add all the analysis info in the global template
            self._populatedTemplate = re.sub("\${AnalysisResults}", all_analyses_xml, self._populatedTemplate)
         
    
    def _fillCalibrationCoeffs(self, prefix, calibInfos):
        """ Insert the calibration information
        
            Args:
               prefix: the prefix for constituting the UID identifying the currently treated sampleID in the fetcher object
               calibInfos: set of calib info ids that have already been included in the xml
            
            Returns: generated xml data for displaying calibration info
               
            Raises:
               exception if issue fetching data (CTBTOError)
        """
        
        # first add Energy Cal
        template = self._conf.get("ParticulateTemplatingSystem", "particulateEnergyCalTemplate")
        
        xml = ""
        dummy_template = ""
        
        # get energy calibration 
        en_id = self._fetcher.get("%s_G_ENERGY_CAL" % (prefix), None)
        
        if (en_id is not None):
        
            # add calib info if it isn't there already
            if en_id not in calibInfos:
                energy = self._fetcher.get(en_id, {})
                dummy_template = re.sub("\${TERM0}", str(energy.get(u'COEFF1', UNDEFINED)), template)
                dummy_template = re.sub("\${TERM1}", str(energy.get(u'COEFF2', UNDEFINED)), dummy_template)
                dummy_template = re.sub("\${TERM2}", str(energy.get(u'COEFF3', UNDEFINED)), dummy_template)
                dummy_template = re.sub("\${TERM3}", str(energy.get(u'COEFF4', UNDEFINED)), dummy_template)
                dummy_template = re.sub("\${EN_ID}", en_id, dummy_template)
                # add generated xml in final container
                xml += dummy_template
                # add the id in the set of existing infos
                calibInfos.add(en_id)
        else:
            GenieParticulateRenderer.c_log.warning("Could not find any energy calibration info for sample %s\n" % (prefix))
        
        template = self._conf.get("ParticulateTemplatingSystem", "particulateResolutionCalTemplate")
        
        re_id = self._fetcher.get("%s_G_RESOLUTION_CAL" % (prefix), None)
        
        if re_id is not None: 
            # add calib info if it isn't there already
            if re_id not in calibInfos:
                # get resolution calibration 
                resolution = self._fetcher.get(re_id, {})
        
                dummy_template = re.sub("\${TERM0}", str(resolution.get('COEFF1', UNDEFINED)), template)
                dummy_template = re.sub("\${TERM1}", str(resolution.get('COEFF2', UNDEFINED)), dummy_template)
                dummy_template = re.sub("\${TERM2}", str(resolution.get('COEFF3', UNDEFINED)), dummy_template)
                dummy_template = re.sub("\${RE_ID}", re_id, dummy_template)
        
                # add generated xml in final container
                xml += dummy_template
    
                # add the id in the set of existing infos
                calibInfos.add(re_id)
        else:
            GenieParticulateRenderer.c_log.warning("Warning. Could not find any resolution calibration info for sample %s\n" % (prefix))
        
        template = self._conf.get("ParticulateTemplatingSystem", "particulateEfficencyCalTemplate")
        
        eff_id = self._fetcher.get("%s_G_EFFICIENCY_CAL" % (prefix), None)
        
        
        
        if (eff_id is not None):
            # add calib info if it isn't there already
            if eff_id not in calibInfos:
                # get efficiency calibration 
                eff = self._fetcher.get(eff_id, {})
        
                dummy_template = re.sub("\${LN_TERM0}", str(eff.get('COEFF1', UNDEFINED)), template)
                dummy_template = re.sub("\${TERM0}", str(eff.get('COEFF2', UNDEFINED)), dummy_template)
                dummy_template = re.sub("\${TERM1}", str(eff.get('COEFF3', UNDEFINED)), dummy_template)
                dummy_template = re.sub("\${TERM2}", str(eff.get('COEFF4', UNDEFINED)), dummy_template)
                dummy_template = re.sub("\${TERM3}", str(eff.get('COEFF5', UNDEFINED)), dummy_template)
                dummy_template = re.sub("\${TERM4}", str(eff.get('COEFF6', UNDEFINED)), dummy_template)
                dummy_template = re.sub("\${TERM5}", str(eff.get('COEFF7', UNDEFINED)), dummy_template)
                dummy_template = re.sub("\${EF_ID}", eff_id, dummy_template)
        
                # add generated xml in final container
                xml += dummy_template
            
                # add the id in the set of existing infos
                calibInfos.add(eff_id)
        
        return xml
    
    def _fillCalibration(self):
        """ Add the calibration parameters for each of the spectrum
        
            Args:
               requestDict: dictionary representing the different elements of the request (analysis, spectrum, ...)
            
            Returns: Nothing
              
              
            Raises:
               exception if issue fetching data (CTBTOError)
        """
        xml = ""
        # list of ids added in the xml document
        addedCalibrationIDs = set()
        
        for ty in self._fetcher.get('CONTENT_PRESENT', []):
            
            # treat preliminary samples differently as there is another indirection
            if ty == 'PREL':
                for prefix in self._fetcher.get('CURR_List_OF_PRELS', []):
                    if prefix is None:
                        raise CTBTOError(- 1, "Error when filling Calibration info for prefix %s, There is no CURRENT_%s in the dataBag\n" % (prefix, prefix))
                
                    xml += self._fillCalibrationCoeffs(prefix, addedCalibrationIDs)    
            else:
                prefix = self._fetcher.get(u'CURRENT_%s' % (ty), None)
                if prefix is None:
                    raise CTBTOError(- 1, "Error when fetching Calibration info for prefix %s, There is no CURRENT_%s in the dataBag\n" % (prefix, prefix))
               
                xml += self._fillCalibrationCoeffs(prefix, addedCalibrationIDs)      
            
        # out of the loop
        self._populatedTemplate = re.sub("\${CALIBRATION}", xml, self._populatedTemplate)
    
    
    def _oldfillData(self, requestDict):
        """ Insert the spectrum data expected as defined in the initial passed request
        
            Args:
               requestDict: dictionary representing the different elements of the request (analysis, spectrum, ...)
            
            Returns: Nothing
              
              
            Raises:
               exception if issue fetching data (CTBTOError)
        """
    
        # check if there is a spectrum in the hashtable. If not replace ${SPECTRUM} by an empty string ""
        requestedTypes = requestDict[RequestParser.SPECTRUM]
        
        if 'PREL' in requestedTypes:
            # add all prels found in CURR_List_OF_PRELS in the set
            requestedTypes.remove('PREL')
            requestedTypes.update(self._fetcher.get(u'CURR_List_OF_PRELS', []))
        
        spectrums = self._sortSpectrumsSet(requestedTypes)
        
        
        finalTemplate = ""
        
      
        for ty in spectrums:
            
            spectrumTemplate = ""
            
            # add Spectrum
            fname = "%s_G_DATA" % (ty)
              
            data = self._fetcher.get(fname, None)
            
            if data is not None:
               
                spectrumTemplate = self._conf.get("SpalaxTemplatingSystem", "spalaxSpectrumTemplate")
              
                # insert data
                spectrumTemplate = re.sub("\${SPECTRUM_DATA}", data, spectrumTemplate)
              
                # insert spectrum ID
                spectrumTemplate = re.sub("\${SPECTRUM_ID}", self._fetcher.get("%s_ID" % (fname)), spectrumTemplate)
            
                # insert energy and channel span
                spectrumTemplate = re.sub("\${SPECTRUM_DATA_CHANNEL_SPAN}", str(self._fetcher.get("%s_CHANNEL_SPAN" % (fname))), spectrumTemplate)
                spectrumTemplate = re.sub("\${SPECTRUM_DATA_ENERGY_SPAN}", str(self._fetcher.get("%s_ENERGY_SPAN" % (fname))), spectrumTemplate)
            
                # get the date information (for the moment it is repeated for each data (beta and gamma spectra and histogram)
                spectrumTemplate = re.sub("\${COL_START}", str(self._fetcher.get("%s_COLLECT_START" % (fname))), spectrumTemplate)
                spectrumTemplate = re.sub("\${COL_STOP}", str(self._fetcher.get("%s_COLLECT_STOP" % (fname))), spectrumTemplate)
                
                spectrumTemplate = re.sub("\${ACQ_START}", str(self._fetcher.get("%s_ACQ_START" % (fname))), spectrumTemplate)
                spectrumTemplate = re.sub("\${ACQ_STOP}", str(self._fetcher.get("%s_ACQ_STOP" % (fname))), spectrumTemplate)
                spectrumTemplate = re.sub("\${SAMPLING_TIME}", str(self._fetcher.get("%s_SAMPLING_TIME" % (fname))), spectrumTemplate)
                spectrumTemplate = re.sub("\${REAL_ACQ_TIME}", str(self._fetcher.get("%s_ACQ_REAL_SEC" % (fname))), spectrumTemplate)
                spectrumTemplate = re.sub("\${LIVE_ACQ_TIME}", str(self._fetcher.get("%s_ACQ_LIVE_SEC" % (fname))), spectrumTemplate)
                spectrumTemplate = re.sub("\${ARRIVAL_DATE}", str(self._fetcher.get("%s_TRANSMIT_DTG" % (fname))), spectrumTemplate)
              
                spectrumTemplate = re.sub("\${DECAY_TIME}", str(self._fetcher.get("%s_DECAY_TIME" % (fname))), spectrumTemplate)
                spectrumTemplate = re.sub("\${SPECTRUM_TYPE}", str(self._fetcher.get("%s_SPECTRAL_QUALIFIER" % (fname))), spectrumTemplate)
                spectrumTemplate = re.sub("\${MEASUREMENT_TYPE}", str(self._fetcher.get("%s_DATA_TYPE" % (fname))), spectrumTemplate)
                # add quantity and geometry
                spectrumTemplate = re.sub("\${QUANTITY}", str(self._fetcher.get("%s_SAMPLE_QUANTITY" % (fname))), spectrumTemplate)
                spectrumTemplate = re.sub("\${FLOW_RATE}", str(self._fetcher.get("%s_FLOW_RATE" % (fname))), spectrumTemplate)
                
                spectrumTemplate = re.sub("\${GEOMETRY}", str(self._fetcher.get("%s_SAMPLE_GEOMETRY" % (fname))), spectrumTemplate)
              
                l = self._fetcher.get("%s_ALL_CALS" % (fname))
                if l is None:
                    SpalaxRenderer.c_log.warning("No calibration information for sample %s" % (ty))
                    l = []
                
                # add calibration info
                spectrumTemplate = re.sub("\${CAL_INFOS}", ' '.join(map(str, l)), spectrumTemplate) #IGNORE:W0141
              
                # TODO to remove just there for testing, deal with the compression flag
                if self._fetcher.get("%s_COMPRESSED" % (fname), False):
                    spectrumTemplate = re.sub("\${COMPRESS}", "compress=\"base64,zip\"", spectrumTemplate)
                else:
                    spectrumTemplate = re.sub("\${COMPRESS}", "", spectrumTemplate)
                     
                # add fill spectrum template in global template 
                finalTemplate += spectrumTemplate
        
        self._populatedTemplate = re.sub("\${DATA}", finalTemplate, self._populatedTemplate)

    def _fillData(self, requestDict):
        """ Insert the spectrum data expected as defined in the initial passed request
        
            Args:
               requestDict: dictionary representing the different elements of the request (analysis, spectrum, ...)
            
            Returns: Nothing
              
              
            Raises:
               exception if issue fetching data (CTBTOError)
        """
    
        # check if there is a spectrum in the hashtable. If not replace ${SPECTRUM} by an empty string ""
        requestedTypes = requestDict[RequestParser.SPECTRUM]
        
        if 'PREL' in requestedTypes:
            # add all prels found in CURR_List_OF_PRELS in the set
            requestedTypes.remove('PREL')
            requestedTypes.update(self._fetcher.get(u'CURR_List_OF_PRELS', []))
        
        spectrums = self._sortSpectrumsSet(requestedTypes)
        
        
        finalTemplate = ""
        
        for ty in spectrums:
            
            #group Template            
            group_spec_template = self._conf.get("SpalaxTemplatingSystem", "spalaxSpectrumGroupTemplate")
            
            # add the general parameters
            group_spec_template = re.sub("\${SPECTRUM_GROUP_ID}",self._fetcher.get("%s_DATA_NAME" % (ty)), group_spec_template)
            group_spec_template = re.sub("\${COL_START}", str(self._fetcher.get("%s_G_DATA_COLLECT_START" % (ty))), group_spec_template)
            group_spec_template = re.sub("\${COL_STOP}", str(self._fetcher.get("%s_G_DATA_COLLECT_STOP" % (ty))), group_spec_template)
            group_spec_template = re.sub("\${ACQ_START}", str(self._fetcher.get("%s_G_DATA_ACQ_START" % (ty))), group_spec_template)
            group_spec_template = re.sub("\${ACQ_STOP}", str(self._fetcher.get("%s_G_DATA_ACQ_STOP" % (ty))), group_spec_template)
            group_spec_template = re.sub("\${SAMPLING_TIME}", str(self._fetcher.get("%s_G_DATA_SAMPLING_TIME" % (ty))), group_spec_template)
            group_spec_template = re.sub("\${REAL_ACQ_TIME}", str(self._fetcher.get("%s_G_DATA_ACQ_REAL_SEC" % (ty))), group_spec_template)
            group_spec_template = re.sub("\${LIVE_ACQ_TIME}", str(self._fetcher.get("%s_G_DATA_ACQ_LIVE_SEC" % (ty))), group_spec_template)
            group_spec_template = re.sub("\${ARRIVAL_DATE}", str(self._fetcher.get("%s_G_DATA_TRANSMIT_DTG" % (ty))), group_spec_template)
              
            group_spec_template = re.sub("\${DECAY_TIME}", str(self._fetcher.get("%s_G_DATA_DECAY_TIME" % (ty))), group_spec_template)
             
            group_spec_template = re.sub("\${SPECTRUM_TYPE}",str(self._fetcher.get("%s_G_DATA_SPECTRAL_QUALIFIER" % (ty))), group_spec_template)
            group_spec_template = re.sub("\${MEASUREMENT_TYPE}",str(self._fetcher.get("%s_G_DATA_DATA_TYPE" % (ty))), group_spec_template)
            # add quantity and geometry
            group_spec_template = re.sub("\${QUANTITY}", str(self._fetcher.get("%s_G_DATA_SAMPLE_QUANTITY" % (ty))), group_spec_template)
            group_spec_template = re.sub("\${FLOW_RATE}", str(self._fetcher.get("%s_G_DATA_FLOW_RATE" % (ty))), group_spec_template)
                
            group_spec_template = re.sub("\${GEOMETRY}", str(self._fetcher.get("%s_G_DATA_SAMPLE_GEOMETRY" % (ty))), group_spec_template)
            
            # add the calibration info
            l = self._fetcher.get("%s_G_DATA_ALL_CALS" % (ty))
            if l is None:
                SaunaRenderer.c_log.warning("No calibration information for sample %s" % (ty))
                l = []
            
            group_spec_template = re.sub("\${CAL_INFOS}", ' '.join(map(str, l)), group_spec_template) #IGNORE:W0141
              
            dataTemplate=""
            # add spectra
            fname = "%s_G_DATA" % (ty)

            data = self._fetcher.get(fname, None)
            if data is not None:
                # add gamma Spectrum
                sTemplate = self._conf.get("SaunaTemplatingSystem", "saunaSpectrumTemplate")
                # insert energy and channel span
                sTemplate = re.sub("\${SPECTRUM_DATA_CHANNEL_SPAN}", str(self._fetcher.get("%s_CHANNEL_SPAN" % (fname))), sTemplate)
                sTemplate = re.sub("\${SPECTRUM_DATA_ENERGY_SPAN}",  str(self._fetcher.get("%s_ENERGY_SPAN" % (fname))) , sTemplate)
                # insert spectrum ID
                sTemplate = re.sub("\${SPECTRUM_ID}", self._fetcher.get("%s_ID" % (fname)), sTemplate)
                sTemplate = re.sub("\${S_TYPE}", self._fetcher.get("%s_TY" % (fname)), sTemplate)
                    
                # insert data
                sTemplate = re.sub("\${SPECTRUM_DATA}", data, sTemplate)
                    
                # TODO to remove just there for testing, deal with the compression flag
                if self._fetcher.get("%s_COMPRESSED" % (fname), False):
                    sTemplate = re.sub("\${COMPRESS}", "compress=\"base64,zip\"", sTemplate)
                else:
                    sTemplate = re.sub("\${COMPRESS}", "", sTemplate)
            
                dataTemplate += sTemplate
                     
            #Add all found data in group Spectrum
            group_spec_template = re.sub("\${GSPECTRUMDATA}",dataTemplate,group_spec_template)
            
            
            # add groupTemplate in finalTemplate
            finalTemplate += group_spec_template
        
        self._populatedTemplate = re.sub("\${DATA}", finalTemplate, self._populatedTemplate)
        
      
class SaunaRenderer(BaseRenderer):
    
    # Class members
    c_log = logging.getLogger("SAMPMLrendererv1.SaunaRenderer")
    c_log.setLevel(logging.INFO)
    
      
    def __init__(self, aDataFetcher):
        
        super(SaunaRenderer, self).__init__(aDataFetcher)
        
        # add values specific to Particulates
        dummy_dict = {  
                        # to be changed as only one analysis is supported at the moment
                        "SPECTRUM_ID"                    :   "CURR_DATA_ID"
                      }
        # add specific particulate keys
        self._substitutionDict.update(dummy_dict)
        
        self._xe_lib = set()
    
    def _createTemplate(self):
        """ Read the template from a file. Old method now everything is read from the conf """
        
        # get template path from conf
        self._template = self._conf.get("SaunaTemplatingSystem", "saunaBaseTemplate")
        
        # old version => template was read from a file
        #path = self._conf.get("SaunaTemplatingSystem", "saunaBaseTemplate")
        # assert that the file exists
        #ctbto.common.utils.file_exits(path)
        # read the full template in a string buffer
        #f = open(path, "r") 
        #self._template = f.read()
        
        self._populatedTemplate = self._template
    
    def asXmlStr(self, aRequest=""):
        """ return the xml particulate product according to the passed request
        
            Args:
               aRequest: string containing some parameters for each fetching bloc (ex params="specturm=curr/qc/prels/bk"). Default = ""
            
            Returns: the populated template
              
              
            Raises:
               exception if issue fetching data (CTBTOError)
         """
       
        # parse request to know what need to be added in the product
        # [Parsing could be done for once and shared between fetcher and renderer]
        reqDict = self._parser.parse(aRequest, RequestParser.GAS)
         
        self._fillData(reqDict)
       
        self._fillAnalysisResults(reqDict)
       
        self._fillCalibration()
       
        # father 
        BaseRenderer.asXmlStr(self, aRequest)
       
        return self._populatedTemplate
   
    def _isQuantifiable(self, aVal):
        """ true if quantifiable, false otherwise """
        xe_lib = self._fetcher.get("XE_NUCL_LIB")
     
        # if set hasn't been populated do it
        if len(self._xe_lib) == 0:
            # create a set containing all quantifiable elements
            for elem in xe_lib:
                [(_, val)] = elem.items()
                self._xe_lib.add(val)
        
        return (aVal in self._xe_lib)
   
    def _fillCalibrationCoeffs(self, prefix, calibInfos):
        """ Insert the calibration information
        
            Args:
               prefix: the prefix for constituting the UID identifying the currently treated sampleID in the fetcher object
               calibInfos: set of calib info ids that have already been included in the xml
            
            Returns: generated xml data for displaying calibration info
               
            Raises:
               exception if issue fetching data (CTBTOError)
        """
        xml = ""
        dummy_template = ""
        
        # get energy calibration 
        en_id = self._fetcher.get("%s_B_ENERGY_CAL" % (prefix), None)
        
        if (en_id is not None):
        
            # first add Energy Cal
            template = self._conf.get("SaunaTemplatingSystem", "saunaEnergyCalTemplate")
          
            # add calib info if it isn't there already
            if en_id not in calibInfos:
                energy = self._fetcher.get(en_id, {})
                dummy_template = re.sub("\${TERM0}", str(energy.get(u'BETA_COEFF1', UNDEFINED)), template)
                dummy_template = re.sub("\${TERM1}", str(energy.get(u'BETA_COEFF2', UNDEFINED)), dummy_template)
                dummy_template = re.sub("\${TERM2}", str(energy.get(u'BETA_COEFF3', UNDEFINED)), dummy_template)
                dummy_template = re.sub("\${EN_ID}", en_id, dummy_template)
                dummy_template = re.sub("\${EN_TYPE}", "Beta", dummy_template)
                # add generated xml in final container
                xml += dummy_template
                # add the id in the set of existing infos
                calibInfos.add(en_id)
        else:
            SaunaRenderer.c_log.warning("Could not find any energy calibration info for sample %s\n" % (prefix))
        
        # get energy calibration 
        en_id = self._fetcher.get("%s_G_ENERGY_CAL" % (prefix), None)
        
        if (en_id is not None):
        
            # first add Energy Cal
            template = self._conf.get("SaunaTemplatingSystem", "saunaEnergyCalTemplate")
          
            # add calib info if it isn't there already
            if en_id not in calibInfos:
                energy = self._fetcher.get(en_id, {})
                dummy_template = re.sub("\${TERM0}", str(energy.get(u'GAMMA_COEFF1', 'N/A')), template)
                dummy_template = re.sub("\${TERM1}", str(energy.get(u'GAMMA_COEFF2', 'N/A')), dummy_template)
                dummy_template = re.sub("\${TERM2}", str(energy.get(u'GAMMA_COEFF3', 'N/A')), dummy_template)
                dummy_template = re.sub("\${EN_ID}", en_id, dummy_template)
                dummy_template = re.sub("\${EN_TYPE}", "Gamma", dummy_template)
                # add generated xml in final container
                xml += dummy_template
                # add the id in the set of existing infos
                calibInfos.add(en_id)
        else:
            SaunaRenderer.c_log.warning("Could not find any energy calibration info for sample %s\n" % (prefix))
        
        return xml
        
    def _getNuclides(self, id):
        """ fill and return the information regarding the nuclides """
        
        # first add Non Quantified Nuclides
        template = self._conf.get("SaunaTemplatingSystem", "saunaNuclideTemplate")
        
        xml_nuclides = ""
        dummy_template = ""
        
        SaunaRenderer.c_log.debug("id = %s\n" % ("%s_IDED_NUCLIDES" % (id)))
        
        # get categories
        ided_nuclides = self._fetcher.get("%s_IDED_NUCLIDES" % (id), [])
        
        for nuclide in ided_nuclides:
            dummy_template = re.sub("\${NAME}", nuclide[u'NAME'], template)
            dummy_template = re.sub("\${QUANTIFIABLE}", str(self._isQuantifiable(nuclide['NAME'])).lower(), dummy_template)
            dummy_template = re.sub("\${TYPE}", str(nuclide['TYPE']), dummy_template)
            dummy_template = re.sub("\${HALFLIFE}", str(nuclide['HALFLIFE']), dummy_template)
            dummy_template = re.sub("\${CONCENTRATION}", str(nuclide['CONC']), dummy_template)
            dummy_template = re.sub("\${CONCENTRATION_ERROR}", str(nuclide['CONC_ERR']), dummy_template)
            dummy_template = re.sub("\${CONCENTRATION_ERROR_PERC}", str(nuclide.get('CONC_ERR_PERC', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${ACTIVITY}", str(nuclide['ACTIVITY']), dummy_template)
            dummy_template = re.sub("\${ACTIVITY_ERROR}", str(nuclide['ACTIVITY_ERR']), dummy_template)
            dummy_template = re.sub("\${ACTIVITY_ERROR_PERC}", str(nuclide.get('ACTIVITY_ERR_PERC', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${MDC}", "%s" % (str(nuclide['MDC'])), dummy_template)
            # LC and LD in concentration
            dummy_template = re.sub("\${LC}", "%s" % (str(nuclide['LC'])), dummy_template)
            dummy_template = re.sub("\${LD}", "%s" % (str(nuclide['LD'])), dummy_template)
            # LC and LD in activity
            dummy_template = re.sub("\${LC_ACTIVITY}", str(nuclide['LC_ACTIVITY']), dummy_template)
            dummy_template = re.sub("\${LD_ACTIVITY}", str(nuclide['LD_ACTIVITY']), dummy_template)
            dummy_template = re.sub("\${IDENTIFICATION_INDICATOR}", str(nuclide['NID_FLAG']), dummy_template)
            dummy_template = re.sub("\${IDENTIFICATION_NUM}", str(nuclide['NID_FLAG_NUM']), dummy_template)
            
            # add generated xml in final container
            xml_nuclides += dummy_template
             
        return xml_nuclides

    def _getROIInfo(self, id):
        """ fill and return the information regarding the Region of Interest (ROI) """
        
        # first add Non Quantified Nuclides
        template = self._conf.get("SaunaTemplatingSystem", "saunaRoiTemplate")
        
        xml_nuclides = ""
        dummy_template = ""
        
        # get rois info
        rois = self._fetcher.get("%s_ROI_INFO" % (id), [])
        
        for roi in rois:
            dummy_template = re.sub("\${ROINB}", str(roi[u'ROI']), template)
            dummy_template = re.sub("\${NAME}", "%s" % (roi[u'Nuclide']), dummy_template)
            dummy_template = re.sub("\${NETCOUNTS}", "%s %s" % (str(roi[u'NET_COUNT']), str(roi[u'NET_COUNT_ERR'])), dummy_template)
            dummy_template = re.sub("\${DETNETCOUNTS}", "%s %s" % (str(roi[u'DET_BKGND_COUNT']), str(roi[u'DET_BKGND_COUNT'])), dummy_template)
            dummy_template = re.sub("\${GASNETCOUNTS}", "%s %s" % (str(roi[u'GAS_BKGND_COUNT']), str(roi[u'GAS_BKGND_COUNT'])), dummy_template)
            dummy_template = re.sub("\${LC}", "%s" % (str(roi['LC'])), dummy_template)
            dummy_template = re.sub("\${LD}", "%s" % (str(roi['LD'])), dummy_template)
            dummy_template = re.sub("\${MDC}", "%s" % (str(roi['MDC'])), dummy_template)
            dummy_template = re.sub("\${EFF}", "%s" % (str(roi.get(u'EFFICIENCY', UNDEFINED))), dummy_template)
            dummy_template = re.sub("\${EFF_ERR}", "%s" % (str(roi.get(u'EFFICIENCY_ERROR', UNDEFINED))), dummy_template)
            dummy_template = re.sub("\${EFF_ERR_PERC}", "%s" % (str(roi.get(u'EFFICIENCY_ERROR_PERC', UNDEFINED))), dummy_template)
            
            # add generated xml in final container
            xml_nuclides += dummy_template
             
        return xml_nuclides
    
    def _getCategory(self, id): #IGNORE:W0613
        """ return Categorization for the passed sample_id. Do nothing for the moment """
        return ""
    
    def _getParameters(self, id): #IGNORE:W0613
        """ return Categorization for the passed sample_id. Do nothing for the moment """
        return ""
    
    def _getROIBoundaries(self, id):
        """ fill and return the information regarding the Region of Interest (ROI) Boundaries"""
        
        # first add Non Quantified Nuclides
        template = self._conf.get("SaunaTemplatingSystem", "saunaRoiBoundariesTemplate")
        
        xml_nuclides = ""
        dummy_template = ""
    
        # get boundaries info
        boundaries = self._fetcher.get("%s_ROI_BOUNDARIES" % (id), [])
        
        for bound in boundaries:
            dummy_template = re.sub("\${ROINB}", str(bound[u'ROI']), template)
            dummy_template = re.sub("\${GAMMA_LOW}", "%s" % (str(bound[u'G_ENERGY_START'])), dummy_template)
            dummy_template = re.sub("\${GAMMA_HIGH}", "%s" % (str(bound[u'G_ENERGY_STOP'])), dummy_template)
            dummy_template = re.sub("\${BETA_LOW}", "%s" % (str(bound[u'B_ENERGY_START'])), dummy_template)
            dummy_template = re.sub("\${BETA_HIGH}", "%s" % (str(bound[u'B_ENERGY_STOP'])), dummy_template)
          
            # add generated xml in final container
            xml_nuclides += dummy_template
             
        return xml_nuclides

    def _getFlags(self, id):
        """create xml part with the flag info """
        
        # first add timeliness Flags
        template = self._conf.get("SaunaTemplatingSystem", "saunaTimelinessFlagsTemplate")
        
        xml = ""
        dummy_template = ""
        dummy_template += template
          
        # Collection flags or sampling flags
        dummy_template = re.sub("\${CollectionTimeFlag}", self._fetcher.get('%s_TIME_FLAGS_COLLECTION_FLAG' % (id), UNDEFINED), dummy_template)
        
        # pretty print in hours
        v = self._fetcher.get('%s_TIME_FLAGS_COLLECTION_VAL' % (id), - 1)
        if v != - 1:
            hr = ctbto.common.time_utils.getSecondsInHours(v)
        else:
            hr = UNDEFINED
            
        dummy_template = re.sub("\${CollectionTimeValueUnit}", 'h', dummy_template)
        dummy_template = re.sub("\${CollectionTimeValue}", str(hr), dummy_template)
        dummy_template = re.sub("\${CollectionTimeTest}", self._fetcher.get('%s_TIME_FLAGS_COLLECTION_TEST' % (id), UNDEFINED), dummy_template)
        
        # Acquisition flags or sampling flags
        dummy_template = re.sub("\${AcquisitionTimeFlag}", self._fetcher.get('%s_TIME_FLAGS_ACQUISITION_FLAG' % (id), UNDEFINED), dummy_template)
        # pretty print in hours
        v = self._fetcher.get('%s_TIME_FLAGS_ACQUISITION_VAL' % (id), - 1)
        if v != - 1:
            hr = ctbto.common.time_utils.getSecondsInHours(v)
        else:
            hr = UNDEFINED
        
        dummy_template = re.sub("\${AcquisitionTimeValueUnit}", 'h', dummy_template)
        dummy_template = re.sub("\${AcquisitionTimeValue}", str(hr), dummy_template)
        dummy_template = re.sub("\${AcquisitionTimeTest}", self._fetcher.get('%s_TIME_FLAGS_ACQUISITION_TEST' % (id), UNDEFINED), dummy_template)
        
        # Decay flags
        dummy_template = re.sub("\${DecayTimeFlag}", self._fetcher.get('%s_TIME_FLAGS_DECAY_FLAG' % (id), UNDEFINED), dummy_template)
        # pretty print in hours
        v = self._fetcher.get('%s_TIME_FLAGS_DECAY_VAL' % (id), - 1)
        if v != - 1:
            hr = ctbto.common.time_utils.getSecondsInHours(v)
        else:
            hr = UNDEFINED
        
        # uniti is hour
        dummy_template = re.sub("\${DecayTimeValueUnit}", 'h', dummy_template)
        dummy_template = re.sub("\${DecayTimeValue}", str(hr), dummy_template)
        dummy_template = re.sub("\${DecayTimeTest}", self._fetcher.get('%s_TIME_FLAGS_DECAY_TEST' % (id), UNDEFINED), dummy_template)
        
        # respondTimeFlag
        dummy_template = re.sub("\${RespondTimeFlag}", self._fetcher.get('%s_TIME_FLAGS_RESPOND_TIME_FLAG' % (id), UNDEFINED), dummy_template)
        # pretty print in hours
        v = self._fetcher.get('%s_TIME_FLAGS_RESPOND_TIME_VAL' % (id), - 1)
        if v != - 1:
            hr = ctbto.common.time_utils.getSecondsInHours(v)
        else:
            hr = UNDEFINED
            
        dummy_template = re.sub("\${RespondTimeValueUnit}", 'h', dummy_template)
        dummy_template = re.sub("\${RespondTimeValue}", str(hr), dummy_template)
        dummy_template = re.sub("\${RespondTimeTest}", self._fetcher.get('%s_TIME_FLAGS_RESPOND_TIME_TEST' % (id), UNDEFINED), dummy_template)
        
        xml += dummy_template
            
        # Data Quality Flags
        template = self._conf.get("SaunaTemplatingSystem", "saunaDataQualityFlagsTemplate")    
        dummy_template = template
        
        # Xenon Vol Flag
        dummy_template = re.sub("\${XeVolumeFlag}", self._fetcher.get('%s_VOLUME_FLAG' % (id), UNDEFINED), dummy_template)
        dummy_template = re.sub("\${XeVolumeValueUnit}", 'ml', dummy_template)
        dummy_template = re.sub("\${XeVolumeValue}", str(self._fetcher.get('%s_VOLUME_VAL' % (id), UNDEFINED)), dummy_template)
        dummy_template = re.sub("\${XeVolumeTest}", self._fetcher.get('%s_VOLUME_TEST' % (id), UNDEFINED), dummy_template)
       
        # add generated xml in final container
        xml += dummy_template
        
        return xml
    
    def _fillAnalysisResults(self, requestDict):
        """fill the analysis results for each result"""
        
        # check if there is a spectrum in the hashtable. If not replace ${SPECTRUM} by an empty string ""
        requestedTypes = requestDict[RequestParser.ANALYSIS]
        
        all_analyses_xml = ""
      
        for ty in requestedTypes:
           
            #identifier in the dict for this analysis  
            sindict_id = self._fetcher.get("CURRENT_%s" % (ty), None)
           
            if sindict_id is not None:
        
                # first get the template
                template = self._conf.get("SaunaTemplatingSystem", "saunaAnalysisTemplate")
                dummy_template = ""
        
                # for the moment only one result
                dummy_template += template
   
                #spectrum_id = self._fetcher.get("%s_DATA_G_ID" % (self._fetcher.get("CURRENT_%s" % (ty), '')), "n/a")
                #use group id now 
                spectrum_gid = self._fetcher.get("%s_DATA_NAME" % (self._fetcher.get("CURRENT_%s" % (ty), '')), "n/a")
             
                # Add analysis identifier => SpectrumID prefixed by AN
                dummy_template = re.sub("\${ANALYSIS_ID}", "AN-%s" % (spectrum_gid), dummy_template)
        
                dummy_template = re.sub("\${SPECTRUM_ID}", spectrum_gid, dummy_template)
        
                dummy_template = re.sub("\${CATEGORY}", self._getCategory(sindict_id), dummy_template)
        
                dummy_template = re.sub("\${NUCLIDES}", self._getNuclides(sindict_id), dummy_template)
             
                dummy_template = re.sub("\${ROIINFO}", self._getROIInfo(sindict_id), dummy_template)
             
                dummy_template = re.sub("\${ROIBOUNDARIES}", self._getROIBoundaries(sindict_id), dummy_template)
             
                dummy_template = re.sub("\${PARAMETERS}", self._getParameters(sindict_id), dummy_template)
        
                dummy_template = re.sub("\${FLAGS}", self._getFlags(sindict_id), dummy_template)
             
                #add Calibration references
                l = self._fetcher.get("%s_G_DATA_ALL_CALS" % (sindict_id))
                if l is None :
                    SaunaRenderer.c_log.warning("No calibration information for sample %s" % (ty))
                    l = []
                else:
                    # add calibration info
                    dummy_template = re.sub("\${CAL_INFOS}", ' '.join(map(str, l)), dummy_template) #IGNORE:W0141
        
                # add software method version info
                dummy_template = re.sub("\${SOFTWARE}", "bg_analyse", dummy_template)
                dummy_template = re.sub("\${METHOD}", "standard", dummy_template)
                dummy_template = re.sub("\${VERSION}", "1.0", dummy_template)
                dummy_template = re.sub("\${SOFTCOMMENTS}", "Old version", dummy_template)
             
                all_analyses_xml += dummy_template
        
            # add all the analysis info in the global template
            self._populatedTemplate = re.sub("\${AnalysisResults}", all_analyses_xml, self._populatedTemplate)
         
    def _fillCalibration(self):
        """ Add the calibration parameters for each of the spectrum"""
        
        xml = ""
        # list of ids added in the xml document
        addedCalibrationIDs = set()
        
        for ty in self._fetcher.get('CONTENT_PRESENT', []):
            
            # treat preliminary samples differently as there is another indirection
            if ty == 'PREL':
                for prefix in self._fetcher.get('CURR_List_OF_PRELS', []):
                    if prefix is None:
                        raise CTBTOError(- 1, "Error when filling Calibration info for prefix %s, There is no CURRENT_%s in the dataBag\n" % (prefix, prefix))
                
                    xml += self._fillCalibrationCoeffs(prefix, addedCalibrationIDs)    
            else:
                prefix = self._fetcher.get(u'CURRENT_%s' % (ty), None)
                if prefix is None:
                    raise CTBTOError(- 1, "Error when fetching Calibration info for prefix %s, There is no CURRENT_%s in the dataBag\n" % (prefix, prefix))
               
                xml += self._fillCalibrationCoeffs(prefix, addedCalibrationIDs)      
            
        # out of the loop
        self._populatedTemplate = re.sub("\${CALIBRATION}", xml, self._populatedTemplate)
       
        
    def _fillData(self, requestDict):
        """ Insert the spectrum data expected as defined in the initial passed request
        
            Args:
               requestDict: dictionary representing the different elements of the request (analysis, spectrum, ...)
            
            Returns: Nothing
              
              
            Raises:
               exception if issue fetching data (CTBTOError)
        """
    
        # check if there is a spectrum in the hashtable. If not replace ${SPECTRUM} by an empty string ""
        requestedTypes = requestDict[RequestParser.SPECTRUM]
        
        if 'PREL' in requestedTypes:
            # add all prels found in CURR_List_OF_PRELS in the set
            requestedTypes.remove('PREL')
            requestedTypes.update(self._fetcher.get(u'CURR_List_OF_PRELS', []))
        
        spectrums = self._sortSpectrumsSet(requestedTypes)
        
        finalTemplate = ""
        
        for ty in spectrums:
            
            #group Template            
            spectrumTemplate = self._conf.get("SaunaTemplatingSystem", "saunaSpectrumGroupTemplate")
            
            # add the general parameters
            spectrumTemplate = re.sub("\${SPECTRUM_GROUP_ID}",self._fetcher.get("%s_DATA_NAME" % (ty)), spectrumTemplate)
            spectrumTemplate = re.sub("\${COL_START}", str(self._fetcher.get("%s_DATA_COLLECT_START" % (ty))), spectrumTemplate)
            spectrumTemplate = re.sub("\${COL_STOP}", str(self._fetcher.get("%s_DATA_COLLECT_STOP" % (ty))), spectrumTemplate)
            spectrumTemplate = re.sub("\${ACQ_START}", str(self._fetcher.get("%s_DATA_ACQ_START" % (ty))), spectrumTemplate)
            spectrumTemplate = re.sub("\${ACQ_STOP}", str(self._fetcher.get("%s_DATA_ACQ_STOP" % (ty))), spectrumTemplate)
            spectrumTemplate = re.sub("\${SAMPLING_TIME}", str(self._fetcher.get("%s_DATA_SAMPLING_TIME" % (ty))), spectrumTemplate)
            spectrumTemplate = re.sub("\${REAL_ACQ_TIME}", str(self._fetcher.get("%s_DATA_ACQ_REAL_SEC" % (ty))), spectrumTemplate)
            spectrumTemplate = re.sub("\${LIVE_ACQ_TIME}", str(self._fetcher.get("%s_DATA_ACQ_LIVE_SEC" % (ty))), spectrumTemplate)
            spectrumTemplate = re.sub("\${ARRIVAL_DATE}", str(self._fetcher.get("%s_DATA_TRANSMIT_DTG" % (ty))), spectrumTemplate)
              
            spectrumTemplate = re.sub("\${DECAY_TIME}", str(self._fetcher.get("%s_DATA_DECAY_TIME" % (ty))), spectrumTemplate)
             
            spectrumTemplate = re.sub("\${SPECTRUM_TYPE}",str(self._fetcher.get("%s_DATA_SPECTRAL_QUALIFIER" % (ty))), spectrumTemplate)
            spectrumTemplate = re.sub("\${MEASUREMENT_TYPE}",str(self._fetcher.get("%s_DATA_DATA_TYPE" % (ty))), spectrumTemplate)
            # add quantity and geometry
            spectrumTemplate = re.sub("\${QUANTITY}", str(self._fetcher.get("%s_DATA_SAMPLE_QUANTITY" % (ty))), spectrumTemplate)
            spectrumTemplate = re.sub("\${FLOW_RATE}", str(self._fetcher.get("%s_DATA_FLOW_RATE" % (ty))), spectrumTemplate)
                
            spectrumTemplate = re.sub("\${GEOMETRY}", str(self._fetcher.get("%s_DATA_SAMPLE_GEOMETRY" % (ty))), spectrumTemplate)
            
            # add the calibration info
            l = self._fetcher.get("%s_G_DATA_ALL_CALS" % (ty))
            if l is None:
                SaunaRenderer.c_log.warning("No calibration information for sample %s" % (ty))
                l = []
            
            spectrumTemplate = re.sub("\${CAL_INFOS}", ' '.join(map(str, l)), spectrumTemplate) #IGNORE:W0141
              
            dataTemplate=""
            # add spectra
            l = ["%s_DATA_G" % (ty), "%s_DATA_B" % (ty)]
            for fname in l:
                data = self._fetcher.get(fname, None)
                if data is not None:
                    # add gamma Spectrum
                    sTemplate = self._conf.get("SaunaTemplatingSystem", "saunaSpectrumTemplate")
                    # insert energy and channel span
                    sTemplate = re.sub("\${SPECTRUM_DATA_CHANNEL_SPAN}", str(self._fetcher.get("%s_CHANNEL_SPAN" % (fname))), sTemplate)
                    sTemplate = re.sub("\${SPECTRUM_DATA_ENERGY_SPAN}",  str(self._fetcher.get("%s_ENERGY_SPAN" % (fname))) , sTemplate)
                    # insert spectrum ID
                    sTemplate = re.sub("\${SPECTRUM_ID}", self._fetcher.get("%s_ID" % (fname)), sTemplate)
                    sTemplate = re.sub("\${S_TYPE}", self._fetcher.get("%s_TY" % (fname)), sTemplate)
                    
                    # insert data
                    sTemplate = re.sub("\${SPECTRUM_DATA}", data, sTemplate)
                    
                    # TODO to remove just there for testing, deal with the compression flag
                    if self._fetcher.get("%s_COMPRESSED" % (fname), False):
                        sTemplate = re.sub("\${COMPRESS}", "compress=\"base64,zip\"", sTemplate)
                    else:
                        sTemplate = re.sub("\${COMPRESS}", "", sTemplate)
            
                    dataTemplate += sTemplate
            
            #add histogram
            fname = "%s_DATA_H" % (ty)
            data = self._fetcher.get(fname, None)
            if data is not None:
                hTemplate = self._conf.get("SaunaTemplatingSystem", "saunaHistogramTemplate")
              
                # insert data
                hTemplate = re.sub("\${H_DATA}", data, hTemplate)
              
                # insert spectrum ID
                hTemplate = re.sub("\${H_ID}", self._fetcher.get("%s_ID" % (fname)), hTemplate)
                hTemplate = re.sub("\${H_TYPE}", self._fetcher.get("%s_TY" % (fname)), hTemplate)
                
                
                # insert energy and channel span for beta and gamma
                hTemplate = re.sub("\${H_G_DATA_CHANNEL_SPAN}", str(self._fetcher.get("%s_DATA_G_CHANNEL_SPAN" % (ty))), hTemplate)
                hTemplate = re.sub("\${H_G_DATA_ENERGY_SPAN}", str(self._fetcher.get("%s_DATA_G_ENERGY_SPAN" % (ty))), hTemplate)
                hTemplate = re.sub("\${H_B_DATA_CHANNEL_SPAN}", str(self._fetcher.get("%s_DATA_B_CHANNEL_SPAN" % (ty))), hTemplate)
                hTemplate = re.sub("\${H_B_DATA_ENERGY_SPAN}", str(self._fetcher.get("%s_DATA_B_ENERGY_SPAN" % (ty))), hTemplate)
            
                # TODO to remove just there for testing, deal with the compression flag
                if self._fetcher.get("%s_COMPRESSED" % (fname), False):
                    hTemplate = re.sub("\${COMPRESS}", "compress=\"base64,zip\"", hTemplate)
                else:
                    hTemplate = re.sub("\${COMPRESS}", "", hTemplate)
                
                dataTemplate += hTemplate
                
            
            #Add all found data in group Spectrum
            spectrumTemplate = re.sub("\${GSPECTRUMDATA}",dataTemplate,spectrumTemplate)
            
            
            # add groupTemplate in finalTemplate
            finalTemplate += spectrumTemplate
                
        self._populatedTemplate = re.sub("\${DATA}", finalTemplate, self._populatedTemplate)
    
        
class GenieParticulateRenderer(BaseRenderer):
    
    # Class members
    c_log = logging.getLogger("SAMPMLrendererv1.GenieParticulateRenderer")
    c_log.setLevel(logging.INFO)
    
      
    def __init__(self, aDataFetcher):
        
        super(GenieParticulateRenderer, self).__init__(aDataFetcher)
        
        # add values specific to Particulates
        dummy_dict = {  
                        # to be changed as only one analysis is supported at the moment
                        "SPECTRUM_ID"                    :   "CURR_DATA_ID"
                      }
        # add specific particulate keys
        self._substitutionDict.update(dummy_dict)
    
    def _createTemplate(self):
        """ Read the template from a file. Old method now everything is read from the conf """
        
        # get template path from conf
        self._template = self._conf.get("ParticulateTemplatingSystem", "particulateBaseTemplate")
        
        #old method
        # get template path from conf
        #path = self._conf.get("ParticulateTemplatingSystem", "ParticulateBaseTemplate")
        # assert that the file exists
        #ctbto.common.utils.file_exits(path)
        # read the full template in a string buffer
        #f = open(path, "r") 
        #self._template = f.read()
        
        self._populatedTemplate = self._template
      
    def _fillData(self, requestDict):
        """ Insert the spectrum data expected as defined in the initial passed request
        
            Args:
               requestDict: dictionary representing the different elements of the request (analysis, spectrum, ...)
            
            Returns: Nothing
              
              
            Raises:
               exception if issue fetching data (CTBTOError)
        """
    
        # check if there is a spectrum in the hashtable. If not replace ${SPECTRUM} by an empty string ""
        requestedTypes = requestDict[RequestParser.SPECTRUM]
        
        if 'PREL' in requestedTypes:
            # add all prels found in CURR_List_OF_PRELS in the set
            requestedTypes.remove('PREL')
            requestedTypes.update(self._fetcher.get(u'CURR_List_OF_PRELS', []))
        
        spectrums = self._sortSpectrumsSet(requestedTypes)
        
        
        finalTemplate = ""
        
      
        for ty in spectrums:
            
            spectrumTemplate = ""
            
            # add Spectrum
            fname = "%s_G_DATA" % (ty)
              
            data = self._fetcher.get(fname, None)
            
            if data is not None:
               
                spectrumTemplate = self._conf.get("ParticulateTemplatingSystem", "particulateSpectrumTemplate")
              
                # insert data
                spectrumTemplate = re.sub("\${SPECTRUM_DATA}", data, spectrumTemplate)
              
                # insert spectrum ID
                spectrumTemplate = re.sub("\${SPECTRUM_ID}", self._fetcher.get("%s_ID" % (fname)), spectrumTemplate)
            
                # insert energy and channel span
                spectrumTemplate = re.sub("\${SPECTRUM_DATA_CHANNEL_SPAN}", str(self._fetcher.get("%s_CHANNEL_SPAN" % (fname))), spectrumTemplate)
                spectrumTemplate = re.sub("\${SPECTRUM_DATA_ENERGY_SPAN}", str(self._fetcher.get("%s_ENERGY_SPAN" % (fname))), spectrumTemplate)
            
                # get the date information
                spectrumTemplate = re.sub("\${COL_START}", str(self._fetcher.get("%s_COLLECT_START" % (fname))), spectrumTemplate)
                spectrumTemplate = re.sub("\${COL_STOP}", str(self._fetcher.get("%s_COLLECT_STOP" % (fname))), spectrumTemplate)
                spectrumTemplate = re.sub("\${ACQ_START}", str(self._fetcher.get("%s_ACQ_START" % (fname))), spectrumTemplate)
                spectrumTemplate = re.sub("\${ACQ_STOP}", str(self._fetcher.get("%s_ACQ_STOP" % (fname))), spectrumTemplate)
                spectrumTemplate = re.sub("\${SAMPLING_TIME}", str(self._fetcher.get("%s_SAMPLING_TIME" % (fname))), spectrumTemplate)
                spectrumTemplate = re.sub("\${REAL_ACQ_TIME}", str(self._fetcher.get("%s_ACQ_REAL_SEC" % (fname))), spectrumTemplate)
                spectrumTemplate = re.sub("\${LIVE_ACQ_TIME}", str(self._fetcher.get("%s_ACQ_LIVE_SEC" % (fname))), spectrumTemplate)
              
                spectrumTemplate = re.sub("\${DECAY_TIME}", str(self._fetcher.get("%s_DECAY_TIME" % (fname))), spectrumTemplate)
                spectrumTemplate = re.sub("\${SPECTRUM_TYPE}", str(self._fetcher.get("%s_SPECTRAL_QUALIFIER" % (fname))), spectrumTemplate)
                spectrumTemplate = re.sub("\${MEASUREMENT_TYPE}", str(self._fetcher.get("%s_DATA_TYPE" % (fname))), spectrumTemplate)
              
                # add quantity and geometry
                spectrumTemplate = re.sub("\${QUANTITY}", str(self._fetcher.get("%s_SAMPLE_QUANTITY" % (fname))), spectrumTemplate)
                spectrumTemplate = re.sub("\${GEOMETRY}", str(self._fetcher.get("%s_SAMPLE_GEOMETRY" % (fname))), spectrumTemplate)
              
                l = self._fetcher.get("%s_ALL_CALS" % (fname))
                if l is None:
                    raise CTBTOError(- 1, "Error no calibration information for sample %s\n" % (ty))
             
                # add calibration info
                spectrumTemplate = re.sub("\${CAL_INFOS}", ' '.join(map(str, l)), spectrumTemplate) #IGNORE:W0141
              
                # to remove just there for testing, deal with the compression flag
                if self._fetcher.get("%s_COMPRESSED" % (fname), False):
                    spectrumTemplate = re.sub("\${COMPRESS}", "compress=\"base64,zip\"", spectrumTemplate)
                else:
                    spectrumTemplate = re.sub("\${COMPRESS}", "", spectrumTemplate)
                     
                # add fill spectrum template in global template 
                finalTemplate += spectrumTemplate
        
        self._populatedTemplate = re.sub("\${SPECTRUM}", finalTemplate, self._populatedTemplate)
        
     
    def _getCategory(self, id):
        """Get the Catgeory Information from the data hashtable and render it.
           If there are no category information insert an empty tag.
        
            Args:
               id: to fetch the info in the dict
        
            Returns:
              
              
            Raises:
               exception
        """
        dummy_template = "" 
       
        # first get the category info for this particular sample
        cat_dict = self._fetcher.get(u'%s_CAT_INFOS' % (id), {})
       
        # get the status. If it is R or Q get category otherwise it isn't defined yet
        status = cat_dict.get(u'CAT_STATUS', "")
        
        # TODO: If Status is P then add autoCategory tag otherwise nothing
        # If status == R or Q add CATEGORY and AUTOMATIC CATEGORY
        # If status == P only add AUTOMATIC CATEGORY
        # Possibly add status Processed, Released, Queued and Release Date
        if (status == 'R') or (status == 'Q') or (status == 'P'):
            category = cat_dict.get(u'CAT_CATEGORY',None)
            comment  = cat_dict.get(u'CAT_COMMENT', "No Comment")
            auto_category = cat_dict.get(u'CAT_AUTO_CATEGORY',None)
            
            # if there is something fill the template otherwise do nothing
            if category != None:
                # xml filler 
                cat_template = self._conf.get("ParticulateTemplatingSystem", "particulateCategoryTemplate")
        
                dummy_template = re.sub("\${CATEGORY}", str(category), cat_template)
                dummy_template = re.sub("\${CATEGORY_COMMENT}", comment, dummy_template)
                dummy_template = re.sub("\${AUTO_CATEGORY}",str(auto_category),dummy_template)
                
            elif auto_category != None:
                # xml filler 
                cat_template = self._conf.get("ParticulateTemplatingSystem", "particulateAutoCategoryTemplate")
                dummy_template = re.sub("\${AUTO_CATEGORY}",str(auto_category),cat_template)
        
        return dummy_template
    
    def _getNuclides(self, id):
        """ fill and return the information regarding the nuclides """
        
        # first add Non Quantified Nuclides
        template = self._conf.get("ParticulateTemplatingSystem", "particulateNuclideTemplate")
        
        xml_nuclides = ""
        dummy_template = ""
       
        GenieParticulateRenderer.c_log.debug("id = %s\n" % ("%s_IDED_NUCLIDES" % (id)))
        
        # get categories
        ided_nuclides = self._fetcher.get("%s_IDED_NUCLIDES" % (id), [])
        
        for nuclide in ided_nuclides:
            dummy_template = re.sub("\${REPORTMDA}", (("true") if nuclide['REPORT_MDA'] == 1 else "false"), template)
            dummy_template = re.sub("\${QUANTIFIABLE}", str(self._isQuantifiable(nuclide['NAME'])).lower(), dummy_template)
            dummy_template = re.sub("\${NAME}", nuclide['NAME'], dummy_template)
            dummy_template = re.sub("\${TYPE}", nuclide['TYPE'], dummy_template)
            dummy_template = re.sub("\${HALFLIFE}", str(nuclide['HALFLIFE']), dummy_template)
            dummy_template = re.sub("\${CONCENTRATION}", str(nuclide['ACTIV_KEY']), dummy_template)
            dummy_template = re.sub("\${CONCENTRATION_ERROR}", str(nuclide['ACTIV_KEY_ERR']), dummy_template)
            dummy_template = re.sub("\${MDA}", "%s %s" % (str(nuclide['MDA']), str(nuclide['MDA_ERR'])), dummy_template)
            dummy_template = re.sub("\${IDENTIFICATION_INDICATOR}", str(nuclide['NID_FLAG']), dummy_template)
            dummy_template = re.sub("\${IDENTIFICATION_NUM}", str(nuclide['NID_FLAG_NUM']), dummy_template)
            
            # add generated xml in final container
            xml_nuclides += dummy_template
             
        return xml_nuclides
    
    def _isQuantifiable(self, aVal):
        """ true if quantifiable, false otherwise """
        nucl2quantify = self._fetcher.get("NUCLIDES_2_QUANTIFY")
     
        # if set hasn't been populated do it
        if len(self._quantifiable) == 0:
            # create a set containing all quantifiable elements
            for elem in nucl2quantify:
                [(_, val)] = elem.items()
                self._quantifiable.add(val)
        
        return (aVal in self._quantifiable)
            
        
    def _getNuclideLines(self, id):
        """Get the Nuclide Lines information from the data hashtable and render it.
        
            Args:
               id: to fetch the info in the dict
        
            Returns:
              An XML string containing the formatted data.
              
            Raises:
               exception
        """
        
        # check if we need nuclidelines otherwise quit
        if self._conf.getboolean("Options", "addNuclideLines") is False:
            SaunaRenderer.c_log.info("Configuration says no nuclide lines")
            return ""
        
        # get the global template
        global_template = self._conf.get("ParticulateTemplatingSystem", "particulateNuclideLinesTemplate")
        
        # first get Nuclide Lines template
        template = self._conf.get("ParticulateTemplatingSystem", "particulateOneNuclideLineTemplate")
        
        xml_nuclidelines = ""
        dummy_template = ""
        
        # get categories
        nuclidelines = self._fetcher.get(u'%s_IDED_NUCLIDE_LINES' % (id), [])
        
        for line in nuclidelines:
            
            # if there is a peakID in the hash then replace it otherwise remove this info from the XML
            dummy_template = re.sub("\${PEAKID}", ("peakID=\"%s\"" % (line['PEAK']) if (line.get('PEAK', 0) != 0) else ""), template)
            dummy_template = re.sub("\${NAME}", line['NAME'], dummy_template)
            dummy_template = re.sub("\${MDA}", "%s" % (str(line['MDA'])), dummy_template)
           
            dummy_template = re.sub("\${ACTIVTIY}", (("<Activity unit=\"mBq\">%s %s</Activity>" % (str(line['ACTIVITY']), str(line['ACTIV_ERR']))) if not (line['ACTIVITY'] == 0) else ""), dummy_template)
            dummy_template = re.sub("\${ENERGY}", ("<Energy unit=\"keV\">%s %s</Energy>" % (str(line['ENERGY']), str(line['ENERGY_ERR'])) if ('ENERGY' in line) else ""), dummy_template)
            dummy_template = re.sub("\${ABUNDANCE}", ("<Abundance unit=\"percent\">%s %s</Abundance>" % (str(line['ABUNDANCE']), str(line['ABUNDANCE_ERR'])) if ('ABUNDANCE' in line) else ""), dummy_template)
            dummy_template = re.sub("\${EFFICIENCY}", ("<Efficiency unit=\"percent\">%s %s</Efficiency>" % (str(line['EFFIC']), str(line['EFFIC_ERR'])) if ('EFFIC' in line) else ""), dummy_template)
            
            # add generated xml in final container
            xml_nuclidelines += dummy_template
            
        #add nuclide lines in global template
        return re.sub("\${NUCLIDELINES}", xml_nuclidelines, global_template)
    
    def _getPeaks(self, id):
        """Get the peaks information from the data hashtable and render it .

         Args: 
           id: to fetch the info in the dict
          

         Returns:
           An XML String containing the formatted data.

         Raises:
          None.
        """
  
        peak_template = self._conf.get("ParticulateTemplatingSystem", "peaksTemplate")
        
        xml_peaks = ""
        dummy_template = ""
        
        # get peak
        peaks = self._fetcher.get(u'%s_PEAKS' % (id), {})
        
        for peak in peaks:
            dummy_template = re.sub("\${ENERGY}", "%s %s" % (str(peak['ENERGY']), str(peak['ENERGY_ERR'])), peak_template)
            dummy_template = re.sub("\${PEAKID}", "%s" % (str(peak['PEAK_ID'])), dummy_template)
            dummy_template = re.sub("\${CENTROID}", "%s %s" % (str(peak['CENTROID']), str(peak['CENTROID_ERR'])), dummy_template)
            dummy_template = re.sub("\${AREA}", "%s %s" % (str(peak['AREA']), str(peak['AREA_ERR'])), dummy_template)
            dummy_template = re.sub("\${WIDTH}", str(peak['WIDTH']), dummy_template)
            dummy_template = re.sub("\${FWHM}", "%s %s" % (str(peak['FWHM']), str(peak['FWHM_ERR'])), dummy_template)
            dummy_template = re.sub("\${BACKGROUNDCOUNTS}", "%s %s" % (str(peak['BACK_COUNT']), str(peak['BACK_UNCER'])), dummy_template)
            dummy_template = re.sub("\${EFFICIENCY}", "%s %s" % (str(peak['EFFICIENCY']), str(peak['EFF_ERROR'])), dummy_template)
            dummy_template = re.sub("\${LC}", str(peak['LC']), dummy_template)
            
            # to be checked with Romano
            dummy_template = re.sub("\${LD}", UNDEFINED, dummy_template)
            dummy_template = re.sub("\${DETECTIBILITY}", str(peak.get('DETECTABILITY', UNDEFINED)), dummy_template)
            
            dummy_template = re.sub("\${NUCLIDE}", UNDEFINED, dummy_template)
            # to be checked
            dummy_template = re.sub("\${NUCLIDE_PERCENTAGE}", str(100), dummy_template)
            
            # add generated xml in final container
            xml_peaks += dummy_template
               
        return xml_peaks
    
    def _getParameters(self, id):
        """Get the parameters information from the data hashtable and render it .

         Args: 
           id: to fetch the info in the dict
          

         Returns:
           An XML String containing the formatted data.

         Raises:
          None.
        """
        
         # first add Quantified Nuclides
        template = self._conf.get("ParticulateTemplatingSystem", "processingParametersTemplate")
        
        xml_parameters = ""
        dummy_template = ""
        
        # get processing parameters
        parameters = self._fetcher.get("%s_PROCESSING_PARAMETERS" % (id), None)
        
        if (parameters is not None) and (len(parameters) > 0) :
            dummy_template = re.sub("\${THRESHOLD}", parameters.get('THRESHOLD', UNDEFINED), template)
            dummy_template = re.sub("\${PEAK_START}", str(parameters.get('PEAK_START', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${PEAK_END}", str(parameters.get('PEAK_END', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${LEFT_FWHM}", str(parameters.get('LEFT_FWHM_LIM', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${RIGHT_FWHM}", str(parameters.get('RIGHT_FWHM_LIM', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${MULTI_FWHM}", str(parameters.get('FWHM_MULT_WIDTH', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${FIT_SINGLETS}", str(parameters.get('FIT_SINGLETS', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${CRITICAL_LEV_TEST}", str(parameters.get('CRIT_LEVEL', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${ESTIMATED_PEAK_WIDTHS}", str(parameters.get('MDC_WIDTH', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${BASELINE_TYPE}", str(parameters.get('BACK_TYPE', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${BASELINE_CHANNELS}", str(parameters.get('BACK_CHAN', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${SUBSTRACTION}", str(parameters.get('ToBeDefined', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${ENERGY_TOLERANCE}", str(parameters.get('ENERGY_TOL', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${CONFIDENCE_THRESHOLD}", str(parameters.get('NID_CONFID', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${RISK_LEVEL}", str(parameters.get('ToBeDefined', UNDEFINED)), dummy_template)
               
        # add generated xml in final container
        xml_parameters += dummy_template
       
        # add Update parameters
        # first add Quantified Nuclides
        template = self._conf.get("ParticulateTemplatingSystem", "updateParametersTemplate")
        dummy_template = ""
        
        # get update parameters
        parameters = self._fetcher.get("%s_UPDATE_PARAMETERS" % (id), {})
        
        if (parameters is not None) and (len(parameters) > 0):
            dummy_template = re.sub("\${USE_MRP}", str(parameters.get('MRP_USED', UNDEFINED)), template)
            dummy_template = re.sub("\${MRP_SAMPLEID}", str(parameters.get('MRP_SAMPLE_ID', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${GAIN_SHIFT}", str(parameters.get('GAINSHIFT', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${ZERO_SHIFT}", str(parameters.get('ZEROSHIFT', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${AREA_LIMIT}", str(parameters.get('AREA_LIM', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${USE_WEIGHT}", str(parameters.get('USE_WEIGHT', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${USE_MULTIPLET}", str(parameters.get('USE_MULT', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${FORCE_LINEAR}", str(parameters.get('F_LINEAR', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${IGNORE_PREVIOUS_ECR}", str(parameters.get('BOOTSTRAP', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${MINIMUM_LIB_LOOKUP_TOLERANCE}", str(parameters.get('MIN_LOOKUP', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${RER_INTERCEPT}", str(parameters.get('RER_INTERCEPT', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${RER_SLOPE}", str(parameters.get('RER_SLOPE', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${ECR_SLOPE}", str(parameters.get('ECR_SLOPE', UNDEFINED)), dummy_template)
            dummy_template = re.sub("\${DO_RESOLUTION_UPDATE}", str(parameters.get('DO_RERU', UNDEFINED)), dummy_template)
            
        # add generated xml in final container
        xml_parameters += dummy_template
       
        return xml_parameters
        
    def _getFlags(self, id):
        """create xml part with the flag info """
        
        # first add timeliness Flags
        template = self._conf.get("ParticulateTemplatingSystem", "timelinessFlagsTemplate")
        
        xml = ""
        dummy_template = ""
        dummy_template += template
          
        param = self._fetcher.get('%s_TIME_FLAGS_PREVIOUS_SAMPLE' % (id), False)
        if param:
            dummy_template = re.sub("\${PreviousSamplePresent}", "true", dummy_template)
        else:
            dummy_template = re.sub("\${PreviousSamplePresent}", "false", dummy_template)
        
        param = self._fetcher.get('%s_TIME_FLAGS_COLLECTION_WITHIN_24' % (id), 0)
        if param == 0:
            dummy_template = re.sub("\${CollectionTime}", "true", dummy_template)
        else:
            dummy_template = re.sub("\${CollectionTime}", "false", dummy_template)
            
        param = self._fetcher.get('%s_TIME_FLAGS_ACQUISITION_FLAG' % (id), 0)
        if param == 0:
            dummy_template = re.sub("\${AcquisitionTime}", "true", dummy_template)
        else:
            dummy_template = re.sub("\${AcquisitionTime}", "false", dummy_template)
        
        param = self._fetcher.get('%s_TIME_FLAGS_DECAY_FLAG' % (id), 0)
        if param == 0:
            dummy_template = re.sub("\${DecayTime}", "true", dummy_template)
        else:
            dummy_template = re.sub("\${DecayTime}", "false", dummy_template)
            
        param = self._fetcher.get('%s_TIME_FLAGS_SAMPLE_ARRIVAL_FLAG' % (id), 0)
        if param == 0:
            dummy_template = re.sub("\${SampleReceived}", "true", dummy_template)
        else:
            dummy_template = re.sub("\${SampleReceived}", "false", dummy_template)
       
        # add generated xml in final container
        xml += dummy_template
        
        # get Data Quality Flags
        template = self._conf.get("ParticulateTemplatingSystem", "dataQualityFlagsTemplate")
        
        # add Data Quality Flags
        dataQFlags = self._fetcher.get('%s_DATA_QUALITY_FLAGS' % (id), [])
        
        # list of all flags found
        dq_xml = ""
        
        if len(dataQFlags) > 0:
            for flag in dataQFlags:
                name = flag['DQ_NAME']
              
                # check if it has a template if not ignore.
              
                dummy_template = self._conf.get("ParticulateTemplatingSystem", "dataQFlags_%s_Template" % (name), None)
                if dummy_template != None:
                    dummy_template = re.sub("\${%s_VAL}" % (name), str(flag['DQ_VALUE']), dummy_template)
                    dummy_template = re.sub("\${%s_PASS}" % (name), str(flag['DQ_RESULT']), dummy_template)
                    dummy_template = re.sub("\${%s_THRESOLD}" % (name), str(flag['DQ_THRESHOLD']), dummy_template)
                 
                    # add non empty template to data flags
                    dq_xml += dummy_template
              
        template = re.sub("\${DQ_FLAGS}", dq_xml, template)
        
        # replace global data quality flag template
        xml += template
           
        return xml
        
    def _fillAnalysisResults(self, requestDict):
        """fill the analysis results for each result"""
        
        # check if there is a spectrum in the hashtable. If not replace ${SPECTRUM} by an empty string ""
        requestedTypes = requestDict[RequestParser.ANALYSIS]
        
        all_analyses_xml = ""
      
        for ty in requestedTypes:
           
            #identifier in the dict for this analysis  
            sindict_id = self._fetcher.get("CURRENT_%s" % (ty), None)
           
            if sindict_id is not None:
        
                # first get the template
                template = self._conf.get("ParticulateTemplatingSystem", "particulateAnalysisTemplate")
                dummy_template = ""
        
                # for the moment only one result
                dummy_template += template
        
                spectrum_id = self._fetcher.get("%s_G_DATA_ID" % (self._fetcher.get("CURRENT_%s" % (ty), '')), "n/a")
             
                # Add analysis identifier => SpectrumID prefixed by AN
                dummy_template = re.sub("\${ANALYSISID}", "AN-%s" % (spectrum_id), dummy_template)
        
                dummy_template = re.sub("\${SPECTRUM_ID}", spectrum_id, dummy_template)
        
                dummy_template = re.sub("\${CATEGORY}", self._getCategory(sindict_id), dummy_template)
        
                dummy_template = re.sub("\${NUCLIDES}", self._getNuclides(sindict_id), dummy_template)
         
                dummy_template = re.sub("\${WITHNUCLIDELINES}", self._getNuclideLines(sindict_id), dummy_template)
        
                dummy_template = re.sub("\${PEAKS}", self._getPeaks(sindict_id), dummy_template)
         
                dummy_template = re.sub("\${PARAMETERS}", self._getParameters(sindict_id), dummy_template)
        
                dummy_template = re.sub("\${FLAGS}", self._getFlags(sindict_id), dummy_template)
             
                #add Calibration references
                l = self._fetcher.get("%s_G_DATA_ALL_CALS" % (sindict_id))
                if l is None :
                    raise CTBTOError(- 1, "Error no calibration information for sample %s, sid: %s\n" % (ty, spectrum_id))
                else:
                    # add calibration info
                    dummy_template = re.sub("\${CAL_INFOS}", ' '.join(map(str, l)), dummy_template) #IGNORE:W0141
        
                # add software method version info
                dummy_template = re.sub("\${SOFTWARE}", "genie", dummy_template)
                dummy_template = re.sub("\${METHOD}", "standard", dummy_template)
                dummy_template = re.sub("\${VERSION}", "1.0", dummy_template)
                dummy_template = re.sub("\${SOFTCOMMENTS}", "Old version", dummy_template)
             
                all_analyses_xml += dummy_template
        
        # add all the analysis info in the global template
        self._populatedTemplate = re.sub("\${AnalysisResults}", all_analyses_xml, self._populatedTemplate)
         
    def _fillCalibrationCoeffs(self, prefix, calibInfos):
        """ Insert the calibration information
        
            Args:
               prefix: the prefix for constituting the UID identifying the currently treated sampleID in the fetcher object
               calibInfos: set of calib info ids that have already been included in the xml
            
            Returns: generated xml data for displaying calibration info
               
            Raises:
               exception if issue fetching data (CTBTOError)
        """
        
        # first add Energy Cal
        template = self._conf.get("ParticulateTemplatingSystem", "particulateEnergyCalTemplate")
        
        xml = ""
        dummy_template = ""
        
        # get energy calibration 
        en_id = self._fetcher.get("%s_G_ENERGY_CAL" % (prefix), None)
        
        if (en_id is not None):
        
            # add calib info if it isn't there already
            if en_id not in calibInfos:
                energy = self._fetcher.get(en_id, {})
                dummy_template = re.sub("\${TERM0}", str(energy.get(u'COEFF1', UNDEFINED)), template)
                dummy_template = re.sub("\${TERM1}", str(energy.get(u'COEFF2', UNDEFINED)), dummy_template)
                dummy_template = re.sub("\${TERM2}", str(energy.get(u'COEFF3', UNDEFINED)), dummy_template)
                dummy_template = re.sub("\${TERM3}", str(energy.get(u'COEFF4', UNDEFINED)), dummy_template)
                dummy_template = re.sub("\${EN_ID}", en_id, dummy_template)
                # add generated xml in final container
                xml += dummy_template
                # add the id in the set of existing infos
                calibInfos.add(en_id)
        else:
            GenieParticulateRenderer.c_log.warning("Could not find any energy calibration info for sample %s\n" % (prefix))
        
        template = self._conf.get("ParticulateTemplatingSystem", "particulateResolutionCalTemplate")
        
        re_id = self._fetcher.get("%s_G_RESOLUTION_CAL" % (prefix), None)
        
        if re_id is not None: 
            # add calib info if it isn't there already
            if re_id not in calibInfos:
                # get resolution calibration 
                resolution = self._fetcher.get(re_id, {})
        
                dummy_template = re.sub("\${TERM0}", str(resolution.get('COEFF1', UNDEFINED)), template)
                dummy_template = re.sub("\${TERM1}", str(resolution.get('COEFF2', UNDEFINED)), dummy_template)
                dummy_template = re.sub("\${RE_ID}", re_id, dummy_template)
        
                # add generated xml in final container
                xml += dummy_template
    
                # add the id in the set of existing infos
                calibInfos.add(re_id)
        else:
            GenieParticulateRenderer.c_log.warning("Warning. Could not find any resolution calibration info for sample %s\n" % (prefix))
        
        template = self._conf.get("ParticulateTemplatingSystem", "particulateEfficencyCalTemplate")
        
        eff_id = self._fetcher.get("%s_G_EFFICIENCY_CAL" % (prefix), None)
        
        
        
        if (eff_id is not None):
            # add calib info if it isn't there already
            if eff_id not in calibInfos:
                # get efficiency calibration 
                eff = self._fetcher.get(eff_id, {})
        
                dummy_template = re.sub("\${LN_TERM0}", str(eff.get('COEFF1', UNDEFINED)), template)
                dummy_template = re.sub("\${TERM0}", str(eff.get('COEFF2', UNDEFINED)), dummy_template)
                dummy_template = re.sub("\${TERM1}", str(eff.get('COEFF3', UNDEFINED)), dummy_template)
                dummy_template = re.sub("\${TERM2}", str(eff.get('COEFF4', UNDEFINED)), dummy_template)
                dummy_template = re.sub("\${TERM3}", str(eff.get('COEFF5', UNDEFINED)), dummy_template)
                dummy_template = re.sub("\${TERM4}", str(eff.get('COEFF6', UNDEFINED)), dummy_template)
                dummy_template = re.sub("\${TERM5}", str(eff.get('COEFF7', UNDEFINED)), dummy_template)
                dummy_template = re.sub("\${EF_ID}", eff_id, dummy_template)
        
                # add generated xml in final container
                xml += dummy_template
            
                # add the id in the set of existing infos
                calibInfos.add(eff_id)
        
        return xml
        
    def _fillCalibration(self):
        """ Add the calibration parameters for each of the spectrum"""
        
        xml = ""
        # list of ids added in the xml document
        addedCalibrationIDs = set()
        
        for ty in self._fetcher.get('CONTENT_PRESENT', []):
            
            # treat preliminary samples differently as there is another indirection
            if ty == 'PREL':
                for prefix in self._fetcher.get('CURR_List_OF_PRELS', []):
                    if prefix is None:
                        raise CTBTOError(- 1, "Error when filling Calibration info for prefix %s, There is no CURRENT_%s in the dataBag\n" % (prefix, prefix))
                
                    xml += self._fillCalibrationCoeffs(prefix, addedCalibrationIDs)    
            else:
                prefix = self._fetcher.get(u'CURRENT_%s' % (ty), None)
                if prefix is None:
                    raise CTBTOError(- 1, "Error when fetching Calibration info for prefix %s, There is no CURRENT_%s in the dataBag\n" % (prefix, prefix))
               
                xml += self._fillCalibrationCoeffs(prefix, addedCalibrationIDs)      
            
        # out of the loop
        self._populatedTemplate = re.sub("\${CALIBRATION}", xml, self._populatedTemplate)
       
    
    def asXmlStr(self, aRequest=""):
        """ return the xml particulate product according to the passed request
        
            Args:
               aRequest: string containing some parameters for each fetching bloc (ex params="specturm=curr/qc/prels/bk"). Default = ""
            
            Returns: the populated template
              
              
            Raises:
               exception if issue fetching data (CTBTOError)
        """
       
        # parse request to know what need to be added in the product
        # [Parsing could be done for once and shared between fetcher and renderer]
        reqDict = self._parser.parse(aRequest, RequestParser.PAR)
         
        self._fillData(reqDict)
       
        self._fillAnalysisResults(reqDict)
       
        self._fillCalibration()
       
        # father 
        BaseRenderer.asXmlStr(self, aRequest)
       
        return self._populatedTemplate
       
       
       
       
""" Dictionary used to map Sample type with the right renderer """ #IGNORE:W0105
RENDERER_TYPE = {'SAUNA':SaunaRenderer, 'ARIX-4':SaunaRenderer, 'SPALAX':SpalaxRenderer, 'PARTICULATE':GenieParticulateRenderer,None:None}
              
       