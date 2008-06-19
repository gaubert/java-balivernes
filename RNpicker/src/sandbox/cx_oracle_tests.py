#!/usr/bin/python

import cx_Oracle

def accessWithcx_Oracle():

    conn = cx_Oracle.connect('aubert/ernest25@idcdev')
    curs = curs = conn.cursor()
    sql = """SELECT * FROM FILEPRODUCT"""

    #execute req
    curs.execute(sql)
    row = curs.fetchone()
    while row:
        (param, val) = (row[0], row[1])
        print "param = %s, val = %s"%(param,val)
        row = curs.fetchone()

    curs.close()


def main():
    print "Hello %d, string = %s"%(1,"my String")

    accessWithcx_Oracle()



if __name__ == "__main__":
    main()

