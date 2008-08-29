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
        
        # for debug purpose
        self._fetcher.printContent(open("/tmp/sample_extract.data","w"))
        
        for (key,val) in self._substitutionDict.items():
            pattern = "\${%s}"%(key)
            self._populatedTemplate = re.sub(pattern, str(self._fetcher.get(val,"None")), self._populatedTemplate)
            
        common.utils.printInFile(self._populatedTemplate,"/tmp/subs-template.xml")
             
        
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
        
    
    def _fillRawData(self):
        
        
        
    def asXmlStr(self):
       """ Return an xml tree as a string """
        
       # father method first
       BaseRenderer.asXmlStr(self)
       
       self._fillRawData()
       
       
       
       
       