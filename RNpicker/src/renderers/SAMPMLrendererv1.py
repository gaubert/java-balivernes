import logging
import re


import common.utils


class BaseRenderer(object):
    """ Base Class used to transform the fetcher content into XML """
    
    # Class members
    c_log = logging.getLogger("SAMPMLrendererv1.BaseRenderer")
    c_log.setLevel(logging.DEBUG)
    
    
    
    def __init__(self,aDataFetcher):
        
        self._conf              = common.utils.Conf.get_instance()
        self._fetcher           = aDataFetcher
        self._quantifiable      = set()
        self._template          = None
        self._populatedTemplate = None
        self._analysisCounter   = 0
        
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
                                    "SAMPLE_GEOMETRY"    :   "SAMPLE_GEOMETRY",
                                    "SAMPLE_QUANTITY"    :   "SAMPLE_QUANTITY",
                                    "REMARK"             :   "TEMPLATE_COMMAND_NOTHING", 
                                 }
                                  
        self._createTemplate()
        
       
    def _readTemplateMainTemplateFromFile(self):
        """ Read the template from a file. Old method now everything is read from the conf """
        
        # get template path from conf
        path = self._conf.get("TemplatingSystem","baseTemplate")
        
        # assert that the file exists
        common.utils.file_exits(path)
        
        # read the full template in a string buffer
        f = open(path,"r") 
        
        self._template = f.read()
        
        self._populatedTemplate = self._template
        
    
    def _createTemplate(self):
        """ Read XML template from a file and store it in a String 
            Read main template from a file because do not know how to setup the encoding.
            When open(...) is used, the encoding is read properly
        """
        
        self._readTemplateMainTemplateFromFile()
        
        #self._template = self._conf.get("TemplatingSystem","particulateSAMPMLTemplate")
        
        #print "template [%s]\n"%(self._template)
        
        #self._populatedTemplate = self._template
        
    def _generateAnalysisID(self):
        """ simple counter incremented """
     
        self._analysisCounter += 1
     
        return "analysis-%d"%(self._analysisCounter)
    
    def _substituteValues(self):
        """ substitue values """
        
        for (key,val) in self._substitutionDict.items():
            pattern = "\${%s}"%(key)
            
            if val == "TEMPLATE_COMMAND_NOTHING":
               self._populatedTemplate = re.sub(pattern, "", self._populatedTemplate)
            
            self._populatedTemplate = re.sub(pattern, str(self._fetcher.get(val,"None")), self._populatedTemplate)
            
    def asXml(self):
        """  """
        
    def asXmlStr(self):
        """ Return an xml tree as a string """
        
        print "into asXMLStr"
        
        self._substituteValues()
        
