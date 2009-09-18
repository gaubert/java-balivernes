from jinja2   import Environment
from jinja2   import FileSystemLoader
from lxml     import etree
from datetime import datetime

import logging

import ctbto.common.utils as utils
import ctbto.common.time_utils as time_utils

UNDEFINED = "N/A"
RDIGITS   = 5 
BGDIGITS  = 2
HDIGITS   = 2

class XML2HTMLRenderer(object):
    """ Base Class used to transform XML in HTML """
    
    # Class members
    c_log = logging.getLogger("html.XML2HTMLRenderer")
    
    c_namespaces = {'sml':'http://www.ctbto.org/SAMPML/0.7'}

class SAUNAXML2HTMLRenderer(object):
    """ Base Class used to transform SAUNA XML in HTML """
    
    def __init__(self, TemplateDir='/home/aubert/dev/src-reps/java-balivernes/RNpicker/etc/conf/templates', TemplateName='NewSaunaArrHtml.html'):
        
        self._env         = Environment(loader=FileSystemLoader(TemplateDir))
        
        self._template    = self._env.get_template(TemplateName)
        
        self._context     = {}
    
    def render(self, aXmlPath):
        """ render the file using a template engine """  
        self._fill_values(aXmlPath)
       
        XML2HTMLRenderer.c_log.debug("context = %s\n" % (self._context))
         
        return self._template.render(self._context)    
      
    def _fill_values(self, aXmlPath):
        
        dom_tree = etree.parse(open(aXmlPath,'r'))
       
        root = dom_tree.getroot()
       
        expr = "//*[local-name() = $name]"

        # get station code
        res = root.xpath(expr, name = "StationCode")
        if len(res) > 0:
            self._context['station_code'] = res[0].text
        else:
            self._context['station_code'] = UNDEFINED
    
        # get station location
        res = root.xpath(expr, name = "StationLocation")
        if len(res) > 0:
            self._context['station_location'] = res[0].text
        else:
            self._context['station_location'] = UNDEFINED
           
        # get station coordinates
        res = root.xpath(expr, name = "Coordinates")
        if len(res) > 0:
            dummy_str = res[0].text
            if dummy_str != None:
                (lat,lon,height) = dummy_str.split(' ')
                self._context['station_lat'] = lat
                self._context['station_lon'] = lon
                self._context['station_height'] = height
                self._context['station_gmaps']     = "http://maps.google.com/maps?q=%s,%s+(%s)&iwloc=A&hl=en&z=3"%(lat,lon,self._context['station_code'])
                self._context['station_static_gmaps'] = "http://maps.google.com/staticmap?center=%s,%s&zoom=5&size=400x400&markers=%s,%s,greens"%(lat,lon,lat,lon)
            else:
                self._context['station_lat']    = UNDEFINED
                self._context['station_lon']    = UNDEFINED
                self._context['station_height'] = UNDEFINED
                self._context['station_gmaps']  = "#"
        else:
            self._context['station_lat']    = UNDEFINED
            self._context['station_lon']    = UNDEFINED
            self._context['station_height'] = UNDEFINED
            self._context['station_gmaps']  = "#"
       
           
           
        # http://maps.google.com/maps?q=-12.4,+130.7+(This%20is%20my%20station%20here)&iwloc=A&hl=en&z=5
       
        # get Detector Code
        res = root.xpath(expr, name = "DetectorCode")
        if len(res) > 0:
            self._context['detector_code'] = res[0].text
        else:
            self._context['detector_code'] = UNDEFINED
       
        # get detector description
        res = root.xpath(expr, name = "DetectorDescription")
        if len(res) > 0:
            self._context['detector_description'] = res[0].text
        else:
            self._context['detector_description'] = UNDEFINED
           
        # get sample type
        res = root.xpath(expr, name = "SampleType")
        if len(res) > 0:
            self._context['sample_type'] = res[0].text
        else:
            self._context['sample_type']     = UNDEFINED
          
       
        res = root.xpath(expr, name = "ArrivalDate")
        if len(res) > 0:
            self._context['arrival_date'] = time_utils.getOracleDateFromISO8601(res[0].text)
        else:
            self._context['arrival_date']     = UNDEFINED
       
        self._context['collection_comments'] = UNDEFINED
       
        # for the dates, a prefix is needed
        # for the moment always take SPHD-G but it has to be configurable
        #dateExpr = "//*[local-name() = \"Spectrum\" and ends-with(@id,\"SPHD-G\")]"
        # no ends-with in xpath 1.0 use contains instead substring('','') as it is simpler
        # and it does the trick
        dateExpr             = "//*[local-name() = $name and contains(@id,$suffix)]"
        curr_spectrum_id     = None
 
        # res is Element Spectrum 
        res = root.xpath(dateExpr,suffix = 'SPHD',name   = 'SpectrumGroup')
        if len(res) > 0:
            elem = res[0]
            # get attribute id
            curr_spectrum_id = elem.get('id')
            l = curr_spectrum_id.split('-')
            self._context['sample_id'] = '%s'%(l[1])
           
            # get calibrationIDs
            self._context['calibration_ids'] = elem.get('calibrationIDs').split(' ')
           
            # get geometry
            res = elem.xpath(expr,name = "Geometry")
            if len(res) == 0:
                self._context['sample_geometry'] = UNDEFINED
            else:
                self._context['sample_geometry'] = res[0].text
           
            # get quantity
            res = elem.xpath(expr,name = "ProcessedAirVolume")
            if len(res) == 0:
                self._context['sample_quantity']      = UNDEFINED
                self._context['sample_quantity_unit'] = "" 
            else:
                self._context['sample_quantity']      = utils.round_as_string(res[0].text, 3)
                self._context['sample_quantity_unit'] = res[0].get('unit') 
                
            # get Xe volume
            res = elem.xpath(expr, name = "XeVolume")
            if len(res) == 0:
                self._context['xe_vol']      = UNDEFINED
                self._context['xe_vol_unit'] = "" 
            else:
                self._context['xe_vol']      = utils.round_as_string(res[0].text,3)
                self._context['xe_vol_unit'] = res[0].get('unit') 
            
            #get Corr Xe volume also called sample quantity
            res = elem.xpath(expr,name = "SampleQuantity")
            if len(res) == 0:
                self._context['xe_corr_vol']      = UNDEFINED
                self._context['xe_corr_vol_unit'] = "" 
            else:
                self._context['xe_corr_vol']      = utils.round_as_string(res[0].text,3)
                self._context['xe_corr_vol_unit'] = res[0].get('unit')
           
            # all timing information
            c_start = time_utils.getOracleDateFromISO8601(elem.xpath(expr,name = "CollectionStart")[0].text)
            c_stop  = time_utils.getOracleDateFromISO8601(elem.xpath(expr,name = "CollectionStop")[0].text)
           
            a_start = time_utils.getOracleDateFromISO8601(elem.xpath(expr,name = "AcquisitionStart")[0].text)
            a_stop  = time_utils.getOracleDateFromISO8601(elem.xpath(expr,name = "AcquisitionStop")[0].text)
           
            a_time  = time_utils.transformISO8601PeriodInFormattedTime(elem.xpath(expr,name = "RealAcquisitionTime")[0].text)
           
            sampling_time = time_utils.transformISO8601PeriodInFormattedTime(elem.xpath(expr,name = "SamplingTime")[0].text)
            decay_time    = time_utils.transformISO8601PeriodInFormattedTime(elem.xpath(expr,name = "DecayTime")[0].text)
           
            # to be added
            flow_rate     = utils.round_as_string(elem.xpath(expr,name = "FlowRate")[0].text,3)
           
            self._context['collection_start']  = c_start
            self._context['collection_stop']   = c_stop
            self._context['acquisition_start'] = a_start
            self._context['acquisition_stop']  = a_stop
            self._context['acquisition_time']  = a_time
            self._context['sampling_time']     = sampling_time
            self._context['decay_time']        = decay_time
            self._context['avg_flow_rate']     = flow_rate      
        else:
            self._context['sample_id']         = UNDEFINED
            self._context['sample_geometry']   = UNDEFINED
           
        # add Activity Concentration for Nuclides
        #concNuclideExpr = "//*[local-name() = $name and contains(@spectrumIDs,'NOX49-239646-SPHD-G')]"
        concNuclideExpr = "//*[local-name() = $name and contains(@spectrumIDs,$spectrum_id)]"
        res = root.xpath(concNuclideExpr,name = "Analysis",spectrum_id=curr_spectrum_id )
        if len(res) > 0:
            analysis_elem = res[0]
            # get all ided nuclides
            res = analysis_elem.find("{%s}IdedNuclides"%(XML2HTMLRenderer.c_namespaces['sml']))
            q_nuclides  = []
            nq_nuclides = []
            a_nuclides  = []
            # iterate over the children of ided nuclides => the nuclides
            for nuclide in res:
              
                # check that nid_flag is 1 to go in quantified_nuclides otherwise goes into non_quantified_nuclides
                nid_flag = nuclide.find('{%s}NuclideIdentificationIndicator'%(XML2HTMLRenderer.c_namespaces['sml'])).get("numericVal")
                if nid_flag == '1':
                    d = {}
                    # get Name, 
                    d['name']      = nuclide.find('{%s}Name'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                    d['half_life'] = nuclide.find('{%s}HalfLife'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                    d['conc']      = utils.round_as_string(nuclide.find('{%s}Concentration'%(XML2HTMLRenderer.c_namespaces['sml'])).text,RDIGITS)
                    d['conc_abs_err']  = utils.round_as_string(nuclide.find('{%s}AbsoluteConcentrationError'%(XML2HTMLRenderer.c_namespaces['sml'])).text,RDIGITS)
                    d['conc_rel_err']  = utils.round_as_string(nuclide.find('{%s}RelativeConcentrationError'%(XML2HTMLRenderer.c_namespaces['sml'])).text,RDIGITS)
              
                    q_nuclides.append(d)
                else:
                    d = {}
                    # get Name, 
                    d['name']      = nuclide.find('{%s}Name'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                    mdc = nuclide.find('{%s}MDC'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                    if mdc != "N/A":
                        d['mdc']       = utils.round_as_string(mdc,RDIGITS)
                    else:
                        d['mdc']       = "N/A"
               
                    # get numeric val for the moment but can put some text there
                    # removed as asked by Matthias
                    #d['nid_flag']  = nuclide.find('{%s}NuclideIdentificationIndicator'%(XML2HTMLRenderer.c_namespaces['sml'])).get("numericVal")
                    nq_nuclides.append(d)
                
                # in any cases fill Activity results dict
                d = {}
                d['name']              = nuclide.find('{%s}Name'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                d['activity']          = utils.round_as_string(nuclide.find('{%s}Activity'%(XML2HTMLRenderer.c_namespaces['sml'])).text,RDIGITS)
                d['activity_abs_err']  = utils.round_as_string(nuclide.find('{%s}AbsoluteActivityError'%(XML2HTMLRenderer.c_namespaces['sml'])).text,RDIGITS)
                d['activity_rel_err']  = utils.round_as_string(nuclide.find('{%s}RelativeActivityError'%(XML2HTMLRenderer.c_namespaces['sml'])).text,RDIGITS)
                d['lc']                = utils.round_as_string(nuclide.find('{%s}LCActivity'%(XML2HTMLRenderer.c_namespaces['sml'])).text,RDIGITS)
                d['ld']                = utils.round_as_string(nuclide.find('{%s}LDActivity'%(XML2HTMLRenderer.c_namespaces['sml'])).text,RDIGITS)
                a_nuclides.append(d)
           
            self._context['non_quantified_nuclides'] = nq_nuclides
            self._context['quantified_nuclides']     = q_nuclides 
            self._context['activities_nuclides']     = a_nuclides 
        
            # Add ROI results
            # get ROIInfo
            res = analysis_elem.find("{%s}RoiInfo"%(XML2HTMLRenderer.c_namespaces['sml'])) 
            if res == None:
                res = []
           
            # iterate over RoiNetCount
            roi_results    = []
            roi_boundaries = []
           
            for roi in res:
               
                if roi.tag.find('RoiNetCount') != -1:
                    # if it is RoiNetCount 
                    d = {}
                    d['roi_number']       =  roi.find('{%s}RoiNumber'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                    d['name']             =  roi.find('{%s}Name'%(XML2HTMLRenderer.c_namespaces['sml'])).text
               
                    n_counts              =  roi.find('{%s}NetCounts'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                    if n_counts is not None:
                        (n_c,n_c_err) = n_counts.split(' ')
                        d['net_counts']     = utils.round_as_string(n_c,RDIGITS)
                        d['net_counts_err'] = utils.round_as_string(n_c_err,RDIGITS)
                    else:
                        d['net_counts']     = "N/A"
                        d['net_counts_err'] = "N/A"
                      
                    d['lc']               =  utils.round_as_string(roi.find('{%s}LC'%(XML2HTMLRenderer.c_namespaces['sml'])).text,RDIGITS)
                 
                    val = roi.find('{%s}Efficiency'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                    if val != UNDEFINED:
                        val = utils.round_as_string(val,RDIGITS)
                    
                    d['efficiency']       =  val
                 
                    val = roi.find('{%s}AbsoluteEfficiencyError'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                    if val != UNDEFINED:
                        val = utils.round_as_string(val,RDIGITS)
                    
                    d['efficiency_abs_error'] =  val
                 
                    val = roi.find('{%s}RelativeEfficiencyError'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                    if val != UNDEFINED:
                        val = utils.round_as_string(val,RDIGITS)
           
                    d['efficiency_rel_error'] =  val
                 
                    roi_results.append(d)
                 
                elif roi.tag.find('RoiBoundaries') != -1:
                    # Boundaries
                    d = {}
                    d['roi_number']       =  roi.find('{%s}RoiNumber'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                    d['gammalow']         =  utils.round_as_string(roi.find('{%s}GammaLow'%(XML2HTMLRenderer.c_namespaces['sml'])).text,BGDIGITS)
                    d['gammahigh']        =  utils.round_as_string(roi.find('{%s}GammaHigh'%(XML2HTMLRenderer.c_namespaces['sml'])).text,BGDIGITS)
                    d['betalow']          =  utils.round_as_string(roi.find('{%s}BetaLow'%(XML2HTMLRenderer.c_namespaces['sml'])).text,BGDIGITS)
                    d['betahigh']         =  utils.round_as_string(roi.find('{%s}BetaHigh'%(XML2HTMLRenderer.c_namespaces['sml'])).text,BGDIGITS)
                   
                    roi_boundaries.append(d)
                else:
                    XML2HTMLRenderer.c_log.error("No ROI info for %s"%(self._context['sample_id'])) 
                  
            self._context['roi_results']    = roi_results
            self._context['roi_boundaries'] = roi_boundaries
           
            # Add Flags
           
            # timeliness flags
            res = analysis_elem.find("{%s}Flags/{%s}TimelinessAndAvailabilityFlags"%(XML2HTMLRenderer.c_namespaces['sml'],XML2HTMLRenderer.c_namespaces['sml']))  
            if res == None:
                res = []
            
            flags = []
           
            for timeflag in res:
                d = {}
               
                if timeflag.tag.find('CollectionTime') != -1:
                   
                    d['name']  = 'Sampling Time'
                   
                elif timeflag.tag.find('AcquisitionTime') != -1:
                  
                    d['name']  = 'AcquisitionTime'
                   
                elif timeflag.tag.find('DecayTime') != -1:
               
                    d['name']  = 'Decay Time'
               
                elif timeflag.tag.find('ResponseTime') != -1:
               
                    d['name']  = 'Response Time'
                else:
                    XML2HTMLRenderer.c_log.error("Unknown Timeliness Flag: %s"%(timeflag.tag))   
                    d['name']  = timeflag.tag
               
                d['result'] = timeflag.find('{%s}Pass'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                try:
                    d['value']  = utils.round_as_string(timeflag.find('{%s}Value'%(XML2HTMLRenderer.c_namespaces['sml'])).text,HDIGITS)
                except Exception, e:
                    #cannot convert this number value so put the string as it is
                    d['value']  = timeflag.find('{%s}Value'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                    
                d['test']   = timeflag.find('{%s}Test'%(XML2HTMLRenderer.c_namespaces['sml'])).text
            
                flags.append(d)
            
            # data quality flags
            res = analysis_elem.find("{%s}Flags/{%s}DataQualityFlags"%(XML2HTMLRenderer.c_namespaces['sml'],XML2HTMLRenderer.c_namespaces['sml']))  
            if res == None:
                res = []
                
            for dqflag in res:
                d = {}
               
                if dqflag.tag.find('XeVolume') != -1:
                    d['name']  = 'Stable Xenon Volume'
                else:
                    XML2HTMLRenderer.c_log.error("Unknown DataQuality Flag: %s"%(dqflag.tag))   
                    d['name']  = dqflag.tag
               
                d['result'] = dqflag.find('{%s}Pass'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                d['value']  = utils.round_as_string(dqflag.find('{%s}Value'%(XML2HTMLRenderer.c_namespaces['sml'])).text,3)
                d['test']   = dqflag.find('{%s}Test'%(XML2HTMLRenderer.c_namespaces['sml'])).text
            
                flags.append(d)
            
            self._context['flags'] = flags
           
            res = root.xpath("//*[local-name() = $name]",name = "CalibrationInformation")
            if len(res) > 0:
             
                # add calibration 
                res = res[0]
             
                calibrations = []
           
                for calibration in res:
               
                    # if calibration is related to the displayed spectrum
                    cid = calibration.get('ID')
                    if cid in self._context['calibration_ids']:
                        d   = {}
                        d['desc'] = calibration.get('Type','N/A')
               
                        equation  = calibration.find("{%s}Equation"%(XML2HTMLRenderer.c_namespaces['sml']))
                        if equation is not None:
                            d['form']  = equation.get('Form','N/A')
                            d['model'] = equation.get('Model','N/A')
                  
                            # get coefficients
                            coefficients = equation.find("{%s}Coefficients"%(XML2HTMLRenderer.c_namespaces['sml'])).text
                            if coefficients is None:
                                d['coeffs'] = []
                            else:
                                c_list = []
                                cpt    = 0
                                for coeff in coefficients.split(' '):
                                    c_list.append({'name':'t%s'%(cpt),'val':coeff})
                                    cpt +=1
                      
                                    d['coeffs'] = c_list  
                        else:
                            d['form']  = 'N/A'
                            d['model'] = 'N/A'
                
                        calibrations.append(d)
               
                self._context['calibrations'] = calibrations  
             
             
                # add creation time
                self._context['creation_date'] = time_utils.getOracleDateFromDateTime(datetime.now())

class SPALAXXML2HTMLRenderer(object):
    """ Base Class used to transform the SPALAX XML in SAUNA """
    
    def __init__(self,TemplateDir='/home/aubert/dev/src-reps/java-balivernes/RNpicker/etc/conf/templates', TemplateName='NewSpalaxArrHtml.html'):
        
        self._env         = Environment(loader=FileSystemLoader(TemplateDir))
        
        self._template    = self._env.get_template(TemplateName)
        
        self._context     = {}
    
    def render(self,aXmlPath):
          
        self._fill_values(aXmlPath)
       
        XML2HTMLRenderer.c_log.debug("context = %s\n"%(self._context))
         
        return self._template.render(self._context)    
      
    def _fill_values(self,aXmlPath):
        
        dom_tree = etree.parse(open(aXmlPath,'r'))
       
        root = dom_tree.getroot()
       
        expr = "//*[local-name() = $name]"

        # get station code
        res = root.xpath(expr, name = "StationCode")
        if len(res) > 0:
            self._context['station_code'] = res[0].text
        else:
            self._context['station_code'] = UNDEFINED
    
        # get station location
        res = root.xpath(expr, name = "StationLocation")
        if len(res) > 0:
            self._context['station_location'] = res[0].text
        else:
            self._context['station_location'] = UNDEFINED
           
        # get station coordinates
        res = root.xpath(expr, name = "Coordinates")
        if len(res) > 0:
            dummy_str = res[0].text
            if dummy_str != None:
                (lat,lon,height) = dummy_str.split(' ')
                self._context['station_lat'] = lat
                self._context['station_lon'] = lon
                self._context['station_height'] = height
                self._context['station_gmaps']     = "http://maps.google.com/maps?q=%s,%s+(%s)&iwloc=A&hl=en&z=3"%(lat,lon,self._context['station_code'])
                self._context['station_static_gmaps'] = "http://maps.google.com/staticmap?center=%s,%s&zoom=5&size=400x400&markers=%s,%s,greens"%(lat,lon,lat,lon)
            else:
                self._context['station_lat']    = UNDEFINED
                self._context['station_lon']    = UNDEFINED
                self._context['station_height'] = UNDEFINED
                self._context['station_gmaps']  = "#"
        else:
            self._context['station_lat']    = UNDEFINED
            self._context['station_lon']    = UNDEFINED
            self._context['station_height'] = UNDEFINED
            self._context['station_gmaps']  = "#"
       
           
           
        # http://maps.google.com/maps?q=-12.4,+130.7+(This%20is%20my%20station%20here)&iwloc=A&hl=en&z=5
       
        # get Detector Code
        res = root.xpath(expr, name = "DetectorCode")
        if len(res) > 0:
            self._context['detector_code'] = res[0].text
        else:
            self._context['detector_code'] = UNDEFINED
       
        # get detector description
        res = root.xpath(expr, name = "DetectorDescription")
        if len(res) > 0:
            self._context['detector_description'] = res[0].text
        else:
            self._context['detector_description'] = UNDEFINED
           
        # get sample type
        res = root.xpath(expr, name = "SampleType")
        if len(res) > 0:
            self._context['sample_type'] = res[0].text
        else:
            self._context['sample_type']     = UNDEFINED
          
       
        res = root.xpath(expr, name = "ArrivalDate")
        if len(res) > 0:
            self._context['arrival_date'] = time_utils.getOracleDateFromISO8601(res[0].text)
        else:
            self._context['arrival_date']     = UNDEFINED
       
        self._context['collection_comments'] = UNDEFINED
       
        # for the dates, a prefix is needed
        # for the moment always take SPHD-G but it has to be configurable
        #dateExpr = "//*[local-name() = \"Spectrum\" and ends-with(@id,\"SPHD-G\")]"
        # no ends-with in xpath 1.0 use contains instead substring('','') as it is simpler
        # and it does the trick
        dateExpr             = "//*[local-name() = $name and contains(@id,$suffix)]"
        curr_spectrum_id     = None
 
        # res is Element Spectrum 
        res = root.xpath(dateExpr,suffix = 'SPHD',name   = 'SpectrumGroup')
        if len(res) > 0:
            elem = res[0]
            # get attribute id
            curr_spectrum_id = elem.get('id')
            l = curr_spectrum_id.split('-')
            self._context['sample_id'] = '%s'%(l[1])
           
            # get calibrationIDs
            self._context['calibration_ids'] = elem.get('calibrationIDs').split(' ')
           
            # get geometry
            res = elem.xpath(expr,name = "Geometry")
            if len(res) == 0:
                self._context['sample_geometry'] = UNDEFINED
            else:
                self._context['sample_geometry'] = res[0].text
           
            # get quantity
            res = elem.xpath(expr,name = "AirVolume")
            if len(res) == 0:
                self._context['sample_quantity']      = UNDEFINED
                self._context['sample_quantity_unit'] = "" 
            else:
                self._context['sample_quantity']      = utils.round_as_string(res[0].text,3)
                self._context['sample_quantity_unit'] = res[0].get('unit') 
                
             # get Xe volume
            res = elem.xpath(expr,name = "XeVolume")
            if len(res) == 0:
                self._context['xe_vol']      = UNDEFINED
                self._context['xe_vol_unit'] = "" 
            else:
                self._context['xe_vol']      = utils.round_as_string(res[0].text,3)
                self._context['xe_vol_unit'] = res[0].get('unit') 
           
            # all timing information
            c_start = time_utils.getOracleDateFromISO8601(elem.xpath(expr,name = "CollectionStart")[0].text)
            c_stop  = time_utils.getOracleDateFromISO8601(elem.xpath(expr,name = "CollectionStop")[0].text)
           
            a_start = time_utils.getOracleDateFromISO8601(elem.xpath(expr,name = "AcquisitionStart")[0].text)
            a_stop  = time_utils.getOracleDateFromISO8601(elem.xpath(expr,name = "AcquisitionStop")[0].text)
           
            a_time  = time_utils.transformISO8601PeriodInFormattedTime(elem.xpath(expr,name = "RealAcquisitionTime")[0].text)
           
            sampling_time = time_utils.transformISO8601PeriodInFormattedTime(elem.xpath(expr,name = "SamplingTime")[0].text)
            decay_time    = time_utils.transformISO8601PeriodInFormattedTime(elem.xpath(expr,name = "DecayTime")[0].text)
           
            # to be added
            flow_rate     = utils.round_as_string(elem.xpath(expr,name = "FlowRate")[0].text,3)
           
            self._context['collection_start']  = c_start
            self._context['collection_stop']   = c_stop
            self._context['acquisition_start'] = a_start
            self._context['acquisition_stop']  = a_stop
            self._context['acquisition_time']  = a_time
            self._context['sampling_time']     = sampling_time
            self._context['decay_time']        = decay_time
            self._context['avg_flow_rate']     = flow_rate      
        else:
            self._context['sample_id']         = UNDEFINED
            self._context['sample_geometry']   = UNDEFINED
           
        # add Activity Concentration for Nuclides
        #concNuclideExpr = "//*[local-name() = $name and contains(@spectrumIDs,'NOX49-239646-SPHD-G')]"
        concNuclideExpr = "//*[local-name() = $name and contains(@spectrumIDs,$spectrum_id)]"
        res = root.xpath(concNuclideExpr,name = "Analysis",spectrum_id=curr_spectrum_id )
        if len(res) > 0:
            analysis_elem = res[0]
            # get all ided nuclides
            res = analysis_elem.find("{%s}IdedNuclides"%(XML2HTMLRenderer.c_namespaces['sml']))
            q_nuclides  = []
            nq_nuclides = []
            a_nuclides  = []
            # iterate over the children of ided nuclides => the nuclides
            for nuclide in res:
              
                # check that nid_flag is 1 to go in quantified_nuclides otherwise goes into non_quantified_nuclides
                nid_flag = nuclide.find('{%s}NuclideIdentificationIndicator'%(XML2HTMLRenderer.c_namespaces['sml'])).get("numericVal")
                if nid_flag == '1':
                    d = {}
                    # get Name, 
                    d['name']      = nuclide.find('{%s}Name'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                    hl = nuclide.find('{%s}HalfLife'%(XML2HTMLRenderer.c_namespaces['sml']))
                    d['half_life'] = hl.text if hl != None else UNDEFINED
                    d['conc']      = utils.round_as_string(nuclide.find('{%s}Concentration'%(XML2HTMLRenderer.c_namespaces['sml'])).text,RDIGITS)
                    d['conc_abs_err']  = utils.round_as_string(nuclide.find('{%s}AbsoluteConcentrationError'%(XML2HTMLRenderer.c_namespaces['sml'])).text,RDIGITS)
                    d['conc_rel_err']  = utils.round_as_string(nuclide.find('{%s}RelativeConcentrationError'%(XML2HTMLRenderer.c_namespaces['sml'])).text,RDIGITS)
              
                    q_nuclides.append(d)
                else:
                    d = {}
                    # get Name, 
                    d['name']      = nuclide.find('{%s}Name'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                    mdc = nuclide.find('{%s}MDC'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                    if mdc != "N/A":
                        d['mdc']       = utils.round_as_string(mdc,RDIGITS)
                    else:
                        d['mdc']       = UNDEFINED
               
                    # get numeric val for the moment but can put some text there
                    # removed as asked by Matthias
                    #d['nid_flag']  = nuclide.find('{%s}NuclideIdentificationIndicator'%(XML2HTMLRenderer.c_namespaces['sml'])).get("numericVal")
                    nq_nuclides.append(d)
                
                # in any cases fill Activity results dict
                d = {}
                d['name']              = nuclide.find('{%s}Name'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                temp_val               = nuclide.find('{%s}Activity'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                d['activity']          = utils.round_as_string(temp_val,RDIGITS) if temp_val != UNDEFINED else UNDEFINED
                temp_val               = nuclide.find('{%s}AbsoluteActivityError'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                d['activity_abs_err']  = utils.round_as_string(temp_val,RDIGITS) if temp_val != UNDEFINED else UNDEFINED
                temp_val               = nuclide.find('{%s}RelativeActivityError'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                d['activity_rel_err']  = utils.round_as_string(temp_val,RDIGITS) if temp_val != UNDEFINED else UNDEFINED
                d['lc']                = utils.round_as_string(nuclide.find('{%s}LCActivity'%(XML2HTMLRenderer.c_namespaces['sml'])).text,RDIGITS)
                d['ld']                = utils.round_as_string(nuclide.find('{%s}LDActivity'%(XML2HTMLRenderer.c_namespaces['sml'])).text,RDIGITS)
                a_nuclides.append(d)
           
            self._context['non_quantified_nuclides'] = nq_nuclides
            self._context['quantified_nuclides']     = q_nuclides 
            self._context['activities_nuclides']     = a_nuclides 
        
            # Add Cov matrixes here
            # used to respect order of the columns
            self._context['matrix_row_order'] = ['XE-131M','XE-133M','XE-133','XE-135']
            
            #first peak fit method
            covMatrix = "//*[local-name() = 'XeCovarianceMatrixes']/*[local-name() = 'XeCovarianceMatrix' and contains(@method,$method)]"
            res = root.xpath(covMatrix,method = "Peak Fit Method")
            matrix_result = {}
            matrix_col = {'XE_131M':0,'XE_133M':1,'XE_133':2,'XE_135':3}
            if len(res) > 0:
                matrix_elem = res[0]
                for cell in matrix_elem:
                    key = cell.get('row')
                    if matrix_result.has_key(key):
                        d = matrix_result[key]
                    else:
                        d = {}
                        matrix_result[key] = d
                    
                    col = cell.get('col').upper()
                    #get position 
                    d[matrix_col[col]] = cell.text
                    
            self._context['peak_fit_matrix'] = matrix_result 
   
            #second Decay Analysis Method
            covMatrix = "//*[local-name() = 'XeCovarianceMatrixes']/*[local-name() = 'XeCovarianceMatrix' and contains(@method,$method)]"
            res = root.xpath(covMatrix,method = "Decay Analysis Method")
            matrix_result = {}
            matrix_col = {'XE_131M':0,'XE_133M':1,'XE_133':2,'XE_135':3}
            if len(res) > 0:
                matrix_elem = res[0]
                for cell in matrix_elem:
                    key = cell.get('row')
                    if matrix_result.has_key(key):
                        d = matrix_result[key]
                    else:
                        d = {}
                        matrix_result[key] = d
                    
                    col = cell.get('col').upper()
                    #get position 
                    d[matrix_col[col]] = utils.round_as_string(cell.text,RDIGITS)
                    
            self._context['decay_analysis_matrix'] = matrix_result         
                    
                        
            # Add Flags
           
            # timeliness flags
            res = analysis_elem.find("{%s}Flags/{%s}TimelinessAndAvailabilityFlags"%(XML2HTMLRenderer.c_namespaces['sml'],XML2HTMLRenderer.c_namespaces['sml']))  
            if res == None:
                res = []
            
            flags = []
           
            for timeflag in res:
                d = {}
               
                if timeflag.tag.find('CollectionTime') != -1:
                   
                    d['name']  = 'Sampling Time'
                   
                elif timeflag.tag.find('AcquisitionTime') != -1:
                  
                    d['name']  = 'AcquisitionTime'
                   
                elif timeflag.tag.find('DecayTime') != -1:
               
                    d['name']  = 'Decay Time'
               
                elif timeflag.tag.find('ResponseTime') != -1:
               
                    d['name']  = 'Response Time'
                else:
                    XML2HTMLRenderer.c_log.error("Unknown Timeliness Flag: %s"%(timeflag.tag))   
                    d['name']  = timeflag.tag
               
                d['result'] = timeflag.find('{%s}Pass'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                try:
                    d['value']  = utils.round_as_string(timeflag.find('{%s}Value'%(XML2HTMLRenderer.c_namespaces['sml'])).text,HDIGITS)
                except Exception, e:
                    #cannot convert this number value so put the string as it is
                    d['value']  = timeflag.find('{%s}Value'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                    
                d['test']   = timeflag.find('{%s}Test'%(XML2HTMLRenderer.c_namespaces['sml'])).text
            
                flags.append(d)
            
            # data quality flags
            res = analysis_elem.find("{%s}Flags/{%s}DataQualityFlags"%(XML2HTMLRenderer.c_namespaces['sml'],XML2HTMLRenderer.c_namespaces['sml']))  
            if res == None:
                res = []
                
            for dqflag in res:
                d = {}
               
                if dqflag.tag.find('XeVolume') != -1:
                    d['name']  = 'Stable Xenon Volume'
                else:
                    XML2HTMLRenderer.c_log.error("Unknown DataQuality Flag: %s"%(dqflag.tag))   
                    d['name']  = dqflag.tag
               
                d['result'] = dqflag.find('{%s}Pass'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                d['value']  = utils.round_as_string(dqflag.find('{%s}Value'%(XML2HTMLRenderer.c_namespaces['sml'])).text,3)
                d['test']   = dqflag.find('{%s}Test'%(XML2HTMLRenderer.c_namespaces['sml'])).text
            
                flags.append(d)
            
            self._context['flags'] = flags
           
            res = root.xpath("//*[local-name() = $name]",name = "CalibrationInformation")
            if len(res) > 0:
             
                # add calibration 
                res = res[0]
             
                calibrations    = []
                eff_equations = []
           
                for calibration in res:
               
                    # if calibration is related to the displayed spectrum
                    cid = calibration.get('ID')
                    if cid in self._context['calibration_ids']:
                        d   = {}
                        
                        d['desc']  = calibration.get('Type','N/A')
                        d['model'] = calibration.get('Model','N/A')
                        
                        if d['desc'].lower() != 'efficiency':
                            
                            equation  = calibration.find("{%s}Equation"%(XML2HTMLRenderer.c_namespaces['sml']))
                            if equation is not None:
                                d['form']  = equation.get('Form','N/A')
                      
                                # get coefficients
                                coefficients = equation.find("{%s}Coefficients"%(XML2HTMLRenderer.c_namespaces['sml'])).text
                                if coefficients is None:
                                    d['coeffs'] = []
                                else:
                                    c_list = []
                                    cpt    = 0
                                    for coeff in coefficients.split(' '):
                                        c_list.append({'name':'t%s'%(cpt),'val':coeff})
                                        cpt +=1
                          
                                        d['coeffs'] = c_list  
                            else:
                                d['form']  = 'N/A'
                    
                            calibrations.append(d)
                        #Efficiency case
                        else:
                            equations  = calibration.findall("{%s}Equation"%(XML2HTMLRenderer.c_namespaces['sml']))
                            
                            for eq in equations:
                                d = {}
                                d['form']  = eq.get('Form','N/A')
                                d['model'] = eq.get('Model','N/A')
                                
                                # get coefficients
                                coefficients = eq.find("{%s}Coefficients"%(XML2HTMLRenderer.c_namespaces['sml'])).text
                                if coefficients is None:
                                    d['coeffs'] = []
                                else:
                                    c_list = []
                                    cpt    = 0
                                    for coeff in coefficients.split(' '):
                                        c_list.append({'name':'t%s'%(cpt),'val':coeff})
                                        cpt +=1
                          
                                        d['coeffs'] = c_list  
                                
                                eff_equations.append(d)
                              
               
                self._context['calibrations']     = calibrations 
                self._context['eff_calibration']  = eff_equations
             
                # add creation time
                self._context['creation_date'] = time_utils.getOracleDateFromDateTime(datetime.now())

                  
              
               
                  