import common.utils
from lxml import etree



def pretty_print_xml(aFDescriptor,aOutput):
   """ xml pretty printing from a stream. Take a file descriptor (fd or StringIO for example """
   
   tree = etree.parse(aFDescriptor)
   
   # get xslt stylesheet doing the transformation
   xsltPath = common.utils.Conf.get_instance().get("Transformer","xsltPrettyPrinter")
   
   transform = etree.XSLT(etree.parse(open(xsltPath)))
   
   result = transform(tree)
   
   common.utils.printInFile(str(result),aOutput)