# standard libraries
import logging

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

    def render(self,aTableName):
        """ Render a table in xml """
        
        # preconditions
        if self._dbConnector is None: raise CTBTOError(-1,"Need a database connector")
   
        DBRawRenderer.c_log.info("start rendering for table %s"%(aTableName))
        
        # get table metadata
        metadata = self._dbConnector.getTableMetadata(aTableName)
        
        for col in metadata:
          utils.printDict(col)
        
        
    def executeOnRow(self,aRow):
        
        print "Hello"