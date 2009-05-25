
import os
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
    
class XSDValidationError(Exception):
    """XSDValidationError"""

    def __init__(self,a_message):
        
        super(XSDValidationError,self).__init__(a_message)

class XSDValidator(object):
    
    
    def __init__(self,a_xsd_path = None):
        
        super(XSDValidator,self).__init__()
        
        self._xsd_path   = a_xsd_path
        
        self._xml_schema = None
        
        if self._xsd_path != None:
            self._read_xsd()
    
    def _read_xsd(self):
        
        # asserting input parameters
        if self._xsd_path == None:
           raise Exception("self._xsd_path is None")
        else:
            # check if file exits
            if not os.path.exists(self._xsd_path):
                raise Exception("the file %s does not exits"%(self._xsd_path))
        
        f = open(self._xsd_path,"r")
        
        # open xsd file
        xml_schema_doc = etree.parse(f)
        
        # validate as an xsd compliant file
        self._xml_schema = etree.XMLSchema(xml_schema_doc)
    
    
    def validate_xml(self,a_path):
        
        valid = open(a_path,"r")
    
        data_xml = etree.parse(valid)
    
    
        try:
            self._xml_schema.assertValid(data_xml)
        except Exception, _:
            
            log = self._xml_schema.error_log
        
            if len(log) > 0:
                # get iterator to get the first error in file
                iter    = log.__iter__()
                err     = iter.next()
                error   = "line %d, error %s"%(err.line,err.message)
            else:
                error   = e.message
                    
            raise XSDValidationError(error)
        
def main():
     
    try:
        schema_file = "SAMPML.xsd"
     
        validator = XSDValidator("/home/aubert/dev/src-reps/java-balivernes/RNpicker/etc/ext/xsd/%s"%(schema_file))
        
        dir = "/tmp/TestNewFormat/samples"
        dirList=os.listdir(dir)
        
        for path in dirList:
            _, extension = path.split('.')
            if extension != None and extension == 'xml':
                print "validate %s/%s"%(dir,path)
                validator.validate_xml("%s/%s"%(dir,path))
        #validator.validate_xml("/tmp/15Jan_NobleGas/samples/sampml-full-253305.xml")
        
        #validator.validate_xml("/tmp/15Jan_NobleGas/samples/sampml-full-254121.xml")
    except Exception,e:
        print("Exception %s message = [%s]"%(type(e),e))


if __name__ == "__main__":
    main()   
    