class ParticulateRenderer(BaseRenderer):
    
     # Class members
    c_log = logging.getLogger("SAMPMLrendererv1.ParticulateRenderer")
    c_log.setLevel(logging.DEBUG)
    
    
    
    def __init__(self,aDataFetcher):
        
        super(ParticulateRenderer,self).__init__(aDataFetcher)
        
        # add values specific to Particulates
        dummy_dict = {  
                        # to be changed as only one analysis is supported at the moment
                        "SPECTRUM_ID"                    :   "CURRENT_DATA_ID"
                      }
        # add specific particulate keys
        self._substitutionDict.update(dummy_dict)
        
    def _fillData(self):
        """ insert all spectrum data in final produced XML file """
    
        # check if there is a spectrum in the hashtable. If not replace ${SPECTRUM} by an empty string ""
        
        spectrumType = ['CURRENT','BACKGROUND']
        
        finalTemplate = ""
        
        for type in spectrumType:
            
            spectrumTemplate = ""
            
            fname = "%s_DATA"%(type)
            data  = self._fetcher.get(fname,None)
            
            if data is not None:
               
              spectrumTemplate = self._conf.get("TemplatingSystem","particulateSpectrumTemplate")
              
              # insert data
              spectrumTemplate = re.sub("\${SPECTRUM_DATA}",data, spectrumTemplate)
              
              # insert spectrum ID
              spectrumTemplate = re.sub("\${SPECTRUM_ID}",self._fetcher.get("%s_ID"%(fname)), spectrumTemplate)
              
              # insert spectrum type
              # insert spectrum ID
              spectrumTemplate = re.sub("\${SPECTRUM_TYPE}",self._fetcher.get("%s_TYPE"%(fname)), spectrumTemplate)
              
              #print "fetched = %s, data=%s\n"%("%s_channel_span"%(fname),self._fetcher.get("%s_channel_span"%(fname),None))
              
              # insert energy and channel span
              spectrumTemplate = re.sub("\${SPECTRUM_DATA_CHANNEL_SPAN}",str(self._fetcher.get("%s_CHANNEL_SPAN"%(fname))), spectrumTemplate)
              spectrumTemplate = re.sub("\${SPECTRUM_DATA_ENERGY_SPAN}",str(self._fetcher.get("%s_ENERGY_SPAN"%(fname))), spectrumTemplate)
            
              # get the date information
              spectrumTemplate = re.sub("\${COL_START}",str(self._fetcher.get("%s_COLLECT_START"%(fname))), spectrumTemplate)
              spectrumTemplate = re.sub("\${COL_STOP}",str(self._fetcher.get("%s_COLLECT_STOP"%(fname))), spectrumTemplate)
              spectrumTemplate = re.sub("\${ACQ_START}",str(self._fetcher.get("%s_ACQ_START"%(fname))), spectrumTemplate)
              spectrumTemplate = re.sub("\${ACQ_STOP}",str(self._fetcher.get("%s_ACQ_STOP"%(fname))), spectrumTemplate)
              spectrumTemplate = re.sub("\${SAMPLING_TIME}",str(self._fetcher.get("%s_SAMPLING_TIME"%(fname))), spectrumTemplate)
              spectrumTemplate = re.sub("\${REAL_ACQ_TIME}",str(self._fetcher.get("%s_ACQ_REAL_SEC"%(fname))), spectrumTemplate)
              spectrumTemplate = re.sub("\${LIVE_ACQ_TIME}",str(self._fetcher.get("%s_ACQ_LIVE_SEC"%(fname))), spectrumTemplate)
              
              spectrumTemplate = re.sub("\${DECAY_TIME}",str(self._fetcher.get("%s_DECAY_TIME"%(fname))), spectrumTemplate)
              spectrumTemplate = re.sub("\${SAMPLE_TYPE}",str(self._fetcher.get("%s_SPECTRAL_QUALIFIER"%(fname))), spectrumTemplate)
              spectrumTemplate = re.sub("\${MEASUREMENT_TYPE}",str(self._fetcher.get("%s_DATA_TYPE"%(fname))), spectrumTemplate)
              
              # TODO to remove just there for testing, deal with the compression flag
              if self._fetcher.get("%s_COMPRESSED"%(fname),False) == True :
                 spectrumTemplate = re.sub("\${COMPRESS}","compress=\"base64,zip\"",spectrumTemplate)
              else:
                 spectrumTemplate = re.sub("\${COMPRESS}","",spectrumTemplate)
                     
            # add fill spectrum template in global template 
            finalTemplate += spectrumTemplate
        
        self._populatedTemplate = re.sub("\${SPECTRUM}",finalTemplate, self._populatedTemplate)
        
     
    def _getCategory(self):
        """ fill and return the category XML structure stringified """
          
        category = "undefined"
        comment  = "No Comment"
        
        # get the status. If it is R or Q get category otherwise it isn't defined yet
        status = self._fetcher.get(u'CAT_STATUS',"")
        
        if (status == 'R') or (status == 'Q'):
            category = self._fetcher.get(u'CAT_CATEGORY')
            comment  = self._fetcher.get(u'CAT_COMMENT',"No Comment")
          
        # xml filler 
        cat_template = self._conf.get("TemplatingSystem","particulateCategoryTemplate")
        
        dummy_template = ""
        
        dummy_template = re.sub("\${CATEGORY}",str(category), cat_template)
        dummy_template = re.sub("\${CATEGORY_COMMENT}",comment, dummy_template)
        
        return dummy_template
    
    def _getNuclides(self):
        """ fill and return the information regarding the nuclides """
        
        # first add Non Quantified Nuclides
        template = self._conf.get("TemplatingSystem","particulateNuclideTemplate")
        
        xml_nuclides = ""
        dummy_template = ""
        cpt = 1
        
        # get categories
        ided_nuclides = self._fetcher.get("IDED_NUCLIDES","None")
        
        for nuclide in ided_nuclides:
            dummy_template = re.sub("\${REPORTMDA}",( ("true") if nuclide['REPORT_MDA'] == 1 else "false"), template)
            dummy_template = re.sub("\${QUANTIFIABLE}",str(self._isQuantifiable(nuclide['NAME'])).lower(),dummy_template)
            dummy_template = re.sub("\${NAME}",nuclide['NAME'], dummy_template)
            dummy_template = re.sub("\${TYPE}",nuclide['TYPE'], dummy_template)
            dummy_template = re.sub("\${HALFLIFE}",str(nuclide['HALFLIFE']), dummy_template)
            dummy_template = re.sub("\${CONCENTRATION}",str(nuclide['ACTIV_KEY']), dummy_template)
            dummy_template = re.sub("\${CONCENTRATION_ERROR}",str(nuclide['ACTIV_KEY_ERR']), dummy_template)
            dummy_template = re.sub("\${MDA}","%s %s"%(str(nuclide['MDA']),str(nuclide['MDA_ERR'])), dummy_template)
            dummy_template = re.sub("\${IDENTIFICATION_INDICATOR}",str(nuclide['NID_FLAG']), dummy_template)
            
            # add generated xml in final container
            xml_nuclides += dummy_template
            
        #print "xml_nuclides = %s"%(xml_nuclides)
        
        return xml_nuclides
    
    def _isQuantifiable(self,aVal):
        """ true if quantifiable, false otherwise """
        nucl2quantify = self._fetcher.get("NUCLIDES_2_QUANTIFY")
     
        # if set hasn't been populated do it
        if len(self._quantifiable) == 0:
          # create a set containing all quantifiable elements
          for elem in nucl2quantify:
              [(key,val)] = elem.items()
              self._quantifiable.add(val)
        
        return (aVal in self._quantifiable)
            
        
    def _getNuclideLines(self):
        """Get the Nuclide Lines information from the data hashtable and render it.
        
            Args:
               None:
        
            Returns:
              An XML string containing the formatted data.
              
            Raises:
               exception
        """
        
        # check if we need nuclidelines otherwise quit
        if self._conf.getboolean("Options","addNuclideLines") is False:
            print "Configuration says no nuclide lines\n"
            return ""
        
        # get the global template
        global_template = self._conf.get("TemplatingSystem","particulateNuclideLinesTemplate")
        
        # first get Nuclide Lines template
        template = self._conf.get("TemplatingSystem","particulateOneNuclideLineTemplate")
        
        xml_nuclidelines   = ""
        dummy_template = ""
        cpt = 1
        
        # get categories
        nuclidelines = self._fetcher.get(u'IDED_NUCLIDE_LINES',"None")
        
        for line in nuclidelines:
            
            # if there is a peakID in the hash then replace it otherwise remove this info from the XML
            dummy_template = re.sub("\${PEAKID}",("peakID=\"%s\""%(line['PEAK_ID']) if ('PEAK_ID' in line) else ""), template)
            dummy_template = re.sub("\${NAME}",line['NAME'], dummy_template)
            dummy_template = re.sub("\${TYPE}",line['TYPE'], dummy_template)
            dummy_template = re.sub("\${HALFLIFE}",str(line['HALFLIFE']), dummy_template)
            dummy_template = re.sub("\${MDA}","%s %s"%(str(line['MDA']),str(line['MDA_ERR'])), dummy_template)
           
            dummy_template = re.sub("\${ACTIVTIY}",( ("<Activity unit=\"mBq\">%s %s</Activity>"%(str(line['ACTIV_KEY']),str(line['ACTIV_KEY_ERR']))) if not (line['ACTIV_KEY'] == 0) else ""), dummy_template)
            dummy_template = re.sub("\${ENERGY}",("<Energy unit=\"keV\">%s %s</Energy>"%(str(line['ENERGY']),str(line['ENERGY_ERR'])) if ('ENERGY' in line) else ""), dummy_template)
            dummy_template = re.sub("\${ABUNDANCE}",("<Abundance unit=\"percent\">%s %s</Abundance>"%(str(line['ABUNDANCE']),str(line['ABUNDANCE_ERR'])) if ('ABUNDANCE' in line) else ""), dummy_template)
            dummy_template = re.sub("\${EFFICIENCY}",("<Efficiency unit=\"percent\">%s %s</Efficiency>"%(str(line['EFFIC']),str(line['EFFIC_ERR'])) if ('EFFIC' in line) else ""), dummy_template)
            
            # add generated xml in final container
            xml_nuclidelines += dummy_template
            
        #add nuclide lines in global template
        return re.sub("\${NUCLIDELINES}",xml_nuclidelines, global_template)
    
    def _getPeaks(self):
        
        """Get the peaks information from the data hashtable and render it .

         Args: 
           None
          

         Returns:
           An XML String containing the formatted data.

         Raises:
          None.
        """
  
        peak_template = self._conf.get("TemplatingSystem","peaksTemplate")
        
        xml_peaks = ""
        dummy_template = ""
        
        # get peak
        peaks = self._fetcher.get(u'PEAKS',"None")
        
        for peak in peaks:
            #print "peak = %s"%(peak)
            dummy_template = re.sub("\${ENERGY}","%s %s"%(str(peak['ENERGY']),str(peak['ENERGY_ERR'])), peak_template)
            dummy_template = re.sub("\${PEAKID}","%s"%(str(peak['PEAK_ID'])), dummy_template)
            dummy_template = re.sub("\${CENTROID}","%s %s"%(str(peak['CENTROID']),str(peak['CENTROID_ERR'])), dummy_template)
            dummy_template = re.sub("\${AREA}","%s %s"%(str(peak['AREA']),str(peak['AREA_ERR'])), dummy_template)
            dummy_template = re.sub("\${WIDTH}",str(peak['WIDTH']), dummy_template)
            dummy_template = re.sub("\${FWHM}","%s %s"%(str(peak['FWHM']),str(peak['FWHM_ERR'])), dummy_template)
            dummy_template = re.sub("\${BACKGROUNDCOUNTS}","%s %s"%(str(peak['BACK_COUNT']),str(peak['BACK_UNCER'])), dummy_template)
            dummy_template = re.sub("\${EFFICIENCY}","%s %s"%(str(peak['EFFICIENCY']),str(peak['EFF_ERROR'])), dummy_template)
            dummy_template = re.sub("\${LC}",str(peak['LC']), dummy_template)
            
            # to be checked with Romano
            dummy_template = re.sub("\${LD}","None", dummy_template)
            dummy_template = re.sub("\${DETECTIBILITY}",str(peak.get('DETECTABILITY',"None")), dummy_template)
            
            dummy_template = re.sub("\${NUCLIDE}","None", dummy_template)
            # to be checked
            dummy_template = re.sub("\${NUCLIDE_PERCENTAGE}",str(100),dummy_template)
            
            # add generated xml in final container
            xml_peaks += dummy_template
               
        return xml_peaks
    
    def _getParameters(self):
        """ return parameters """
        
         # first add Quantified Nuclides
        template = self._conf.get("TemplatingSystem","processingParametersTemplate")
        
        xml_parameters = ""
        dummy_template = ""
        
        # get processing parameters
        parameters = self._fetcher.get("PROCESSING_PARAMETERS",None)
        
        #print "parameters = %s"%(parameters)
        
        if (parameters is not None) and (len(parameters) > 0) :
           dummy_template = re.sub("\${THRESHOLD}",parameters.get('THRESHOLD',"None"), template)
           dummy_template = re.sub("\${PEAK_START}",str(parameters.get('PEAK_START',"None")), dummy_template)
           dummy_template = re.sub("\${PEAK_END}",str(parameters.get('PEAK_END',"None")), dummy_template)
           dummy_template = re.sub("\${LEFT_FWHM}",str(parameters.get('LEFT_FWHM_LIM',"None")), dummy_template)
           dummy_template = re.sub("\${RIGHT_FWHM}",str(parameters.get('RIGHT_FWHM_LIM',"None")), dummy_template)
           dummy_template = re.sub("\${MULTI_FWHM}",str(parameters.get('FWHM_MULT_WIDTH',"None")), dummy_template)
           dummy_template = re.sub("\${FIT_SINGLETS}",str(parameters.get('FIT_SINGLETS',"None")), dummy_template)
           dummy_template = re.sub("\${CRITICAL_LEV_TEST}",str(parameters.get('CRIT_LEVEL',"None")), dummy_template)
           dummy_template = re.sub("\${ESTIMATED_PEAK_WIDTHS}",str(parameters.get('MDC_WIDTH',"None")), dummy_template)
           dummy_template = re.sub("\${BASELINE_TYPE}",str(parameters.get('BACK_TYPE',"None")), dummy_template)
           dummy_template = re.sub("\${BASELINE_CHANNELS}",str(parameters.get('BACK_CHAN',"None")), dummy_template)
           dummy_template = re.sub("\${SUBSTRACTION}",str(parameters.get('ToBeDefined',"None")), dummy_template)
           dummy_template = re.sub("\${ENERGY_TOLERANCE}",str(parameters.get('ENERGY_TOL',"None")), dummy_template)
           dummy_template = re.sub("\${CONFIDENCE_THRESHOLD}",str(parameters.get('NID_CONFID',"None")), dummy_template)
           dummy_template = re.sub("\${RISK_LEVEL}",str(parameters.get('ToBeDefined',"None")), dummy_template)
               
        # add generated xml in final container
        xml_parameters += dummy_template
       
        # add Update parameters
        # first add Quantified Nuclides
        template = self._conf.get("TemplatingSystem","updateParametersTemplate")
        dummy_template = ""
        
        # get update parameters
        parameters = self._fetcher.get("UPDATE_PARAMETERS","None")
        
        if (parameters is not None) and (len(parameters) > 0):
           dummy_template = re.sub("\${USE_MRP}",str(parameters.get('MRP_USED',"None")), template)
           dummy_template = re.sub("\${MRP_SAMPLEID}",str(parameters.get('MRP_SAMPLE_ID',"None")), dummy_template)
           dummy_template = re.sub("\${GAIN_SHIFT}",str(parameters.get('GAINSHIFT',"None")), dummy_template)
           dummy_template = re.sub("\${ZERO_SHIFT}",str(parameters.get('ZEROSHIFT',"None")), dummy_template)
           dummy_template = re.sub("\${AREA_LIMIT}",str(parameters.get('AREA_LIM',"None")), dummy_template)
           dummy_template = re.sub("\${USE_WEIGHT}",str(parameters.get('USE_WEIGHT',"None")), dummy_template)
           dummy_template = re.sub("\${USE_MULTIPLET}",str(parameters.get('USE_MULT',"None")), dummy_template)
           dummy_template = re.sub("\${FORCE_LINEAR}",str(parameters.get('F_LINEAR',"None")), dummy_template)
           dummy_template = re.sub("\${IGNORE_PREVIOUS_ECR}",str(parameters.get('BOOTSTRAP',"None")), dummy_template)
           dummy_template = re.sub("\${MINIMUM_LIB_LOOKUP_TOLERANCE}",str(parameters.get('MIN_LOOKUP',"None")), dummy_template)
           dummy_template = re.sub("\${RER_INTERCEPT}",str(parameters.get('RER_INTERCEPT',"None")), dummy_template)
           dummy_template = re.sub("\${RER_SLOPE}",str(parameters.get('RER_SLOPE',"None")), dummy_template)
           dummy_template = re.sub("\${ECR_SLOPE}",str(parameters.get('ECR_SLOPE',"None")), dummy_template)
           dummy_template = re.sub("\${DO_RESOLUTION_UPDATE}",str(parameters.get('DO_RERU',"None")), dummy_template)
            
        # add generated xml in final container
        xml_parameters += dummy_template
       
        return xml_parameters
        
    def _getFlags(self):
        """create xml part with the flag info """
        
        # first add timeliness Flags
        template = self._conf.get("TemplatingSystem","timelinessFlagsTemplate")
        
        xml = ""
        dummy_template = ""
        dummy_template += template
          
        param = self._fetcher.get('TIME_FLAGS_PREVIOUS_SAMPLE',False)
        if param == True:
            dummy_template = re.sub("\${PreviousSamplePresent}","true", dummy_template)
        else:
            dummy_template = re.sub("\${PreviousSamplePresent}","false", dummy_template)
        
        param = self._fetcher.get('TIME_FLAGS_COLLECTION_WITHIN_24',0)
        if param == 0:
            dummy_template = re.sub("\${CollectionTime}","true", dummy_template)
        else:
            dummy_template = re.sub("\${CollectionTime}","false", dummy_template)
            
        param = self._fetcher.get('TIME_FLAGS_ACQUISITION_FLAG',0)
        if param == 0:
            dummy_template = re.sub("\${AcquisitionTime}","true", dummy_template)
        else:
            dummy_template = re.sub("\${AcquisitionTime}","false", dummy_template)
        
        param = self._fetcher.get('TIME_FLAGS_DECAY_FLAG',0)
        if param == 0:
            dummy_template = re.sub("\${DecayTime}","true", dummy_template)
        else:
            dummy_template = re.sub("\${DecayTime}","false", dummy_template)
            
        param = self._fetcher.get('TIME_FLAGS_SAMPLE_ARRIVAL_FLAG',0)
        if param == 0:
            dummy_template = re.sub("\${SampleReceived}","true", dummy_template)
        else:
            dummy_template = re.sub("\${SampleReceived}","false", dummy_template)
       
        # add generated xml in final container
        xml += dummy_template
        
        # get Data Quality Flags
        template = self._conf.get("TemplatingSystem","dataQualityFlagsTemplate")
        
        # add Data Quality Flags
        dataQFlags = self._fetcher.get('DATA_QUALITY_FLAGS',[])
        
        #print "DataQFlags %s\n"%(dataQFlags)
        
        # list of all flags found
        dq_xml = ""
        
        if len(dataQFlags) > 0:
           for flag in dataQFlags:
              name = flag['DQ_NAME']
              
              # check if it has a template if not ignore.
              
              dummy_template = self._conf.get("TemplatingSystem","dataQFlags_%s_Template"%(name),None)
              if dummy_template != None:
                 dummy_template = re.sub("\${%s_VAL}"%(name),str(flag['DQ_VALUE']), dummy_template)
                 dummy_template = re.sub("\${%s_PASS}"%(name),str(flag['DQ_RESULT']), dummy_template)
                 dummy_template = re.sub("\${%s_THRESOLD}"%(name),str(flag['DQ_THRESHOLD']), dummy_template)
                 
                 # add non empty template to data flags
                 dq_xml += dummy_template
              
        template = re.sub("\${DQ_FLAGS}",dq_xml, template)
        
        # replace global data quality flag template
        xml += template
           
        return xml
        
    def _fillAnalysisResults(self):
        """fill the analysis results for each result"""
        
        # first get the template
        template = self._conf.get("TemplatingSystem","particulateAnalysisTemplate")
        dummy_template = ""
        
        # for the moment only one result
        dummy_template += template
        
        # Add analysis identifier
        dummy_template = re.sub("\${ANALYSISID}", self._generateAnalysisID(),dummy_template)
        
        dummy_template = re.sub("\${CATEGORY}", self._getCategory(), dummy_template)
        
        dummy_template = re.sub("\${NUCLIDES}",self._getNuclides(),dummy_template)
         
        dummy_template = re.sub("\${WITHNUCLIDELINES}",self._getNuclideLines(),dummy_template)
        
        dummy_template = re.sub("\${PEAKS}",self._getPeaks(),dummy_template)
        
        dummy_template = re.sub("\${PARAMETERS}",self._getParameters(),dummy_template)
        
        dummy_template = re.sub("\${FLAGS}",self._getFlags(),dummy_template)
        
        # add software method version info
        dummy_template = re.sub("\${SOFTWARE}","genie", dummy_template)
        dummy_template = re.sub("\${METHOD}","standard", dummy_template)
        dummy_template = re.sub("\${VERSION}","1.0", dummy_template)
        dummy_template = re.sub("\${SOFTCOMMENTS}","Old version", dummy_template)
        
         # add Category info in generated template
        self._populatedTemplate = re.sub("\${AnalysisResults}",dummy_template, self._populatedTemplate)
         
    def _fillCalibration(self):
        """ Add the calibration parameters """
        
        # first add Energy Cal
        template = self._conf.get("TemplatingSystem","particulateEnergyCalTemplate")
        
        xml = ""
        dummy_template = ""
        
        # get energy calibration 
        energy = self._fetcher.get("ENERGY_CAL","None")
        
        dummy_template = re.sub("\${TERM0}",str(energy.get('COEFF1',"None")), template)
        dummy_template = re.sub("\${TERM1}",str(energy.get('COEFF2',"None")), dummy_template)
        dummy_template = re.sub("\${TERM2}",str(energy.get('COEFF3',"None")), dummy_template)
        dummy_template = re.sub("\${TERM3}",str(energy.get('COEFF4',"None")), dummy_template)
            
        # add generated xml in final container
        xml += dummy_template
        
        template = self._conf.get("TemplatingSystem","particulateResolutionCalTemplate")
        
        # get resolution calibration 
        resolution = self._fetcher.get("RESOLUTION_CAL","None")
        
        dummy_template = re.sub("\${TERM0}",str(resolution.get('COEFF1',"None")), template)
        dummy_template = re.sub("\${TERM1}",str(resolution.get('COEFF2',"None")), dummy_template)
        
        # add generated xml in final container
        xml += dummy_template
        
        template = self._conf.get("TemplatingSystem","particulateEfficencyCalTemplate")
        
        # get resolution calibration 
        eff = self._fetcher.get("EFFICIENCY_CAL","None")
        
        dummy_template = re.sub("\${LN_TERM0}",str(eff.get('COEFF1',"None")), template)
        dummy_template = re.sub("\${TERM0}",str(eff.get('COEFF2',"None")), dummy_template)
        dummy_template = re.sub("\${TERM1}",str(eff.get('COEFF3',"None")), dummy_template)
        dummy_template = re.sub("\${TERM2}",str(eff.get('COEFF4',"None")), dummy_template)
        dummy_template = re.sub("\${TERM3}",str(eff.get('COEFF5',"None")), dummy_template)
        dummy_template = re.sub("\${TERM4}",str(eff.get('COEFF6',"None")), dummy_template)
        dummy_template = re.sub("\${TERM5}",str(eff.get('COEFF7',"None")), dummy_template)
        
        # add generated xml in final container
        xml += dummy_template
        
        self._populatedTemplate = re.sub("\${CALIBRATION}",xml, self._populatedTemplate)
    
    def asXmlStr(self):
       """ Return an xml tree as a string """
         
       self._fillData()
       
       self._fillAnalysisResults()
       
       self._fillCalibration()
       
       # father 
       BaseRenderer.asXmlStr(self)
       
       return self._populatedTemplate
       
       
       
       
       
       