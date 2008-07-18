package org.idc.xml.renderers;

import org.idc.common.sql.DatabaseConnector
import org.idc.common.exceptions.CTBTOException




public class RawDBRenderer extends DBRenderer
{
	private _staticTablesList
	private _extractionDir
	
	public def RawDBRenderer()
	{	
	}	
	
	/**_init()
	private def _readConfig() throws CTBTOException
	{
		// get the list of tables to dump
		if ( (_staticTablesList =  Config.stringsAt("RawDBRenderer","static_tables")) == null)
			throw new CTBTOException("Error: needs a list of static tables to extract")
		
		_extractionDir = Config.at("RawDBRenderer","extractionDir","/tmp")
			
	}
}