
import os

from lxml import etree
from StringIO import StringIO

from  ctbto.common.exceptions import CTBTOError


def valid_schema():
    
    print " Startjjj Tests \n"
    
    f = StringIO('''\
    <xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">
       <xsd:element name="a" type="AType"/>
      <xsd:complexType name="AType">
        <xsd:sequence>
           <xsd:element name="b" type="xsd:string" />
        </xsd:sequence>
      </xsd:complexType>
    </xsd:schema>
    ''')
    
    xmlschema_doc = etree.parse(f)
    
    xmlschema = etree.XMLSchema(xmlschema_doc)
    
    valid = StringIO('''<a>\
                          <b>
                            
                          </b>
                        </a>''')
    
    doc = etree.parse(valid)
    
    xmlschema.assertValid(doc)

    print "Validated \n"

    
    print " End Tests \n"


def read_sampml_file(filePath = None):
    """ validate an XML sample file against a the XSD schema file SAMPML.xsd """
    
    # asserting input parameters
    if filePath == None:
        raise CTBTOError(-1,"passed argument filePath is null")
    else:
        # check if file exits
        if not os.path.exists(filePath):
            raise CTBTOError(-1,"the file %s does not exits"%(filePath))
    
    schema_file = "SAMPML.xsd"
    
    #schema_file = "test.xsd"
    f = open("/home/aubert/dev/src-reps/java-balivernes/RNpicker/etc/ext/%s"%(schema_file),"r")
    
    print "1:read XML Schema file\n"
    
    xmlschema_doc = etree.parse(f)
    
    print "1:done"
    
    xmlschema = etree.XMLSchema(xmlschema_doc)
    
    print "2:schematize XML schema file Done"
    
    valid = open(filePath,"r")
    
    data_xml = etree.parse(valid)
    
    print "3:done read data file \n"
    
    try:
        xmlschema.assertValid(data_xml)
    except:
        log = xmlschema.error_log
        
        #print "dir(log)=%s"%(dir(log))
        
        # get iterator to get the first error in file
        iter = log.__iter__()
        error      = iter.next()
        
        print "line %d, error %s"%(error.line,error.message)


def main():
    read_sampml_file("/home/aubert/Desktop/sampml-working-with-xsd.xml")
    
    #read_sampml_file("/home/aubert/ecmwf/workspace/RNpicker/etc/ext/TestGeneratedRNParticulateSample.xml")
    


if __name__ == "__main__":
    main()