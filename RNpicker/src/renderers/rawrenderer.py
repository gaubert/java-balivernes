# standard libraries
import logging
import sys
import re
from xml.etree.ElementTree import ElementTree, Element, SubElement, dump # Python 2.5

# internal libraries
from  common.exceptions import CTBTOError
from  db.connections    import DatabaseConnector
import common.utils as utils

""" Module used to dump the database table content in an xml relational context """

class DBRawRenderer:
    """ Class used to get table content and renderer it in a crude xml format """
    
    # Class members
    c_log = logging.getLogger("rawrenderer.DBRawRenderer")
    c_log.setLevel(logging.DEBUG)
    
    c_pattern = re.compile(r'\.')
    
    def __init__(self,aDbConnector=None):
        
        self._dbConnector = aDbConnector
        self._callbackObj = None
        
    def __repr__(self):
        return "<DBRawRenderer instance>"
    
    def _generateTableFilename(self,aTablename):
    
        # replace all . with _
        result = DBRawRenderer.c_pattern.sub("_",aTablename)
        
        return result
    
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
    
    def _save_content_in_file(self,aDir,aFilename,aXmlRoot): 
        """ Save an XmlRoot into a file. """
       
        # write xml tree in file
        f = open("%s/%s.xml"%(aDir,aFilename), 'w')
        
        utils.prettyFormatElem(aXmlRoot)
         
        tree = ElementTree(aXmlRoot)
        
        # write in file
        tree.write(f, 'utf-8')
        
        f.close()
        
    def _render_static_table(self,aTableName):
        """ Retrieve the full content of these tables which are read from the configuration file"""
        
        DBRawRenderer.c_log.info("Generate XML for static table %s"%aTableName)
        
        filename = self._generateTableFilename(aTableName) 
        
        # preconditions
        if self._dbConnector is None: raise CTBTOError(-1,"Need a database connector")
   
        DBRawRenderer.c_log.info("start rendering for static table %s"%(aTableName))
        
        # get table metadata
        metadata = self._dbConnector.getTableMetadata(aTableName)
        
        # create xml tree
        xmlRoot = Element("table")
    
        xmlRoot.set("name",aTableName)
        
        # get table metadata
        self._render_metadata(aTableName,xmlRoot,metadata)
        
        # get table content
        sql = "select * from %s"%(aTableName)
        
        # add a data subElement to root
        xmlData = SubElement(xmlRoot,"data")
        
        # store xml Tree in _callbackObj
        self._callbackObj = xmlData
        
        self._dbConnector.executeOnEachRow(sql,self)
        
        self._save_content_in_file("/tmp",filename, xmlRoot)
        
        
    def executeOnRow(self,row = None):  
        """ callback method used by the DB connection object. """
         
        if row == None: return
         
        # get callbackObj
        xmlData = self._callbackObj
        
         # add a row element in xml Tree
        xmlRow = SubElement(xmlData,"row")
        
        for key in row.keys():
            #add tag with col name
            r = SubElement(xmlRow,"%s"%key)
            r.text = "%s"%row[key] 
        
        
    def render(self,aTableName, aSampleIDs = []):
        """ Render a table in xml """
        
        self._render_static_table(aTableName)
            
            