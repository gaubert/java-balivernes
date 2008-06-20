# standard libraries
import logging
import sys
from xml.etree.ElementTree import ElementTree, Element, SubElement, dump # Python 2.5

# internal libraries
from  common.exceptions import CTBTOError
from  db.connections    import DatabaseConnector
import common.utils as utils


class DBRawRenderer:
    """ Class used to get table content and renderer it in a crude xml format """
    
    # Class members
    c_log = logging.getLogger("rawrenderer.DBRawRenderer")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self,aDbConnector=None):
        
        self._dbConnector = aDbConnector
        
    def __repr__(self):
        return "<DBRawRenderer instance>"
    
    def _render_metadata(self,aTableName,xmlRoot,metadata=None):
        """render the metadata in columns formats"""
        
         # preconditions
        if metadata is None: raise CTBTOError(-1,"passed argument metadata is null")
   
        # add metadata tag
        xmlMetadata = SubElement(xmlRoot,"metadata")
   
   
        cpt=1
   
        for col in metadata:
            
            # create column element in metadata element
            column = SubElement(xmlMetadata,"column")
    
            # add col_id
            elem      = Element("col_id")
            elem.text = "%s"%cpt
            column.append(elem)
           
            # add name tag
            elem      = Element("name")
            elem.text = col["name"]
            column.append(elem)
    
            # add type tag
            elem      = Element("type")
            elem.text = "%s"%(col["type"].get_col_spec())
            
             # add length tag
             # for this need to parse get_col_spec result
             #elem      = Element("length")
             #elem.text = "%s"%(dir(col["type"]))
            
            column.append(elem)
            
             # add nullable
            elem      = Element("nullable")
            elem.text = "%s"%(col["nullable"])
            column.append(elem)

            cpt += 1
        
    def _create_filterable_sql(self,aTables=[],aSampleIDs=[]):    
        """ create and return an sql statement with the sampleIDS """
        
        producedSql = []
        
        if len(aSampleIDs) > 0:
           
            samples = ",".join(["%s" % (sid) for sid in aSampleIDs])
            
            sqlWhere = "where SAMPLE_ID in ( %s )"%(samples)

            for table in aTables:
               sql = "select * from %s %s"%(table,sqlWhere)
               producedSql.append(sql)            
        
        else:
            raise CTBTOError(-1,"No SampleIDS. Empty Sql request")
         
        return producedSql   
        
            
    def render(self,aTableName, aSampleIDs = []):
        """ Render a table in xml """
        
        # preconditions
        if self._dbConnector is None: raise CTBTOError(-1,"Need a database connector")
   
        DBRawRenderer.c_log.info("start rendering for table %s"%(aTableName))
        
        # get table metadata
        metadata = self._dbConnector.getTableMetadata(aTableName)
        
        # create xml tree
        xmlRoot = Element("table")
    
        xmlRoot.set("name",aTableName)
        
        # get table metadata
        self._render_metadata(aTableName,xmlRoot,metadata)
        
        sqls = self._create_filterable_sql(["tableA","tableB","tableC"],[1234567,3435343])
        
        print "sqls %s"%(sqls)
        
        # write xml tree in file
        f = open('/tmp/output.xml', 'w')
        
        utils.prettyFormatElem(xmlRoot)
         
        tree = ElementTree(xmlRoot)
        
        # write in file
        tree.write(f, 'utf-8')
        
        # write in stdout
        #tree.write(sys.stdout, "utf-8")
       
        f.close()
            
    def executeOnRow(self,aRow):
        
        print "Hello"