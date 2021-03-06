""" sql requests to be optimized """
 
""" These two requests are slow because no indexes are used on GARDS_SAMPLE_STATUS """
SQL_GETPARTICULATE_BK_SAMPLEID_old = "select * from \
(select gd.sample_id from gards_sample_data gd, gards_sample_status gs \
where detector_id=%s and gd.sample_id = gs.sample_id and data_type='D' and Spectral_qualifier='FULL' and gs.status in ('V','P') and gd.acquisition_stop <= to_date('%s','YYYY-MM-DD HH24:MI:SS')\
order by gd.acquisition_start DESC)\
where rownum=1"
 
SQL_GETPARTICULATE_QC_SAMPLEID_old = "select * from \
(select gd.sample_id from rmsman.gards_sample_data gd, rmsman.gards_sample_status gs \
where detector_id=%s and gd.sample_id = gs.sample_id and data_type='Q' and Spectral_qualifier='FULL' \
and gs.status in ('V','P') and gd.acquisition_stop <= to_date('%s','YYYY-MM-DD HH24:MI:SS') order by gd.sample_id DESC) \
where rownum=1"
   
""" No index in GARDS_SAMPLE_AUX on sample_ref_id. This would be very beneficial. In the mean time trick using the Collection_date """
SQL_GETPARTICULATE_PREL_SAMPLEIDS_old = "select gsd.sample_id from GARDS_SAMPLE_AUX gsx,GARDS_SAMPLE_DATA gsd where gsd.sample_id=gsx.sample_id and gsx.sample_ref_id='%s' and gsd.Spectral_qualifier='PREL'"
 
""" There is no index on chan in moorea. It would be very benefical to have it. No solutions regarding that """
SQL_GETPARTICULATE_SPECTRUM_old = "select prod.dir, prod.DFIle,fp.prodtype,prod.FOFF,prod.DSIZE from idcx.FILEPRODUCT prod,idcx.FPDESCRIPTIoN fp where fp.typeid=29 and prod.chan='%s' and prod.typeID= fp.typeID and sta='%s'"
 
""" Forced to use between operator to trigger the use of the index. Because on maui if < is used the index is not used. If > is used it works. """
# beware with the date trick. In order to use the index and not perform a full scan on the table use between superior newest date and 1980-xxxxx
# to do the same as gsd.collect_stop < to_date(XXXXX) because in this case the index is not used
SQL_PARTICULATE_GET_MRP_old = "select gsd.sample_id as mrp_sample_id, to_char (gsd.collect_stop, 'YYYY-MM-DD HH24:MI:SS') as mrp_collect_stop, gsd.collect_stop - to_date('%s', 'YYYY-MM-DD HH24:MI:SS') as mrp_collect_stop_diff from gards_sample_data gsd \
where gsd.collect_stop between to_date ('%s','YYYY-MM-DD HH24:MI:SS')-1 and to_date ('1980-01-01','YYYY-MM-DD HH24:MI:SS')\
and gsd.data_type = '%s' \
and gsd.detector_id = %s \
and gsd.sample_type = '%s' \
and gsd.spectral_qualifier = 'FULL' \
order by collect_stop desc"
 
# OLD
SQL_SAUNA_GET_ROI_CONCS_OLD = "select ROI,CONC,CONC_ERR,MDC,NID_FLAG,LC,LD from gards_BG_ROI_CONCS where sample_id=%s"
 
SQL_SAUNA_GET_ROI_COUNTS_OLD = "select ROI,GROSS, GROSS_ERR, GAS_BKGND_GROSS, GAS_BKGND_COUNT, GAS_BKGND_COUNT_ERR, DET_BKGND_COUNT, DET_BKGND_COUNT_ERR, NET_COUNT, NET_COUNT_ERR, CRITICAL_LEV_SAMP, CRITICAL_LEV_GAS from gards_BG_ROI_counts where sample_id=%s"
 
SQL_GET_SAUNA_DETBK_SAMPLEID_OLD = "select * from \
(select gd.sample_id from gards_sample_data gd, rmsauto.gards_sample_status gs \
where gd.station_id=%s \
and gd.DETECTOR_ID=%s \
and gd.SPECTRAL_QUALIFIER='FULL' \
and gd.data_type='D' \
and gd.acquisition_start <= (select acquisition_start from gards_sample_data where SAMPLE_ID=%s and station_id=%s \
and detector_id=%s) \
and gd.sample_id = gs.sample_id \
and gs.status in ('V','P')) \
where rownum=1"
 
