class IMLExporterMain {
 
static void main(args) 
{
 
def cli = new CliBuilder(usage: 'iml_exporter -s sampleIDs. For example -s 123456,456789', parser: new org.apache.commons.cli.GnuParser ())
cli.h(longOpt: 'help', 'usage information')
cli.s(longOpt: 'sampleids', 'list of sampleids', args: 1, required:false, type:GString)
def opt = cli.parse(args)

if (opt.h) 
{
  cli.usage()
  exit 0;
}

if(!opt.s)
{ 
  println "Error: Need a list of sampleids"
  cli.usage()
}
else
{
  def dummyStr = opt.s

  // split with ,
  def sampleIDs = dummyStr.split(',|:| ')

  println "splitted string a list = ${sampleIDs}"

  // need to check that all the sampleIDS are only number => regular expression
  // need to trim the sampleIDs and check that they are number
  def validSampleIDs = []

  sampleIDs.each
  {
    def stripped = it.trim()
    println "local = ${stripped}" 
    
    if (stripped.size() > 0)
       validSampleIDs.add(stripped)
  }

  println "sampleIDS = ${validSampleIDs}"
}
 
}
}
