from lxml import etree
from StringIO import StringIO


def valid_schema():
    
    print " Start Tests \n"
    
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


def read_sampml_file():
    
    schema_file = "SAMPML.xsd"
    
    #schema_file = "test.xsd"
    f = open("/home/aubert/ecmwf/workspace/RNpicker/etc/ext/%s"%(schema_file),"r")
    
    print "1:read XML Schema file\n"
    
    xmlschema_doc = etree.parse(f)
    
    print "1:done"
    
    xmlschema = etree.XMLSchema(xmlschema_doc)
    
    print "2:schematize XML schema file Done"
    
    valid = open("/home/aubert/ecmwf/workspace/RNpicker/etc/ext/GeneratedRNParticulateSample.xml","r")
    
    data_xml = etree.parse(valid)
    
    print "3:done read data file \n"
    
    try:
        xmlschema.assertValid(data_xml)
    except:
        log = xmlschema.error_log
        
        #print "dir(log)=%s"%(dir(log))
        error = log.last_error
        print "line %d, error %s"%(error.line,error.message)

    
    #for line in f:
    #    print "%s"%(line)
   # print "Start parsing SAMPML.xsd\n"
   # xmlschema_doc = etree.parse(f)
   # print "parsing of SAMPML.xsd finished"

   # valid = open("/home/aubert/ecmwf/workspace/RNpicker/etc/ext/TestGeneratedRNParticulateSample.xml","r")
    
   # doc = etree.parse(valid)
    
   # print "Data XML file parsed. Validate file \n"
    
   # xmlschema.assertValid(doc)
    


def main():
    read_sampml_file()
    


if __name__ == "__main__":
    main()