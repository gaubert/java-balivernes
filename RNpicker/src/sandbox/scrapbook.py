from StringIO import StringIO


if __name__ == '__main__':
    
    s = "Mypath"
    
    f = open("/tmp/subs-template.xml")
    
    print "Hello Scrapbook"
    
    sIO = StringIO("Blah Blsh")
    
    print "D",s.__class__
    print f.__class__
    print sIO.__class__
