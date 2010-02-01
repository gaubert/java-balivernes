""" html transformation module """
from jinja2   import Environment
from jinja2   import FileSystemLoader
from lxml     import etree
from datetime import datetime
import cStringIO

import ctbto.common.utils as utils
import ctbto.common.time_utils as time_utils
from ctbto.common.logging_utils import LoggerFactory

UNDEFINED = "N/A"
RDIGITS   = 5 
BGDIGITS  = 2
HDIGITS   = 2

class XML2HTMLRenderer(object):
    """ Base Class used to transform XML in HTML """
    
    c_namespaces = {'sml':'http://www.ctbto.org/SAMPML/0.7'}

class SAUNAXML2HTMLRenderer(object):
    """ Base Class used to transform SAUNA XML in HTML """
    
    def __init__(self, a_template_dir='/home/aubert/dev/src-reps/java-balivernes/RNpicker/etc/conf/templates', \
                       a_template_name='SaunaArrHtml-v1.0.html'):
        
        self._env         = Environment(loader=FileSystemLoader(a_template_dir))
        
        self._template    = self._env.get_template(a_template_name)
        
        self._context     = {}
        
        self._log         = LoggerFactory.get_logger(self)
        
    def render(self, a_xml_path):
        """ render the file using a template engine """  
        
        self._log.info( "Create html ARR from %s" % (a_xml_path) )
        
        self._fill_values(a_xml_path)
                
        return self._template.render(self._context)    
      
    def _fill_values(self, a_xml_path):
        """ fill the values """
        dom_tree = etree.parse(open(a_xml_path,'r'))
       
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
                (lat, lon, height) = dummy_str.split(' ')
                self._context['station_lat'] = lat
                self._context['station_lon'] = lon
                self._context['station_height'] = height
                self._context['station_gmaps']     = "http://maps.google.com/maps?q=%s,%s+(%s)&iwloc=A&hl=en&z=3" \
                                                      % (lat, lon, self._context['station_code'])
                self._context['station_static_gmaps'] = \
                "http://maps.google.com/staticmap?center=%s,%s&zoom=5&size=400x400&markers=%s,%s,greens" \
                % (lat,lon,lat,lon)
       
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
            self._context['arrival_date']    = UNDEFINED
       
        # for the dates, a prefix is needed
        # for the moment always take SPHD-G but it has to be configurable
        #dateExpr = "//*[local-name() = \"Spectrum\" and ends-with(@id,\"SPHD-G\")]"
        # no ends-with in xpath 1.0 use contains instead substring('','') as it is simpler
        # and it does the trick
        date_expr            = "//*[local-name() = $name and contains(@id,$suffix)]"
        curr_spectrum_id     = None
 
        # res is Element Spectrum 
        res = root.xpath(date_expr, suffix = 'SPHD', name   = 'SpectrumGroup')
        if len(res) > 0:
            elem = res[0]
            # get attribute id
            curr_spectrum_id = elem.get('id')
            self._context['sample_id'] = '%s' % (curr_spectrum_id.split('-')[1])
           
            # get calibrationIDs
            self._context['calibration_ids'] = elem.get('calibrationIDs').split(' ')
           
            # get geometry
            res = elem.xpath(expr, name = "Geometry")
            if len(res) == 0:
                self._context['sample_geometry'] = UNDEFINED
            else:
                self._context['sample_geometry'] = res[0].text
           
            # get quantity
            res = elem.xpath(expr, name = "ProcessedAirVolume")
            if len(res) == 0 or res[0].text == UNDEFINED:
                self._context['processed_air_volume']      = UNDEFINED
                self._context['processed_air_volume_unit'] = "" 
            else:
                self._context['processed_air_volume']      = utils.round_as_string(res[0].text, 3)
                self._context['processed_air_volume_unit'] = res[0].get('unit') 
            
            # get sample quantity
            res = elem.xpath(expr, name = "SampleQuantity")
            if len(res) == 0 or res[0].text == UNDEFINED:
                self._context['sample_quantity']      = UNDEFINED
                self._context['sample_quantity_unit'] = "" 
            else:
                self._context['sample_quantity']      = utils.round_as_string(res[0].text, 3)
                self._context['sample_quantity_unit'] = res[0].get('unit') 
                
            # get Xe volume
            res = elem.xpath(expr, name = "XeVolume")
            if len(res) == 0 or res[0].text == UNDEFINED:
                self._context['xe_vol']      = UNDEFINED
                self._context['xe_vol_unit'] = "" 
            else:
                self._context['xe_vol']      = utils.round_as_string(res[0].text, 3)
                self._context['xe_vol_unit'] = res[0].get('unit') 
            
            # get collection comments
            res = elem.xpath(expr, name = "Comments")
            if len(res) == 0 or res[0].text == UNDEFINED: 
                self._context['collection_comments'] = UNDEFINED
            else:
                comments = []
                ios = cStringIO.StringIO(res[0].text.strip()) 
                for line in ios:
                    comments.append(line.strip())
                self._context['collection_comments'] = comments
           
            # all timing information
            c_start = time_utils.getOracleDateFromISO8601(elem.xpath(expr, name = "CollectionStart")[0].text)
            c_stop  = time_utils.getOracleDateFromISO8601(elem.xpath(expr, name = "CollectionStop")[0].text)
           
            a_start = time_utils.getOracleDateFromISO8601(elem.xpath(expr, name = "AcquisitionStart")[0].text)
            a_stop  = time_utils.getOracleDateFromISO8601(elem.xpath(expr, name = "AcquisitionStop")[0].text)
           
            a_time  = time_utils.transformISO8601PeriodInFormattedTime(elem.xpath(expr, name = "RealAcquisitionTime")[0].text)
           
            sampling_time = time_utils.transformISO8601PeriodInFormattedTime(elem.xpath(expr, name = "SamplingTime")[0].text)
            decay_time    = time_utils.transformISO8601PeriodInFormattedTime(elem.xpath(expr, name = "DecayTime")[0].text)
           
            # to be added
            flow_rate     = utils.round_as_string(elem.xpath(expr, name = "FlowRate")[0].text, 3)
           
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
        conc_nuclide_expr = "//*[local-name() = $name and contains(@spectrumIDs,$spectrum_id)]"
        res = root.xpath(conc_nuclide_expr, name = "Analysis", spectrum_id = curr_spectrum_id )
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
                    one_dict = {}
                    # get Name, 
                    one_dict['name']      = nuclide.find('{%s}Name'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                    one_dict['half_life'] = nuclide.find('{%s}HalfLife'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                    one_dict['conc']      = utils.round_as_string(nuclide.find('{%s}Concentration' \
                                     % (XML2HTMLRenderer.c_namespaces['sml'])).text, RDIGITS)
                    one_dict['conc_abs_err']  = utils.round_as_string(nuclide.find('{%s}AbsoluteConcentrationError' \
                                         % (XML2HTMLRenderer.c_namespaces['sml'])).text, RDIGITS)
                    one_dict['conc_rel_err']  = utils.round_as_string(nuclide.find('{%s}RelativeConcentrationError' \
                                         % (XML2HTMLRenderer.c_namespaces['sml'])).text, RDIGITS)
              
                    q_nuclides.append(one_dict)
                else:
                    one_dict = {}
                    # get Name, 
                    one_dict['name']      = nuclide.find('{%s}Name'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                    mdc = nuclide.find('{%s}MDC' % (XML2HTMLRenderer.c_namespaces['sml'])).text
                    if mdc != "N/A":
                        one_dict['mdc']       = utils.round_as_string(mdc, RDIGITS)
                    else:
                        one_dict['mdc']       = "N/A"
               
                    nq_nuclides.append(one_dict)
                
                # in any cases fill Activity results dict
                dummy = {}
                
                dummy['name']              = nuclide.find('{%s}Name'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                
                dummy['activity']          = utils.round_as_string(nuclide.find('{%s}Activity' \
                                             % (XML2HTMLRenderer.c_namespaces['sml'])).text, RDIGITS)
                dummy['activity']          = utils.round_as_string(nuclide.find('{%s}Activity'\
                                             % (XML2HTMLRenderer.c_namespaces['sml'])).text, RDIGITS)
                
                dummy['undecay_corr_activity']          = utils.round_as_string(nuclide.find('{%s}UndecayCorrectedActivity'\
                                             % (XML2HTMLRenderer.c_namespaces['sml'])).text, RDIGITS)
                
                dummy['activity_abs_err']  = utils.round_as_string(nuclide.find('{%s}AbsoluteActivityError'\
                                             % (XML2HTMLRenderer.c_namespaces['sml'])).text, RDIGITS)
                dummy['activity_rel_err']  = utils.round_as_string(nuclide.find('{%s}RelativeActivityError'\
                                             % (XML2HTMLRenderer.c_namespaces['sml'])).text, RDIGITS)
                dummy['lc']                = utils.round_as_string(nuclide.find('{%s}LCActivity'\
                                             % (XML2HTMLRenderer.c_namespaces['sml'])).text, RDIGITS)
                dummy['ld']                = utils.round_as_string(nuclide.find('{%s}LDActivity'\
                                             % (XML2HTMLRenderer.c_namespaces['sml'])).text, RDIGITS)
                a_nuclides.append(dummy)
                
                
                
           
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
                    one_dict = {}
                    one_dict['roi_number']       =  roi.find('{%s}RoiNumber'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                    one_dict['name']             =  roi.find('{%s}Name'%(XML2HTMLRenderer.c_namespaces['sml'])).text
               
                    n_counts              =  roi.find('{%s}NetCounts'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                    if n_counts is not None:
                        (n_c, n_c_err) = n_counts.split(' ')
                        one_dict['net_counts']     = utils.round_as_string(n_c, RDIGITS)
                        one_dict['net_counts_err'] = utils.round_as_string(n_c_err, RDIGITS)
                    else:
                        one_dict['net_counts']     = "N/A"
                        one_dict['net_counts_err'] = "N/A"
                      
                    one_dict['lc']               =  utils.round_as_string(roi.find('{%s}LC' \
                                             %(XML2HTMLRenderer.c_namespaces['sml'])).text, RDIGITS)
                 
                    val = roi.find('{%s}Efficiency' % (XML2HTMLRenderer.c_namespaces['sml'])).text
                    if val != UNDEFINED:
                        val = utils.round_as_string(val, RDIGITS)
                    
                    one_dict['efficiency']       =  val
                 
                    val = roi.find('{%s}AbsoluteEfficiencyError' % (XML2HTMLRenderer.c_namespaces['sml'])).text
                    if val != UNDEFINED:
                        val = utils.round_as_string(val, RDIGITS)
                    
                    one_dict['efficiency_abs_error'] =  val
                 
                    val = roi.find('{%s}RelativeEfficiencyError' % (XML2HTMLRenderer.c_namespaces['sml'])).text
                    if val != UNDEFINED:
                        val = utils.round_as_string(val, RDIGITS)
           
                    one_dict['efficiency_rel_error'] =  val
                 
                    roi_results.append(one_dict)
                 
                elif roi.tag.find('RoiBoundaries') != -1:
                    # Boundaries
                    one_dict = {}
                    one_dict['roi_number']       =  roi.find('{%s}RoiNumber'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                    one_dict['gammalow']         =  utils.round_as_string(roi.find('{%s}GammaLow'\
                                             %(XML2HTMLRenderer.c_namespaces['sml'])).text, BGDIGITS)
                    one_dict['gammahigh']        =  utils.round_as_string(roi.find('{%s}GammaHigh'\
                                             %(XML2HTMLRenderer.c_namespaces['sml'])).text, BGDIGITS)
                    one_dict['betalow']          =  utils.round_as_string(roi.find('{%s}BetaLow'\
                                             %(XML2HTMLRenderer.c_namespaces['sml'])).text, BGDIGITS)
                    one_dict['betahigh']         =  utils.round_as_string(roi.find('{%s}BetaHigh'\
                                             %(XML2HTMLRenderer.c_namespaces['sml'])).text, BGDIGITS)
                   
                    roi_boundaries.append(one_dict)
                else:
                    self._log.error("No ROI info for %s" % (self._context['sample_id'])) 
                  
            self._context['roi_results']    = roi_results
            self._context['roi_boundaries'] = roi_boundaries
           
            # Add Flags
           
            # timeliness flags
            res = analysis_elem.find("{%s}Flags/{%s}TimelinessAndAvailabilityFlags" \
                                     % (XML2HTMLRenderer.c_namespaces['sml'], XML2HTMLRenderer.c_namespaces['sml']))  
            if res == None:
                res = []
            
            flags = []
           
            for timeflag in res:
                one_dict = {}
               
                if timeflag.tag.find('CollectionTime') != -1:
                   
                    one_dict['name']  = 'Sampling Time'
                   
                elif timeflag.tag.find('AcquisitionTime') != -1:
                  
                    one_dict['name']  = 'AcquisitionTime'
                   
                elif timeflag.tag.find('DecayTime') != -1:
               
                    one_dict['name']  = 'Decay Time'
               
                elif timeflag.tag.find('ResponseTime') != -1:
               
                    one_dict['name']  = 'Response Time'
                else:
                    self._log.error("Unknown Timeliness Flag: %s"%(timeflag.tag))   
                    one_dict['name']  = timeflag.tag
               
                one_dict['result'] = timeflag.find('{%s}Pass'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                try:
                    one_dict['value']  = utils.round_as_string(timeflag.find('{%s}Value' \
                                         % (XML2HTMLRenderer.c_namespaces['sml'])).text, HDIGITS)
                except Exception, _: #pylint: disable-msg= W0703
                    #cannot convert this number value so put the string as it is
                    one_dict['value']  = timeflag.find('{%s}Value'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                    
                one_dict['test']   = timeflag.find('{%s}Test'%(XML2HTMLRenderer.c_namespaces['sml'])).text
            
                flags.append(one_dict)
            
            # data quality flags
            res = analysis_elem.find("{%s}Flags/{%s}DataQualityFlags"% (XML2HTMLRenderer.c_namespaces['sml'], \
                                                                       XML2HTMLRenderer.c_namespaces['sml']))  
            if res == None:
                res = []
                
            for dqflag in res:
                one_dict = {}
               
                if dqflag.tag.find('XeVolume') != -1:
                    one_dict['name']  = 'Stable Xenon Volume'
                else:
                    self._log.error("Unknown DataQuality Flag: %s"%(dqflag.tag))   
                    one_dict['name']  = dqflag.tag
               
                one_dict['result'] = dqflag.find('{%s}Pass' % (XML2HTMLRenderer.c_namespaces['sml'])).text
                one_dict['value']  = utils.round_as_string(dqflag.find('{%s}Value' % (XML2HTMLRenderer.c_namespaces['sml'])).text, 3)
                one_dict['test']   = dqflag.find('{%s}Test'%(XML2HTMLRenderer.c_namespaces['sml'])).text
            
                flags.append(one_dict)
            
            self._context['flags'] = flags
           
            res = root.xpath("//*[local-name() = $name]", name = "CalibrationInformation")
            if len(res) > 0:
             
                # add calibration 
                res = res[0]
             
                calibrations = []
           
                for calibration in res:
               
                    # if calibration is related to the displayed spectrum
                    cid = calibration.get('ID')
                    if cid in self._context['calibration_ids']:
                        one_dict   = {}
                        one_dict['desc'] = calibration.get('Type','N/A')
               
                        equation  = calibration.find("{%s}Equation"%(XML2HTMLRenderer.c_namespaces['sml']))
                        if equation is not None:
                            one_dict['form']  = equation.get('Form','N/A')
                            one_dict['model'] = equation.get('Model','N/A')
                  
                            # get coefficients
                            coefficients = equation.find("{%s}Coefficients"%(XML2HTMLRenderer.c_namespaces['sml'])).text
                            if coefficients is None:
                                one_dict['coeffs'] = []
                            else:
                                c_list = []
                                cpt    = 0
                                for coeff in coefficients.split(' '):
                                    c_list.append({'name':'t%s' % (cpt), 'val':coeff})
                                    cpt += 1
                      
                                    one_dict['coeffs'] = c_list  
                        else:
                            one_dict['form']  = 'N/A'
                            one_dict['model'] = 'N/A'
                
                        calibrations.append(one_dict)
               
                self._context['calibrations'] = calibrations  
             
             
                # add creation time
                self._context['creation_date'] = time_utils.getOracleDateFromDateTime(datetime.now())

class SPALAXXML2HTMLRenderer(object):
    """ Base Class used to transform the SPALAX XML in SAUNA """
    
    def __init__(self, a_template_dir='/home/aubert/dev/src-reps/java-balivernes/RNpicker/etc/conf/templates', \
                       a_template_name='SpalaxArrHtml-v1.0.html'):
        
        self._env         = Environment(loader=FileSystemLoader(a_template_dir))
        
        self._template    = self._env.get_template(a_template_name)
        
        self._context     = {}
        
        self._log         = LoggerFactory.get_logger(self)
    
    def render(self, a_xml_path):
        """ render """  
        self._fill_values(a_xml_path)
       
        self._log.debug("context = %s\n"%(self._context))
         
        return self._template.render(self._context)    
      
    def _fill_values(self, a_xml_path):
        """ extract the values from the XML file """
        
        dom_tree = etree.parse(open(a_xml_path, 'r'))
       
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
                (lat, lon, height) = dummy_str.split(' ')
                self._context['station_lat'] = lat
                self._context['station_lon'] = lon
                self._context['station_height'] = height
                self._context['station_gmaps']     = "http://maps.google.com/maps?q=%s,%s+(%s)&iwloc=A&hl=en&z=3" \
                                                      % (lat, lon, self._context['station_code'])
                self._context['station_static_gmaps'] = \
                "http://maps.google.com/staticmap?center=%s,%s&zoom=5&size=400x400&markers=%s,%s,greens" \
                % (lat,lon,lat,lon)
       
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
       
        # for the dates, a prefix is needed
        # for the moment always take SPHD-G but it has to be configurable
        #dateExpr = "//*[local-name() = \"Spectrum\" and ends-with(@id,\"SPHD-G\")]"
        # no ends-with in xpath 1.0 use contains instead substring('','') as it is simpler
        # and it does the trick
        date_expr             = "//*[local-name() = $name and contains(@id,$suffix)]"
        curr_spectrum_id     = None
 
        # res is Element Spectrum 
        res = root.xpath(date_expr, suffix = 'SPHD', name   = 'SpectrumGroup')
        if len(res) > 0:
            elem = res[0]
            # get attribute id
            curr_spectrum_id = elem.get('id')
            self._context['sample_id'] = '%s' % ( curr_spectrum_id.split('-')[1])
           
            # get calibrationIDs
            self._context['calibration_ids'] = elem.get('calibrationIDs').split(' ')
           
            # get geometry
            res = elem.xpath(expr, name = "Geometry")
            if len(res) == 0:
                self._context['sample_geometry'] = UNDEFINED
            else:
                self._context['sample_geometry'] = res[0].text
           
            # get quantity
            res = elem.xpath(expr, name = "AirVolume")
            if len(res) == 0:
                self._context['processed_air_volume']      = UNDEFINED
                self._context['processed_air_volume_unit'] = "" 
            else:
                self._context['processed_air_volume']      = utils.round_as_string(res[0].text, 3)
                self._context['processed_air_volume_unit'] = res[0].get('unit') 
                
            # get Xe volume
            res = elem.xpath(expr, name = "XeVolume")
            if len(res) == 0:
                self._context['xe_vol']      = UNDEFINED
                self._context['xe_vol_unit'] = "" 
            else:
                self._context['xe_vol']      = utils.round_as_string(res[0].text, 3) if res[0].text != UNDEFINED else UNDEFINED
                if res[0].text != UNDEFINED:
                    self._context['xe_vol_unit'] = res[0].get('unit') 
            
            # get collection comments
            res = elem.xpath(expr, name = "Comments")
            if len(res) == 0 or res[0].text == UNDEFINED: 
                self._context['collection_comments'] = UNDEFINED
            else:
                comments = []
                ios = cStringIO.StringIO(res[0].text.strip()) 
                for line in ios:
                    comments.append(line.strip())
                self._context['collection_comments'] = comments
           
            # all timing information
            c_start = time_utils.getOracleDateFromISO8601(elem.xpath(expr, name = "CollectionStart")[0].text)
            c_stop  = time_utils.getOracleDateFromISO8601(elem.xpath(expr, name = "CollectionStop")[0].text)
           
            a_start = time_utils.getOracleDateFromISO8601(elem.xpath(expr, name = "AcquisitionStart")[0].text)
            a_stop  = time_utils.getOracleDateFromISO8601(elem.xpath(expr, name = "AcquisitionStop")[0].text)
           
            a_time  = time_utils.transformISO8601PeriodInFormattedTime(elem.xpath(expr, name = "RealAcquisitionTime")[0].text)
           
            sampling_time = time_utils.transformISO8601PeriodInFormattedTime(elem.xpath(expr, name = "SamplingTime")[0].text)
            decay_time    = time_utils.transformISO8601PeriodInFormattedTime(elem.xpath(expr, name = "DecayTime")[0].text)
           
            # to be added
            flow_rate     = utils.round_as_string(elem.xpath(expr, name = "FlowRate")[0].text, 3)
           
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
        conc_nuclide_expr = "//*[local-name() = $name and contains(@spectrumIDs,$spectrum_id)]"
        res = root.xpath(conc_nuclide_expr, name = "Analysis", spectrum_id = curr_spectrum_id )
        if len(res) > 0:
            analysis_elem = res[0]
            # get all ided nuclides
            res = analysis_elem.find("{%s}IdedNuclides"%(XML2HTMLRenderer.c_namespaces['sml']))
            
            #init structures
            q_nuclides  = {'peak' : {}, 'decay' : {} }
            nq_nuclides = {'peak' : {}, 'decay' : {} }
            a_nuclides  = {'peak' : {}, 'decay' : {} }
           
            # iterate over the children of ided nuclides => the nuclides
            for nuclide in res:
                
                method = nuclide.get('method')
                
                if method == 'Peak Fit Method':
                    method = 'peak'
                elif method == 'Decay Analysis Method':
                    method = 'decay'
                
                # check that nid_flag is 1 to go in quantified_nuclides otherwise goes into non_quantified_nuclides
                nid_flag = nuclide.find('{%s}NuclideIdentificationIndicator' % (XML2HTMLRenderer.c_namespaces['sml'])).get("numericVal")
                if nid_flag >= '1':
                    one_dict = {}
                    # get Name, 
                    one_dict['name']          = nuclide.find('{%s}Name' % (XML2HTMLRenderer.c_namespaces['sml'])).text
                    
                    temp_val                  = nuclide.find('{%s}Concentration' % (XML2HTMLRenderer.c_namespaces['sml'])).text
                    one_dict['conc']          = utils.round_as_string(temp_val, RDIGITS) if temp_val != UNDEFINED else UNDEFINED
                    
                    temp_val                  = nuclide.find('{%s}AbsoluteConcentrationError' % (XML2HTMLRenderer.c_namespaces['sml'])).text
                    one_dict['conc_abs_err']  = utils.round_as_string(temp_val, 3) if temp_val != UNDEFINED else UNDEFINED
                    
                    temp_val                  = nuclide.find('{%s}RelativeConcentrationError' % (XML2HTMLRenderer.c_namespaces['sml'])).text
                    one_dict['conc_rel_err']  = utils.round_as_string(temp_val, 3) if temp_val != UNDEFINED else UNDEFINED
                    
                    temp_val                  = nuclide.find('{%s}MDI' % (XML2HTMLRenderer.c_namespaces['sml'])).text
                    one_dict['mdi']           = utils.round_as_string(temp_val, RDIGITS) if temp_val != UNDEFINED else UNDEFINED
                    
                    q_nuclides[method][one_dict['name']] = one_dict
                else:
                    one_dict = {}
                    # get Name, 
                    one_dict['name']      = nuclide.find('{%s}Name' % (XML2HTMLRenderer.c_namespaces['sml'])).text
                    mdc = nuclide.find('{%s}MDC' % (XML2HTMLRenderer.c_namespaces['sml'])).text
                    if mdc != "N/A":
                        
                        one_dict['mdc']           = utils.round_as_string(mdc, RDIGITS) if mdc != UNDEFINED else UNDEFINED
                        
                    else:
                        one_dict['mdc']          = UNDEFINED
                        
                    # add concetration anyway
                    temp_val                  = nuclide.find('{%s}Concentration' % (XML2HTMLRenderer.c_namespaces['sml'])).text
                    one_dict['conc']          = utils.round_as_string(temp_val, RDIGITS) if temp_val != UNDEFINED else UNDEFINED
                    
                    temp_val                  = nuclide.find('{%s}AbsoluteConcentrationError' % (XML2HTMLRenderer.c_namespaces['sml'])).text
                    one_dict['conc_abs_err']  = utils.round_as_string(temp_val, 3) if temp_val != UNDEFINED else UNDEFINED
                    
                    temp_val                  = nuclide.find('{%s}RelativeConcentrationError' % (XML2HTMLRenderer.c_namespaces['sml'])).text
                    one_dict['conc_rel_err']  = utils.round_as_string(temp_val, 3) if temp_val != UNDEFINED else UNDEFINED
                    
                        
                    nq_nuclides[method][one_dict['name']] = one_dict
                
                # in any cases fill Activity results dict
                one_dict = {}
                
                method = nuclide.get('method')
                
                if method == 'Peak Fit Method':
                    method = 'peak'
                elif method == 'Decay Analysis Method':
                    method = 'decay'
                
                one_dict['name']              = nuclide.find('{%s}Name'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                temp_val                      = nuclide.find('{%s}Activity'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                one_dict['activity']          = utils.round_as_string(temp_val, RDIGITS) if temp_val != UNDEFINED else UNDEFINED
                
                temp_val                       = nuclide.find('{%s}UndecayCorrectedActivity' % (XML2HTMLRenderer.c_namespaces['sml'])).text
                one_dict['undecay_corr_activity'] = utils.round_as_string(temp_val, RDIGITS) if temp_val != UNDEFINED else UNDEFINED
                
                temp_val                      = nuclide.find('{%s}AbsoluteActivityError'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                one_dict['activity_abs_err']  = utils.round_as_string(temp_val, RDIGITS) if temp_val != UNDEFINED else UNDEFINED
                temp_val                      = nuclide.find('{%s}RelativeActivityError'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                one_dict['activity_rel_err']  = utils.round_as_string(temp_val, RDIGITS) if temp_val != UNDEFINED else UNDEFINED
                temp_val                      = nuclide.find('{%s}LCActivity'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                one_dict['lc']                = utils.round_as_string(temp_val, RDIGITS) if temp_val != UNDEFINED else UNDEFINED
                temp_val                      = nuclide.find('{%s}LDActivity'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                one_dict['ld']                = utils.round_as_string(temp_val, RDIGITS) if temp_val != UNDEFINED else UNDEFINED
                
                a_nuclides[method][one_dict['name']] = one_dict
           
            self._context['non_quantified_nuclides'] = nq_nuclides
            self._context['quantified_nuclides']     = q_nuclides 
            self._context['activities_nuclides']     = a_nuclides 
        
            # Add Cov matrixes here
            # used to respect order of the columns
            self._context['matrix_row_order'] = ['XE-131M', 'XE-133M', 'XE-133', 'XE-135']
            
            #first peak fit method
            cov_matrix = "//*[local-name() = 'XeCovarianceMatrixes']/*[local-name() = 'XeCovarianceMatrix' and contains(@method,$method)]"
            res = root.xpath(cov_matrix, method = "Peak Fit Method")
            
            matrix_result = {'XE-133M': {0: UNDEFINED, 1: UNDEFINED, 2: UNDEFINED, 3: UNDEFINED}, \
                             'XE-131M': {0: UNDEFINED, 1: UNDEFINED, 2: UNDEFINED, 3: UNDEFINED}, \
                             'XE-135': {0: UNDEFINED, 1: UNDEFINED, 2: UNDEFINED, 3: UNDEFINED}, \
                             'XE-133': {0: UNDEFINED, 1: UNDEFINED, 2: UNDEFINED, 3: UNDEFINED}\
                            }
            
            matrix_col = {'XE-131M':0, 'XE-133M':1, 'XE-133':2, 'XE-135':3}
            if len(res) > 0:
                matrix_elem = res[0]
                for cell in matrix_elem:
                    key = cell.get('row')
                    if matrix_result.has_key(key):
                        one_dict = matrix_result[key]
                    else:
                        one_dict = {}
                        matrix_result[key] = one_dict
                    
                    col = cell.get('col').upper()
                    #get position 
                    one_dict[matrix_col[col]] = utils.round_as_string(cell.text, RDIGITS)
                    
            self._context['peak_fit_matrix'] = matrix_result 
   
            #second Decay Analysis Method
            cov_matrix = "//*[local-name() = 'XeCovarianceMatrixes']/*[local-name() = 'XeCovarianceMatrix' and contains(@method,$method)]"
            
            res = root.xpath(cov_matrix, method = "Decay Analysis Method")
            
            matrix_col = {'XE-131M':0, 'XE-133M':1, 'XE-133':2, 'XE-135':3}
            if len(res) > 0:
                matrix_elem = res[0]
                for cell in matrix_elem:
                    key = cell.get('row')
                    if matrix_result.has_key(key):
                        one_dict = matrix_result[key]
                    else:
                        one_dict = {}
                        matrix_result[key] = one_dict
                
                    col = cell.get('col').upper()
                    #get position 
                    one_dict[matrix_col[col]] = utils.round_as_string(cell.text, RDIGITS)
            else:
                matrix_result = {}
                    
            self._context['decay_analysis_matrix'] = matrix_result         
                    
                        
            # Add Flags
           
            # timeliness flags
            res = analysis_elem.find("{%s}Flags/{%s}TimelinessAndAvailabilityFlags" \
                                     %(XML2HTMLRenderer.c_namespaces['sml'], XML2HTMLRenderer.c_namespaces['sml']))  
            if res == None:
                res = []
            
            flags = []
           
            for timeflag in res:
                one_dict = {}
               
                if timeflag.tag.find('CollectionTime') != -1:
                   
                    one_dict['name']  = 'Sampling Time'
                   
                elif timeflag.tag.find('AcquisitionTime') != -1:
                  
                    one_dict['name']  = 'AcquisitionTime'
                   
                elif timeflag.tag.find('DecayTime') != -1:
               
                    one_dict['name']  = 'Decay Time'
               
                elif timeflag.tag.find('ResponseTime') != -1:
               
                    one_dict['name']  = 'Response Time'
                else:
                    self._log.error("Unknown Timeliness Flag: %s"%(timeflag.tag))   
                    one_dict['name']  = timeflag.tag
               
                one_dict['result'] = timeflag.find('{%s}Pass'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                try:
                    one_dict['value']  = utils.round_as_string(timeflag.find('{%s}Value' \
                                         % (XML2HTMLRenderer.c_namespaces['sml'])).text, HDIGITS)
                except Exception, _: #pylint: disable-msg= W0703
                    #cannot convert this number value so put the string as it is
                    one_dict['value']  = timeflag.find('{%s}Value'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                    
                one_dict['test']   = timeflag.find('{%s}Test'%(XML2HTMLRenderer.c_namespaces['sml'])).text
            
                flags.append(one_dict)
            
            # data quality flags
            res = analysis_elem.find("{%s}Flags/{%s}DataQualityFlags" \
                                     % (XML2HTMLRenderer.c_namespaces['sml'], XML2HTMLRenderer.c_namespaces['sml']))  
            if res == None:
                res = []
                
            for dqflag in res:
                one_dict = {}
               
                if dqflag.tag.find('XeVolume') != -1:
                    one_dict['name']  = 'Stable Xenon Volume'
                else:
                    self._log.error("Unknown DataQuality Flag: %s"%(dqflag.tag))   
                    one_dict['name']  = dqflag.tag
               
                one_dict['result'] = dqflag.find('{%s}Pass' % (XML2HTMLRenderer.c_namespaces['sml'])).text
                one_dict['value']  = utils.round_as_string(dqflag.find('{%s}Value'  % (XML2HTMLRenderer.c_namespaces['sml'])).text, 3)
                one_dict['test']   = dqflag.find('{%s}Test' % (XML2HTMLRenderer.c_namespaces['sml'])).text
            
                flags.append(one_dict)
            
            self._context['flags'] = flags
           
            res = root.xpath("//*[local-name() = $name]", name = "CalibrationInformation")
            if len(res) > 0:
             
                # add calibration 
                res = res[0]
             
                calibrations    = []
                eff_equations = []
           
                for calibration in res:
               
                    # if calibration is related to the displayed spectrum
                    cid = calibration.get('ID')
                    if cid in self._context['calibration_ids']:
                        one_dict   = {}
                        
                        one_dict['desc']  = calibration.get('Type','N/A')
                        one_dict['model'] = calibration.get('Model','N/A')
                        
                        if one_dict['desc'].lower() != 'efficiency':
                            
                            equation  = calibration.find("{%s}Equation" % (XML2HTMLRenderer.c_namespaces['sml']))
                            if equation is not None:
                                one_dict['form']  = equation.get('Form','N/A')
                      
                                # get coefficients
                                coefficients = equation.find("{%s}Coefficients" % (XML2HTMLRenderer.c_namespaces['sml'])).text
                                if coefficients is None:
                                    one_dict['coeffs'] = []
                                else:
                                    c_list = []
                                    cpt    = 0
                                    for coeff in coefficients.split(' '):
                                        c_list.append({'name':'t%s' % (cpt), 'val':coeff})
                                        cpt += 1
                          
                                        one_dict['coeffs'] = c_list  
                            else:
                                one_dict['form']  = 'N/A'
                    
                            calibrations.append(one_dict)
                        #Efficiency case
                        else:
                            equations  = calibration.findall("{%s}Equation" % (XML2HTMLRenderer.c_namespaces['sml']))
                            
                            for one_eq in equations:
                                one_dict = {}
                                one_dict['form']  = one_eq.get('Form', 'N/A')
                                one_dict['model'] = one_eq.get('Model', 'N/A')
                                
                                # get coefficients
                                coefficients = one_eq.find("{%s}Coefficients"%(XML2HTMLRenderer.c_namespaces['sml'])).text
                                if coefficients is None:
                                    one_dict['coeffs'] = []
                                else:
                                    c_list = []
                                    cpt    = 0
                                    for coeff in coefficients.split(' '):
                                        c_list.append({'name':'t%s'%(cpt), 'val':coeff})
                                        cpt += 1
                          
                                        one_dict['coeffs'] = c_list  
                                
                                eff_equations.append(one_dict)
                              
               
                self._context['calibrations']     = calibrations 
                self._context['eff_calibration']  = eff_equations
             
                # add creation time
                self._context['creation_date'] = time_utils.getOracleDateFromDateTime(datetime.now())