SQL_GET_SAUNA_GASBK_SAMPLEID_OLD = "select * from \
(select gd.sample_id from gards_sample_data gd, gards_sample_status gs \
where gd.station_id=%s \
and gd.DETECTOR_ID=%s \
and gd.SPECTRAL_QUALIFIER='FULL' \
and gd.data_type='G' \
and gd.acquisition_start <= (select acquisition_start from gards_sample_data where SAMPLE_ID=%s and station_id=%s \
and detector_id=%s) \
and gd.sample_id = gs.sample_id \
and gs.status in ('V','P')) \
where rownum=1"
 
SQL_GET_SAUNA_QC_SAMPLEID_OLD = "select * from \
(select gd.sample_id from gards_sample_data gd, gards_sample_status gs \
where gd.station_id=%s \
and gd.DETECTOR_ID=%s \
and gd.SPECTRAL_QUALIFIER='FULL' \
and gd.data_type='Q' \
and gd.acquisition_start <= (select acquisition_start from gards_sample_data where SAMPLE_ID=%s and station_id=%s \
and detector_id=%s) \
and gd.sample_id = gs.sample_id \
and gs.status in ('V','P')) \
where rownum=1"
 
""" ************************************ Common Part ********************************************"""
 
""" sql used requests """
SQL_GETDETECTORINFO = "select det.detector_id as detector_id, det.detector_code as detector_code, det.description as detector_description, det.type as detector_type from RMSMAN.GARDS_DETECTORS det, RMSAUTO.GARDS_SAMPLE_DATA data where data.sample_id=%s and data.DETECTOR_ID=det.DETECTOR_ID"
SQL_GETSTATIONINFO = "select sta.station_id as station_id, sta.station_code as station_code, sta.country_code as station_country_code, sta.type as station_type, sta.description as station_location,to_char(sta.lat)||' '||to_char(sta.lon)||' '||to_char(sta.elevation) as station_coordinates from RMSMAN.GARDS_STATIONS sta, RMSAUTO.GARDS_SAMPLE_DATA data where data.sample_id=%s and sta.STATION_ID=data.STATION_ID"
SQL_GET_SAMPLE_TYPE = "select sta.type as sample_type from RMSMAN.GARDS_STATIONS sta, RMSAUTO.GARDS_SAMPLE_DATA data where data.sample_id=%s and sta.STATION_ID=data.STATION_ID"
 
 
SQL_GETSAMPLEINFO = "select input_file_name as spectrum_filepath, data_type as data_data_type, geometry as data_sample_geometry, \
spectral_qualifier as data_spectral_qualifier, quantity as data_sample_quantity, transmit_dtg as data_transmit_dtg , \
collect_start as data_collect_start, collect_stop as data_collect_stop, acquisition_start as data_acq_start, \
acquisition_stop as data_acq_stop, acquisition_live_sec as data_acq_live_sec, acquisition_real_sec as data_acq_real_sec, \
quantity/(86400*(collect_stop - collect_start )/3600) as data_flow_rate from RMSAUTO.GARDS_SAMPLE_DATA where sample_id=%s"
  
""" ************************************ Noble Gaz Part ******************************************** """
  
# SPALAX is more like particulates. The same method is used for the spectroscopic analysis
SQL_SPALAX_GET_SPECTRUM = "select prod.dir, prod.DFIle,fp.prodtype,prod.FOFF,prod.DSIZE from idcx.FILEPRODUCT prod,idcx.FPDESCRIPTIoN fp where fp.typeid=29 and prod.chan='%s' and prod.typeID= fp.typeID and sta='%s'"
SQL_SPALAX_GET_RAW_SPECTRUM = "select prod.dir, prod.DFIle,fp.prodtype,prod.FOFF,prod.DSIZE from idcx.FILEPRODUCT prod,idcx.FPDESCRIPTIoN fp where fp.PRODTYPE='%s' and prod.chan='%s' and prod.typeID= fp.typeID and sta='%s'"
   
