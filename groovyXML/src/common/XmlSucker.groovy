package common;

import groovy.sql.Sql
import java.sql.ResultSetMetaData
import groovy.xml.MarkupBuilder

public class XmlSucker
{
	private _dbUrl;
	private _dbPassword;
	private _dbLogin;
	
	
	//orac1.ctbto.org:1521/IDCDEV.CTBTO.ORG
	private _dbDrivertype = "thin";
	private _dbDriver     = "oracle.jdbc.driver.OracleDriver";
	
	private _connected = false;
	private _sqlConn = null;
	
	public XmlSucker(dbDriver,dbUrl,login, password)
	{
		_dbUrl       = dbUrl;
		_dbLogin     = login;
		_dbPassword  = password;
		_dbDriver    = dbDriver;
	}
	
	public def disconnect() throws Exception
	{
		_sqlConn.close()
		
		_sqlConn = null
		
		_connected = false;
	}
	
	public def connect() throws Exception
	{
		if (! _connected)
		{
		  _sqlConn   = Sql.newInstance(_dbUrl, _dbLogin, _dbPassword, _dbDriver)
		
		  _connected = true
		}
	}
	
	public def connect(dbUrl,login,password,dbDriver = null)
	{
		if (! _connected)
		{
		  _dbUrl       = dbUrl
		  _dbLogin     = login
		  _dbPassword  = password
		
		  if (dbDriver != null)
			 _dbDriver = dbDriver
		
		  connect()
		
		  _connected = true
		}
	}
	
	public def saveTableContentIn(tablename, filename,limit = 0)
	{
		if (! _connected)
			throw CTBTOException("Error: Please connect first to the database")
		
		def strLimit = "all"
		def sqlLimit = ""
		
		if ( limit != 0)
		{
			strLimit = limit
			sqlLimit = " where rownum <= ${limit}"
		}
		
		println "saveTableContentIn: Saving data for table ${tablename} in ${filename}. Get ${strLimit} row(s) max."
		
		def out    = new File(filename)
		def writer = new FileWriter( out )
		def xml    = new MarkupBuilder( writer )
		
		def cpt         = 1
		def key         = null
		def map         = null
		def val         = null
		def hasMetadata = false
		
		def dataSql     = "SELECT * FROM " + tablename + sqlLimit
		def metadataSql = "SELECT * FROM " + tablename + " where rownum=1"

		 xml.table(name:"${tablename}")
		 {
			try
			{
		      _sqlConn.eachRow(dataSql) 
		      {
			      row -> 
			      
			      if (! hasMetadata) 
			      {
			    	  hasMetadata = storeMetadata(xml,row)
			      }
			      
			      map = getColumnAsMap(row)
			
			      xml.row
			      {
		            map.entrySet().each()
		            {
		               entry ->
		                 key = entry.getKey();
		                 val = entry.getValue();
		                 addNode(xml,key,val)
		            }
			      }
		    
		          cpt++
		        } 
		     }
		     catch (Exception e)
		     {
			   println e.getMessage() 
		     }
		   }
		
		  println " Retrieved ${cpt} rows for ${tablename}"
		  println "End of saveTableContentIn for ${tablename}. Data stored in in ${filename}."
	}
	
    /*	 create method to add generic node <key>value</value>
     *	 little helper to add a Node in the Xml Tree
     * 
     */
	private def addNode(builder,key,value) 
	{ 
		if ( key != null && value != null)
		{
			// to do xml.key where key = name or station_id. At the end we will have <station_id> my val </station_id>
			builder.invokeMethod(key,value)
		}
	}

    private def getMetadataDefinition(resultSet)
    {
    	def inMap = null
    	def list = []
		ResultSetMetaData metaData = resultSet.getMetaData();
		
		//println "Metadata " + metaData
		
		int count = metaData.getColumnCount();
		
		for (int i = 1; i <= count; i++) 
		{
			inMap = [:]
			
			inMap["name"]         = metaData.getColumnName(i)
			inMap["id"]           = i
			inMap["type"]         = metaData.getColumnType(i)
			inMap["length"]       = metaData.getPrecision(i)
			inMap["isNullable"]   = metaData.isNullable(i)
			
			if (inMap.size() > 0) list[i-1] = inMap
			
			
			//printf("colName = %s, colType= %s, colTypeName=%s, colLabel=%s, colScale=%s, colPrecision=%s, isNullable=%s\n",metaData.getColumnName(i),metaData.getColumnType(i),metaData.getColumnTypeName(i),metaData.getColumnLabel(i),metaData.getScale(i),metaData.getPrecision(i),metaData.isNullable(i))
		}
		
		//println "list = ${list}"
		
		return list
    }
    
    // For the moment store in XML
    private def storeMetadata(xml,row)
    {
    	def l = getMetadataDefinition(row)
    	
    	xml.metadata
    	{
    	 
    	   l.each() {
    		   info ->
    		   xml.column
    		   {
    			   xml.col_id(info["id"])
    			   xml.name(info["name"])
    			   xml.type(info["type"])
    			   
    			   if (info["length"] > 0) xml.data_lengh(info["length"])
    			   
    			   (info["isNullable"]) ? xml.nullable("TRUE") : xml.nullable("FALSE")
    			   
    		   }
    	   }
    	}
    	
    	// no pbs return true
    	return true
    }
     
    /*
     * return SQL Column content (Col name + val) as a Map
     */	 
	private def getColumnAsMap(resultSet)
	{
		def colMap = [:]
		ResultSetMetaData metaData = resultSet.getMetaData();
		
		int count = metaData.getColumnCount();
		
		for (int i = 1; i <= count; i++) 
		{
			Object obj = (resultSet.getObject(i) == null) ? "" : resultSet.getObject(i)
			colMap[metaData.getColumnName(i)] = obj    
		}
		
		return colMap
	}
    
    /* 
     * another way to get the data in memory.
     * This isn't used for the moment
     */
	def private getAllRowsInMemoryAndCreateXml()
	{

	  def out = new File('/tmp/gards_stations.xml')
	  def writer = new FileWriter( out )
	  def xml = new MarkupBuilder( writer )
	  
	  def rows = sql.rows("SELECT * FROM rmsauto.gards_stations");

	  //create xml.table
	  xml.table(name:"GARDS_STATIONS")
	  {
	     rows.each() 
	     { 
	        row ->
	          // create xml.row
	  	      xml.row
	  	      {
	            row.entrySet().each()
	            {
	          	  entry ->
	          	    key = entry.getKey();
	          	    val = entry.getValue();
	          	    println("key ${key} val ${val}")
	          	    addNode(xml,key,val)
	            }
	         
	  	     }
	     }
	  }
	}
}