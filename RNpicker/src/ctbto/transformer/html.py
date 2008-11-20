from jinja2   import Template
from jinja2   import Environment
from jinja2   import FileSystemLoader
from lxml     import etree
from datetime import datetime

import logging

import ctbto.common.utils as utils
import ctbto.common.time_utils as time_utils
from ctbto.common import CTBTOError
from ctbto.common import Conf

UNDEFINED="N/A"
RDIGITS   = 5 
BGDIGITS  = 2
HDIGITS   = 2

class XML2HTMLRenderer(object):
    """ Base Class used to transform the fetcher content into XML """
    
    # Class members
    c_log = logging.getLogger("html.XML2HTMLRenderer")
    c_log.setLevel(logging.DEBUG)
    
    c_namespaces = {'sml':'http://www.ctbto.org/SAMPML/0.5'}
    
    def __init__(self,TemplateDir='/home/aubert/dev/src-reps/java-balivernes/RNpicker/etc/conf/templates',TemplateName='ArrHtml.html'):
        
        self._env      = Environment(loader=FileSystemLoader(TemplateDir))
        
        self._template = self._env.get_template(TemplateName)
        
        self._context  = {}
    
    def render(self,aXmlPath):
        
       self._fill_values(aXmlPath)
       
       print "context = %s\n"%(self._context)
         
       #print self._template.render(self._context)
       str = self._template.render(self._context)
       utils.printInFile(str,"/tmp/Transformed.html")
       
      
    
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
       dateExpr         = "//*[local-name() = $name and contains(@id,$suffix)]"
       curr_spectrum_id = None
       
       # res is Element Spectrum 
       res = root.xpath(dateExpr,suffix = 'SPHD-G',name   = 'Spectrum')
       if len(res) > 0:
           elem = res[0]
           # get attribute id
           curr_spectrum_id = elem.get('id')
           l = curr_spectrum_id.split('-')
           self._context['sample_id'] = '%s-%s'%(l[0],l[1])
           
           # get geometry
           res = elem.xpath(expr,name = "Geometry")
           if len(res) == 0:
               self._context['sample_geometry'] = UNDEFINED
           else:
               self._context['sample_geometry'] = res[0].text
           
           # get quantity
           res = elem.xpath(expr,name = "Quantity")
           if len(res) == 0:
               self._context['sample_quantity']      = UNDEFINED
               self._context['sample_quantity_unit'] = UNDEFINED 
           else:
               self._context['sample_quantity']      = res[0].text
               self._context['sample_quantity_unit'] = res[0].get('unit') 
           
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
                d['conc_err']  = utils.round_as_string(nuclide.find('{%s}AbsoluteConcentrationError'%(XML2HTMLRenderer.c_namespaces['sml'])).text,RDIGITS)
              
                q_nuclides.append(d)
              else:
                d = {}
                # get Name, 
                d['name']      = nuclide.find('{%s}Name'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                d['mdc']       = utils.round_as_string(nuclide.find('{%s}MDC'%(XML2HTMLRenderer.c_namespaces['sml'])).text,RDIGITS)
                # get numeric val for the moment but can put some text there
                d['nid_flag']  = nuclide.find('{%s}NuclideIdentificationIndicator'%(XML2HTMLRenderer.c_namespaces['sml'])).get("numericVal")
                nq_nuclides.append(d)
                
              # in any cases fill Activity results dict
              d = {}
              d['name']          = nuclide.find('{%s}Name'%(XML2HTMLRenderer.c_namespaces['sml'])).text
              d['activity']      = utils.round_as_string(nuclide.find('{%s}Activity'%(XML2HTMLRenderer.c_namespaces['sml'])).text,RDIGITS)
              d['activity_err']  = utils.round_as_string(nuclide.find('{%s}ActivityError'%(XML2HTMLRenderer.c_namespaces['sml'])).text,RDIGITS)
              d['lc']            = utils.round_as_string(nuclide.find('{%s}LCActivity'%(XML2HTMLRenderer.c_namespaces['sml'])).text,RDIGITS)
              d['ld']            = utils.round_as_string(nuclide.find('{%s}LDActivity'%(XML2HTMLRenderer.c_namespaces['sml'])).text,RDIGITS)
              a_nuclides.append(d)
           
           self._context['non_quantified_nuclides'] = nq_nuclides
           self._context['quantified_nuclides']     = q_nuclides 
           self._context['activities_nuclides']     = a_nuclides 
        
           # Add ROI results
           # get ROIInfo
           res = analysis_elem.find("{%s}ROIInfo"%(XML2HTMLRenderer.c_namespaces['sml']))    
           
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
                 
                 val = roi.find('{%s}EfficiencyError'%(XML2HTMLRenderer.c_namespaces['sml'])).text
                 if val != UNDEFINED:
                    val = utils.round_as_string(val,RDIGITS)
                    
                 d['efficiency_error'] =  val
           
                 roi_results.append(d)
                 
               elif roi.tag.find('RoiBoundaries') != -1:
                   # Boundaries
                   d = {}
                   d['roi_number']       =  utils.round_as_string(roi.find('{%s}RoiNumber'%(XML2HTMLRenderer.c_namespaces['sml'])).text,BGDIGITS)
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
           flags = []
           
           for timeflag in res:
               d = {}
               
               if timeflag.tag.find('CollectionTime') != -1:
                   
                  d['name']  = 'Sampling Time'
                   
               elif timeflag.tag.find('AcquisitionTime') != -1:
                  
                  d['name']  = 'AcquisitionTime'
                   
               elif timeflag.tag.find('DecayTime') != -1:
               
                  d['name']  = 'Processing Time'
               else:
                  XML2HTMLRenderer.c_log.error("Unknown Timeliness Flag: %s"%(timeflag.tag))   
                  d['name']  = timeflag.tag
               
               d['result'] = timeflag.find('{%s}Flag'%(XML2HTMLRenderer.c_namespaces['sml'])).text
               d['value']  = utils.round_as_string(timeflag.find('{%s}Value'%(XML2HTMLRenderer.c_namespaces['sml'])).text,HDIGITS)
               d['test']   = timeflag.find('{%s}Test'%(XML2HTMLRenderer.c_namespaces['sml'])).text
            
               flags.append(d)
            
           # data quality flags
           res = analysis_elem.find("{%s}Flags/{%s}DataQualityFlags"%(XML2HTMLRenderer.c_namespaces['sml'],XML2HTMLRenderer.c_namespaces['sml']))  
           
           for dqflag in res:
               d = {}
               
               if dqflag.tag.find('XeVolume') != -1:
                   
                  d['name']  = 'Stable Xenon Volume'
               else:
                  XML2HTMLRenderer.c_log.error("Unknown Timeliness Flag: %s"%(timeflag.tag))   
                  d['name']  = dqflag.tag
               
               d['result'] = dqflag.find('{%s}Flag'%(XML2HTMLRenderer.c_namespaces['sml'])).text
               d['value']  = utils.round_as_string(dqflag.find('{%s}Value'%(XML2HTMLRenderer.c_namespaces['sml'])).text,3)
               d['test']   = dqflag.find('{%s}Test'%(XML2HTMLRenderer.c_namespaces['sml'])).text
            
               flags.append(d)
            
           self._context['flags'] = flags
           
           res = root.xpath("//*[local-name() = $name]",name = "CalibrationInformation")
           if len(res) > 0:
             
             # add calibration 
             res = res[0]
             
             #res = analysis_elem.find("{%s}CalibrationInformation"%(XML2HTMLRenderer.c_namespaces['sml']))  
             calibrations = []
           
             for calibration in res:
               
                 d   = {}
                 d['type'] = calibration.get('Type','N/A')
               
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
                        c_list.append({'name':'Term%s'%(cpt),'val':coeff})
                        cpt +=1
                      
                      d['coeffs'] = c_list  
                 else:
                    d['form']  = 'N/A'
                
                 calibrations.append(d)
               
             self._context['calibrations'] = calibrations  
             
             
             # add creation time
             self._context['creation_date'] = time_utils.getOracleDateFromDateTime(datetime.now())

                  
              
               
                  