SQL_SPALAX_GET_DETBK_SAMPLEID = "select * from \
(select gd.sample_id from rmsauto.gards_sample_data gd, rmsauto.gards_sample_status gs \
where gd.station_id=%s and gd.DETECTOR_ID=%s \
and gd.SPECTRAL_QUALIFIER='FULL' and gd.data_type='D' \
and gd.acquisition_start <= (select acquisition_start from rmsauto.gards_sample_data where SAMPLE_ID=%s and station_id=%s and detector_id=%s) \
and gd.sample_id = gs.sample_id and gs.status in ('V','P') order by sample_id desc \
) \
where rownum = 1"
                                  
 
SQL_SPALAX_GET_PREL_SAMPLEIDS = "select sample_id from rmsauto.gards_sample_data \
where COLLECT_STOP=\
(select COLLECT_STOP from rmsauto.gards_sample_data where sample_id=%s)\
and detector_id=%s\
and Spectral_qualifier='PREL'\
order by ACQUISITION_REAL_SEC asc"
 
                                   
SQL_SPALAX_GET_QC_SAMPLEID = "select * from \
(select gd.sample_id from rmsauto.gards_sample_data gd, rmsauto.gards_sample_status gs \
where gd.station_id=%s and gd.DETECTOR_ID=%s \
and gd.SPECTRAL_QUALIFIER='FULL' and gd.data_type='Q' \
and gd.acquisition_start <= (select acquisition_start from rmsauto.gards_sample_data where SAMPLE_ID=%s and station_id=%s and detector_id=%s) \
and gd.sample_id = gs.sample_id and gs.status in ('V','P') order by sample_id desc \
) \
where rownum = 1"
   
SQL_SPALAX_GET_XE_RESULTS = "select METHOD_ID,NUCLIDE_ID,CONC,CONC_ERR,MDC,MDI,NID_FLAG,LC,LD,SAMPLE_ACT,COV_XE_131M,COV_XE_133M,COV_XE_133,COV_XE_135,COV_RADON from RMSAUTO.GARDS_XE_RESULTS where sample_id=%s"
 
SQL_SPALAX_GET_XE_REF_LINES = "select * from RMSAUTO.GARDS_XE_REFLINE_MASTER order by refpeak_energy"
 
SQL_SPALAX_GET_ENERGY_CAL = "select * from RMSAUTO.GARDS_ENERGY_CAL where sample_id=%s"

SQL_SPALAX_GET_ENERGY_CAL_WINNER = "select * from RMSAUTO.GARDS_ENERGY_CAL where sample_id=%s and winner='Y'"
 
SQL_SPALAX_GET_RESOLUTION_CAL = "select * from RMSAUTO.GARDS_RESOLUTION_CAL where sample_id=%s"

SQL_SPALAX_GET_RESOLUTION_CAL_WINNER = "select * from RMSAUTO.GARDS_RESOLUTION_CAL where sample_id=%s and winner='Y'"
 
SQL_SPALAX_GET_EFFICIENCY_CAL = "select * from RMSAUTO.GARDS_EFFICIENCY_CAL where sample_id=%s"
 
SQL_SPALAX_GET_DATA_QUALITY_FLAGS = "select gflags.flag_id as dq_flag_id, result as dq_result, value as dq_value, name as dq_name, threshold as dq_threshold, units as dq_units, test as dq_test from RMSAUTO.GARDS_SAMPLE_FLAGS sflags,RMSMAN.GARDS_FLAGS gflags where sample_id=%s and sflags.FLAG_ID = gflags.FLAG_ID"
 
SQL_SPALAX_GET_QC_FLAGS = "select TEST_NAME,FLAG,QC_COMMENT from RMSAUTO.GARDS_QC_RESULTS where sample_id=%s"
 
SQL_SPALAX_GET_PROCESSING_PARAMETERS = "select NAME,VALUE from RMSAUTO.GARDS_SAINT_PROCESS_PARAMS where sample_id=%s"
 
SQL_GET_AUTOSAINT_DEFAULT_PARAMS = "select NAME,VALUE from RMSAUTO.GARDS_SAINT_DEFAULT_PARAMS"
 
