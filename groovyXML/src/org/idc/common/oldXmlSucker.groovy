package org.idc.common;

import groovy.sql.Sql
import java.sql.ResultSetMetaData
import groovy.xml.MarkupBuilder


/**
   Read information in the DB and produce an XML files

   @author Guillaume Aubert (guillaume.aubert@ctbto.org)
   @since 0.5
*/
public class XmlSucker
{
	private _dbUrl;
	private _dbPassword;
	private _dbLogin;
	
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
	
	/**
    * Dump the content of specified table in an XML file following the specified xml dialect
    * @param tablename name of the table to dump
    * @param filename filename where to write the xmlized DB dump
    * 
    */
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
	
	/**
	 * Execute a request and store its result as xml default
	 * @param tablename name of the table to dump
	 * @param filename filename where to write the xmlized DB dump
	 * @param sampleIDs list of sampleIDs 
	 * 
	*/
	public def storeRequestResultInXml(tablename,filename,sqlRequest,addMetadata)
	{
		if (! _connected)
			throw CTBTOException("Error: Please connect first to the database")
		
		def out    = new File(filename)
		def writer = new FileWriter( out )
		def xml    = new MarkupBuilder( writer )
		
		def cpt         = 0
		def key         = null
		def map         = null
		def val         = null
		def hasMetadata = false
		
		 xml.table(name:"${tablename}")
		 {
			try
			{
		      _sqlConn.eachRow(sqlRequest) 
		      {
			      row -> 
			      
			      if ( (!hasMetadata) && addMetadata) 
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
		
		  if (cpt > 0)
		  {
		     println " Retrieved ${cpt} rows for ${tablename} when request ${sqlRequest} has been executed"
		     println "End of saveTableContentIn for ${tablename}. Data stored in in ${filename}."
		  }
		  else
		  {
			  // delete file as there is no data
			  if (out.exists())
			  {
				println "There is no data related to the specified sampleIDs in ${tablename} so delete ${filename}"
			    out.delete();
			  }
		  }
	}
	
	/**
	 * Dump the content of specified table restricted to the passed sampleIDs in an XML file following the specified xml dialect
	 * @param tablename name of the table to dump
	 * @param filename filename where to write the xmlized DB dump
	 * @param sampleIDs list of sampleIDs 
	 * 
	*/
	public def saveTableContentForSampleIDs(tablename, filename,sampleIDs)
	{
		if (! _connected)
			throw CTBTOException("Error: Please connect first to the database")
		
	
		// create a string of sampleIds
		def strSampleIDs = sampleIDs.join(", ")
		def sqlWhere = ""
		
		if ( strSampleIDs.size() > 0)
		{
			sqlWhere = " where SAMPLE_ID in ( $strSampleIDs )"
		}
		
		println "saveTableContentIn: Saving data for table ${tablename} in ${filename} for sampleIDs: ${strSampleIDs}"
		
		def out    = new File(filename)
		def writer = new FileWriter( out )
		def xml    = new MarkupBuilder( writer )
		
		def cpt         = 1
		def key         = null
		def map         = null
		def val         = null
		def hasMetadata = false
		
		def dataSql     = "SELECT * FROM " + tablename + sqlWhere
		
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
		
		  println " Retrieved ${cpt} rows for ${tablename} for sampleIDs = ${strSampleIDs}"
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