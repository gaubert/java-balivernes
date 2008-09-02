import logging
import re


import common.utils


class BaseRenderer(object):
    """ Base Class used to transform the fetcher content into XML """
    
    # Class members
    c_log = logging.getLogger("SAMPMLrendererv1.BaseRenderer")
    c_log.setLevel(logging.DEBUG)
    
    
    
    def __init__(self,aDataFetcher):
        
        self._conf     = common.utils.Conf.get_conf()
        self._fetcher  = aDataFetcher
        self._template = None
        self._populatedTemplate = None
        
        # dict used to substitute values in fetcher with template values
        self._substitutionDict = {  "SAMPLEID"           :   "SAMPLE_ID",
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
                                 }
                                  
        self._createTemplate()
        
        
    
    def _createTemplate(self):
        """ Read XML template from a file and store it in a String """
        
        # get template path from conf
        path = self._conf.get("TemplatingSystem","baseTemplate")
        
        # assert that the file exists
        common.utils.file_exits(path)
        
        # read the full template in a string buffer
        f = open(path,"r") 
        
        self._template = f.read()
        
        self._populatedTemplate = self._template
        
    
    def _substituteValues(self):
        """ substitue values """
        
        for (key,val) in self._substitutionDict.items():
            pattern = "\${%s}"%(key)
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
        self._spectrumTemplate = None
        
        self._readSpectrumTemplate()
        
        # add values specific to Particulates
        dummy_dict = {  "COL_START"                      :   "DATA_COLLECT_START",
                        "COL_STOP"                       :   "DATA_COLLECT_STOP",
                        "ACQ_START"                      :   "DATA_ACQ_START",
                        "ACQ_STOP"                       :   "DATA_ACQ_STOP",
                        "SAMPLING_TIME"                  :   "DATA_SAMPLING_TIME",
                        "REAL_ACQ_TIME"                  :   "DATA_ACQ_REAL_SEC",
                        "LIVE_ACQ_TIME"                  :   "DATA_ACQ_LIVE_SEC",
                        "DECAY_TIME"                     :   "DATA_DECAY_TIME",
                        "SPECTRUM_DATA"                  :   "rawdata_SPECTRUM",
                        "SPECTRUM_DATA_CHANNEL_SPAN"     :   "rawdata_SPECTRUM_channel_span",
                        "SPECTRUM_DATA_ENERGY_SPAN"      :   "rawdata_SPECTRUM_energy_span",                
                      }
        # add specific particulate keys
        self._substitutionDict.update(dummy_dict)
        
    def _readSpectrumTemplate(self):
        """ Read XML template from a file and store it in a String """
        
        # get template path from conf
        path = self._conf.get("TemplatingSystem","particulateSpectrumTemplate")
        
        # assert that the file exists
        common.utils.file_exits(path)
        
        # read the full template in a string buffer
        f = open(path,"r") 
        
        self._spectrumTemplate = f.read()
        
    
    def _fillRawData(self):
        """ insert particulate spectrum data in final produced XML file """
     
        # Add spectrum template in final SAMPML template
        pattern = "\${SPECTRUM}"
        self._populatedTemplate = re.sub(pattern,self._spectrumTemplate, self._populatedTemplate)
        
    def _fillCategories(self):
        """ fill Categories """
        
        cat_template = self._conf.get("TemplatingSystem","particulateCategoryTemplate")
        
        xml_categories = ""
        dummy_template = ""
        
        # get categories
        categories = self._fetcher.get(u'CATEGORIES',"None")
        
        for category in categories:
            dummy_template = re.sub("\${CATEGORY}",str(category['CAT_CATEGORY']), cat_template)
            dummy_template = re.sub("\${CATEGORY_NUCLIDE}",category['CAT_NUCL_NAME'], dummy_template)
            dummy_template = re.sub("\${CATEGORY_COMMENT}",category.get('CAT_COMMENT',"No Comment"), dummy_template)
            # add generated xml in final container
            xml_categories += dummy_template
             
        # add Category info in generated template
        self._populatedTemplate = re.sub("\${CATEGORIES}",xml_categories, self._populatedTemplate)
     
    def _fillPeaks(self):
        """ fill Categories """
        
        peak_template = self._conf.get("TemplatingSystem","peaksTemplate")
        
        xml_peaks = ""
        dummy_template = ""
        
        # get peak
        peaks = self._fetcher.get(u'PEAKS',"None")
        
        for peak in peaks:
            #print "peak = %s"%(peak)
            dummy_template = re.sub("\${ENERGY}","%s %s"%(str(peak['ENERGY']),str(peak['ENERGY_ERR'])), peak_template)
            dummy_template = re.sub("\${CENTROID}","%s %s"%(str(peak['CENTROID']),str(peak['CENTROID_ERR'])), dummy_template)
            dummy_template = re.sub("\${AREA}","%s %s"%(str(peak['AREA']),str(peak['AREA_ERR'])), dummy_template)
            dummy_template = re.sub("\${WIDTH}",str(peak['WIDTH']), dummy_template)
            dummy_template = re.sub("\${FWHM}","%s %s"%(str(peak['FWHM']),str(peak['FWHM_ERR'])), dummy_template)
            dummy_template = re.sub("\${BACKGROUNDCOUNTS}","%s %s"%(str(peak['BACK_COUNT']),str(peak['BACK_UNCER'])), dummy_template)
            dummy_template = re.sub("\${EFFICIENCY}","%s %s"%(str(peak['EFFICIENCY']),str(peak['EFF_ERROR'])), dummy_template)
            dummy_template = re.sub("\${LC}",str(peak['LC']), dummy_template)
            
            # to be checked with Romano
            dummy_template = re.sub("\${LD}","None", dummy_template)
            dummy_template = re.sub("\${DETECTIBILITY}",str(peak['DETECTABILITY']), dummy_template)
            
            dummy_template = re.sub("\${NUCLIDE}","None", dummy_template)
            # to be checked
            dummy_template = re.sub("\${NUCLIDE_PERCENTAGE}",str(100),dummy_template)
            
            # add generated xml in final container
            xml_peaks += dummy_template
               
        # add Category info in generated template
        self._populatedTemplate = re.sub("\${PEAKS}",xml_peaks, self._populatedTemplate)
        
    def _fillNuclides(self):
        """ fill Quantified and Non Quantified Nuclides """
        
        # first add Non Quantified Nuclides
        template = self._conf.get("TemplatingSystem","particulateNonQuantifiedTemplate")
        
        xml_nonquantified_nuclides = ""
        dummy_template = ""
        
        # get categories
        nquantifiedNuclides = self._fetcher.get("NON_QUANTIFIED_NUCLIDES","None")
        
        for nuclide in nquantifiedNuclides:
            dummy_template = re.sub("\${NAME}",nuclide['NAME'], template)
            dummy_template = re.sub("\${TYPE}",nuclide['TYPE'], dummy_template)
            # add generated xml in final container
            xml_nonquantified_nuclides += dummy_template
            
        #print "xml_nonquantified_nuclides = %s"%(xml_nonquantified_nuclides)
        
        # add Category info in generated template
        self._populatedTemplate = re.sub("\${NON_QUANTIFIED_NUCLIDES}",xml_nonquantified_nuclides, self._populatedTemplate)
        
         # first add Quantified Nuclides
        template = self._conf.get("TemplatingSystem","particulateQuantifiedTemplate")
        
        xml_quantified_nuclides = ""
        dummy_template = ""
        
        # get categories
        quantifiedNuclides = self._fetcher.get("QUANTIFIED_NUCLIDES","None")
        
        for nuclide in quantifiedNuclides:
            dummy_template = re.sub("\${NAME}",nuclide['NAME'], template)
            dummy_template = re.sub("\${TYPE}",nuclide['TYPE'], dummy_template)
            dummy_template = re.sub("\${HALFLIFE}",str(nuclide['HALFLIFE']), dummy_template)
            dummy_template = re.sub("\${CONCENTRATION}",str(nuclide['ACTIV_KEY']), dummy_template)
            dummy_template = re.sub("\${CONCENTRATION_ERROR}",str(nuclide['ACTIV_KEY_ERR']), dummy_template)
            # add generated xml in final container
            xml_quantified_nuclides += dummy_template
            
        #print "xml_quantified_nuclides = %s"%(xml_quantified_nuclides)
        
        # add Category info in generated template
        self._populatedTemplate = re.sub("\${QUANTIFIED_NUCLIDES}",xml_quantified_nuclides, self._populatedTemplate)
        
        # first add MDA information
        template = self._conf.get("TemplatingSystem","particulateMDATemplate")
        
        xml_mda = ""
        dummy_template = ""
        
        # get categories
        mdaNuclides = self._fetcher.get("MDA_NUCLIDES","None")
        
        for nuclide in mdaNuclides:
            dummy_template = re.sub("\${NAME}",nuclide['NAME'], template)
            dummy_template = re.sub("\${HALFLIFE}",str(nuclide['HALFLIFE']), dummy_template)
            dummy_template = re.sub("\${MDA}","%s %s"%(str(nuclide['MDA']),str(nuclide['MDA_ERR'])), dummy_template)
            # add generated xml in final container
            xml_quantified_nuclides += dummy_template
            
        #print "xml_quantified_nuclides = %s"%(xml_quantified_nuclides)
        
        # add Category info in generated template
        self._populatedTemplate = re.sub("\${MDA_NUCLIDES}",xml_quantified_nuclides, self._populatedTemplate)
        
        
        
    def _fillAnalysisResults(self):
        """fill the analysis results """
         
        self._fillCategories()
        
        self._fillNuclides()
        
        self._fillPeaks()
       
        
        
        
    def asXmlStr(self):
       """ Return an xml tree as a string """
        
       self._fetcher.printContent(open("/tmp/sample_extract.data","w"))
        
       self._fillRawData()
       
       self._fillAnalysisResults()
        
       # father 
       BaseRenderer.asXmlStr(self)
       
       return self._populatedTemplate
       
       
       
       
       
       