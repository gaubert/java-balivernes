import re
import logging


from ctbto.common import CTBTOError
from org.ctbto.conf import Conf


class RequestParser(object):
    """ Class used to parse a user request """
    
    SPECTRUM = 'spectrum'
    ANALYSIS = 'analysis'
    GAS      = 'GAS'
    PAR      = 'PAR'
    
    # Class members
    c_log = logging.getLogger("query.RequestParser")
    c_log.setLevel(logging.DEBUG)
    
    # spectrum types
    c_spectrum_particulate_types   = set(['NONE','CURR','QC','PREL','BK'])
    c_spectrum_particulate_default = set(['CURR','QC','PREL','BK'])
    
    c_analysis_particulate_types   = set(['NONE','CURR','QC','PREL','BK'])
    c_analysis_particulate_default = set(['CURR','QC','PREL','BK'])
    
    c_spectrum_gas_types           = set(['NONE','CURR','QC','PREL','DETBK','GASBK'])
    c_spectrum_gas_default         = set(['CURR','QC','PREL','GASBK','DETBK'])
    
    c_analysis_gas_types           = set(['NONE','CURR','QC','PREL','BK'])
    c_analysis_gas_default         = set(['CURR','QC','PREL','BK'])
    
    # regular expression stuff for spectrum param
    c_spectrum_pattern             ="(?P<command>\s*spectrum\s*=\s*)(?P<values>[\w+\s*/\s*]*\w)\s*"
    c_spectrum_rex        = re.compile(c_spectrum_pattern, re.IGNORECASE)
    c_analysis_pattern    ="(?P<command>\s*analysis\s*=\s*)(?P<values>[\w+\s*/\s*]*\w)\s*"
    c_analysis_rex        = re.compile(c_analysis_pattern, re.IGNORECASE)
    
    c_spectrum = "spectrum"
    c_analysis = "analysis"
    
    def __init__(self,):
        """ constructor """
        # get reference to the conf object
        self._conf              = Conf.get_instance()
        
        
    def parse(self,aRequest,aTechnType):
        """ parse the query request.
        
            Args:
               aTechType: Technology Type : GAS or PAR
               aRequest: Request to parse as a string
               
            Returns:
               return dict containing the different parts of the request (spectrum, ....)
        
            Raises:
               exception CTBTOError if the syntax of the aString string is incorrect
        """
        
        # preconditions
        if aTechnType == None or aTechnType == "":
            raise CTBTOError(-1,"Error. No technology type passed to the parser %s\n"%(aTechnType))
        
        # for the moment we only have the spectrum part
        # quick and dirty parser, needs to be changed
        result = {}
        
        l = aRequest.split(',')
        
        for elem in l:  
            if elem.lower().find(RequestParser.c_spectrum) != -1:
                if aTechnType == RequestParser.GAS:
                   result[RequestParser.SPECTRUM] = self._parseSpectrumParams(elem,RequestParser.c_spectrum_gas_types,RequestParser.c_spectrum_gas_default)
                elif aTechnType == RequestParser.PAR:
                   result[RequestParser.SPECTRUM] = self._parseSpectrumParams(elem,RequestParser.c_spectrum_particulate_types,RequestParser.c_spectrum_particulate_default)
            
            if elem.lower().find(RequestParser.c_analysis) != -1:
                if aTechnType == RequestParser.GAS:
                   result[RequestParser.ANALYSIS] = self._parseAnalysisParams(elem,RequestParser.c_analysis_gas_types,RequestParser.c_analysis_gas_default)
                elif aTechnType == RequestParser.PAR:
                   result[RequestParser.ANALYSIS] = self._parseAnalysisParams(elem,RequestParser.c_analysis_particulate_types,RequestParser.c_analysis_particulate_default)
        
        return result
    
    def _parseAnalysisParams(self,aRequest,aAnalysisTypes,aAnalysisTypesDefault):
       
        """ parse the analysis part of the params string. It should be something like analysis=CURR/QC/BK/PREL.
            This is used to specify which of the spectra related to the current spectrum must be retrieved
            The different values:
            - ALL all the analyses. 
            - CURR if the analysis associated with the current spectrum should be retrieved,
            - QC the QC Analysis
            - BK the Background Analysis
        
            Args:
               aRequest: string of parameters in the form of param=values,param=values ....
                        From this string the analysis=ALL or analysis=QC/CURR is searched. 
                        The found values will be used to retrieved the related associated samples
               
            Returns:
               return List of spectrum types to fetch
        
            Raises:
               exception CTBTOError if the syntax of the aRequest string is incorrect
        """
        
        result = set()
        
        # try to match the spectrum param
        m = RequestParser.c_analysis_rex.match(aRequest)
    
        if m is None:
            RequestParser.c_log.warning("Warning, Cannot find the analysis=val1/val2 in param string %s\nUse default analysis=CURR"%(aRequest))
            result.add('CURR')
            return result
        
        values = m.group('values')
      
        vals = values.split('/')
      
        if len(vals) == 0:
          raise CTBTOError(-1,"Cannot find values for the analysis params in parameters string %s"%(aRequest))
        
        for val in vals:
          dummy = val.strip().upper()
          
          if dummy == 'ALL':
             #ALL superseeds everything and add all the different types
             result.update(aAnalysisTypesDefault)
             # leave loop
             break
                
          if dummy not in aAnalysisTypes:
              raise CTBTOError(-1,"Unknown analysis type %s. The analysis type can only be one of the following %s"%(dummy,aAnalysisTypes))
          
          result.add(dummy)
          
        return result  
    
     
    def _parseSpectrumParams(self,aRequest,aSpectrumTypes,aSpectrumTypeDefault):
       
        """ parse the spectrum part of the params string. It should be something like spectrum=CURR/QC/BK.
            This is used to specify which of the spectra related to the current spectrum must be retrieved
            The different values:
            - ALL all the spectrum. This is the default,
            - CURR if the associated CURR spectrum should be retrieved,
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
            RequestParser.c_log.warning("Warning, Cannot find the spectrum=val1/val2 in param string %s\nUse default spectrum=ALL"%(aRequest))
            result.update(aSpectrumTypes)
            return result
        
        values = m.group('values')
      
        vals = values.split('/')
      
        if len(vals) == 0:
            raise CTBTOError(-1,"Cannot find values for the spectrum params in parameters string %s"%(aRequest))
        
        for val in vals:
            dummy = val.strip().upper()
          
            if dummy == 'ALL':
                #ALL superseeds everything and add all the different types
                result.update(aSpectrumTypeDefault)
                # leave loop
                break
                
            if dummy not in aSpectrumTypes:
                raise CTBTOError(-1,"Unknown spectrum type %s. The spectrum type can only be one of the following %s"%(dummy,aSpectrumTypes))
          
            result.add(dummy)
          
        return result   