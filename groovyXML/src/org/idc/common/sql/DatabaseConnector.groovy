package org.idc.common.sql;

import groovy.sql.Sql
import java.sql.SQLExceptionimport org.idc.common.exceptions.CTBTOExceptionimport org.idc.common.exceptions.CTBTOException
import org.shakra.common.config.Config
/**
   Read Database Configuration information and connect to the DB

   @author Guillaume Aubert (guillaume.aubert@ctbto.org)
   @since 0.5
*/
public class DatabaseConnector
{
	private   _dbUrl        = null;
	private   _dbPassword   = null;
	private   _dbLogin      = null;
	
	private   _dbDrivertype = "thin";
	private   _dbDriver     = "oracle.jdbc.driver.OracleDriver";
	
	private   _connected = false;
	protected _sqlConn = null;
	
	public DatabaseConnector(dbDriver,dbUrl,login, password)
	{
		_dbUrl       = dbUrl;
		_dbLogin     = login;
		_dbPassword  = password;
		_dbDriver    = dbDriver;
	}
	
	/**
	 * Default Constructor try to read the database connection information from the configuration file
	 */
	public DatabaseConnector()
	{
		_readConfig()
	}
	
	/**
	 * Close connection with the database
	 */
	public def disconnect() throws Exception
	{
		_sqlConn.close()
		
		_sqlConn = null
		
		_connected = false;
	}
	
	/**
	 * Connect to the database with the DB parameters passed in the constructor
	 */
	public def connect() throws Exception
	{
		if (! _connected)
		{		
		
		  assertDBInformation()
			
		  _sqlConn   = Sql.newInstance(_dbUrl, _dbLogin, _dbPassword, _dbDriver)
		
		  _connected = true
		}
	}
	
	private def assertDBInformation() throws CTBTOException
	{
		if (this._dbUrl == null)
			throw new CTBTOException("dbUrl has not been set. Provide DatabaseConnector with the database details")
		
		if (this._dbLogin == null)
			throw new CTBTOException("dbLogin has not been set. Provide DatabaseConnector with the database details")
		
		if (this._dbPassword == null)
			throw new CTBTOException("dbPassword has not been set. Provide DatabaseConnector with the database details")
		
		if (this._dbDriver == null)
			throw new CTBTOException("dbDriver has not been set. Provide DatabaseConnector with the database details")
	}
	
	/**
	 * Connect to the database with the passed parameters if the connection is not established yet or has been close.
	 * Update the Object attributes with the passed values
	 * @param dbUrl      JDBC connection URL
	 * @param login      Login
	 * @param password   Password
	 * @param dbDriver   Database driver flavour
	 */
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
	
	def private _readConfig()
	{
        //		 get dbUrl default oracle driver
		_dbDriver    = Config.at("DatabaseAccess","driverClassName","oracle.jdbc.driver.OracleDriver")
		
		_dbUrl       = Config.at("DatabaseAccess","url")

		_dbLogin     = Config.at("DatabaseAccess","uid")
		
		_dbPassword  =  Config.at("DatabaseAccess","password")
	
	}
	
	/**
	 * True is connected, false otherwise
	 */
	public boolean isConnected()
	{
		return _connected;
	}
	
	/** methode delegated to SqlConnection **/
	
	public void eachRow(String sql, List params, Closure closure) throws SQLException
	{
		_sqlConn.eachRow(sql,params,closure)
	}
	
	public void eachRow(String sql, Closure closure) throws SQLException
	{
		_sqlConn.eachRow(sql,closure)
	}
	
	public void eachRow(String sql, Closure metadataClosure, Closure closure) throws SQLException
	{
		_sqlConn.eachRow(sql,metadataClosure,closure)
	}
	
}