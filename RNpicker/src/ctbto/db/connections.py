import logging
import sqlalchemy


from ctbto.common.utils import ftimer
from ctbto.common import CTBTOError


class DatabaseConnector:
    """ Class used to access the IDC database """
    
    # Class members
    c_log = logging.getLogger("connections.DatabaseConnector")
    c_log.setLevel(logging.DEBUG)
    
    def __init__(self,aDatabase,aUser,aPassword,aTimeReqs=False):
        
        self._database      = aDatabase
        self._user          = aUser
        self._password      = aPassword
        self._activateTimer = aTimeReqs
        
        self._connected     = False; #IGNORE:W0104
        
        self._url = None
        
        self._createUrl()
        
        self._engine = None
        self._conn   = None
        
    
    def _createUrl(self):
        
        if self._database is None:
            raise CTBTOError(-1,"Need a database hostname to make the connection url\n")
        
        if self._user is None:
            raise CTBTOError(-1,"Need a user to connect to the database\n")
        
        if self._password is None:
            raise CTBTOError(-1,"Need a password to connect to the database\n")
        
        # Add support for other databases
        self._url = "oracle://%s:%s@%s"%(self._user,self._password,self._database)

    def hostname(self):
        return self._database
    
    def user(self):
        return self._user

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
            desc['name']     = c.name
            desc['type']     = c.type
            desc['nullable'] = c.nullable
            cols.append(desc)

        # a dictionary of dict, one dict for each row
        return cols
 
    def execute(self,aSql):
        """execute a sql request on the database"""
        
        sql = sqlalchemy.text(aSql)
        
        if self._activateTimer:
            result = []
            func = self._conn.execute
            t= ftimer(func,[sql],{},result,number=1)
            DatabaseConnector.c_log.info("\nTime: %s secs \nDatabase: %s\nRequest: %s\n"%(t,self._database,aSql))
            return result[0]
        else:
            result = self._conn.execute(sql)
            return result
        
        
        

    def executeOnEachRow(self,aSql,aTreatment):
        """ run the sql request and execute a treatment on each retrieved row """
       
        sql = sqlalchemy.text(aSql)
        
        result = self._conn.execute(sql)
        
        row = result.fetchone()
        
        while row:
            aTreatment.executeOnRow(row)
            row = result.fetchone()
            
        result.close()
        