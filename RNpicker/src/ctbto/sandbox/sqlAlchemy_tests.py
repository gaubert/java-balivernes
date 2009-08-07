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
    
    engine = create_engine('oracle://centre:data@idcdev', echo=False)

    conn = engine.connect()

    print "Connected to test database"

    # create MetaData 
    meta = MetaData()
    
    # bind to an engine
    meta.bind = engine

    the_schema = 'sel3'
    
    origin   = Table('ORIGIN', meta, schema= the_schema, autoload=True)
    assoc    = Table('ASSOC', meta, schema= the_schema, autoload=True)
    origerr  = Table('ORIGERR', meta, schema= the_schema, autoload=True)
    
    the_printed_vals = [origin.c.orid, origin.c.time, origin.c.commid, origin.c.depth, origin.c.ml, origin.c.ms, origin.c.mb]
    the_wheres       = and_()
    the_wheres.append(origin.c.orid == 4874580)
    the_wheres.append(origin.c.orid == assoc.c.orid)
    
    sel = select(the_printed_vals).where(the_wheres).distinct()
    
    print("executed request: \n[\n%s\n]\n"%(sel))
    
    result = conn.execute(sel)
    
    row = result.fetchone()
    
    result.close()
    
    print("orid = %s"% (row.orid) )
    
    
    


def main():
    print "Hello %d, string = %s"%(1,"my String")

    test_with_metadata_and_select()



if __name__ == "__main__":
    main()

