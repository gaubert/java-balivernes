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
	private _tablesList	private _limits = [:]
	private _extractionDir
	
	public def DatabaseDumper()
	{			_init()
	}	
	
	/**
	 * Connect to the database with the conf file settings. 
	 * Create the XmlSucker Object and runnit for each tables in the DB
	 */
	public def dumpDatabase()
	{
		 
		XmlSucker hoover = new XmlSucker(_dbDriver,_dbUrl,_dbLogin,_dbPassword)
		
		hoover.connect()
				def tempo = "";		def limit;		
		for (table in _tablesList)		{			println "Dump table ${table}"						tempo = _generateTableFilename(table)						// if there is limit update limit			if (this._limits.containsKey(table))			{				limit = this._limits[table]			}			else			{				limit = 0			}						hoover.saveTableContentIn(table,"${_extractionDir}/${tempo}.xml",limit)		}				hoover.disconnect()
	}		/** 	 * Generate a file name for the table	 */	private def _generateTableFilename(tablename)	{		// replace all . with _		def result = (tablename =~ /\./).replaceAll("_")				return result	}		public def _init()	{        // just read the config		_readConfig()                // create directories if necessary         FileSystem.createDirs(this._extractionDir)        	}		
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
		if ( (_tablesList =  Config.stringsAt("DataExtraction","tables")) == null)
			throw new CTBTOException("Error: needs a list of tables to extract")						// get limit values for each table		def dummyList = Config.stringsAt("DataExtraction","limits")				if ( dummyList != null)		{			def tableInfo = null;			def items     = null;						dummyList.each {				tableInfo = it				items = tableInfo.split(':')								// syntax error if there are more or less than 2 elements				if (items.size() != 2)					throw new CTBTOException("Parse Error. the limit ${tableInfo} should be formatted following tablename:limit. For Example limits=GARDS_STATION:10,GARDS_DATA:1000")							_limits[items[0]] = items[1]			}		}					println "Got the limits"
		
		_extractionDir = Config.at("DataExtraction","extractionDir","/tmp")
			
	}
}