from xml.etree.ElementTree import ElementTree, Element, SubElement, dump # Python 2.5
import sys

def main():
    
    print "Hello"
    s = set()
    
    s.add("One")
    s.add("Two")
    s.add("Three")
    
    sys.exit(1)
      
    # Build tree structure
    root = Element("table")
    
    root.set("name","RMS_GARDS_IT_IS_TOO_COMPLICATED")
       
    metadata = SubElement(root,"metadata")
    
    column = SubElement(metadata,"column")
    
    col_id = Element("col_id")
    col_id.text = "1"
    
    name = Element("name")
    name.text = "SITE_DET_CODE"
    
    type = Element("type")
    type.text = "CHAR"
    
    data_length = Element("data_length")
    data_length.text = "15"
    
    nullable = Element("nullable")
    nullable.text = "TRUE"
    
    column.append(col_id)
    column.append(name)
    column.append(type)
    column.append(data_length)
    column.append(nullable)
    
    f = open('/tmp/output.xml', 'w')
    tree = ElementTree(root)
    tree.write(f, 'utf-8')
    
    f.close()
    
    """ <column>
      <col_id>1</col_id>
      <name>SITE_DET_CODE</name>
      <type>CHAR</type>
      <data_lengh>15</data_lengh>
      <nullable>TRUE</nullable>
    </column>
    """





if __name__ == "__main__":
    main()