""" ************************************ Sauna Part ************************************************ """
""" get SAUNA Sample files : beta and gamma spectrum plus histogram. parameters station and sampleid """
SQL_SAUNA_GET_FILES = "select prod.dir, prod.DFIle,fp.prodtype,prod.FOFF,prod.DSIZE from idcx.FILEPRODUCT prod,idcx.FPDESCRIPTIoN fp where fp.typeid in (30, 29, 34, 8, 12, 13, 20) and prod.chan='%s' and prod.typeID= fp.typeID and sta='%s'"
SQL_SAUNA_GET_RAW_FILE = "select prod.dir, prod.DFIle,fp.prodtype,prod.FOFF,prod.DSIZE from idcx.FILEPRODUCT prod,idcx.FPDESCRIPTIoN fp where fp.PRODTYPE='%s' and prod.chan='%s' and prod.typeID= fp.typeID and sta='%s'"
SQL_SAUNA_GET_HISTOGRAM_INFO = "select G_CHANNELS, B_CHANNELS, G_ENERGY_SPAN, B_ENERGY_SPAN from RMSAUTO.gards_histogram where sample_id=%s"
 
""" Get information regarding all identified nuclides """
SQL_SAUNA_GET_IDENTIFIED_NUCLIDES = "select lib.NAME as NAME, lib.HALFLIFE as halflife, lib.type as type, conc.conc as conc, conc.conc_err as conc_err, conc.MDC as MDC, conc.LC as LC, conc.LD as LD, conc.NID_FLAG as NID_FLAG from RMSAUTO.GARDS_BG_ISOTOPE_CONCS conc, RMSMAN.GARDS_XE_NUCL_LIB lib where sample_id=%s and conc.NUCLIDE_ID=lib.NUCLIDE_ID"
  
SQL_SAUNA_GET_NUCLIDE_FOR_ROI ="select lib.name, p.roi from gards_bg_proc_params_roi p, GARDS_XE_NUCL_LIB lib where p.sample_id=%s and p.nuclide_id=lib.nuclide_id order by roi"
 
SQL_SAUNA_GET_ROI_INFO = "select c.roi as ROI,c.GROSS as GROSS, c.GROSS_ERR as GROSS_ERR, c.GAS_BKGND_GROSS as GAS_BKGND_GROSS,\
c.GAS_BKGND_COUNT as GAS_BKGND_COUNT, c.GAS_BKGND_COUNT_ERR as GAS_BKGND_COUNT_ERR, c.DET_BKGND_COUNT as DET_BKGND_COUNT,\
c.DET_BKGND_COUNT_ERR as DET_BKGND_COUNT_ERR,c.NET_COUNT as NET_COUNT, c.NET_COUNT_ERR as NET_COUNT_ERR, c.CRITICAL_LEV_SAMP as CRITICAL_LEV_SAMP,\
c.CRITICAL_LEV_GAS as CRITICAL_LEV_GAS,conc.CONC as CONC, conc.CONC_ERR as CONC_ERR, conc.MDC as MDC,\
conc.NID_FLAG as NID_FLAG, conc.LC as LC, conc.LD as LD from gards_BG_ROI_counts c, gards_BG_ROI_CONCS conc \
where c.sample_id=%s and c.sample_id = conc.sample_id and c.roi = conc.roi order by c.roi"
 
SQL_SAUNA_GET_ROI_EFFICIENCY = "select ROI, BG_EFFICIENCY, BG_EFFIC_ERROR from GARDS_BG_EFFICIENCY_PAIRS where sample_id=%s"
 
SQL_SAUNA_GET_ROI_BOUNDARIES = "select roi,B_ENERGY_START,B_ENERGY_STOP,G_ENERGY_START, G_ENERGY_STOP from GARDS_ROI_LIMITS where sample_id=%s order by roi"
 
SQL_SAUNA_GET_PROCESSING_PARAMS = "select * from gards_bg_proc_params where sample_id=%s"
 
SQL_SAUNA_GET_ROI_PARAMS = "select * from gards_bg_proc_params_roi where sample_id=%s"
 
