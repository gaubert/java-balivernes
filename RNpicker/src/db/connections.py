import logging
import sqlalchemy

from common.exceptions import CTBTOError


class DatabaseConnector:
    """ Class used to access the IDC database """
    
    # Class members
    c_log = logging.getLogger("connections.DatabaseConnector")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self,aUrl,aEchoLevel=True):
        
        self._url  = aUrl
        self._echo = aEchoLevel
        self._connected = False;
        
        
    def __repr__(self):
        return "<DatabaseConnector instance. id = %s, length = %d>" %(self._id,self._length)


    def connect(self):
        """ connect to the database. 
            raise CTBTOError in case of problems
        """
        
        # return if already connected
        if self._connected: return
        
        # preconditions
        if self._url is None: raise CTBTOError(-1,"Need a connection url")
 
        self._engine = sqlalchemy.create_engine(self._url)

        self._conn = self._engine.connect()
        
        self._connected = True
        
        DatabaseConnector.c_log.info("Connected to the database")
    
    def disconnect(self):
        
        self._conn.close()
        
        self._engine.dispose()
        
        self._connected = False
        
    def isConnected(self):
        return self._connected
       
        
    def getTableMetadata(self,aTableName):
        
        """ Return the metadata related to a table """
        
        self.connect()

        # create MetaData 
        meta = sqlalchemy.MetaData()

        # bind to an engine
        meta.bind = self._engine

        tableMetadata = sqlalchemy.Table(aTableName, meta, autoload=True)

        cols = [] 

        for c in tableMetadata.columns:
            desc = {}
            #print "C = %s"%dir(c)
            desc['name']     = c.name
            desc['type']     = c.type
            desc['nullable'] = c.nullable
            cols.append(desc)

        # a dictionary of dict, one dict for each row
        return cols
 

    def executeOnEachRow(self,aSql,aTreatment):
        """ run the sql request and execute a treatment on each retrieved row """
       
        sql = text(aSql)
        
        result = self._conn.execute(sql)
        
        row = result.fetchone()
        
        while row:
            aTreatment.executeOnRow(row)
            result.fetchone()
            
        result.close()
        