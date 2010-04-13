
import re
import ctbto.common.utils
import datetime
import time


def main():
    
    f = open("/home/aubert/ecmwf/workspace/RNpicker/etc/ext/SAMPMLTemplate.xml","r")
    
    common.utils.file_exits("/home/aubert/ecmwf/workspace/RNpicker/etc/ext/SAMPMLTemplate.xml")
    
    
    fileContent = f.read()
    
   # print "fileContent %s"%(fileContent)
    
    str = "<xml><a><b>${REMARK}</b></a></xml>"
    pattern = "\${REMARK}"
    
    result = re.sub(pattern, "YOUWIN", fileContent)
    
    print "Result = %s"%(result[1:200])
    
    
def convert(aStr):
    
    return datetime.datetime.strptime(aStr,'%Y-%m-%dT%H:%M:%S')


if __name__ == "__main__":
    
    
    start = '2007-12-20T08:50:17'
    stop  = '2007-12-21T08:48:37'
    
    s1 = datetime.datetime.strptime(start,'%Y-%m-%dT%H:%M:%S')
    
   # start = common.time.getDateTimeFromISO8601(start)
    
    stop = convert(stop)
      
   
    print "epoch start time %s"%(time.mktime(s1.timetuple()))
   # print "epoch stop time %s"%(time.mktime(stop.timetuple()))
    
    
    exit(1)
    
    
    textValue = '5PPP3.29 Y'
    
    t = datetime.timedelta(days=53.29)
    
    print "t %s"%(t.seconds)
    
    ex = "53.24 H"
    
    pattern = "(?P<value>[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)(\s)*D"
    
    compiled = re.compile(pattern)
    
    print "group index %s"%(compiled.groupindex)
    
    aResult = re.match("(?P<year>[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)(\s)*Y|(?P<month>[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)(\s)*M|(?P<day>[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)(\s)*D|(?P<hour>[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)(\s)*H|(?P<minute>[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)(\s)*M|(?P<second>[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)(\s)*S",ex)
    
    value = aResult.group('hour')
    
    print "Result ", float(value)

    print "parser = %s"%(common.iso8601.parse("PT118939.968S"))

    main()