from lxml import etree

import ctbto.common.utils
from ctbto.common import Conf

def pretty_print_xml(aFDescriptor,aOutput):
   """ xml pretty printing from a stream. Take a file descriptor (fd or StringIO for example """
   
   #str = aFDescriptor.read()
   
   #print " Result = %s\n"%(str)
   
   tree = etree.parse(aFDescriptor)
   
   # get xslt stylesheet doing the transformation
   xsltPath = Conf.get_instance().get("Transformer","xsltPrettyPrinter")
   
   transform = etree.XSLT(etree.parse(open(xsltPath)))
   
   result = transform(tree)
   
   ctbto.common.utils.printInFile(str(result),aOutput)