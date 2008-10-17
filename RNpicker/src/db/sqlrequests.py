
""" sql requests """
SQL_GETDETECTORINFO   = "select det.detector_id as detector_id, det.detector_code as detector_code, det.description as detector_description, det.type as detector_type from RMSMAN.GARDS_DETECTORS det, RMSMAN.GARDS_SAMPLE_DATA data where data.sample_id=%s and data.DETECTOR_ID=det.DETECTOR_ID"
SQL_GETSTATIONINFO    = "select sta.station_code as station_code, sta.country_code as station_country_code, sta.type as station_type, sta.description as station_location,to_char(sta.lat)||' '||to_char(sta.lon)||' '||to_char(sta.elevation) as station_coordinates from RMSMAN.GARDS_STATIONS sta, RMSMAN.GARDS_SAMPLE_DATA data where data.sample_id=%s and sta.STATION_ID=data.STATION_ID"
SQL_GETSAMPLETYPE     = "select sta.type as sample_type from RMSMAN.GARDS_STATIONS sta, RMSMAN.GARDS_SAMPLE_DATA data where data.sample_id=%s and sta.STATION_ID=data.STATION_ID"


SQL_GETSAMPLEINFO     = "select sample_id as sample_id, input_file_name as spectrum_filepath, data_type as data_data_type, geometry as data_sample_geometry, \
                                spectral_qualifier as data_spectral_qualifier, quantity as data_sample_quantity, transmit_dtg as data_transmit_dtg , \
                                collect_start as data_collect_start, collect_stop as data_collect_stop, acquisition_start as data_acq_start, \
                                acquisition_stop as data_acq_stop, acquisition_live_sec as data_acq_live_sec, acquisition_real_sec as data_acq_real_sec \
                                from RMSMAN.GARDS_SAMPLE_DATA where sample_id=%s"
                                
""" get SAUNA Sample files : beta and gamma spectrum plus histogram. parameters station and sampleid """
SQL_GETSAUNA_FILES    = "select prod.dir, prod.DFIle,fp.prodtype from idcx.FILEPRODUCT prod,idcx.FPDESCRIPTIoN fp where (fp.typeid=30 or fp.typeid=29 or fp.typeid=34) and prod.chan='%s' and prod.typeID= fp.typeID and sta='%s'"

""" get any spectrum full or prel or qc or back """
SQL_GETPARTICULATE_SPECTRUM      = "select prod.dir, prod.DFIle,fp.prodtype,prod.FOFF,prod.DSIZE from FILEPRODUCT prod,FPDESCRIPTIoN fp where fp.typeid=29 and prod.chan='%s' and prod.typeID= fp.typeID and sta='%s'"
#SQL_GETPARTICULATE_SPECTRUM      = "select prod.dir, prod.DFIle,fp.prodtype from FILEPRODUCT prod,FPDESCRIPTIoN fp where (fp.typeid=29 or fp.typeid=13) and prod.chan='%s' and prod.typeID= fp.typeID and sta='%s'"

SQL_GETPARTICULATE_BK_SAMPLEID   = "select gd.sample_id from gards_sample_data gd, gards_sample_status gs where detector_id=%s and gd.sample_id = gs.sample_id and data_type='D' and Spectral_qualifier='FULL' and gs.status in ('V','P') order by gd.acquisition_start DESC"

SQL_GETPARTICULATE_PREL_SAMPLEIDS = "select gsd.sample_id from GARDS_SAMPLE_AUX gsx,GARDS_SAMPLE_DATA gsd where gsd.sample_id=gsx.sample_id and gsx.sample_ref_id='%s' and gsd.Spectral_qualifier='PREL'"

""" Should be dependant on the date as well otherwise we get the latest qc """
SQL_GETPARTICULATE_QC_SAMPLEID = "select gd.sample_id from gards_sample_data gd, gards_sample_status gs where rownum<=500 and detector_id=%s and gd.sample_id = gs.sample_id and data_type='Q' and Spectral_qualifier='FULL' and gs.status in ('V','P') order by gd.sample_id DESC"

""" Get information regarding all identified nuclides """
SQL_SAUNA_GETIDENTIFIEDNUCLIDES = "select conc.conc as conc, conc.conc_err as conc_err, conc.MDC as MDC, conc.LC as LC, conc.LD as LD, lib.NAME as Nuclide, lib.HALFLIFE as halflife from RMSMAN.GARDS_BG_ISOTOPE_CONCS conc, RMSMAN.GARDS_XE_NUCL_LIB lib where sample_id=%s and conc.NUCLIDE_ID=lib.NUCLIDE_ID and conc.NID_FLAG=1"