# Get information regarding all nuclides
SQL_SAUNA_GETALLNUCLIDES = "select conc.conc as conc, conc.conc_err as conc_err, conc.MDC as MDC, conc.LC as LC, conc.LD as LD, lib.NAME as Name, lib.type as Type, lib.HALFLIFE as halflife from RMSAUTO.GARDS_BG_ISOTOPE_CONCS conc, RMSMAN.GARDS_XE_NUCL_LIB lib where sample_id=%s and conc.NUCLIDE_ID=lib.NUCLIDE_ID"
 
 
SQL_GET_SAUNA_AUX_DETBK_ID = "SELECT aux.bkgd_measurement_id as mid FROM \
rmsauto.gards_sample_data sam, rmsauto.gards_sample_aux aux \
WHERE sam.sample_id = %s AND sam.sample_id = aux.sample_id"
                                    
SQL_GET_SAUNA_DETBK_SAMPLEID_FROM_MID = "SELECT sam.sample_id as sid FROM \
rmsauto.gards_sample_aux aux, rmsauto.gards_sample_data sam WHERE \
aux.measurement_id = '%s' and aux.sample_id = sam.sample_id and \
sam.data_type = 'D' and sam.spectral_qualifier = 'FULL'"
                                               
SQL_GET_SAUNA_MRP_DETBK_SAMPLEID = "select * from \
(select gd.sample_id from rmsauto.gards_sample_data gd, rmsauto.gards_sample_status gs \
where gd.station_id=%s and gd.DETECTOR_ID=%s and gd.SPECTRAL_QUALIFIER='FULL' and gd.data_type='D' \
and gd.acquisition_start <= (select acquisition_start from rmsauto.gards_sample_data where SAMPLE_ID=%s and station_id=%s \
and detector_id=%s) and gd.sample_id = gs.sample_id and gs.status in ('V','P') order by sample_id desc) \
where rownum = 1"
 
SQL_GET_SAUNA_AUX_GASBK_ID = "SELECT aux.GAS_BKGD_MEASUREMENT_ID as mid FROM \
rmsauto.gards_sample_data sam, rmsauto.gards_sample_aux aux \
WHERE sam.sample_id = %s AND sam.sample_id = aux.sample_id"
                                    
SQL_GET_SAUNA_GASBK_SAMPLEID_FROM_MID = "SELECT sam.sample_id as sid FROM \
rmsauto.gards_sample_aux aux, rmsauto.gards_sample_data sam WHERE \
aux.measurement_id = '%s' and aux.sample_id = sam.sample_id and \
sam.data_type = 'G' and sam.spectral_qualifier = 'FULL'"
 
SQL_GET_SAUNA_MRP_GASBK_SAMPLEID = "select * from \
(select gd.sample_id from rmsauto.gards_sample_data gd, rmsauto.gards_sample_status gs \
where gd.station_id=%s and gd.DETECTOR_ID=%s and gd.SPECTRAL_QUALIFIER='FULL' and gd.data_type='G' \
and gd.acquisition_start <= (select acquisition_start from rmsauto.gards_sample_data where SAMPLE_ID=%s and station_id=%s \
and detector_id=%s) and gd.sample_id = gs.sample_id and gs.status in ('V','P') order by sample_id desc) \
where rownum = 1"
 
SQL_GET_SAUNA_PREL_SAMPLEIDS = "select sample_id from rmsauto.gards_sample_data \
where COLLECT_STOP=\
(select COLLECT_STOP from rmsauto.gards_sample_data where sample_id=%s)\
and detector_id=%s\
and Spectral_qualifier='PREL'\
order by ACQUISITION_REAL_SEC asc"
 
# give the latest QC mesured
# this method is inherited from the particulates part
SQL_GET_SAUNA_QC_SAMPLEID = "select * from \
(select gd.sample_id from rmsauto.gards_sample_data gd, rmsauto.gards_sample_status gs \
where gd.station_id=%s and gd.DETECTOR_ID=%s and gd.SPECTRAL_QUALIFIER='FULL' and gd.data_type='Q' \
and gd.acquisition_start <= (select acquisition_start from rmsauto.gards_sample_data where SAMPLE_ID=%s and station_id=%s \
and detector_id=%s) and gd.sample_id = gs.sample_id and gs.status in ('V','P') order by sample_id desc) \
where rownum = 1"
 
