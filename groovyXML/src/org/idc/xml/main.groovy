package org.idc.xml;


def cli = new CliBuilder( usage: 'iml_export -s sampleids')
cli.h(longOpt:'help', 'usage information')
cli.s(argName:'sampleids', longOpt:'samples', args:1, required:true, type:String, '')

def opt = cli.parse(args)
if (!opt) return
if (opt.h) cli.usage()


println "Dump Database "

dbDumper = new DatabaseDumper()

dbDumper.dumpDatabase()

println "Job Done. BYYE"

System.exit(0)