""" Get information regarding all nuclides """
SQL_SAUNA_GETALLNUCLIDES = "select conc.conc as conc, conc.conc_err as conc_err, conc.MDC as MDC, conc.LC as LC, conc.LD as LD, lib.NAME as Nuclide, lib.HALFLIFE as halflife from RMSMAN.GARDS_BG_ISOTOPE_CONCS conc, RMSMAN.GARDS_XE_NUCL_LIB lib where sample_id=%s and conc.NUCLIDE_ID=lib.NUCLIDE_ID"

""" get particulate category """
SQL_PARTICULATE_CATEGORY_STATUS ="select entry_date as cat_entry_date, cnf_begin_date as cat_cnf_begin_date,cnf_end_date as cat_cnf_end_date, review_date as cat_review_date, review_time as cat_review_time, analyst as cat_analyst, status as cat_status, category as cat_category, auto_category as cat_auto_category, release_date as cat_release_date from RMSMAN.GARDS_SAMPLE_STATUS where sample_id=%s"

SQL_PARTICULATE_CATEGORY ="select NAME as CAT_NUCL_NAME, METHOD_ID as CAT_METHOD_ID, CATEGORY as CAT_CATEGORY, UPPER_BOUND as CAT_UPPER_BOUND, LOWER_BOUND as CAT_LOWER_BOUND, CENTRAL_VALUE as CAT_CENTRAL_VALUE, DELTA as CAT_DELTA, ACTIVITY as CAT_ACTIVITY from RMSMAN.GARDS_SAMPLE_CAT where sample_id=%s and hold=0"

""" returned all ided nuclides for a particular sample """
SQL_PARTICULATE_GET_NUCL2QUANTIFY="select name from RMSMAN.GARDS_NUCL2QUANTIFY"

""" return sample_ref_id. Identifier given by the detector for the sample. It is unique """
SQL_PARTICULATE_GET_SAMPLE_REF_ID="select sample_ref_id from RMSMAN.GARDS_SAMPLE_AUX where sample_id=%s"

SQL_PARTICULATE_GET_NUCLIDES_INFO="select * from RMSMAN.GARDS_NUCL_IDED ided where sample_id=%s"

SQL_PARTICULATE_GET_NUCLIDE_LINES_INFO="select * from RMSMAN.GARDS_NUCL_IDED where sample_id=%s"

SQL_PARTICULATE_GET_PEAKS = "select * from RMSMAN.GARDS_PEAKS where sample_id=%s"

SQL_PARTICULATE_GET_PROCESSING_PARAMETERS = "select * from RMSMAN.GARDS_SAMPLE_PROC_PARAMS where sample_id=%s"

SQL_PARTICULATE_GET_UPDATE_PARAMETERS = "select * from RMSMAN.GARDS_SAMPLE_UPDATE_PARAMS where sample_id=%s"

# beware with the date trick. In order to use the index and not perform a full scan on the table use between superior newest date and 1980-xxxxx 
# to do the same as gsd.collect_stop < to_date(XXXXX) because in this case the index is not used
SQL_PARTICULATE_GET_MRP = "select gsd.sample_id as mrp_sample_id, to_char (gsd.collect_stop, 'YYYY-MM-DD HH24:MI:SS')  as mrp_collect_stop, gsd.collect_stop - to_date('%s', 'YYYY-MM-DD HH24:MI:SS') as mrp_collect_stop_diff from gards_sample_data gsd \
                           where gsd.collect_stop between to_date ('%s','YYYY-MM-DD HH24:MI:SS')-1 and  to_date ('1980-01-01','YYYY-MM-DD HH24:MI:SS')\
                             and gsd.data_type = '%s' \
                             and gsd.detector_id = %s \
                             and gsd.sample_type = '%s' \
                             and gsd.spectral_qualifier = 'FULL' \
                           order by collect_stop desc"

SQL_PARTICULATE_GET_DATA_QUALITY_FLAGS = "select gflags.flag_id as dq_flag_id, result as dq_result, value as dq_value, name as dq_name, threshold as dq_threshold, units as dq_units, test as dq_test from RMSMAN.GARDS_SAMPLE_FLAGS sflags,RMSMAN.GARDS_FLAGS gflags where sample_id=%s and sflags.FLAG_ID = gflags.FLAG_ID"

SQL_PARTICULATE_GET_ENERGY_CAL         = "select * from RMSMAN.GARDS_ENERGY_CAL where sample_id=%s"

SQL_PARTICULATE_GET_RESOLUTION_CAL     = "select * from RMSMAN.GARDS_RESOLUTION_CAL where sample_id=%s"

SQL_PARTICULATE_GET_EFFICIENCY_CAL     = "select * from RMSMAN.GARDS_EFFICIENCY_CAL where sample_id=%s"