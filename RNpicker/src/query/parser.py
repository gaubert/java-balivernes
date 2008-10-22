import re
import logging


import common.utils
from common.exceptions import CTBTOError


class RequestParser(object):
    """ Class used to parse a user request """
    
    SPECTRUM = 'spectrum'
    
    # Class members
    c_log = logging.getLogger("query.RequestParser")
    c_log.setLevel(logging.DEBUG)
    
    # spectrum types
    c_spectrum_types = set(['CURR','QC','PREL','BK'])
    
    # regular expression stuff for spectrum param
    c_pattern        ="(?P<command>\s*spectrum\s*=\s*)(?P<values>[\w+\s*/\s*]*\w)\s*"
    c_spectrum_rex   = re.compile(c_pattern, re.IGNORECASE)
    
    def __init__(self,):
        """ constructor """
        # get reference to the conf object
        self._conf              = common.utils.Conf.get_instance()
        
    
    def parse(self,aRequest):
        """ parse the query request.
        
            Args:
               aRequest: Request to parse as a string
               
            Returns:
               return dict containing the different parts of the request (spectrum, ....)
        
            Raises:
               exception CTBTOError if the syntax of the aString string is incorrect
        """
        
        # for the moment we only have the spectrum part
        result = {}
        
        result[RequestParser.SPECTRUM] = self._parseSpectrumParams(aRequest)
        
        return result
     
     
    def _parseSpectrumParams(self,aRequest=""):
       
        """ parse the spectrum part of the params string. It should be something like spectrum=FULL/QC/BK.
            This is used to specify which of the spectra related to the current spectrum must be retrieved
            The different values:
            - ALL all the spectrum. This is the default,
            - FULL if the associated FULL spectrum should be retrieved,
            - QC the QC Spectrum
            - BK the Background Spectrum
        
            Args:
               aRequest: string of parameters in the form of param=values,param=values ....
                        From this string the spectrum=ALL or spectrum=QC/FULL is searched. 
                        The found values will be used to retrieved the related associated samples
               
            Returns:
               return List of spectrum types to fetch
        
            Raises:
               exception CTBTOError if the syntax of the aRequest string is incorrect
        """
        
        result = set()
        
        # try to match the spectrum param
        m = RequestParser.c_spectrum_rex.match(aRequest)
    
    
        if m is None:
            print("Warning, Cannot find the spectrum=val1/val2 in param string %s\nUse default spectrum=ALL"%(aRequest))
            result.update(DBDataFetcher.c_spectrum_types)
            return result
        
        values = m.group('values')
      
        vals = values.split('/')
      
        if len(vals) == 0:
          raise CTBTOError(-1,"Cannot find values for the spectrum params in parameters string %s"%(aRequest))
        
        for val in vals:
          dummy = val.strip().upper()
          
          if dummy == 'ALL':
             #ALL superseeds everything and add all the different types
             result.update(RequestParser.c_spectrum_types)
             # leave loop
             break
                
          if dummy not in RequestParser.c_spectrum_types:
              raise CTBTOError(-1,"Unknown spectrum type %s. The spectrum type can only be one of the following %s"%(dummy,RequestParser.c_spectrum_types))
          
          result.add(dummy)
          
        return result   