#!/usr/bin/python

from sqlalchemy import *

def access():

    #conn = cx_Oracle.connect('aubert/ernest25@idcdev')
    print "Connect to test database"

    engine = create_engine('oracle://aubert:ernest25@idcdev', echo=True)

    conn = engine.connect()

    print "Connected to test database"

    s = text("""SELECT typeid,dir FROM FILEPRODUCT""")

    result = conn.execute(s)

    row = result.fetchone()

    while row:
        print row
        row = result.fetchone()

def getMetadata():
    print "Connect to test database"

    engine = create_engine('oracle://aubert:ernest25@idcdev', echo=False)

    conn = engine.connect()

    print "Connected to test database"

    # create MetaData 
    meta = MetaData()

    # bind to an engine
    meta.bind = engine

    #fileproduct = Table('FILEPRODUCT', meta, autoload=True)
    fileproduct = Table('GARDS_SAMPLE_DATA', meta, autoload=True)

    cols = [] 

    for c in fileproduct.columns:
        desc = {}
        desc['name'] = c.name
        desc['type'] = c.type
        cols.append(desc)

 
    #print "cols=%s"%(cols)
    for elem in cols:
       printDict(elem)

def printDict(di, format="%-25s %s"):
    for (key, val) in di.items():
        print format % (str(key)+':', val)
        

def test_with_metadata():
    
    print "Connect to test database"

    engine = create_engine('oracle://centre:data@idcdev', echo=False)

    conn = engine.connect()

    print "Connected to test database"

    # create MetaData 
    meta = MetaData()

    # bind to an engine
    meta.bind = engine
    
    #fileproduct = Table('FILEPRODUCT', meta, autoload=True)
    fileproduct = Table('FILEPRODUCT', meta, autoload=True)
    
    the_schema = 'sel3'
    
    sel3_origin   = Table('ORIGIN',meta, schema= the_schema, autoload=True)
    #sel3_assoc    = Table('SEL3.ASSOC',meta, autoload=True)
    #sel3_origerr  = Table('SEL3.ORIGERR',meta, autoload=True)

    the_table = sel3_origin

    cols = [] 

    for c in the_table.columns:
        desc = {}
        desc['name'] = c.name
        desc['type'] = c.type
        cols.append(desc)
    
    print("Cols %s\n"%(cols))
    
def test_with_metadata_and_select():
    


def main():
    print "Hello %d, string = %s"%(1,"my String")

    test_with_metadata()



if __name__ == "__main__":
    main()

