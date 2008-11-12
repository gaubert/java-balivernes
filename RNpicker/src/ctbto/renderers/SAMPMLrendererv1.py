import logging
import re

import ctbto.common.utils

from ctbto.common import CTBTOError

from ctbto.common import Conf
from ctbto.query  import RequestParser

class BaseRenderer(object):
    """ Base Class used to transform the fetcher content into XML """
    
    # Class members
    c_log = logging.getLogger("SAMPMLrendererv1.BaseRenderer")
    c_log.setLevel(logging.DEBUG)
    
    
    
    def __init__(self,aDataFetcher):
        
        self._conf              = ctbto.common.Conf.get_instance()
        self._fetcher           = aDataFetcher
        self._quantifiable      = set()
        self._template          = None
        self._populatedTemplate = None
        self._analysisCounter   = 0
        
        # create query parser 
        self._parser            = RequestParser()
        
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
        
        self._readTemplateMainTemplateFromFile()
       
    def _sortSpectrumsSet(self,aSpectrums):
        
        results = []
        
        if 'CURR' in aSpectrums:
            results.append(self._fetcher.get(u'CURRENT_CURR',None))
            aSpectrums.remove('CURR')
        
        if 'BK' in aSpectrums:
            results.append(self._fetcher.get(u'CURRENT_BK',None))
            aSpectrums.remove('BK')
        
        if 'QC' in aSpectrums:
            results.append(self._fetcher.get(u'CURRENT_QC',None))
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
        
    def asXmlStr(self,aRequest):
        """ return the xml product according to the passed request
        
            Args:
               aRequest: string containing some parameters for each fetching bloc (ex params="specturm=curr/qc/prels/bk")
            
            Returns: the populated template
              
              
            Raises:
               exception if issue fetching data (CTBTOError)
        """
        
        self._substituteValues()
        
        return self._populatedTemplate
        
        
