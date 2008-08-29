
import re
import common.utils


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
    main()