
import re
import common.utils
import common.iso8601
import datetime


def main():
    
    f = open("/home/aubert/ecmwf/workspace/RNpicker/etc/ext/SAMPMLTemplate.xml","r")
    
    common.utils.file_exits("/home/aubert/ecmwf/workspace/RNpicker/etc/ext/SAMPMLTemplate.xml")
    
    
    fileContent = f.read()
    
   # print "fileContent %s"%(fileContent)
    
    str = "<xml><a><b>${REMARK}</b></a></xml>"
    pattern = "\${REMARK}"
    
    result = re.sub(pattern, "YOUWIN", fileContent)
    
    print "Result = %s"%(result[1:200])
    
    


if __name__ == "__main__":
    
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