class SaunaRenderer(BaseRenderer):
    
    # Class members
    c_log = logging.getLogger("SAMPMLrendererv1.SaunaRenderer")
    c_log.setLevel(logging.DEBUG)
    
      
    def __init__(self,aDataFetcher):
        
        super(SaunaRenderer,self).__init__(aDataFetcher)
        
        # add values specific to Particulates
        dummy_dict = {  
                        # to be changed as only one analysis is supported at the moment
                        "SPECTRUM_ID"                    :   "CURR_DATA_ID"
                      }
        # add specific particulate keys
        self._substitutionDict.update(dummy_dict)
        
        self._xe_lib = set()
    
    def _readTemplateMainTemplateFromFile(self):
        """ Read the template from a file. Old method now everything is read from the conf """
        
        # get template path from conf
        path = self._conf.get("SaunaTemplatingSystem","saunaBaseTemplate")
        
        # assert that the file exists
        ctbto.common.utils.file_exits(path)
        
        # read the full template in a string buffer
        f = open(path,"r") 
        
        self._template = f.read()
        
        self._populatedTemplate = self._template
    
    def asXmlStr(self,aRequest=""):
       """ return the xml particulate product according to the passed request
        
            Args:
               aRequest: string containing some parameters for each fetching bloc (ex params="specturm=curr/qc/prels/bk"). Default = ""
            
            Returns: the populated template
              
              
            Raises:
               exception if issue fetching data (CTBTOError)
       """
       
       # parse request to know what need to be added in the product
       # [Parsing could be done for once and shared between fetcher and renderer]
       reqDict = self._parser.parse(aRequest)
         
       self._fillData(reqDict)
       
       self._fillAnalysisResults(reqDict)
       
       self._fillCalibration()
       
       # father 
       BaseRenderer.asXmlStr(self,aRequest)
       
       return self._populatedTemplate
   
    def _isQuantifiable(self,aVal):
        """ true if quantifiable, false otherwise """
        xe_lib = self._fetcher.get("XE_NUCL_LIB")
     
        # if set hasn't been populated do it
        if len(self._xe_lib) == 0:
          # create a set containing all quantifiable elements
          for elem in xe_lib:
              [(key,val)] = elem.items()
              self._xe_lib.add(val)
        
        return (aVal in self._xe_lib)
   
    def _fillCalibrationCoeffs(self,prefix,calibInfos):
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
        en_id = self._fetcher.get("%s_B_ENERGY_CAL"%(prefix),None)
        
        if (en_id is not None):
        
          # first add Energy Cal
          template = self._conf.get("SaunaTemplatingSystem","saunaEnergyCalTemplate")
          
          # add calib info if it isn't there already
          if en_id not in calibInfos:
            energy = self._fetcher.get(en_id,{})
            dummy_template = re.sub("\${TERM0}",str(energy.get(u'BETA_COEFF1',"None")), template)
            dummy_template = re.sub("\${TERM1}",str(energy.get(u'BETA_COEFF2',"None")), dummy_template)
            dummy_template = re.sub("\${TERM2}",str(energy.get(u'BETA_COEFF3',"None")), dummy_template)
            dummy_template = re.sub("\${EN_ID}",en_id, dummy_template)
            dummy_template = re.sub("\${EN_TYPE}","Beta", dummy_template)
            # add generated xml in final container
            xml += dummy_template
            # add the id in the set of existing infos
            calibInfos.add(en_id)
        else:
            GenieParticulateRenderer.c_log.warning("Warning. Could not find any energy calibration info for sample %s\n"%(prefix))
        
         # get energy calibration 
        en_id = self._fetcher.get("%s_G_ENERGY_CAL"%(prefix),None)
        
        if (en_id is not None):
        
          # first add Energy Cal
          template = self._conf.get("SaunaTemplatingSystem","saunaEnergyCalTemplate")
          
          # add calib info if it isn't there already
          if en_id not in calibInfos:
            energy = self._fetcher.get(en_id,{})
            dummy_template = re.sub("\${TERM0}",str(energy.get(u'GAMMA_COEFF1',"None")), template)
            dummy_template = re.sub("\${TERM1}",str(energy.get(u'GAMMA_COEFF2',"None")), dummy_template)
            dummy_template = re.sub("\${TERM2}",str(energy.get(u'GAMMA_COEFF3',"None")), dummy_template)
            dummy_template = re.sub("\${EN_ID}",en_id, dummy_template)
            dummy_template = re.sub("\${EN_TYPE}","Gamma", dummy_template)
            # add generated xml in final container
            xml += dummy_template
            # add the id in the set of existing infos
            calibInfos.add(en_id)
        else:
            GenieParticulateRenderer.c_log.warning("Warning. Could not find any energy calibration info for sample %s\n"%(prefix))
        
        return xml
        
    def _getNuclides(self,id):
        """ fill and return the information regarding the nuclides """
        
        # first add Non Quantified Nuclides
        template = self._conf.get("SaunaTemplatingSystem","saunaNuclideTemplate")
        
        xml_nuclides = ""
        dummy_template = ""
        cpt = 1
        
        SaunaRenderer.c_log.debug("id = %s\n"%("%s_IDED_NUCLIDES"%(id)))
        
        # get categories
        ided_nuclides = self._fetcher.get("%s_IDED_NUCLIDES"%(id),[])
        
        for nuclide in ided_nuclides:
            dummy_template = re.sub("\${NAME}",nuclide[u'NAME'], template)
            dummy_template = re.sub("\${QUANTIFIABLE}",str(self._isQuantifiable(nuclide['NAME'])).lower(),dummy_template)
            dummy_template = re.sub("\${TYPE}",str(nuclide['TYPE']), dummy_template)
            dummy_template = re.sub("\${HALFLIFE}",str(nuclide['HALFLIFE']), dummy_template)
            dummy_template = re.sub("\${CONCENTRATION}",str(nuclide['CONC']), dummy_template)
            dummy_template = re.sub("\${CONCENTRATION_ERROR}",str(nuclide['CONC_ERR']), dummy_template)
            dummy_template = re.sub("\${MDC}","%s"%(str(nuclide['MDC'])), dummy_template)
            dummy_template = re.sub("\${LC}","%s"%(str(nuclide['LC'])), dummy_template)
            dummy_template = re.sub("\${LD}","%s"%(str(nuclide['LD'])), dummy_template)
            dummy_template = re.sub("\${IDENTIFICATION_INDICATOR}",str(nuclide['NID_FLAG']), dummy_template)
            dummy_template = re.sub("\${IDENTIFICATION_NUM}",str(nuclide['NID_FLAG_NUM']), dummy_template)
            
            # add generated xml in final container
            xml_nuclides += dummy_template
             
        return xml_nuclides

    def _getROIInfo(self,id):
        """ fill and return the information regarding the Regoin of Interest (ROI) """
        
        # first add Non Quantified Nuclides
        template = self._conf.get("SaunaTemplatingSystem","saunaRoiTemplate")
        
        xml_nuclides = ""
        dummy_template = ""
        cpt = 1
    
        # get categories
        rois = self._fetcher.get("%s_ROI_INFO"%(id),[])
        
        for roi in rois:
            dummy_template = re.sub("\${ROINB}",str(roi[u'ROI']), template)
            dummy_template = re.sub("\${NAME}","%s"%(roi[u'Nuclide']),dummy_template)
            dummy_template = re.sub("\${NETCOUNTS}","%s %s"%(str(roi[u'NET_COUNT']),str(roi[u'NET_COUNT_ERR'])),dummy_template)
            dummy_template = re.sub("\${DETNETCOUNTS}","%s %s"%(str(roi[u'DET_BKGND_COUNT']),str(roi[u'DET_BKGND_COUNT'])),dummy_template)
            dummy_template = re.sub("\${GASNETCOUNTS}","%s %s"%(str(roi[u'GAS_BKGND_COUNT']),str(roi[u'GAS_BKGND_COUNT'])),dummy_template)
            dummy_template = re.sub("\${LC}","%s"%(str(roi['LC'])), dummy_template)
            dummy_template = re.sub("\${LD}","%s"%(str(roi['LD'])), dummy_template)
            dummy_template = re.sub("\${MDC}","%s"%(str(roi['MDC'])), dummy_template)
            
            # add generated xml in final container
            xml_nuclides += dummy_template
             
        return xml_nuclides
    
    def _fillAnalysisResults(self,requestDict):
        """fill the analysis results for each result"""
        
        # check if there is a spectrum in the hashtable. If not replace ${SPECTRUM} by an empty string ""
        requestedTypes = requestDict[RequestParser.ANALYSIS]
        
        all_analyses_xml = ""
      
        for type in requestedTypes:
           
           #identifier in the dict for this analysis  
           id = self._fetcher.get("CURRENT_%s"%(type),None)
           
           if id is not None:
        
             # first get the template
             template = self._conf.get("SaunaTemplatingSystem","saunaAnalysisTemplate")
             dummy_template = ""
        
             # for the moment only one result
             dummy_template += template
    
             spectrum_id    = self._fetcher.get("%s_DATA_G_ID"%(self._fetcher.get("CURRENT_%s"%(type),'')),"unknown")
             
             # Add analysis identifier => SpectrumID prefixed by AN
             dummy_template = re.sub("\${ANALYSISID}","AN-%s"%(spectrum_id),dummy_template)
        
             dummy_template = re.sub("\${SPECTRUM_ID}",spectrum_id,dummy_template)
        
             #dummy_template = re.sub("\${CATEGORY}", self._getCategory(id), dummy_template)
        
             dummy_template = re.sub("\${NUCLIDES}",self._getNuclides(id),dummy_template)
             
             dummy_template = re.sub("\${ROIINFO}",self._getROIInfo(id),dummy_template)
         
             #dummy_template = re.sub("\${PARAMETERS}",self._getParameters(id),dummy_template)
        
             #dummy_template = re.sub("\${FLAGS}",self._getFlags(id),dummy_template)
             
             #add Calibration references
             l = self._fetcher.get("%s_G_DATA_ALL_CALS"%(id))
             if l is None :
                raise CTBTOError(-1,"Error no calibration information for sample %s, sid: %s\n"%(type,spectrum_id))
             else:
               # add calibration info
               dummy_template = re.sub("\${CAL_INFOS}",' '.join(map(str,l)),dummy_template)
        
             # add software method version info
             dummy_template = re.sub("\${SOFTWARE}","bg_analyse", dummy_template)
             dummy_template = re.sub("\${METHOD}","standard", dummy_template)
             dummy_template = re.sub("\${VERSION}","1.0", dummy_template)
             dummy_template = re.sub("\${SOFTCOMMENTS}","Old version", dummy_template)
             
             all_analyses_xml += dummy_template
        
        # add all the analysis info in the global template
        self._populatedTemplate = re.sub("\${AnalysisResults}",all_analyses_xml, self._populatedTemplate)
         
    def _fillCalibration(self):
        """ Add the calibration parameters for each of the spectrum"""
        
        xml =""
        # list of ids added in the xml document
        addedCalibrationIDs= set()
        
        for type in self._fetcher.get('CONTENT_PRESENT',[]):
            
           # treat preliminary samples differently as there is another indirection
           if type == 'PREL':
              for prefix in self._fetcher.get('CURR_List_OF_PRELS',[]):
                  if prefix is None:
                    raise CTBTOError(-1,"Error when filling Calibration info for prefix %s, There is no CURRENT_%s in the dataBag\n"%(prefix,prefix))
                
                  xml += self._fillCalibrationCoeffs(prefix,addedCalibrationIDs)    
           else:
                prefix = self._fetcher.get(u'CURRENT_%s'%(type),None)
                if prefix is None:
                  raise CTBTOError(-1,"Error when fetching Calibration info for prefix %s, There is no CURRENT_%s in the dataBag\n"%(prefix,prefix))
               
                xml += self._fillCalibrationCoeffs(prefix,addedCalibrationIDs)      
            
        # out of the loop
        self._populatedTemplate = re.sub("\${CALIBRATION}",xml, self._populatedTemplate)
       
        
    def _fillData(self,requestDict):
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
            requestedTypes.update(self._fetcher.get(u'CURR_List_OF_PRELS',[]))
        
       spectrums = self._sortSpectrumsSet(requestedTypes)
        
       finalTemplate = ""
    
       for type in spectrums:
            
           spectrumTemplate = ""
            
           # get Gamma and Beta Spectrum
           l = ["%s_DATA_G"%(type), "%s_DATA_B"%(type)]
           for fname in l:
              data  = self._fetcher.get(fname,None)
              if data is not None:
               
                spectrumTemplate = self._conf.get("SaunaTemplatingSystem","saunaSpectrumTemplate")
              
                # insert data
                spectrumTemplate = re.sub("\${SPECTRUM_DATA}",data, spectrumTemplate)
              
                # insert spectrum ID
                spectrumTemplate = re.sub("\${SPECTRUM_ID}",self._fetcher.get("%s_ID"%(fname)), spectrumTemplate)
            
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
              
                # add quantity and geometry
                spectrumTemplate = re.sub("\${QUANTITY}",str(self._fetcher.get("%s_SAMPLE_QUANTITY"%(fname))), spectrumTemplate)
                spectrumTemplate = re.sub("\${GEOMETRY}",str(self._fetcher.get("%s_SAMPLE_GEOMETRY"%(fname))), spectrumTemplate)
              
                l = self._fetcher.get("%s_G_DATA_ALL_CALS"%(type))
                if l is None:
                  SaunaRenderer.c_log.warning("No calibration information for sample %s"%(type))
                  l = []
                  #raise CTBTOError(-1,"Error no calibration information for sample %s\n"%(type))


                # add calibration info
                spectrumTemplate = re.sub("\${CAL_INFOS}",' '.join(map(str,l)), spectrumTemplate)
              
                # TODO to remove just there for testing, deal with the compression flag
                if self._fetcher.get("%s_COMPRESSED"%(fname),False) == True :
                   spectrumTemplate = re.sub("\${COMPRESS}","compress=\"base64,zip\"",spectrumTemplate)
                else:
                   spectrumTemplate = re.sub("\${COMPRESS}","",spectrumTemplate)
                     
                # add fill spectrum template in global template 
                finalTemplate += spectrumTemplate
              
           # Get histogram data 
           fname =  "%s_DATA_H"%(type)
           data  = self._fetcher.get(fname,None)
           if data is not None:
                spectrumTemplate = self._conf.get("SaunaTemplatingSystem","saunaHistogramTemplate")
              
                # insert data
                spectrumTemplate = re.sub("\${H_DATA}",data, spectrumTemplate)
              
                # insert spectrum ID
                spectrumTemplate = re.sub("\${H_ID}",self._fetcher.get("%s_ID"%(fname)), spectrumTemplate)
            
                # insert energy and channel span for beta and gamma
                spectrumTemplate = re.sub("\${H_G_DATA_CHANNEL_SPAN}",str(self._fetcher.get("%s_DATA_G_CHANNEL_SPAN"%(type))), spectrumTemplate)
                spectrumTemplate = re.sub("\${H_G_DATA_ENERGY_SPAN}",str(self._fetcher.get("%s_DATA_G_ENERGY_SPAN"%(type))), spectrumTemplate)
                spectrumTemplate = re.sub("\${H_B_DATA_CHANNEL_SPAN}",str(self._fetcher.get("%s_DATA_B_CHANNEL_SPAN"%(type))), spectrumTemplate)
                spectrumTemplate = re.sub("\${H_B_DATA_ENERGY_SPAN}",str(self._fetcher.get("%s_DATA_B_ENERGY_SPAN"%(type))), spectrumTemplate)
            
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
              
                # add quantity and geometry
                spectrumTemplate = re.sub("\${QUANTITY}",str(self._fetcher.get("%s_SAMPLE_QUANTITY"%(fname))), spectrumTemplate)
                spectrumTemplate = re.sub("\${GEOMETRY}",str(self._fetcher.get("%s_SAMPLE_GEOMETRY"%(fname))), spectrumTemplate)
              
                l = self._fetcher.get("%s_G_DATA_ALL_CALS"%(type))
                if l is None:
                  SaunaRenderer.c_log.warning("No calibration information for sample %s"%(type))
                  l = []
                  #raise CTBTOError(-1,"Error no calibration information for sample %s\n"%(type))
             
                # add calibration info
                spectrumTemplate = re.sub("\${CAL_INFOS}",' '.join(map(str,l)), spectrumTemplate)
              
                # TODO to remove just there for testing, deal with the compression flag
                if self._fetcher.get("%s_COMPRESSED"%(fname),False) == True :
                   spectrumTemplate = re.sub("\${COMPRESS}","compress=\"base64,zip\"",spectrumTemplate)
                else:
                   spectrumTemplate = re.sub("\${COMPRESS}","",spectrumTemplate)
                     
                # add fill spectrum template in global template 
                finalTemplate += spectrumTemplate      
        
              
          
        
       self._populatedTemplate = re.sub("\${DATA}",finalTemplate, self._populatedTemplate)
    
        
