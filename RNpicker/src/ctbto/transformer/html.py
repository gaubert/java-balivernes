from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
from lxml import etree
import logging
import ctbto.common.utils
from ctbto.common import CTBTOError
from ctbto.common import Conf

UNDEFINED="undefined"

class XML2HTMLRenderer(object):
    """ Base Class used to transform the fetcher content into XML """
    
    # Class members
    c_log = logging.getLogger("html.XML2HTMLRenderer")
    c_log.setLevel(logging.DEBUG)
    
    
    
    def __init__(self,TemplateDir='/home/aubert/dev/src-reps/java-balivernes/RNpicker/etc/conf/templates',TemplateName='ArrHtml.html'):
        
        self._env      = Environment(loader=FileSystemLoader(TemplateDir))
        
        self._template = self._env.get_template(TemplateName)
        
        self._context  = {}
    
    def render(self,aXmlPath):
        
       self._fill_values(aXmlPath)
         
       print self._template.render(self._context)
       
       
      
    
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
       
       # get detector description
       res = root.xpath(expr, name = "DetectorDescription")
       if len(res) > 0:
           self._context['detector_description'] = res[0].text
       else:
           self._context['detector_description'] = UNDEFINED
       
       
       self._context['arrival_date'] = 1
       
       self._context['creation_date'] = 'now'