#this method is inherited from bg analyse
# 7 parameters
SQL_GET_SAUNA_QC_SAMPLEID_BG_ANALYSE = "SELECT sample_id FROM rmsauto.gards_sample_data WHERE \
station_id = %s AND detector_id = %s AND \
acquisition_start = \
(SELECT MAX(acquisition_start) FROM \
rmsauto.gards_sample_data \
WHERE station_id = %s AND detector_id = %s AND \
acquisition_start < (SELECT acquisition_start FROM rmsauto.gards_sample_data \
WHERE SAMPLE_ID=%s and station_id=%s and detector_id=%s) AND data_type = 'Q' AND spectral_qualifier = 'FULL')"
 
SQL_GET_SAUNA_PREL_SAMPLEIDS = "select sample_id from rmsauto.gards_sample_data \
where COLLECT_STOP=\
(select COLLECT_STOP from rmsauto.gards_sample_data where sample_id=%s)\
and detector_id=%s\
and Spectral_qualifier='PREL'\
order by ACQUISITION_REAL_SEC asc"
                                    
SQL_GET_AUX_SAMPLE_INFO = "select * from GARDS_SAMPLE_AUX where sample_id=%s"
 
SQL_GET_SAUNA_ENERGY_CAL = "select * from GARDS_BG_ENERGY_CAL where sample_id=%s"
 
SQL_GET_NOBLEGAS_XE_NUCL_LIB = "select NAME from GARDS_XE_NUCL_LIB"
 
SQL_GET_NOBLEGAS_XE_NUCL_LINES_LIB = "select NAME,ENERGY,ENERGY_ERR,ABUNDANCE,ABUNDANCE_ERR,KEY_FLAG,NUCLIDE_ID from GARDS_XE_NUCL_LINES_LIB order by NUCLIDE_ID"
 
""" ************************************* Particulate Part ********************************************* """
 
# get any spectrum full or prel or qc or back
SQL_GETPARTICULATE_SPECTRUM = "select prod.dir, prod.DFIle,fp.prodtype,prod.FOFF,prod.DSIZE from idcx.FILEPRODUCT prod,idcx.FPDESCRIPTIoN fp where fp.typeid=29 and prod.chan='%s' and prod.typeID= fp.typeID and sta='%s'"
 
SQL_GETPARTICULATE_RAW_SPECTRUM = "select prod.dir, prod.DFIle,fp.prodtype,prod.FOFF,prod.DSIZE from idcx.FILEPRODUCT prod,idcx.FPDESCRIPTIoN fp where fp.PRODTYPE='%s' and prod.chan='%s' and prod.typeID= fp.typeID and sta='%s'"
 
 
 
                                    
SQL_GETPARTICULATE_BK_SAMPLEID = "select * from \
(select gd.sample_id from rmsauto.gards_sample_data gd, rmsauto.gards_sample_status gs \
where gd.station_id=%s \
and gd.DETECTOR_ID=%s \
and gd.SPECTRAL_QUALIFIER='FULL' \
and gd.data_type='D' \
and gd.acquisition_start <= (select acquisition_start from rmsauto.gards_sample_data where SAMPLE_ID=%s and station_id=%s \
and detector_id=%s) \
and gd.sample_id = gs.sample_id \
and gs.status in ('V','P')) \
where rownum=1"
                                  
 
SQL_GETPARTICULATE_PREL_SAMPLEIDS = "select sample_id from rmsauto.gards_sample_data \
where COLLECT_STOP=\
(select COLLECT_STOP from rmsauto.gards_sample_data where sample_id=%s)\
and detector_id=%s\
and Spectral_qualifier='PREL'\
order by ACQUISITION_REAL_SEC asc"
 
                                   
SQL_GETPARTICULATE_QC_SAMPLEID = "select * from \
(select gd.sample_id from rmsauto.gards_sample_data gd, rmsauto.gards_sample_status gs \
where gd.station_id=%s \
and gd.DETECTOR_ID=%s \
and gd.SPECTRAL_QUALIFIER='FULL' \
and gd.data_type='Q' \
and gd.acquisition_start <= (select acquisition_start from rmsauto.gards_sample_data where SAMPLE_ID=%s and station_id=%s \
and detector_id=%s) \
and gd.sample_id = gs.sample_id \
and gs.status in ('V','P')) \
where rownum=1"
 
