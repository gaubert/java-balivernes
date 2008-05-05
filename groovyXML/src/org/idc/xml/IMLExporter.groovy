package org.idc.xml;

import org.idc.xml.renderers.DBRenderer
/**
 * Main class used for extraction
 * @author guillaume.aubert@ctbto.org
 *
 */
class IMLExporter 
{
    static void main(args) 
	{    	
    	def rendererType = "RawDBRenderer"
    	
    	// parse options and arguments
    	def cli = new CliBuilder(usage: 'iml_exporter [-t RawDBRenderer] sampleIDs.\n For example iml_export 130639, 130638.\n To run in debugging mode set the env variable $IML_DEBUG', parser: new org.apache.commons.cli.GnuParser ())
        cli.h(longOpt: 'help', 'usage information')
        cli.t(longOpt: 'type', 'type of xml renderer used. (default = RawDBRenderer)', args: 1, required:false, type:GString,"RawDBRenderer")
        
        def opt = cli.parse(args)

        if (opt.h) 
        {
          cli.usage()
          exit 0;
        }
    	
    	if (opt.t)
    	{
    	   rendererType = opt.t
    	}
    	
    	println "Create XML with a ${rendererType}"
    	
    	def leftArgs = opt.arguments();
    	
    	try
    	{
    		
    	  // no arguments 
    	  if (leftArgs.size() == 0)
    	  {
    		throw new IllegalArgumentException("Error: Please enter a list of sampleIDs")
    	  }

    	  // join all the arguments with space as the joiner
    	  def dummyStr =leftArgs.join(' ') 

	      // split with , or : or space
	      def sampleIDs = dummyStr.split(',|:| ')

	      // need to check that all the sampleIDS are only number => regular expression
	      // need to trim the sampleIDs and check that they are number
	      def validSampleIDs = []

	      // add all valid sample IDs
	      sampleIDs.each
	      {
	        def stripped = it.trim()
	        
	        if (stripped.size() > 0)
	        {
	    	  //check that it is a number
	    	  if (stripped =~ /[1-9]+/)
	    	  {    	  
	    	     validSampleIDs.add(stripped)
	    	  }
	    	  else
	    	  {
	    		  throw new IllegalArgumentException("Error: the passed arguments ${stripped} are unvalid sampleID")
	    	  }
	        }
	        else
	        {
	           throw new IllegalArgumentException("Error: the passed arguments ${stripped} unvalid sampleID")
	        }
	        
	      }
	      
	      println "Identified sampleIDs = ${validSampleIDs}"

	      execute(validSampleIDs)
	    
	      println "Database extraction performed successfully"
    	}
    	catch (IllegalArgumentException e)
    	{
    		println e.getMessage()
    		cli.usage()
            System.exit(1);	
    	}
    	catch (Exception e)
    	{
    		println e.getMessage()
    		cli.usage()
            System.exit(1);	
    	}

	      System.exit(0)

    }
    
    protected static execute(aSampleIDs,aRendererType = "RawDBRenderer")
    {
    	def renderer = DBRenderer.createRenderer(aRendererType)
    	
    	renderer.render(aSampleIDs)
    }
}


