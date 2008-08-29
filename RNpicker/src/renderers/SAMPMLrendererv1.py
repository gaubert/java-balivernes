import logging
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
        
        # dict used to substitute values in fetcher with template values
        self._substitutionDict = {  "\${SAMPLEID}":"data_sample_id",
                                    "\${STATION_CODE}":"station_code",
                                    "\${COUNTY_CODE}":"country_code"
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
        
    
    def _substituteValues(self):
        """ substitue values """
        
        for (key,val) in self._substitutionDict.items():
            print "key = %s, val = %s"%(key,val)
            
        
             
        
    def asXml(self):
        """  """
        
    def asXmlStr(self):
        """ Return an xml tree as a string """
        
        print "into asXMLStr"
        
        self._substituteValues()