# get particulate category
SQL_PARTICULATE_CATEGORY_STATUS ="select entry_date as cat_entry_date, cnf_begin_date as cat_cnf_begin_date,cnf_end_date as cat_cnf_end_date, review_date as cat_review_date, review_time as cat_review_time, analyst as cat_analyst, status as cat_status, category as cat_category, auto_category as cat_auto_category, release_date as cat_release_date from RMSAUTO.GARDS_SAMPLE_STATUS where sample_id=%s"
 
SQL_PARTICULATE_CATEGORY ="select NAME as CAT_NUCL_NAME, METHOD_ID as CAT_METHOD_ID, CATEGORY as CAT_CATEGORY, UPPER_BOUND as CAT_UPPER_BOUND, LOWER_BOUND as CAT_LOWER_BOUND, CENTRAL_VALUE as CAT_CENTRAL_VALUE, DELTA as CAT_DELTA, ACTIVITY as CAT_ACTIVITY from RMSAUTO.GARDS_SAMPLE_CAT where sample_id=%s and hold=0"
 
# returned all ided nuclides for a particular sample """
SQL_PARTICULATE_GET_NUCL2QUANTIFY="select name from RMSMAN.GARDS_NUCL2QUANTIFY"
 
# return sample_ref_id. Identifier given by the detector for the sample. It is unique """
SQL_PARTICULATE_GET_SAMPLE_REF_ID="select sample_ref_id from RMSAUTO.GARDS_SAMPLE_AUX where sample_id=%s"
 
SQL_PARTICULATE_GET_NUCLIDES_INFO="select * from RMSAUTO.GARDS_NUCL_IDED ided where sample_id=%s"
 
SQL_PARTICULATE_GET_NUCLIDE_LINES_INFO="select * from RMSAUTO.GARDS_NUCL_LINES_IDED where sample_id=%s"
 
SQL_PARTICULATE_GET_PEAKS = "select * from RMSAUTO.GARDS_PEAKS where sample_id=%s"
 
SQL_PARTICULATE_GET_PROCESSING_PARAMETERS = "select * from RMSAUTO.GARDS_SAMPLE_PROC_PARAMS where sample_id=%s"
 
SQL_PARTICULATE_GET_UPDATE_PARAMETERS = "select * from RMSAUTO.GARDS_SAMPLE_UPDATE_PARAMS where sample_id=%s"
 
# beware with the date trick. In order to use the index and not perform a full scan on the table use between superior newest date and 1980-xx
""" to do the same as gsd.collect_stop < to_date(XXXXX) because in this case the index is not used """
SQL_PARTICULATE_GET_MRP = "select gsd.sample_id as mrp_sample_id, to_char (gsd.collect_stop, 'YYYY-MM-DD HH24:MI:SS') as mrp_collect_stop, gsd.collect_stop - to_date('%s', 'YYYY-MM-DD HH24:MI:SS') as mrp_collect_stop_diff from gards_sample_data gsd \
where gsd.collect_stop between to_date ('%s','YYYY-MM-DD HH24:MI:SS')-1 and to_date ('1980-01-01','YYYY-MM-DD HH24:MI:SS')\
and gsd.data_type = '%s' \
and gsd.detector_id = %s \
and gsd.sample_type = '%s' \
and gsd.spectral_qualifier = 'FULL' \
order by collect_stop desc"
 
SQL_PARTICULATE_GET_DATA_QUALITY_FLAGS = "select gflags.flag_id as dq_flag_id, result as dq_result, value as dq_value, name as dq_name, threshold as dq_threshold, units as dq_units, test as dq_test from RMSAUTO.GARDS_SAMPLE_FLAGS sflags,RMSAUTO.GARDS_FLAGS gflags where sample_id=%s and sflags.FLAG_ID = gflags.FLAG_ID"
 
SQL_PARTICULATE_GET_ENERGY_CAL = "select * from RMSAUTO.GARDS_ENERGY_CAL where sample_id=%s"
 
SQL_PARTICULATE_GET_RESOLUTION_CAL = "select * from RMSAUTO.GARDS_RESOLUTION_CAL where sample_id=%s"
 
SQL_PARTICULATE_GET_EFFICIENCY_CAL = "select * from RMSAUTO.GARDS_EFFICIENCY_CAL where sample_id=%s"
 