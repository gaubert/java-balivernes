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
    	
    	// join all the arguments with space as the joiner
    	def dummyStr =args.join(' ') 

	    // split with , or : or space
	    def sampleIDs = dummyStr.split(',|:| ')

	    println "splitted string a list = ${sampleIDs}"

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
	    		  println "Error: the passed argument ${stripped} isn't a valid sampleID"
	    		  System.exit(1)
	    	  }
	      }
	        
	    }

	    println "sampleIDS = ${validSampleIDs}"
	  
	    execute(validSampleIDs)
	    
	    println "Job Done. BYYE"

	    System.exit(0)

    }
    
    protected static execute(aSampleIDs,aRendererType = "RawDBRenderer")
    {
    	def renderer = DBRenderer.createRenderer(aRendererType)
    	
    	renderer.render(aSampleIDs)
    }
}


