from lxml import etree

import ctbto.common.utils
from org.ctbto.conf import Conf

def pretty_print_xml(aFDescriptor,aOutput):
    """ xml pretty printing from a stream. Take a file descriptor (fd or StringIO for example """
   
    #str = aFDescriptor.read()
   
    #print " Result = %s\n"%(str)
    #f = open("/tmp/res.xml","w")
    #f.write(str)
    #f.flush()
    #f.close()
    
    offset  = 0
    is_xml  = False
    
    while not is_xml:
        c = aFDescriptor.read(1)
        if c == '<':
            is_xml = True
        else:
            offset +=1
    
    if is_xml == True:
        aFDescriptor.seek(offset)
        tree = etree.parse(aFDescriptor)
   
        # get xslt stylesheet doing the transformation
        xsltPath = Conf.get_instance().get("Transformer","xsltPrettyPrinter")
   
        transform = etree.XSLT(etree.parse(open(xsltPath)))
   
        result = transform(tree)
   
        ctbto.common.utils.printInFile(str(result),aOutput)
    else:
        raise Exception("Error. The file %s doesn't seems to be an XML file. Check its content")