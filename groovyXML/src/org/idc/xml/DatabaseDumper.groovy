package org.idc.xml;import com.sun.org.apache.xalan.internal.xsltc.compiler.ForEachimport com.sun.org.apache.xalan.internal.xsltc.compiler.ForEach
// Groovimports
import org.idc.common.XmlSucker
import org.idc.common.exceptions.CTBTOException

// Java Imports
import org.shakra.common.config.Configimport org.shakra.common.file.FileSystem


public class DatabaseDumper
{
	private _dbUrl
	private _dbPassword
	private _dbLogin
	private _dbDriver
	private _staticTablesList	private _dynamicTablesList	private _limits = [:]
	private _extractionDir
	
	public def DatabaseDumper()
	{			_init()
	}	
	
		/**	 * Create a database dump from the static and dynamic tables in the configuration file	 * All the content is extracted from the static tables and only the content of the sampleIDs passed	 * by the user are extracted from the dynamic tables	 * @param sampleIDs sampleIDs	 */	public def getTailoredDatabaseDump(sampleIDs = [])	{        XmlSucker hoover = new XmlSucker(_dbDriver,_dbUrl,_dbLogin,_dbPassword)				hoover.connect()				def tempo = "";		def limit;						// get data of the static tables		for (table in _staticTablesList)		{			println "Dump table ${table}"						tempo = _generateTableFilename(table)						// if there is limit update limit			if (this._limits.containsKey(table))			{		       limit = this._limits[table]			}			else			{		       limit = 0			}						// hoover in data			hoover.saveTableContentIn(table,"${_extractionDir}/${tempo}.xml",limit)		}                // preparation for get the data from the dynamic tables        // create a string of sampleIds		def strSampleIDs = sampleIDs.join(", ")		def sqlWhere = ""				if ( strSampleIDs.size() > 0)		{			sqlWhere = " where SAMPLE_ID in ( $strSampleIDs )"		}                // for the moment always add metadata        def addMetadata = true                def sqlRequest = "" 				// get dynamic data		for (table in _dynamicTablesList)		{		   sqlRequest = "select * from " + table + sqlWhere		   		   tempo = _generateTableFilename(table)				   hoover.storeRequestResultInXml(table,"${_extractionDir}/${tempo}.xml",sqlRequest,addMetadata)		}                hoover.disconnect()	}		/** 	 * Generate a file name for the table	 */	private def _generateTableFilename(tablename)	{		// replace all . with _		def result = (tablename =~ /\./).replaceAll("_")				return result	}		public def _init()	{        // just read the config		_readConfig()                // create directories if necessary         FileSystem.createDirs(this._extractionDir)        	}		
	/**	 * get the necessary parameters from the configuration file	 */
	private def _readConfig()
	{				println "readConfig"				
		// get dbUrl default oracle driver
		_dbDriver      = Config.at("DatabaseAccess","driverClassName","oracle.jdbc.driver.OracleDriver")
		
		if ( (_dbUrl = Config.at("DatabaseAccess","url")) == null)
			throw new CTBTOException("Error: needs a valid jdbc url in the configuration file")
		
		// login and password, by default nothing
		// Error if null
		if ( (_dbLogin = Config.at("DatabaseAccess","uid")) == null)
			throw new CTBTOException("Error: needs a database login in the configuration file")
		
		if ( (_dbPassword =  Config.at("DatabaseAccess","password")) == null)
			throw new CTBTOException("Error: needs a database password in the configuration file")
				println "Got password get table list"		
		// get the list of tables to dump
		if ( (_staticTablesList =  Config.stringsAt("DataExtraction","static_tables")) == null)
			throw new CTBTOException("Error: needs a list of tables to extract")				if ( (_dynamicTablesList =  Config.stringsAt("DataExtraction","dynamic_tables")) == null)			throw new CTBTOException("Error: needs a list of tables to extract")						// get limit values for each table		def dummyList = Config.stringsAt("DataExtraction","limits")				if ( dummyList != null)		{			def tableInfo = null;			def items     = null;						dummyList.each {				tableInfo = it				items = tableInfo.split(':')								// syntax error if there are more or less than 2 elements				if (items.size() != 2)					throw new CTBTOException("Parse Error. the limit ${tableInfo} should be formatted following tablename:limit. For Example limits=GARDS_STATION:10,GARDS_DATA:1000")							_limits[items[0]] = items[1]			}		}					println "Got the limits"
		
		_extractionDir = Config.at("DataExtraction","extractionDir","/tmp")
			
	}
}