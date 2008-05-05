package org.idc.xml.renderers;

import org.idc.common.exceptions.CTBTOExceptionimport org.idc.common.exceptions.CTBTOException
/**
 * Abstract for all renderers also acting as a factory
 */
public abstract class DBRenderer
{
	public static DBRenderer createRenderer(aType) throws CTBTOException
	{
		
		// check that the TypeName is a renderer
		try
		{
		  def eRenderer = Enum.valueOf(RendererType,aType)
		}
		catch(IllegalArgumentException e)
		{
		   throw new CTBTOException("Error: There is no Renderer Type named ${aType}")
		}
		
		def paKage = "org.idc.xml.renderers"
		
		def className = "${paKage}.${aType}"
		
		Class klass = null
		
		try
		{
		  klass = Class.forName(className)
		  
		  return klass.newInstance()
		}
		catch (ClassNotFoundException e)
		{
			throw new CTBTOException("Error: Class named ${className} doesn't exist")
		}
	}
	
	public abstract render(sampleIDs = [])
}