'''
Created on Aug 18, 2009. Tools for migrating Radionuclide Data

@author: guillaume.aubert@ctbto.org
'''

import sqlalchemy


SQL_GET_SAMPLE_IDS = "select sample_id from RMSAUTO.GARDS_SAMPLE_DATA where moddate between to_date('%s', 'yyyy/mm/dd') and to_date('%s', 'yyyy/mm/dd')"

SQL_GET_GARDS_SAMPLE_DATA_PER_SID = "select * from RMSAUTO.GARDS_SAMPLE_DATA where sample_id = %s"

SQL_GET_FILEPRODUCT_PER_CHANID    = "select * from IDCX.FILEPRODUCT where chan like '%s'"

SQL_GET_FPDESCRIPTION_CONTENT    = "select * from IDCX.FPDESCRIPTION"


class ArchiveExctractor(object):
    """
       This class extract data from the Archive and copies all necessary files
    """
    
    def __init__(self, a_input_url, a_output_url):
        """ constructor """
        
        self._input_engine  = sqlalchemy.create_engine(a_input_url)
         #orac_engine    = sqlalchemy.create_engine('oracle://centre:data@idcdev.ctbto.org')
        self._input_conn    = self._input_engine.connect()
        
        self._output_engine = sqlalchemy.create_engine(a_output_url)
        self._output_conn   = self._output_engine.connect()

    def copy_from_rn_archive_database(self, a_has_to_drop_tables = False):
        
        input_meta = sqlalchemy.MetaData()
        input_meta.bind = self._input_engine
        
        print("Autoload tables \n")
        
        input_gards_sample_data   = sqlalchemy.Table('GARDS_SAMPLE_DATA',  input_meta, schema='RMSAUTO', autoload=True)
        input_file_product        = sqlalchemy.Table('FILEPRODUCT',  input_meta, schema='IDCX', autoload=True)
        input_fp_description      = sqlalchemy.Table('FPDESCRIPTION',  input_meta, schema='IDCX', autoload=True)
        
        #print("gards_sample_data.cols = %s" % (gards_sample_data1.columns) )
        
        print("Get All SampleIDs from the Archive DB \n")
        
        result = self._input_conn.execute(SQL_GET_SAMPLE_IDS % ('2005-01-01', '2005-01-31') )
        
        rows = result.fetchall()
    
        gards_sample_result   = []
        file_product_result   = []
        fp_description_result = []
    
        cpt = 1
        for row in rows:
            result = self._input_conn.execute(SQL_GET_GARDS_SAMPLE_DATA_PER_SID % (row[0]))
            for r in result:
                d = [0, {}]
                for col in input_gards_sample_data.columns:
                    if col.name == "sample_id":
                        d[0] = r[col]
                    d[1][col] = r[col]
                gards_sample_result.append(d) 
            cpt += 1      
        else:
            if cpt == 1:
                print "no rows in results for GARDS_SAMPLE_DATA_REQ\n"
        
        print("Get file product info \n")
        
        cpt = 1
        for row in rows:
            result = self._input_conn.execute(SQL_GET_FILEPRODUCT_PER_CHANID % (row[0]))
            for r in result:
                #first elem is chan, second is typeid
                d = [0, 0, {}]
                for col in input_file_product.columns:
                    if col.name == "chan":
                        d[0] = r[col]
                    if col.name == "typeid":
                        d[1] = r[col]
                    d[2][col] = r[col]
                file_product_result.append(d) 
            cpt += 1      
        else:
            if cpt == 1:
                print "no rows in results for FILEPRODUCT\n"
        
        
        print("Get fpdescription info \n")
        
        result = self._input_conn.execute(SQL_GET_FPDESCRIPTION_CONTENT)
        for r in result:
            #first elem is chan, second is typeid
            d = [0, {}]
            for col in input_fp_description.columns:
                if col.name == "typeid":
                    d[0] = r[col]
                d[1][col] = r[col]
            fp_description_result.append(d) 
                 
        #sqlite_engine  = sqlalchemy.create_engine('sqlite:////tmp/db.db')
        #sqlite_conn   = sqlite_engine.connect()
        #sqlite_conn.execute("ATTACH DATABASE '/tmp/idcx.db' as IDCX")
        #sqlite_conn.execute("ATTACH DATABASE '/tmp/rmsauto.db' as RMSAUTO")
        
        
        output_meta = sqlalchemy.MetaData()
        #first bind it to the input to discover the tables structures
        output_meta.bind = self._input_engine
        
        print("Discover Table structures on Archive")
        
        # autoload tables
        sqlalchemy.Table('GARDS_SAMPLE_DATA',  output_meta, schema='RMSAUTO', autoload=True)
        fileproduct         = sqlalchemy.Table('FILEPRODUCT', output_meta, schema='IDCX', autoload=True)
        sqlalchemy.Table('FPDESCRIPTION',  output_meta, schema= 'IDCX', autoload=True)
        
        #then bind it to the output engine to create delete and populate tables
        output_meta.bind = self._output_engine
        
        #change fileproduct columns to have the right float number
        fileproduct.c.time    = sqlalchemy.Column('TIME', sqlalchemy.FLOAT(38))
        fileproduct.c.endtime = sqlalchemy.Column('ENDTIME', sqlalchemy.FLOAT(38))
        fileproduct.c.version = sqlalchemy.Column('VERSION', sqlalchemy.FLOAT(38))
        
        #delete tables if necessary
        if a_has_to_drop_tables == True:
            print("Will drop all the tables in the output database\n")
            for table in reversed(output_meta.sorted_tables):
                print("Delete Table %s\n" % (table.name) )
                self._output_engine.execute(table.delete())
        
        print("Create Table structures on output DB if they do not exist\n")
        
        output_meta.create_all()
        
        output_gards_sample_data    = sqlalchemy.Table('GARDS_SAMPLE_DATA', output_meta,  schema='RMSAUTO', autoload=True)
        output_file_product         = sqlalchemy.Table('FILEPRODUCT',      output_meta, schema='IDCX',    autoload=True)
        output_fpdescription        = sqlalchemy.Table('FPDESCRIPTION',    output_meta, schema= 'IDCX', autoload=True)
        
        print("Import GARDS_SAMPLE_DATA if not already there")
        
        for elem in gards_sample_result:
            result = self._output_conn.execute(output_gards_sample_data.select(output_gards_sample_data.c.sample_id == elem[0]))
            
            rows = result.fetchall()
            
            if len(rows) == 0:
                self._output_conn.execute(output_gards_sample_data.insert().values(elem[1]))
        
        print("Import FP_DESCRIPTION if not already there")
        
        for elem in fp_description_result:
            result = self._output_conn.execute(output_fpdescription.select(output_fpdescription.c.typeid == elem[0]))
            
            rows = result.fetchall()
            
            if len(rows) == 0:
                self._output_conn.execute(output_fpdescription.insert().values(elem[1]))
        
        print("Import FILEPRODUCT DATA if not already there\n")
        
        for elem in file_product_result:
            
            result = self._output_conn.execute(output_file_product.select( \
                                              (output_file_product.c.chan == elem[0]) & (output_file_product.c.typeid == elem[1]) ))
            
            rows = result.fetchall()
            
            if len(rows) == 0:
                self._output_conn.execute(output_file_product.insert().values(elem[2]))
                            
def main():
    
    archive_db = 'oracle://centre:data@moorea.ctbto.org'
    idcdev_db  = 'oracle://centre:data@idcdev.ctbto.org'
    
    extractor = ArchiveExctractor(a_input_url=idcdev_db, a_output_url='oracle://system:oracle@127.0.0.1')
    
    extractor.copy_from_rn_archive_database(a_has_to_drop_tables = True)
    
    
   
    
if __name__ == "__main__":
    

    main()