class GenieParticulateRenderer(BaseRenderer):
    
    # Class members
    c_log = logging.getLogger("SAMPMLrendererv1.GenieParticulateRenderer")
    c_log.setLevel(logging.DEBUG)
    
      
    def __init__(self,aDataFetcher):
        
        super(GenieParticulateRenderer,self).__init__(aDataFetcher)
        
        # add values specific to Particulates
        dummy_dict = {  
                        # to be changed as only one analysis is supported at the moment
                        "SPECTRUM_ID"                    :   "CURR_DATA_ID"
                      }
        # add specific particulate keys
        self._substitutionDict.update(dummy_dict)
    
    def _readTemplateMainTemplateFromFile(self):
        """ Read the template from a file. Old method now everything is read from the conf """
        
        # get template path from conf
        path = self._conf.get("ParticulateTemplatingSystem","particulateBaseTemplate")
        
        # assert that the file exists
        ctbto.common.utils.file_exits(path)
        
        # read the full template in a string buffer
        f = open(path,"r") 
        
        self._template = f.read()
        
        self._populatedTemplate = self._template
      
    def _fillData(self,requestDict):
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
            requestedTypes.update(self._fetcher.get(u'CURR_List_OF_PRELS',[]))
        
        spectrums = self._sortSpectrumsSet(requestedTypes)
        
        
        finalTemplate = ""
        
      
        for type in spectrums:
            
               spectrumTemplate = ""
            
               # add Spectrum
               fname = "%s_G"%(type)
              
               data  = self._fetcher.get(fname,None)
            
               if data is not None:
               
                 spectrumTemplate = self._conf.get("TemplatingSystem","particulateSpectrumTemplate")
              
                 # insert data
                 spectrumTemplate = re.sub("\${SPECTRUM_DATA}",data, spectrumTemplate)
              
                 # insert spectrum ID
                 spectrumTemplate = re.sub("\${SPECTRUM_ID}",self._fetcher.get("%s_ID"%(fname)), spectrumTemplate)
            
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
              
                 # add quantity and geometry
                 spectrumTemplate = re.sub("\${QUANTITY}",str(self._fetcher.get("%s_SAMPLE_QUANTITY"%(fname))), spectrumTemplate)
                 spectrumTemplate = re.sub("\${GEOMETRY}",str(self._fetcher.get("%s_SAMPLE_GEOMETRY"%(fname))), spectrumTemplate)
              
                 l = self._fetcher.get("%s_ALL_CALS"%(fname))
                 if l is None:
                    raise CTBTOError(-1,"Error no calibration information for sample %s\n"%(type))
             
                 # add calibration info
                 spectrumTemplate = re.sub("\${CAL_INFOS}",' '.join(map(str,l)), spectrumTemplate)
              
                 # TODO to remove just there for testing, deal with the compression flag
                 if self._fetcher.get("%s_COMPRESSED"%(fname),False) == True :
                    spectrumTemplate = re.sub("\${COMPRESS}","compress=\"base64,zip\"",spectrumTemplate)
                 else:
                    spectrumTemplate = re.sub("\${COMPRESS}","",spectrumTemplate)
                     
               # add fill spectrum template in global template 
               finalTemplate += spectrumTemplate
        
        self._populatedTemplate = re.sub("\${SPECTRUM}",finalTemplate, self._populatedTemplate)
        
     
    def _getCategory(self,id):
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
        cat_dict = self._fetcher.get(u'%s_CAT_INFOS'%(id),{})
       
        # get the status. If it is R or Q get category otherwise it isn't defined yet
        status = cat_dict.get(u'CAT_STATUS',"")
        
        if (status == 'R') or (status == 'Q'):
            category = cat_dict.get(u'CAT_CATEGORY',"undefined")
            comment  = cat_dict.get(u'CAT_COMMENT',"No Comment")

            # if there is something fill the template otherwise do nothing
            if category != "undefined":
              # xml filler 
              cat_template = self._conf.get("TemplatingSystem","particulateCategoryTemplate")
        
              dummy_template = re.sub("\${CATEGORY}",str(category), cat_template)
              dummy_template = re.sub("\${CATEGORY_COMMENT}",comment, dummy_template)
        
        return dummy_template
    
    def _getNuclides(self,id):
        """ fill and return the information regarding the nuclides """
        
        # first add Non Quantified Nuclides
        template = self._conf.get("TemplatingSystem","particulateNuclideTemplate")
        
        xml_nuclides = ""
        dummy_template = ""
        cpt = 1
        
        GenieParticulateRenderer.c_log.debug("id = %s\n"%("%s_IDED_NUCLIDES"%(id)))
        
        # get categories
        ided_nuclides = self._fetcher.get("%s_IDED_NUCLIDES"%(id),[])
        
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
            dummy_template = re.sub("\${IDENTIFICATION_NUM}",str(nuclide['NID_FLAG_NUM']), dummy_template)
            
            # add generated xml in final container
            xml_nuclides += dummy_template
             
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
            
        
    def _getNuclideLines(self,id):
        """Get the Nuclide Lines information from the data hashtable and render it.
        
            Args:
               id: to fetch the info in the dict
        
            Returns:
              An XML string containing the formatted data.
              
            Raises:
               exception
        """
        
        # check if we need nuclidelines otherwise quit
        if self._conf.getboolean("Options","addNuclideLines") is False:
            SaunaRenderer.c_log.info("Configuration says no nuclide lines")
            return ""
        
        # get the global template
        global_template = self._conf.get("TemplatingSystem","particulateNuclideLinesTemplate")
        
        # first get Nuclide Lines template
        template = self._conf.get("TemplatingSystem","particulateOneNuclideLineTemplate")
        
        xml_nuclidelines   = ""
        dummy_template = ""
        cpt = 1
        
        # get categories
        nuclidelines = self._fetcher.get(u'%s_IDED_NUCLIDE_LINES'%(id),[])
        
        for line in nuclidelines:
            
            # if there is a peakID in the hash then replace it otherwise remove this info from the XML
            dummy_template = re.sub("\${PEAKID}",("peakID=\"%s\""%(line['PEAK']) if (line.get('PEAK',0) != 0) else ""), template)
            dummy_template = re.sub("\${NAME}",line['NAME'], dummy_template)
            dummy_template = re.sub("\${MDA}","%s"%(str(line['MDA'])), dummy_template)
           
            dummy_template = re.sub("\${ACTIVTIY}",( ("<Activity unit=\"mBq\">%s %s</Activity>"%(str(line['ACTIVITY']),str(line['ACTIV_ERR']))) if not (line['ACTIVITY'] == 0) else ""), dummy_template)
            dummy_template = re.sub("\${ENERGY}",("<Energy unit=\"keV\">%s %s</Energy>"%(str(line['ENERGY']),str(line['ENERGY_ERR'])) if ('ENERGY' in line) else ""), dummy_template)
            dummy_template = re.sub("\${ABUNDANCE}",("<Abundance unit=\"percent\">%s %s</Abundance>"%(str(line['ABUNDANCE']),str(line['ABUNDANCE_ERR'])) if ('ABUNDANCE' in line) else ""), dummy_template)
            dummy_template = re.sub("\${EFFICIENCY}",("<Efficiency unit=\"percent\">%s %s</Efficiency>"%(str(line['EFFIC']),str(line['EFFIC_ERR'])) if ('EFFIC' in line) else ""), dummy_template)
            
            # add generated xml in final container
            xml_nuclidelines += dummy_template
            
        #add nuclide lines in global template
        return re.sub("\${NUCLIDELINES}",xml_nuclidelines, global_template)
    
    def _getPeaks(self,id):
        """Get the peaks information from the data hashtable and render it .

         Args: 
           id: to fetch the info in the dict
          

         Returns:
           An XML String containing the formatted data.

         Raises:
          None.
        """
  
        peak_template = self._conf.get("TemplatingSystem","peaksTemplate")
        
        xml_peaks = ""
        dummy_template = ""
        
        # get peak
        peaks = self._fetcher.get(u'%s_PEAKS'%(id),{})
        
        for peak in peaks:
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
    
    def _getParameters(self,id):
        """Get the parameters information from the data hashtable and render it .

         Args: 
           id: to fetch the info in the dict
          

         Returns:
           An XML String containing the formatted data.

         Raises:
          None.
        """
        
         # first add Quantified Nuclides
        template = self._conf.get("TemplatingSystem","processingParametersTemplate")
        
        xml_parameters = ""
        dummy_template = ""
        
        # get processing parameters
        parameters = self._fetcher.get("%s_PROCESSING_PARAMETERS"%(id),None)
        
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
        parameters = self._fetcher.get("%s_UPDATE_PARAMETERS"%(id),{})
        
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
        
    def _getFlags(self,id):
        """create xml part with the flag info """
        
        # first add timeliness Flags
        template = self._conf.get("TemplatingSystem","timelinessFlagsTemplate")
        
        xml = ""
        dummy_template = ""
        dummy_template += template
          
        param = self._fetcher.get('%s_TIME_FLAGS_PREVIOUS_SAMPLE'%(id),False)
        if param == True:
            dummy_template = re.sub("\${PreviousSamplePresent}","true", dummy_template)
        else:
            dummy_template = re.sub("\${PreviousSamplePresent}","false", dummy_template)
        
        param = self._fetcher.get('%s_TIME_FLAGS_COLLECTION_WITHIN_24'%(id),0)
        if param == 0:
            dummy_template = re.sub("\${CollectionTime}","true", dummy_template)
        else:
            dummy_template = re.sub("\${CollectionTime}","false", dummy_template)
            
        param = self._fetcher.get('%s_TIME_FLAGS_ACQUISITION_FLAG'%(id),0)
        if param == 0:
            dummy_template = re.sub("\${AcquisitionTime}","true", dummy_template)
        else:
            dummy_template = re.sub("\${AcquisitionTime}","false", dummy_template)
        
        param = self._fetcher.get('%s_TIME_FLAGS_DECAY_FLAG'%(id),0)
        if param == 0:
            dummy_template = re.sub("\${DecayTime}","true", dummy_template)
        else:
            dummy_template = re.sub("\${DecayTime}","false", dummy_template)
            
        param = self._fetcher.get('%s_TIME_FLAGS_SAMPLE_ARRIVAL_FLAG'%(id),0)
        if param == 0:
            dummy_template = re.sub("\${SampleReceived}","true", dummy_template)
        else:
            dummy_template = re.sub("\${SampleReceived}","false", dummy_template)
       
        # add generated xml in final container
        xml += dummy_template
        
        # get Data Quality Flags
        template = self._conf.get("TemplatingSystem","dataQualityFlagsTemplate")
        
        # add Data Quality Flags
        dataQFlags = self._fetcher.get('%s_DATA_QUALITY_FLAGS'%(id),[])
        
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
        
    def _fillAnalysisResults(self,requestDict):
        """fill the analysis results for each result"""
        
        # check if there is a spectrum in the hashtable. If not replace ${SPECTRUM} by an empty string ""
        requestedTypes = requestDict[RequestParser.ANALYSIS]
        
        all_analyses_xml = ""
      
        for type in requestedTypes:
           
           #identifier in the dict for this analysis  
           id = self._fetcher.get("CURRENT_%s"%(type),None)
           
           if id is not None:
        
             # first get the template
             template = self._conf.get("TemplatingSystem","particulateAnalysisTemplate")
             dummy_template = ""
        
             # for the moment only one result
             dummy_template += template
        
             spectrum_id    = self._fetcher.get("%s_G_DATA_ID"%(self._fetcher.get("CURRENT_%s"%(type),'')),"unknown")
             
             # Add analysis identifier => SpectrumID prefixed by AN
             dummy_template = re.sub("\${ANALYSISID}","AN-%s"%(spectrum_id),dummy_template)
        
             dummy_template = re.sub("\${SPECTRUM_ID}",spectrum_id,dummy_template)
        
             dummy_template = re.sub("\${CATEGORY}", self._getCategory(id), dummy_template)
        
             dummy_template = re.sub("\${NUCLIDES}",self._getNuclides(id),dummy_template)
         
             dummy_template = re.sub("\${WITHNUCLIDELINES}",self._getNuclideLines(id),dummy_template)
        
             dummy_template = re.sub("\${PEAKS}",self._getPeaks(id),dummy_template)
         
             dummy_template = re.sub("\${PARAMETERS}",self._getParameters(id),dummy_template)
        
             dummy_template = re.sub("\${FLAGS}",self._getFlags(id),dummy_template)
             
             #add Calibration references
             l = self._fetcher.get("%s_G_DATA_ALL_CALS"%(id))
             if l is None :
                raise CTBTOError(-1,"Error no calibration information for sample %s, sid: %s\n"%(type,spectrum_id))
             else:
               # add calibration info
               dummy_template = re.sub("\${CAL_INFOS}",' '.join(map(str,l)),dummy_template)
        
             # add software method version info
             dummy_template = re.sub("\${SOFTWARE}","genie", dummy_template)
             dummy_template = re.sub("\${METHOD}","standard", dummy_template)
             dummy_template = re.sub("\${VERSION}","1.0", dummy_template)
             dummy_template = re.sub("\${SOFTCOMMENTS}","Old version", dummy_template)
             
             all_analyses_xml += dummy_template
        
        # add all the analysis info in the global template
        self._populatedTemplate = re.sub("\${AnalysisResults}",all_analyses_xml, self._populatedTemplate)
         
    def _fillCalibrationCoeffs(self,prefix,calibInfos):
        """ Insert the calibration information
        
            Args:
               prefix: the prefix for constituting the UID identifying the currently treated sampleID in the fetcher object
               calibInfos: set of calib info ids that have already been included in the xml
            
            Returns: generated xml data for displaying calibration info
               
            Raises:
               exception if issue fetching data (CTBTOError)
        """
        
        # first add Energy Cal
        template = self._conf.get("TemplatingSystem","particulateEnergyCalTemplate")
        
        xml = ""
        dummy_template = ""
        
        # get energy calibration 
        en_id = self._fetcher.get("%s_G_ENERGY_CAL"%(prefix),None)
        
        if (en_id is not None):
        
          # add calib info if it isn't there already
          if en_id not in calibInfos:
            energy = self._fetcher.get(en_id,{})
            dummy_template = re.sub("\${TERM0}",str(energy.get(u'COEFF1',"None")), template)
            dummy_template = re.sub("\${TERM1}",str(energy.get(u'COEFF2',"None")), dummy_template)
            dummy_template = re.sub("\${TERM2}",str(energy.get(u'COEFF3',"None")), dummy_template)
            dummy_template = re.sub("\${TERM3}",str(energy.get(u'COEFF4',"None")), dummy_template)
            dummy_template = re.sub("\${EN_ID}",en_id, dummy_template)
            # add generated xml in final container
            xml += dummy_template
            # add the id in the set of existing infos
            calibInfos.add(en_id)
        else:
            GenieParticulateRenderer.c_log.warning("Warning. Could not find any energy calibration info for sample %s\n"%(prefix))
        
        template = self._conf.get("TemplatingSystem","particulateResolutionCalTemplate")
        
        re_id = self._fetcher.get("%s_G_RESOLUTION_CAL"%(prefix),None)
        
        if re_id is not None: 
          # add calib info if it isn't there already
          if re_id not in calibInfos:
            # get resolution calibration 
            resolution = self._fetcher.get(re_id,{})
        
            dummy_template = re.sub("\${TERM0}",str(resolution.get('COEFF1',"None")), template)
            dummy_template = re.sub("\${TERM1}",str(resolution.get('COEFF2',"None")), dummy_template)
            dummy_template = re.sub("\${RE_ID}",re_id, dummy_template)
        
            # add generated xml in final container
            xml += dummy_template
    
            # add the id in the set of existing infos
            calibInfos.add(re_id)
        else:
           GenieParticulateRenderer.c_log.warning("Warning. Could not find any resolution calibration info for sample %s\n"%(prefix))
        
        template = self._conf.get("TemplatingSystem","particulateEfficencyCalTemplate")
        
        eff_id = self._fetcher.get("%s_G_EFFICIENCY_CAL"%(prefix),None)
        
        
        
        if (eff_id is not None):
          # add calib info if it isn't there already
          if eff_id not in calibInfos:
            # get efficiency calibration 
            eff = self._fetcher.get(eff_id,{})
        
            dummy_template = re.sub("\${LN_TERM0}",str(eff.get('COEFF1',"None")), template)
            dummy_template = re.sub("\${TERM0}",str(eff.get('COEFF2',"None")), dummy_template)
            dummy_template = re.sub("\${TERM1}",str(eff.get('COEFF3',"None")), dummy_template)
            dummy_template = re.sub("\${TERM2}",str(eff.get('COEFF4',"None")), dummy_template)
            dummy_template = re.sub("\${TERM3}",str(eff.get('COEFF5',"None")), dummy_template)
            dummy_template = re.sub("\${TERM4}",str(eff.get('COEFF6',"None")), dummy_template)
            dummy_template = re.sub("\${TERM5}",str(eff.get('COEFF7',"None")), dummy_template)
            dummy_template = re.sub("\${EF_ID}",eff_id, dummy_template)
        
            # add generated xml in final container
            xml += dummy_template
            
            # add the id in the set of existing infos
            calibInfos.add(eff_id)
        
        return xml
        
    def _fillCalibration(self):
        """ Add the calibration parameters for each of the spectrum"""
        
        xml =""
        # list of ids added in the xml document
        addedCalibrationIDs= set()
        
        for type in self._fetcher.get('CONTENT_PRESENT',[]):
            
           # treat preliminary samples differently as there is another indirection
           if type == 'PREL':
              for prefix in self._fetcher.get('CURR_List_OF_PRELS',[]):
                  if prefix is None:
                    raise CTBTOError(-1,"Error when filling Calibration info for prefix %s, There is no CURRENT_%s in the dataBag\n"%(prefix,prefix))
                
                  xml += self._fillCalibrationCoeffs(prefix,addedCalibrationIDs)    
           else:
                prefix = self._fetcher.get(u'CURRENT_%s'%(type),None)
                if prefix is None:
                  raise CTBTOError(-1,"Error when fetching Calibration info for prefix %s, There is no CURRENT_%s in the dataBag\n"%(prefix,prefix))
               
                xml += self._fillCalibrationCoeffs(prefix,addedCalibrationIDs)      
            
        # out of the loop
        self._populatedTemplate = re.sub("\${CALIBRATION}",xml, self._populatedTemplate)
       
    
    def asXmlStr(self,aRequest=""):
       """ return the xml particulate product according to the passed request
        
            Args:
               aRequest: string containing some parameters for each fetching bloc (ex params="specturm=curr/qc/prels/bk"). Default = ""
            
            Returns: the populated template
              
              
            Raises:
               exception if issue fetching data (CTBTOError)
       """
       
       # parse request to know what need to be added in the product
       # [Parsing could be done for once and shared between fetcher and renderer]
       reqDict = self._parser.parse(aRequest)
         
       self._fillData(reqDict)
       
       self._fillAnalysisResults(reqDict)
       
       self._fillCalibration()
       
       # father 
       BaseRenderer.asXmlStr(self,aRequest)
       
       return self._populatedTemplate
       
       
       
       
       
       