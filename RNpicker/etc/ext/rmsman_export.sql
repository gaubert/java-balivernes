--------------------------------------------------------
--  File created - Friday-July-11-2008   
--------------------------------------------------------

--------------------------------------------------------
--  DDL for Table COPY_STATIONS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."COPY_STATIONS" 
   (	"STATION_ID" NUMBER, 
	"STATION_CODE" VARCHAR2(5), 
	"COUNTRY_CODE" VARCHAR2(2), 
	"TYPE" VARCHAR2(6), 
	"DESCRIPTION" VARCHAR2(40), 
	"LAT" NUMBER, 
	"LON" NUMBER, 
	"ELEVATION" NUMBER, 
	"DATE_BEGIN" DATE, 
	"DATE_END" DATE, 
	"STATUS" VARCHAR2(2), 
	"POCID" NUMBER, 
	"SPLIT_STATION" NUMBER, 
	"MODDATE" DATE
   ) ;
 
--------------------------------------------------------
--  DDL for Table CREATE$JAVA$LOB$TABLE
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."CREATE$JAVA$LOB$TABLE" 
   (	"NAME" VARCHAR2(700), 
	"LOB" BLOB, 
	"LOADTIME" DATE
   ) ;
 
--------------------------------------------------------
--  DDL for Table DEBUG
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."DEBUG" 
   (	"MESG" VARCHAR2(512)
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."DEBUG"."MESG" IS '#brief=debug#desc=Debug message#category=#ext=a51#na=#range=#unit=';
 
   COMMENT ON TABLE "RMSMAN"."DEBUG"  IS '#category=Automatic Processing#desc=Debugging.';
 
--------------------------------------------------------
--  DDL for Table FOO
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."FOO" 
   (	"GNASK" NUMBER(*,0)
   ) ;
 
--------------------------------------------------------
--  DDL for Table GARDS_AUX_LIB
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_AUX_LIB" 
   (	"NAME" VARCHAR2(8), 
	"BRANCH_RATIO" NUMBER, 
	"CHAIN_ID" NUMBER, 
	"CHAIN_POS" NUMBER, 
	"HALFLIFE_ACT" VARCHAR2(23), 
	"HALFLIFE_ACT_ERR" VARCHAR2(23), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_AUX_LIB"."NAME" IS '#brief=nuclide name #desc=Nuclide name.#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_AUX_LIB"."BRANCH_RATIO" IS '#brief=percentage of decays to given decay path#desc=percentage of decays to given decay path#category=#ext=g8.5#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_AUX_LIB"."CHAIN_ID" IS '#brief=decay chain index#desc=decay chain index#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_AUX_LIB"."CHAIN_POS" IS '#brief=position in decay chain#desc=Decay chain index.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_AUX_LIB"."HALFLIFE_ACT" IS '#brief=actual half-life#desc=actual half-life#category=#ext=a23#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_AUX_LIB"."HALFLIFE_ACT_ERR" IS '#brief=uncertainty of halflife_act#desc=Actual half-life.#category=#ext=a23#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_AUX_LIB"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_AUX_LIB"  IS '#category=Automatic Processing#desc=The gards_aux_lib table provides additional radionuclide information that is useful to the analyst and used in the parent-progeny calculation. ';
 
--------------------------------------------------------
--  DDL for Table GARDS_AUX_LINES_LIB
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_AUX_LINES_LIB" 
   (	"NAME" VARCHAR2(8), 
	"ENERGY" NUMBER, 
	"ABUNDANCE_ACT" NUMBER, 
	"ABUNDANCE_ACT_ERR" NUMBER, 
	"LINE_COMMENT" VARCHAR2(500), 
	"LINE_TYPE" VARCHAR2(8), 
	"REFERENCE" VARCHAR2(8), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_AUX_LINES_LIB"."NAME" IS '#brief=nuclide name #desc=Nuclide name.#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_AUX_LINES_LIB"."ENERGY" IS '#brief=line energy (keV)#desc=line energy (keV)#category=#ext=g8.5#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_AUX_LINES_LIB"."ABUNDANCE_ACT" IS '#brief=intensity of nuclear transition#desc=intensity of nuclear transition#category=#ext=g8.5#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_AUX_LINES_LIB"."ABUNDANCE_ACT_ERR" IS '#brief=uncertainty of abundance_act#desc=Intensity of nuclear transition.#category=#ext=g8.5#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_AUX_LINES_LIB"."LINE_COMMENT" IS '#brief=description of line properties#desc=description of line properties#category=#ext=a50#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_AUX_LINES_LIB"."LINE_TYPE" IS '#brief=type of radiation causing the line#desc=Description of line properties.#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_AUX_LINES_LIB"."REFERENCE" IS '#brief=reference for line properties#desc=reference for line properties#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_AUX_LINES_LIB"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_AUX_LINES_LIB"  IS '#category=Automatic Processing#desc=The gards_aux_lines_lib table provides additional radionuclide line information that is useful to the analyst and is used in the parent-progeny calculation.';
 
--------------------------------------------------------
--  DDL for Table GARDS_BASELINE
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_BASELINE" 
   (	"DETECTOR_ID" NUMBER, 
	"DATA_TYPE" CHAR(1), 
	"INDEX_NO" NUMBER, 
	"ENERGY_LOW" NUMBER, 
	"ENERGY_HIGH" NUMBER, 
	"MULT" NUMBER, 
	"NO_OF_LOOPS" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON TABLE "RMSMAN"."GARDS_BASELINE"  IS '#category=Automatic Processing#desc=gards baseline';
 
--------------------------------------------------------
--  DDL for Table GARDS_BG_CONFIG_PARAMS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_BG_CONFIG_PARAMS" 
   (	"DETECTOR_ID" NUMBER, 
	"LC_ABSCISSA" FLOAT(126), 
	"DEFAULT_METHOD" NUMBER, 
	"MIN_SAMPLE_AIR_FLOW" FLOAT(126), 
	"MIN_SAMPLE_VOLUME" FLOAT(126), 
	"MAX_COLLECTION_TIME" NUMBER, 
	"MAX_ACQUISITION_TIME" NUMBER, 
	"MAX_REPORTING_TIME" NUMBER, 
	"MAX_MDC" FLOAT(126), 
	"MIN_XE_VOLUME" FLOAT(126), 
	"MAX_QC_DEV" NUMBER, 
	"DET_BKGND_USED" NUMBER, 
	"GAS_BKGND_USED" NUMBER, 
	"QC_B_THRESHOLD" NUMBER, 
	"DEF_DET_BKGND_SAMPLE_ID" NUMBER, 
	"XE_IN_AIR" FLOAT(126), 
	"DEF_GAS_DECAY_TIME" NUMBER, 
	"BIN_ROWS" NUMBER, 
	"BIN_MIN_COUNT" NUMBER, 
	"BIN_GAMMA_START" NUMBER, 
	"BIN_BETA_START" NUMBER, 
	"BIN_MAX_VECTOR_SIZE" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_CONFIG_PARAMS"."DETECTOR_ID" IS '#brief=unique detector identifier#desc=unique detector identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_CONFIG_PARAMS"."LC_ABSCISSA" IS '#brief=confidence interval used in the critical level calculation.#desc=The confidence interval used in the critical level calculation. The value in the table corresponds to the abscissa of a confidence interval. This means that a 95% confidence interval should be represented in the database as 1.6449.#category=#ext=f8.5#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_CONFIG_PARAMS"."DEFAULT_METHOD" IS '#brief=default method#desc=default method#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_CONFIG_PARAMS"."MIN_SAMPLE_AIR_FLOW" IS '#brief=minimum accepted air flow from the sample measurement#desc=minimum accepted air flow from the sample measurement#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_CONFIG_PARAMS"."MIN_SAMPLE_VOLUME" IS '#brief=minimum accepted sample volume from the sample measurement#desc=minimum accepted sample volume from the sample measurement#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_CONFIG_PARAMS"."MAX_COLLECTION_TIME" IS '#brief=maximum amount of time accepted for sample collection#desc=maximum amount of time accepted for sample collection#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_CONFIG_PARAMS"."MAX_ACQUISITION_TIME" IS '#brief=maximum amount of time accepted for the measurement#desc=maximum amount of time accepted for the measurement#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_CONFIG_PARAMS"."MAX_REPORTING_TIME" IS '#brief=maximum amount of time accepted for reporting#desc=maximum amount of time accepted for reporting#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_CONFIG_PARAMS"."MAX_MDC" IS '#brief=maximum MDC value#desc=maximum MDC value#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_CONFIG_PARAMS"."MIN_XE_VOLUME" IS '#brief=minimum accepted volume#desc=minimum accepted volume#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_CONFIG_PARAMS"."MAX_QC_DEV" IS '#brief=maximum deviation of the quality check (integer)#desc=maximum deviation of the quality check (integer)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_CONFIG_PARAMS"."DET_BKGND_USED" IS '#brief=flag indicating whether or not to take into account the detector background measurements#desc=Tell the process whether detector background measurements should be taken into account when processing a sample. 0 means do not use, 1 indicates use.#category=#ext=i1#na=#range=in { 0,1}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_CONFIG_PARAMS"."GAS_BKGND_USED" IS '#brief=flag indicating whether or not to take into account the gas background measurements#desc=Tell the process whether gas background measurements should be taken into account when processing a sample. 0 means ?do not use?, 1 indicates ?use?.#category=#ext=i1#na=#range=in { 0,1}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_CONFIG_PARAMS"."QC_B_THRESHOLD" IS '#brief=threshold for channels in the histogram used when calculating beta and gamma spectra#desc=threshold for channels in the histogram used when calculating beta and gamma spectra#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_CONFIG_PARAMS"."DEF_DET_BKGND_SAMPLE_ID" IS '#brief=default detector background sample#desc=default detector background sample#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_CONFIG_PARAMS"."XE_IN_AIR" IS '#brief=the amount of xenon in air#desc=the amount of xenon in air#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_CONFIG_PARAMS"."DEF_GAS_DECAY_TIME" IS '#brief=default gas decay time#desc=default gas decay time#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_CONFIG_PARAMS"."BIN_ROWS" IS '#brief=number of rows to merge in binning#desc=number of rows to merge in binning#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_CONFIG_PARAMS"."BIN_MIN_COUNT" IS '#brief=minimum counts in each bin#desc=minimum counts in each bin#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_CONFIG_PARAMS"."BIN_GAMMA_START" IS '#brief=the gamma start offset in histogram#desc=the gamma start offset in histogram#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_CONFIG_PARAMS"."BIN_BETA_START" IS '#brief=the beta start offset in histogram#desc=the beta start offset in histogram#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_CONFIG_PARAMS"."BIN_MAX_VECTOR_SIZE" IS '#brief=maximum size for the bin vector#desc=maximum size for the bin vector#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_CONFIG_PARAMS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_BG_CONFIG_PARAMS"  IS '#category=Automatic Processing#desc=the gards_bg_config_params table holds details of beta-gamma configuration parameters and fields used for binning data.';
 
--------------------------------------------------------
--  DDL for Table GARDS_BG_CONFIG_PARAMS_ORI
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_BG_CONFIG_PARAMS_ORI" 
   (	"DETECTOR_ID" NUMBER, 
	"LC_ABSCISSA" FLOAT(126), 
	"DEFAULT_METHOD" NUMBER, 
	"MIN_SAMPLE_AIR_FLOW" FLOAT(126), 
	"MIN_SAMPLE_VOLUME" FLOAT(126), 
	"MAX_COLLECTION_TIME" NUMBER, 
	"MAX_ACQUISITION_TIME" NUMBER, 
	"MAX_REPORTING_TIME" NUMBER, 
	"MAX_MDC" FLOAT(126), 
	"MIN_XE_VOLUME" FLOAT(126), 
	"MAX_QC_DEV" NUMBER, 
	"DET_BKGND_USED" NUMBER, 
	"GAS_BKGND_USED" NUMBER, 
	"QC_B_THRESHOLD" NUMBER, 
	"DEF_DET_BKGND_SAMPLE_ID" NUMBER, 
	"XE_IN_AIR" FLOAT(126), 
	"DEF_GAS_DECAY_TIME" NUMBER, 
	"BIN_ROWS" NUMBER, 
	"BIN_MIN_COUNT" NUMBER, 
	"BIN_GAMMA_START" NUMBER, 
	"BIN_BETA_START" NUMBER, 
	"BIN_MAX_VECTOR_SIZE" NUMBER, 
	"MODDATE" DATE
   ) ;
 
--------------------------------------------------------
--  DDL for Table GARDS_BG_CONFIG_PARAMS_TEMP
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_BG_CONFIG_PARAMS_TEMP" 
   (	"DETECTOR_ID" NUMBER, 
	"GAMMA_BINNING" NUMBER, 
	"BETA_BINNING" NUMBER, 
	"LC_ABSCISSA" FLOAT(126), 
	"DEFAULT_METHOD" NUMBER, 
	"MIN_SAMPLE_AIR_FLOW" FLOAT(126), 
	"MIN_SAMPLE_VOLUME" FLOAT(126), 
	"MAX_COLLECTION_TIME" NUMBER, 
	"MAX_ACQUISITION_TIME" NUMBER, 
	"MAX_REPORTING_TIME" NUMBER, 
	"MAX_MDC" FLOAT(126), 
	"MIN_XE_VOLUME" FLOAT(126), 
	"MAX_QC_DEV" NUMBER, 
	"DET_BKGND_USED" NUMBER, 
	"GAS_BKGND_USED" NUMBER, 
	"QC_B_THRESHOLD" NUMBER, 
	"DEF_DET_BKGND_SAMPLE_ID" NUMBER, 
	"XE_IN_AIR" FLOAT(126), 
	"DEF_GAS_DECAY_TIME" NUMBER, 
	"MODDATE" DATE
   ) ;
 
--------------------------------------------------------
--  DDL for Table GARDS_BG_EFFICIENCY_PAIRS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_BG_EFFICIENCY_PAIRS" 
   (	"SAMPLE_ID" NUMBER, 
	"BG_EFFICIENCY" NUMBER, 
	"BG_EFFIC_ERROR" NUMBER, 
	"ROI" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_EFFICIENCY_PAIRS"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_EFFICIENCY_PAIRS"."BG_EFFICIENCY" IS '#brief=detection efficiency of b-g coincidence event#desc=Detection efficiency of b-g coincidence event#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_EFFICIENCY_PAIRS"."BG_EFFIC_ERROR" IS '#brief=uncertainty of bg_efficiency#desc=Uncertainty of bg_efficiency#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_EFFICIENCY_PAIRS"."ROI" IS '#brief=ROI identifier#desc=ROI identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_EFFICIENCY_PAIRS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_BG_EFFICIENCY_PAIRS"  IS '#category=Automatic Processing#desc=The gards_bg_efficiency_pairs table contains the detection efficiency associated with a beta-gamma coincidence event as specified in the PHD file. ';
 
--------------------------------------------------------
--  DDL for Table GARDS_BG_ENERGY_CAL
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_BG_ENERGY_CAL" 
   (	"SAMPLE_ID" NUMBER, 
	"BETA_COEFF1" NUMBER, 
	"BETA_COEFF2" NUMBER, 
	"BETA_COEFF3" NUMBER, 
	"GAMMA_COEFF1" NUMBER, 
	"GAMMA_COEFF2" NUMBER, 
	"GAMMA_COEFF3" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ENERGY_CAL"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ENERGY_CAL"."BETA_COEFF1" IS '#brief=zero shift of the beta ECR equation#desc=zero shift of the beta ECR equation#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ENERGY_CAL"."BETA_COEFF2" IS '#brief=linear coefficient of the beta ECR equation#desc=Zero shift of the beta ECR equation.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ENERGY_CAL"."BETA_COEFF3" IS '#brief=quadratic coefficient of the beta ECR equation#desc=quadratic coefficient of the beta ECR equation#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ENERGY_CAL"."GAMMA_COEFF1" IS '#brief=zero shift of the gamma ECR equation#desc=zero shift of the gamma ECR equation#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ENERGY_CAL"."GAMMA_COEFF2" IS '#brief=linear coefficient of the gamma ECR equation#desc=Gain of the gamma ECR equation.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ENERGY_CAL"."GAMMA_COEFF3" IS '#brief=quadratic coefficient of the gamma ECR equation#desc=Linear coefficient of the gamma ECR equation.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ENERGY_CAL"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_BG_ENERGY_CAL"  IS '#category=Automatic Processing#desc=The gards_bg_energy_cal table contains the energy-to-channel ratios of a sample. ';
 
--------------------------------------------------------
--  DDL for Table GARDS_BG_ISOTOPE_CONCS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_BG_ISOTOPE_CONCS" 
   (	"SAMPLE_ID" NUMBER, 
	"NUCLIDE_ID" NUMBER, 
	"CONC" FLOAT(126), 
	"CONC_ERR" FLOAT(126), 
	"MDC" FLOAT(126), 
	"NID_FLAG" NUMBER, 
	"LC" FLOAT(126), 
	"LD" FLOAT(126), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ISOTOPE_CONCS"."SAMPLE_ID" IS '#brief=unique sample identifier#desc=unique sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ISOTOPE_CONCS"."NUCLIDE_ID" IS '#brief=unique nuclide identifier#desc=unique nuclide identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ISOTOPE_CONCS"."CONC" IS '#brief=concentration#desc=concentration#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ISOTOPE_CONCS"."CONC_ERR" IS '#brief=level of confidence#desc=level of confidence#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ISOTOPE_CONCS"."MDC" IS '#brief=minimum detectable concentration#desc=minimum detectable concentration#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ISOTOPE_CONCS"."NID_FLAG" IS '#brief=nuclide identification indicator#desc=Nuclide identification indicator. (0=nuclide was not identified by automatic analysis; 1=nuclide was identified by automatic analysis; -1=nuclide was initially identified by automatic analysis, but later rejected because the concentration was <0.0; 2=; nuclide was initially identified by automatic analysis, but later removed by the Analyst). Canberra Parameter: CAM_G_NCLFIDENT.#category=#ext=i2#na=#range=nid_flag IN {-1, 0, 1, 2}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ISOTOPE_CONCS"."LC" IS '#brief=critical level#desc=critical level#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ISOTOPE_CONCS"."LD" IS '#brief=detection level#desc=detection level#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ISOTOPE_CONCS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_BG_ISOTOPE_CONCS"  IS '#category=Automatic Processing#desc=holds results of beta gamma processing, including the Critical level (LC) and the Detection level (LD).';
 
--------------------------------------------------------
--  DDL for Table GARDS_BG_PROC_PARAMS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_BG_PROC_PARAMS" 
   (	"SAMPLE_ID" NUMBER, 
	"LC_ABSCISSA" FLOAT(126), 
	"METHOD" NUMBER, 
	"DET_BKGND_USED" NUMBER, 
	"GAS_BKGND_USED" NUMBER, 
	"BETA_ECR_ORDER" NUMBER, 
	"GAMMA_ECR_ORDER" NUMBER, 
	"MAX_QC_DEV" NUMBER, 
	"QC_ID" NUMBER, 
	"XE_IN_AIR" FLOAT(126), 
	"DET_BKGND_ID" NUMBER, 
	"GAS_BKGND_ID" NUMBER, 
	"QC_B_THRESHOLD" NUMBER, 
	"BIN_ROWS" NUMBER, 
	"BIN_MIN_COUNT" NUMBER, 
	"BIN_GAMMA_START" NUMBER, 
	"BIN_BETA_START" NUMBER, 
	"BIN_MAX_VECTOR_SIZE" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_PROC_PARAMS"."SAMPLE_ID" IS '#brief=unique sample identifier#desc=unique sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_PROC_PARAMS"."LC_ABSCISSA" IS '#brief=confidence level for the calculation of critical level#desc=confidence level for the calculation of critical level#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_PROC_PARAMS"."METHOD" IS '#brief=the method that has been used (SSM or NCC)#desc=the method that has been used (SSM or NCC)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_PROC_PARAMS"."DET_BKGND_USED" IS '#brief=flag indicating whether or not to take into account the detector background measurements#desc=flag indicating whether or not to take into account the detector background measurements#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_PROC_PARAMS"."GAS_BKGND_USED" IS '#brief=whether the gas background was used#desc=whether the gas background was used#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_PROC_PARAMS"."BETA_ECR_ORDER" IS '#brief=whether the beta ECR is linear or quadratic#desc=whether the beta ECR is linear or quadratic#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_PROC_PARAMS"."GAMMA_ECR_ORDER" IS '#brief=whether the gamma ECR is linear or quadratic#desc=whether the gamma ECR is linear or quadratic#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_PROC_PARAMS"."MAX_QC_DEV" IS '#brief=threshold value for calibration deviation from qc spectra#desc=threshold value for calibration deviation from qc spectra#category=#ext=#na=#range=>0#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_PROC_PARAMS"."QC_ID" IS '#brief=unique quality control identifier#desc=unique quality control identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_PROC_PARAMS"."XE_IN_AIR" IS '#brief=the amount of xenon in air#desc=the amount of xenon in air#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_PROC_PARAMS"."DET_BKGND_ID" IS '#brief=unique identifier for the gas background used in the calculation#desc=unique identifier for the gas background used in the calculation#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_PROC_PARAMS"."GAS_BKGND_ID" IS '#brief=unique gas background identifier#desc=unique gas background identifier#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_PROC_PARAMS"."QC_B_THRESHOLD" IS '#brief=the value that is used to mask the gamma spectrum in QC control of the spectrum#desc=the value that is used to mask the gamma spectrum in QC control of the spectrum#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_PROC_PARAMS"."BIN_ROWS" IS '#brief=number of rows to merge in binning#desc=number of rows to merge in binning#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_PROC_PARAMS"."BIN_MIN_COUNT" IS '#brief=minimum counts in each bin#desc=minimum counts in each bin#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_PROC_PARAMS"."BIN_GAMMA_START" IS '#brief=the gamma start offset in histogram#desc=the gamma start offset in histogram#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_PROC_PARAMS"."BIN_BETA_START" IS '#brief=the beta start offset in histogram#desc=the beta start offset in histogram#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_PROC_PARAMS"."BIN_MAX_VECTOR_SIZE" IS '#brief=maximum size for the bin vector#desc=maximum size for the bin vector#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_PROC_PARAMS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_BG_PROC_PARAMS"  IS '#category=Automatic Processing#desc=the gards_bg_proc_params table holds details of beta-gamma processing parameters and fields used for binning data.';
 
--------------------------------------------------------
--  DDL for Table GARDS_BG_PROC_PARAMS_ROI
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_BG_PROC_PARAMS_ROI" 
   (	"SAMPLE_ID" NUMBER, 
	"ROI" NUMBER, 
	"HALFLIFE_SEC" NUMBER, 
	"ABUNDANCE" FLOAT(126), 
	"NUCLIDE_ID" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_PROC_PARAMS_ROI"."SAMPLE_ID" IS '#brief=unique sample identifier#desc=unique sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_PROC_PARAMS_ROI"."ROI" IS '#brief=region of interest#desc=region of interest#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_PROC_PARAMS_ROI"."HALFLIFE_SEC" IS '#brief=half life in seconds#desc=half life in seconds#category=#ext=f17.5#na=#range=halflife_sec > 0#unit=seconds';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_PROC_PARAMS_ROI"."ABUNDANCE" IS '#brief=abundance of line (%)#desc=abundance of line (%)#category=#ext=f10.6#na=#range=0 < abundance <= 100#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_PROC_PARAMS_ROI"."NUCLIDE_ID" IS '#brief=unique nuclide identifier#desc=unique nuclide identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_PROC_PARAMS_ROI"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_BG_PROC_PARAMS_ROI"  IS '#category=Automatic Processing#desc=contains details of beta gamma processing regions of interest';
 
--------------------------------------------------------
--  DDL for Table GARDS_BG_QC_RESULT
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_BG_QC_RESULT" 
   (	"SAMPLE_ID" NUMBER, 
	"AMPLITUDE" FLOAT(126), 
	"FWHM" FLOAT(126), 
	"CENTROID" FLOAT(126), 
	"OFFSET" FLOAT(126), 
	"SLOPE" FLOAT(126), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_QC_RESULT"."SAMPLE_ID" IS '#brief=unique sample identifier#desc=unique sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_QC_RESULT"."AMPLITUDE" IS '#brief=Amplitude of QC peak#desc=Amplitude of QC peak#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_QC_RESULT"."FWHM" IS '#brief=full width half maximum (FWHM) value of QC peak#desc=full width half maximum (FWHM) value of QC peak#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_QC_RESULT"."CENTROID" IS '#brief=centroid energy of QC peak#desc=centroid energy of QC peak#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_QC_RESULT"."OFFSET" IS '#brief=noise offset in QC spectrum#desc=noise offset in QC spectrum#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_QC_RESULT"."SLOPE" IS '#brief=noise slope in QC spectrum#desc=noise slope in QC spectrum#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_QC_RESULT"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_BG_QC_RESULT"  IS '#category=Automatic Processing#desc=holds results of beta gamma quality control (QC) processing.';
 
--------------------------------------------------------
--  DDL for Table GARDS_BG_ROI_CONCS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_BG_ROI_CONCS" 
   (	"SAMPLE_ID" NUMBER, 
	"ROI" NUMBER, 
	"CONC" FLOAT(126), 
	"CONC_ERR" FLOAT(126), 
	"MDC" FLOAT(126), 
	"NID_FLAG" NUMBER, 
	"LC" FLOAT(126), 
	"LD" FLOAT(126), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ROI_CONCS"."SAMPLE_ID" IS '#brief=unique sample identifier#desc=unique sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ROI_CONCS"."ROI" IS '#brief=region of interest#desc=region of interest#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ROI_CONCS"."CONC" IS '#brief=concentration#desc=concentration#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ROI_CONCS"."CONC_ERR" IS '#brief=level of confidence#desc=level of confidence#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ROI_CONCS"."MDC" IS '#brief=minimum detectable concentration#desc=minimum detectable concentration#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ROI_CONCS"."NID_FLAG" IS '#brief=whether the nuclide was identified or not#desc=whether the nuclide was identified or not#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ROI_CONCS"."LC" IS '#brief=critical level#desc=critical level#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ROI_CONCS"."LD" IS '#brief=detection level#desc=detection level#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ROI_CONCS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_BG_ROI_CONCS"  IS '#category=Automatic Processing#desc=holds results of beta gamma region of interest processing, including the Critical level (LC) and the Detection level (LD).';
 
--------------------------------------------------------
--  DDL for Table GARDS_BG_ROI_COUNTS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_BG_ROI_COUNTS" 
   (	"SAMPLE_ID" NUMBER, 
	"ROI" NUMBER, 
	"GROSS" FLOAT(126), 
	"GROSS_ERR" FLOAT(126), 
	"GAS_BKGND_GROSS" FLOAT(126), 
	"GAS_BKGND_COUNT" FLOAT(126), 
	"GAS_BKGND_COUNT_ERR" FLOAT(126), 
	"DET_BKGND_COUNT" FLOAT(126), 
	"DET_BKGND_COUNT_ERR" FLOAT(126), 
	"NET_COUNT" FLOAT(126), 
	"NET_COUNT_ERR" FLOAT(126), 
	"CRITICAL_LEV_SAMP" FLOAT(126), 
	"CRITICAL_LEV_GAS" FLOAT(126), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ROI_COUNTS"."SAMPLE_ID" IS '#brief=unique sample identifier#desc=unique sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ROI_COUNTS"."ROI" IS '#brief=region of interest#desc=region of interest#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ROI_COUNTS"."GROSS" IS '#brief=counts in ROI before processing#desc=counts in ROI before processing#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ROI_COUNTS"."GROSS_ERR" IS '#brief=confidence level#desc=confidence level#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ROI_COUNTS"."GAS_BKGND_GROSS" IS '#brief=gas background gross#desc=gas background gross#category=#ext=i8#na=#range=#unit=counts';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ROI_COUNTS"."GAS_BKGND_COUNT" IS '#brief=gas background counts#desc=gas background counts#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ROI_COUNTS"."GAS_BKGND_COUNT_ERR" IS '#brief=confidence level#desc=Value of the specified SOH parameter.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ROI_COUNTS"."DET_BKGND_COUNT" IS '#brief=detector background counts#desc=detector background counts#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ROI_COUNTS"."DET_BKGND_COUNT_ERR" IS '#brief=confidence level#desc=confidence level#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ROI_COUNTS"."NET_COUNT" IS '#brief=counts in ROI after processing#desc=counts in ROI after processing#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ROI_COUNTS"."NET_COUNT_ERR" IS '#brief=confidence level#desc=confidence level#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ROI_COUNTS"."CRITICAL_LEV_SAMP" IS '#brief=critical level in counts#desc=critical level in counts#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ROI_COUNTS"."CRITICAL_LEV_GAS" IS '#brief=critical level gas#desc=critical level gas#category=#ext=i18#na=#range=#unit=counts';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_ROI_COUNTS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_BG_ROI_COUNTS"  IS '#category=Automatic Processing#desc=contains beta gamma region of interest count values';
 
--------------------------------------------------------
--  DDL for Table GARDS_BG_STD_SPECTRA_RESULT
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_BG_STD_SPECTRA_RESULT" 
   (	"SAMPLE_ID" NUMBER, 
	"STD_SPECTRA_ID" NUMBER, 
	"GAMMA_COEFF1" FLOAT(126), 
	"GAMMA_COEFF2" FLOAT(126), 
	"GAMMA_COEFF3" FLOAT(126), 
	"BETA_COEFF1" FLOAT(126), 
	"BETA_COEFF2" FLOAT(126), 
	"BETA_COEFF3" FLOAT(126), 
	"ESTIMATE" FLOAT(126), 
	"ERROR" FLOAT(126), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_STD_SPECTRA_RESULT"."SAMPLE_ID" IS '#brief=unique sample identifier#desc=unique sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_STD_SPECTRA_RESULT"."STD_SPECTRA_ID" IS '#brief=unique identifier for the standard spectra#desc=unique identifier for the standard spectra. This is a sample id for the std spectra)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_STD_SPECTRA_RESULT"."GAMMA_COEFF1" IS '#brief=gamma coefficient 1 (energy to channel)#desc=gamma coefficient 1 (energy to channel)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_STD_SPECTRA_RESULT"."GAMMA_COEFF2" IS '#brief=gamma coefficient 2 (energy to channel)#desc=gamma coefficient 2 (energy to channel)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_STD_SPECTRA_RESULT"."GAMMA_COEFF3" IS '#brief=gamma coefficient 3 (energy to channel)#desc=gamma coefficient 3 (energy to channel)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_STD_SPECTRA_RESULT"."BETA_COEFF1" IS '#brief=beta coefficient 1 (energy to channel)#desc=beta coefficient 1 (energy to channel)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_STD_SPECTRA_RESULT"."BETA_COEFF2" IS '#brief=beta coefficient 2 (energy to channel)#desc=beta coefficient 2 (energy to channel)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_STD_SPECTRA_RESULT"."BETA_COEFF3" IS '#brief=beta coefficient 3 (energy to channel)#desc=beta coefficient 3 (energy to channel)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_STD_SPECTRA_RESULT"."ESTIMATE" IS '#brief=the estimate (SpectraContribution * NumberOfDecays)#desc=the estimate (SpectraContribution * NumberOfDecays)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_STD_SPECTRA_RESULT"."ERROR" IS '#brief=the variance for the estimate#desc=the variance for the estimate#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_BG_STD_SPECTRA_RESULT"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_BG_STD_SPECTRA_RESULT"  IS '#category=Automatic Processing#desc=the gards_bg_std_spectra_result table holds results calculated for each standard spectrum.';
 
--------------------------------------------------------
--  DDL for Table GARDS_B_ENERGY_PAIRS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_B_ENERGY_PAIRS" 
   (	"SAMPLE_ID" NUMBER, 
	"DECAY_MODE" CHAR(1), 
	"CAL_ENERGY" NUMBER, 
	"CAL_ERROR" NUMBER, 
	"CHANNEL" NUMBER, 
	"MODDATE" DATE
   ) ENABLE ROW MOVEMENT ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_B_ENERGY_PAIRS"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_B_ENERGY_PAIRS"."DECAY_MODE" IS '#brief=type of decay; B = beta particle, C = conversion electron#desc=type of decay; B = beta particle, C = conversion electron#category=#ext=a1#na=#range=decay_mode IN {B, C}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_B_ENERGY_PAIRS"."CAL_ENERGY" IS '#brief=calibration energy (keV)#desc=calibration energy (keV)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_B_ENERGY_PAIRS"."CAL_ERROR" IS '#brief=uncertainty of channel#desc=Calibration energy.#category=#ext=#na=#range=#unit=keV';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_B_ENERGY_PAIRS"."CHANNEL" IS '#brief=peak centroid channel#desc=peak centroid channel#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_B_ENERGY_PAIRS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_B_ENERGY_PAIRS"  IS '#category=Automatic Processing#desc=The gards_b_energy_pairs table contains the energy calibration pairs information associated with the beta axis of the spectrum used in rms_xanalyze.  The values in the gards_b_energy_pairs and the gards_b_energy_pairs_orig tables are identical.  ';
 
--------------------------------------------------------
--  DDL for Table GARDS_B_ENERGY_PAIRS_ORIG
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_B_ENERGY_PAIRS_ORIG" 
   (	"SAMPLE_ID" NUMBER, 
	"DECAY_MODE" CHAR(1), 
	"CAL_ENERGY" NUMBER, 
	"CAL_ERROR" NUMBER, 
	"CHANNEL" NUMBER, 
	"MODDATE" DATE
   ) ENABLE ROW MOVEMENT ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_B_ENERGY_PAIRS_ORIG"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_B_ENERGY_PAIRS_ORIG"."DECAY_MODE" IS '#brief=type of decay; B = beta particle, C = conversion electron#desc=type of decay; B = beta particle, C = conversion electron#category=#ext=a1#na=#range=decay_mode IN {B, C}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_B_ENERGY_PAIRS_ORIG"."CAL_ENERGY" IS '#brief=calibration energy (keV)#desc=calibration energy (keV)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_B_ENERGY_PAIRS_ORIG"."CAL_ERROR" IS '#brief=uncertainty of channel#desc=Calibration energy.#category=#ext=#na=#range=#unit=keV';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_B_ENERGY_PAIRS_ORIG"."CHANNEL" IS '#brief=peak centroid channel#desc=peak centroid channel#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_B_ENERGY_PAIRS_ORIG"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_B_ENERGY_PAIRS_ORIG"  IS '#category=Automatic Processing#desc=The gards_b_energy_pairs_orig table contains the original energy calibration pairs information associated with the beta axis of the spectrum as specified in the PHD file. The values in the gards_b_energy_pairs and the gards_b_energy_pairs_orig tables are identical. This table is not used by the rms_xanalyze process.';
 
--------------------------------------------------------
--  DDL for Table GARDS_B_RESOLUTION_PAIRS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_B_RESOLUTION_PAIRS" 
   (	"SAMPLE_ID" NUMBER, 
	"RESOLUTION" NUMBER, 
	"RES_ENERGY" NUMBER, 
	"RES_ERROR" NUMBER, 
	"MODDATE" DATE
   ) ENABLE ROW MOVEMENT ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_B_RESOLUTION_PAIRS"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_B_RESOLUTION_PAIRS"."RESOLUTION" IS '#brief=detector resolution (keV)#desc=Uncertainty of resolution.#category=#ext=#na=#range=0.0 < res_error#unit=keV';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_B_RESOLUTION_PAIRS"."RES_ENERGY" IS '#brief=resolution energy (keV)#desc=resolution energy (keV)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_B_RESOLUTION_PAIRS"."RES_ERROR" IS '#brief=uncertainty of resolution (keV)#desc=Resolution energy.#category=#ext=#na=#range=0.0 < res_energy#unit=keV';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_B_RESOLUTION_PAIRS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_B_RESOLUTION_PAIRS"  IS '#category=Automatic Processing#desc=The gards_b_resolution_pairs table contains the resolution calibration pairs information associated with the beta axis of the spectrum.  This table is not used by the rms_xanalyze process.  The values in the gards_b_resolution_pairs and the gards_b_resolution_pairs_orig tables are identical.  ';
 
--------------------------------------------------------
--  DDL for Table GARDS_B_RESOLUTION_PAIRS_ORIG
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_B_RESOLUTION_PAIRS_ORIG" 
   (	"SAMPLE_ID" NUMBER, 
	"RESOLUTION" NUMBER, 
	"RES_ENERGY" NUMBER, 
	"RES_ERROR" NUMBER, 
	"MODDATE" DATE
   ) ENABLE ROW MOVEMENT ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_B_RESOLUTION_PAIRS_ORIG"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_B_RESOLUTION_PAIRS_ORIG"."RESOLUTION" IS '#brief=detector resolution (keV)#desc=Uncertainty of resolution.#category=#ext=#na=#range=0.0 < res_error#unit=keV';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_B_RESOLUTION_PAIRS_ORIG"."RES_ENERGY" IS '#brief=resolution energy (keV)#desc=resolution energy (keV)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_B_RESOLUTION_PAIRS_ORIG"."RES_ERROR" IS '#brief=uncertainty of resolution (keV)#desc=Resolution energy.#category=#ext=#na=#range=0.0 < res_energy#unit=keV';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_B_RESOLUTION_PAIRS_ORIG"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_B_RESOLUTION_PAIRS_ORIG"  IS '#category=Automatic Processing#desc=The gards_b_resolution_pairs_orig table contains the original resolution calibration pairs information associated with the beta axis of the spectrum as specified in the PHD file.  This table is not used by the rms_xanalyze process.  The values in the gards_b_resolution_pairs and the gards_b_resolution_pairs_orig tables are identical.  ';
 
--------------------------------------------------------
--  DDL for Table GARDS_CAT_CRITERIA_TESTS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_CAT_CRITERIA_TESTS" 
   (	"TEST_ID" NUMBER, 
	"TEST_CODE" VARCHAR2(24), 
	"TEST_NAME" VARCHAR2(48), 
	"LOWER_LIMIT" NUMBER, 
	"UPPER_LIMIT" NUMBER, 
	"UNITS" VARCHAR2(16), 
	"ACTIVE_FLAG" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_CRITERIA_TESTS"."TEST_ID" IS '#brief=unique identitifier#desc=unique identitifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_CRITERIA_TESTS"."TEST_CODE" IS '#brief=unique test code identifier string#desc=unique test code identifier string#category=#ext=a24#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_CRITERIA_TESTS"."TEST_NAME" IS '#brief=test name label for display#desc=unique identifier#category=#ext=a48#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_CRITERIA_TESTS"."LOWER_LIMIT" IS '#brief=lower limit bound of the test#desc=lower limit bound of the test#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_CRITERIA_TESTS"."UPPER_LIMIT" IS '#brief=upper limit bound of the test#desc=upper limit bound of the test#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_CRITERIA_TESTS"."UNITS" IS '#brief=unit values for the test bounds#desc=unit values for the test bounds#category=#ext=a16#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_CRITERIA_TESTS"."ACTIVE_FLAG" IS '#brief=0 if test is inactive#desc=0 if test is inactive#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_CRITERIA_TESTS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_CAT_CRITERIA_TESTS"  IS '#category=Automatic Processing#desc=The gards_cat_criteria_tests table contains a list of all category criteria tests. The column active_flag is set to 0 if the test should not be run. A trigger updates the moddate column when any modification is made to another column.';
 
--------------------------------------------------------
--  DDL for Table GARDS_CAT_TEMPLATE
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_CAT_TEMPLATE" 
   (	"STATION_ID" NUMBER, 
	"DETECTOR_ID" NUMBER, 
	"NAME" VARCHAR2(8), 
	"METHOD_ID" NUMBER, 
	"METHOD_TYPE" NUMBER, 
	"INIT_BEGIN_DATE" DATE, 
	"INIT_END_DATE" DATE, 
	"BEGIN_DATE" DATE, 
	"END_DATE" DATE, 
	"ANALYST" VARCHAR2(30), 
	"COMMENT_TEXT" VARCHAR2(256), 
	"UPPER_BOUND" NUMBER, 
	"LOWER_BOUND" NUMBER, 
	"CENTRAL_VALUE" NUMBER, 
	"DELTA" NUMBER, 
	"ABSCISSA" NUMBER, 
	"DEV_TOLERANCE" NUMBER, 
	"NUM_SAMPLES" NUMBER, 
	"ALPHA" NUMBER, 
	"GAMMA" NUMBER, 
	"TSTAT" NUMBER, 
	"XFORM" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_TEMPLATE"."STATION_ID" IS '#brief=station identifier#desc=station identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_TEMPLATE"."DETECTOR_ID" IS '#brief=unique detector identifier#desc=unique detector identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_TEMPLATE"."NAME" IS '#brief=nuclide name#desc=Nuclide name.#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_TEMPLATE"."METHOD_ID" IS '#brief=method identifier#desc=method identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_TEMPLATE"."METHOD_TYPE" IS '#brief=type of categorization analysis to use#desc=Method identifier.#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_TEMPLATE"."INIT_BEGIN_DATE" IS '#brief=start date for initialization data#desc=start date for initialization data#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_TEMPLATE"."INIT_END_DATE" IS '#brief=end date for initialization data#desc=Start date for initialization data.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_TEMPLATE"."BEGIN_DATE" IS '#brief=date initialization began#desc=date initialization began#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_TEMPLATE"."END_DATE" IS '#brief=date initialization ended#desc=date initialization ended#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_TEMPLATE"."ANALYST" IS '#brief=name of analyst initializing nuclide categorization#desc=Gain of first-order recursive filter for process level.#category=#ext=a30#na=#range=alpha >= 0#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_TEMPLATE"."COMMENT_TEXT" IS '#brief=comment on the filter#desc=comment on the filter#category=#ext=a256#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_TEMPLATE"."UPPER_BOUND" IS '#brief=upper limit of the amount of a nuclide that can be acceptably found#desc=upper limit of the amount of a nuclide that can be acceptably found#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_TEMPLATE"."LOWER_BOUND" IS '#brief=lower limit of the amount of a nuclide that can be acceptably found#desc=lower limit of the amount of a nuclide that can be acceptably found#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_TEMPLATE"."CENTRAL_VALUE" IS '#brief=current estimate of the level of the random process#desc=current estimate of the level of the random process#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_TEMPLATE"."DELTA" IS '#brief=value of a variable used in bounds estimation (EWMA algorithm)#desc=value of a variable used in bounds estimation (EWMA algorithm)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_TEMPLATE"."ABSCISSA" IS '#brief=acceptable number of standard deviations away from the central_value where the amount of a nuclide may be found (RDC algorithm)#desc=acceptable number of standard deviations away from the central_value where the amount of a nuclide may be found (RDC algorithm)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_TEMPLATE"."DEV_TOLERANCE" IS '#brief=tolerance#desc=tolerance#category=#ext=i10#na=NULL#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_TEMPLATE"."NUM_SAMPLES" IS '#brief=number of samples used to collect the average and define the standard deviation (RDC algorithm)#desc=number of samples used to collect the average and define the standard deviation (RDC algorithm)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_TEMPLATE"."ALPHA" IS '#brief=value of a variable used in bounds estimation (EWMA algorithm)#desc=value of a variable used in bounds estimation (EWMA algorithm)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_TEMPLATE"."GAMMA" IS '#brief=value of a variable used in bounds estimation (EWMA algorithm)#desc=value of a variable used in bounds estimation (EWMA algorithm)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_TEMPLATE"."TSTAT" IS '#brief=value of a variable used in bounds estimation (EWMA algorithm)#desc=value of a variable used in bounds estimation (EWMA algorithm)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_TEMPLATE"."XFORM" IS '#brief=code for transform function applied to measurement data#desc=code for transform function applied to measurement data#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CAT_TEMPLATE"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_CAT_TEMPLATE"  IS '#category=Automatic Processing#desc=The gards_cat_template table contains categorization initialization information for typical nuclides.';
 
--------------------------------------------------------
--  DDL for Table GARDS_CODES
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_CODES" 
   (	"TYPE" VARCHAR2(15), 
	"CODE" CHAR(5), 
	"DESCRIPTION" VARCHAR2(40), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CODES"."TYPE" IS '#brief=category of code#desc=Category of code.#category=#ext=a15#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CODES"."CODE" IS '#brief=code symbol #desc=code symbol.#category=#ext=a5#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CODES"."DESCRIPTION" IS '#brief=code explanation#desc=Description of the code, detector, or station.#category=#ext=a40#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CODES"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_CODES"  IS '#category=Automatic Processing#desc=The gards_codes table contains codes for items used throughout radionuclide monitoring system.';
 
--------------------------------------------------------
--  DDL for Table GARDS_COMMENTS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_COMMENTS" 
   (	"SAMPLE_ID" NUMBER, 
	"PEAK_ID" NUMBER, 
	"NUCL_NAME" VARCHAR2(8), 
	"COMMENT_ID" NUMBER, 
	"ANALYST" VARCHAR2(30), 
	"DTG" DATE, 
	"COMMENT_TYPE" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_COMMENTS"."SAMPLE_ID" IS '#brief=sample identifier #desc=sample identifier #category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_COMMENTS"."PEAK_ID" IS '#brief=peak identifier#desc=peak identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_COMMENTS"."NUCL_NAME" IS '#brief=nuclide name referenced by comment#desc=nuclide name referenced by comment#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_COMMENTS"."COMMENT_ID" IS '#brief=unique comment identifier#desc=unique comment identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_COMMENTS"."ANALYST" IS '#brief=individual (or process) entering comment#desc=individual (or process) entering comment#category=#ext=a30#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_COMMENTS"."DTG" IS '#brief=comment entry date#desc=comment entry date#category=#ext=a21#na=#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_COMMENTS"."COMMENT_TYPE" IS '#brief=comment code #desc=comment code #category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_COMMENTS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_COMMENTS"  IS '#category=Automatic Processing#desc=The gards_comments table contains automated analysis and interactive review comments related to peaks in the gards_peaks table and nuclides in the gards_nucl_ided table.';
 
--------------------------------------------------------
--  DDL for Table GARDS_COMMENTS_DEFS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_COMMENTS_DEFS" 
   (	"COMMENT_TYPE" NUMBER, 
	"COMMENT_TEXT" VARCHAR2(256), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_COMMENTS_DEFS"."COMMENT_TYPE" IS '#brief=predefined comment code#desc=Text of analyst comments.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_COMMENTS_DEFS"."COMMENT_TEXT" IS '#brief=predefined comment text#desc=predefined comment text#category=#ext=a25#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_COMMENTS_DEFS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_COMMENTS_DEFS"  IS '#category=Automatic Processing#desc=The gards_comments_defs table contains predefined comments for automated analysis and interactive review.';
 
--------------------------------------------------------
--  DDL for Table GARDS_COMMENTS_DEFS_BG
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_COMMENTS_DEFS_BG" 
   (	"COMMENT_TYPE" NUMBER, 
	"COMMENT_TEXT" VARCHAR2(256), 
	"MODDATE" DATE
   ) ;
 
--------------------------------------------------------
--  DDL for Table GARDS_CSC_MODCOEFF_LIB
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_CSC_MODCOEFF_LIB" 
   (	"DETECTOR_ID" NUMBER, 
	"NAME" VARCHAR2(8), 
	"NAME_D" VARCHAR2(8), 
	"ENERGY" NUMBER, 
	"ABUNDANCE" NUMBER, 
	"APP_ABUNDANCE" NUMBER, 
	"APP_ABUNDANCE_ERR" NUMBER, 
	"CSC_RATIO" NUMBER, 
	"CSC_RATIO_ERR" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CSC_MODCOEFF_LIB"."DETECTOR_ID" IS '#brief=unique detector identifier#desc=unique detector identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CSC_MODCOEFF_LIB"."NAME" IS '#brief=nuclide name#desc=nuclide name#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CSC_MODCOEFF_LIB"."NAME_D" IS '#brief=daughter nuclide name#desc=daughter nuclide name#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CSC_MODCOEFF_LIB"."ENERGY" IS '#brief=energy of nuclide line#desc=energy of nuclide line#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CSC_MODCOEFF_LIB"."ABUNDANCE" IS '#brief=abundance of line (%)#desc=abundance of line (%)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CSC_MODCOEFF_LIB"."APP_ABUNDANCE" IS '#brief=apparent abundance#desc=apparent abundance#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CSC_MODCOEFF_LIB"."APP_ABUNDANCE_ERR" IS '#brief=absolute error in apparent abundance#desc=absolute error in apparent abundance#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CSC_MODCOEFF_LIB"."CSC_RATIO" IS '#brief=CSC correction factor#desc=CSC correction factor#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CSC_MODCOEFF_LIB"."CSC_RATIO_ERR" IS '#brief=error in CSC#desc=error in CSC#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_CSC_MODCOEFF_LIB"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_CSC_MODCOEFF_LIB"  IS '#category=Automatic Processing#desc=The gards_csc_modcoeff_lib table contains the cascade summing ratios used by rms_analyze.';
 
--------------------------------------------------------
--  DDL for Table GARDS_DBROLE_OWNER
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_DBROLE_OWNER" 
   (	"OWNER" VARCHAR2(12), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_DBROLE_OWNER"."OWNER" IS '#brief=name of database user who owns the RMS roles for the MAR tool#desc=name of database user who owns the RMS roles for the MAR tool#category=#ext=a12#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_DBROLE_OWNER"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_DBROLE_OWNER"  IS '#category=Automatic Processing#desc=The gards_dbrole_owner table contains information used by the MAR tool to determine the database user that owns the RMS roles.';
 
--------------------------------------------------------
--  DDL for Table GARDS_DETECTORS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_DETECTORS" 
   (	"DETECTOR_ID" NUMBER, 
	"DETECTOR_CODE" VARCHAR2(9), 
	"DESCRIPTION" VARCHAR2(80), 
	"LAT" NUMBER, 
	"LON" NUMBER, 
	"TYPE" VARCHAR2(6), 
	"CHANNELS" NUMBER, 
	"RATED_EFFICIENCY" NUMBER, 
	"RATED_RESOLUTION" NUMBER, 
	"ECAL_RANGE_MAX" NUMBER, 
	"DATE_BEGIN" DATE, 
	"DATE_END" DATE, 
	"STATUS" VARCHAR2(2), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_DETECTORS"."DETECTOR_ID" IS '#brief=unique detector identifier#desc=Detector identification code.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_DETECTORS"."DETECTOR_CODE" IS '#brief=detector identification code#desc=detector identification code#category=#ext=a9#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_DETECTORS"."DESCRIPTION" IS '#brief=detector description#desc=Description of the code, detector, or station.#category=#ext=a80#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_DETECTORS"."LAT" IS '#brief=latitude (degrees)#desc=latitude (degrees)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_DETECTORS"."LON" IS '#brief=longitude (degrees)#desc=longitude (degrees)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_DETECTORS"."TYPE" IS '#brief=detector type#desc=Brief description of detector or station.#category=#ext=a6#na=#range=ASCII characters#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_DETECTORS"."CHANNELS" IS '#brief=number of channels#desc=number of channels#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_DETECTORS"."RATED_EFFICIENCY" IS '#brief=rated efficiency of detector #desc=rated efficiency of detector #category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_DETECTORS"."RATED_RESOLUTION" IS '#brief=rated resolution of detector#desc=Efficiency of the detector relative to a standard 3 in. x 3 in. (7.62 cm x 7.62 cm) cylindrical NaI(Tl) detector at 1332 keV. The rated efficiency is usually supplied by the detector manufacturer.#category=#ext=#na=#range=0 < rated_efficiency < 130#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_DETECTORS"."ECAL_RANGE_MAX" IS '#brief=maximum detector calibration energy (keV)#desc=maximum detector calibration energy (keV)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_DETECTORS"."DATE_BEGIN" IS '#brief=detector initialization date#desc=detector initialization date#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_DETECTORS"."DATE_END" IS '#brief=detector decommissioning date#desc=Station/Detector initialization date.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_DETECTORS"."STATUS" IS '#brief=status of detector, if Y then data from this detector are automatically processed if N then they are not automatically processed#desc=Status of detector: if Y, then data from this detector are automatically processed; if N, then they are not processed automatically.#category=#ext=a2#na=#range=status IN {N, Y}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_DETECTORS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_DETECTORS"  IS '#category=Automatic Processing#desc=The gards_detectors table contains detector overviews and characteristics. ';
 
--------------------------------------------------------
--  DDL for Table GARDS_DIST_SAMPLE_QUEUE
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_DIST_SAMPLE_QUEUE" 
   (	"SAMPLE_ID" NUMBER, 
	"USER_ID" NUMBER, 
	"ROLE_ID" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_DIST_SAMPLE_QUEUE"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_DIST_SAMPLE_QUEUE"."USER_ID" IS '#brief=user identifier#desc=user identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_DIST_SAMPLE_QUEUE"."ROLE_ID" IS '#brief=role identifier#desc=role identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_DIST_SAMPLE_QUEUE"  IS '#category=Automatic Processing#desc=The gards_dist_sample_queue table contains a list of samples and the user or role to which they are assigned. ';
 
--------------------------------------------------------
--  DDL for Table GARDS_EFFICIENCY_CAL
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_EFFICIENCY_CAL" 
   (	"SAMPLE_ID" NUMBER, 
	"DEGREE" NUMBER, 
	"EFFTYPE" CHAR(8), 
	"COEFF1" NUMBER, 
	"COEFF2" NUMBER, 
	"COEFF3" NUMBER, 
	"COEFF4" NUMBER, 
	"COEFF5" NUMBER, 
	"COEFF6" NUMBER, 
	"COEFF7" NUMBER, 
	"COEFF8" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_EFFICIENCY_CAL"."SAMPLE_ID" IS '#brief=sample identifier #desc=sample identifier #category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_EFFICIENCY_CAL"."DEGREE" IS '#brief=degree of efficiency equation#desc=degree of efficiency equation#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_EFFICIENCY_CAL"."EFFTYPE" IS '#brief=efficiency type#desc=efficiency type#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_EFFICIENCY_CAL"."COEFF1" IS '#brief=first order calibration coefficient#desc=first order calibration coefficient#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_EFFICIENCY_CAL"."COEFF2" IS '#brief=second order calibration coefficient#desc=First order calibration coefficient.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_EFFICIENCY_CAL"."COEFF3" IS '#brief=third order calibration coefficient#desc=Second order calibration coefficient.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_EFFICIENCY_CAL"."COEFF4" IS '#brief=fourth order calibration coefficient#desc=Third order calibration coefficient.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_EFFICIENCY_CAL"."COEFF5" IS '#brief=fifth order calibration coefficient#desc=Fourth order calibration coefficient.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_EFFICIENCY_CAL"."COEFF6" IS '#brief=sixth order calibration coefficient#desc=Fifth order calibration coefficient.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_EFFICIENCY_CAL"."COEFF7" IS '#brief=seventh order calibration coefficient#desc=Sixth order calibration coefficient.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_EFFICIENCY_CAL"."COEFF8" IS '#brief=eighth order calibration coefficient#desc=Seventh order calibration coefficient.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_EFFICIENCY_CAL"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_EFFICIENCY_CAL"  IS '#category=Automatic Processing#desc=The gards_efficiency_cal table contains the efficiency calibration equation that is computed for each spectra.';
 
--------------------------------------------------------
--  DDL for Table GARDS_EFFICIENCY_PAIRS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_EFFICIENCY_PAIRS" 
   (	"SAMPLE_ID" NUMBER, 
	"EFFIC_ENERGY" NUMBER, 
	"EFFICIENCY" NUMBER, 
	"EFFIC_ERROR" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_EFFICIENCY_PAIRS"."SAMPLE_ID" IS '#brief=sample identifier #desc=sample identifier #category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_EFFICIENCY_PAIRS"."EFFIC_ENERGY" IS '#brief=efficiency energy (keV)#desc=efficiency energy (keV)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_EFFICIENCY_PAIRS"."EFFICIENCY" IS '#brief=efficiency#desc=Uncertainty of efficiency.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_EFFICIENCY_PAIRS"."EFFIC_ERROR" IS '#brief=uncertainty of efficiency#desc=uncertainty of efficiency#category=#ext=#na=#range=#unit=';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_EFFICIENCY_PAIRS"  IS '#category=Automatic Processing#desc=The gards_efficiency_pairs table contains efficiency calibration pairs as specified in the PHD file.';
 
--------------------------------------------------------
--  DDL for Table GARDS_EFFICIENCY_VGSL_PAIRS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_EFFICIENCY_VGSL_PAIRS" 
   (	"DETECTOR_ID" NUMBER, 
	"EFFIC_ENERGY" NUMBER, 
	"EFFICIENCY" NUMBER, 
	"EFFIC_ERROR" NUMBER, 
	"MODDATE" DATE DEFAULT SYSDATE, 
	"BEGIN_DATE" DATE, 
	"END_DATE" DATE
   ) ;
 
   COMMENT ON TABLE "RMSMAN"."GARDS_EFFICIENCY_VGSL_PAIRS"  IS '#category=Automatic Processing#desc=gards efficiency vgsl pairs';
 
--------------------------------------------------------
--  DDL for Table GARDS_ENERGY_CAL
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_ENERGY_CAL" 
   (	"SAMPLE_ID" NUMBER, 
	"COEFF1" NUMBER, 
	"COEFF2" NUMBER, 
	"COEFF3" NUMBER, 
	"COEFF4" NUMBER, 
	"COEFF5" NUMBER, 
	"COEFF6" NUMBER, 
	"COEFF7" NUMBER, 
	"COEFF8" NUMBER, 
	"ENERGY_UNITS" CHAR(3), 
	"CNV_FACTOR" NUMBER, 
	"APE" NUMBER, 
	"DET" NUMBER, 
	"MSE" NUMBER, 
	"TSTAT" NUMBER, 
	"SCORE" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL"."COEFF1" IS '#brief=first order calibration coefficient#desc=first order calibration coefficient#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL"."COEFF2" IS '#brief=second order calibration coefficient#desc=First order calibration coefficient.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL"."COEFF3" IS '#brief=third order calibration coefficient#desc=Second order calibration coefficient.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL"."COEFF4" IS '#brief=fourth order calibration coefficient#desc=Third order calibration coefficient.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL"."COEFF5" IS '#brief=fifth order calibration coefficient#desc=Fourth order calibration coefficient.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL"."COEFF6" IS '#brief=sixth order calibration coefficient#desc=Fifth order calibration coefficient.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL"."COEFF7" IS '#brief=seventh order calibration coefficient#desc=Sixth order calibration coefficient.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL"."COEFF8" IS '#brief=eighth order calibration coefficient#desc=Seventh order calibration coefficient.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL"."ENERGY_UNITS" IS '#brief=energy units#desc=energy units#category=#ext=a3#na=#range=energy_units IN {MeV, keV}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL"."CNV_FACTOR" IS '#brief=conversion to keV#desc=conversion to keV#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL"."APE" IS '#brief=average prediction error, a measure of the average confidence interval for the calculated energy vs. channel regression (ECR) over the range of 100 keV#desc=average prediction error, a measure of the average confidence interval for the calculated energy vs. channel regression (ECR) over the range of 100 keV#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL"."DET" IS '#brief=determinant of the weighted design matrix, a measure of the spread of fitted data points and the error in the fitted points#desc=determinant of the weighted design matrix, a measure of the spread of fitted data points and the error in the fitted points#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL"."MSE" IS '#brief=mean-squared error of the fit, a measure of how large the residuals are#desc=mean-squared error of the fit, a measure of how large the residuals are#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL"."TSTAT" IS '#brief=percentage point of the t-statistic for Type I error with a probability set to 99%#desc=percentage point of the t-statistic for Type I error with a probability set to 99%#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL"."SCORE" IS '#brief=score used when comparing this ECR to other ECRs, a measure of both the ape and determinant#desc=score used when comparing this ECR to other ECRs, a measure of both the ape and determinant#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_ENERGY_CAL"  IS '#category=Automatic Processing#desc=The gards_energy_cal table contains efficiency calibration coefficients associated with spectra.  The equation is calculated during energy calibration update.';
 
--------------------------------------------------------
--  DDL for Table GARDS_ENERGY_CAL_COV
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_ENERGY_CAL_COV" 
   (	"SAMPLE_ID" NUMBER(22,0), 
	"ROW_INDEX" NUMBER(10,0), 
	"COL_INDEX" NUMBER(10,0), 
	"MODDATE" DATE DEFAULT SYSDATE, 
	"COEFF" FLOAT(22)
   ) ;
 
--------------------------------------------------------
--  DDL for Table GARDS_ENERGY_CAL_ORIG
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_ENERGY_CAL_ORIG" 
   (	"SAMPLE_ID" NUMBER, 
	"COEFF1" NUMBER, 
	"COEFF2" NUMBER, 
	"COEFF3" NUMBER, 
	"COEFF4" NUMBER, 
	"COEFF5" NUMBER, 
	"COEFF6" NUMBER, 
	"COEFF7" NUMBER, 
	"COEFF8" NUMBER, 
	"ENERGY_UNITS" CHAR(3), 
	"CNV_FACTOR" NUMBER, 
	"APE" NUMBER, 
	"DET" NUMBER, 
	"MSE" NUMBER, 
	"TSTAT" NUMBER, 
	"SCORE" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL_ORIG"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL_ORIG"."COEFF1" IS '#brief=first order calibration coefficient#desc=first order calibration coefficient#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL_ORIG"."COEFF2" IS '#brief=second order calibration coefficient#desc=First order calibration coefficient.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL_ORIG"."COEFF3" IS '#brief=third order calibration coefficient#desc=Second order calibration coefficient.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL_ORIG"."COEFF4" IS '#brief=fourth order calibration coefficient#desc=Third order calibration coefficient.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL_ORIG"."COEFF5" IS '#brief=fifth order calibration coefficient#desc=Fourth order calibration coefficient.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL_ORIG"."COEFF6" IS '#brief=sixth order calibration coefficient#desc=Fifth order calibration coefficient.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL_ORIG"."COEFF7" IS '#brief=seventh order calibration coefficient#desc=Sixth order calibration coefficient.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL_ORIG"."COEFF8" IS '#brief=eighth order calibration coefficient#desc=Seventh order calibration coefficient.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL_ORIG"."ENERGY_UNITS" IS '#brief=energy units#desc=energy units#category=#ext=a3#na=#range=energy_units IN {MeV, keV}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL_ORIG"."CNV_FACTOR" IS '#brief=conversion to keV#desc=conversion to keV#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL_ORIG"."APE" IS '#brief=average prediction error, a measure of the average confidence interval for the calculated energy vs. channel regression (ECR) over the range of 100 keV#desc=average prediction error, a measure of the average confidence interval for the calculated energy vs. channel regression (ECR) over the range of 100 keV#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL_ORIG"."DET" IS '#brief=determinant of the weighted design matrix, a measure of the spread of fitted data points and the error in the fitted points#desc=determinant of the weighted design matrix, a measure of the spread of fitted data points and the error in the fitted points#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL_ORIG"."MSE" IS '#brief=mean-squared error of the fit, a measure of how large the residuals are#desc=mean-squared error of the fit, a measure of how large the residuals are#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL_ORIG"."TSTAT" IS '#brief=percentage point of the t-statistic for Type I error with a probability set to 99%#desc=percentage point of the t-statistic for Type I error with a probability set to 99%#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL_ORIG"."SCORE" IS '#brief=score used when comparing this ECR to other ECRs, a measure of both the ape and determinant#desc=score used when comparing this ECR to other ECRs, a measure of both the ape and determinant#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_CAL_ORIG"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_ENERGY_CAL_ORIG"  IS '#category=Automatic Processing#desc=The gards_energy_cal_orig table contains original energy calibration equation information associated with samples (calculated using energy pair data).';
 
--------------------------------------------------------
--  DDL for Table GARDS_ENERGY_PAIRS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_ENERGY_PAIRS" 
   (	"SAMPLE_ID" NUMBER, 
	"CAL_ENERGY" NUMBER, 
	"CHANNEL" NUMBER, 
	"CAL_ERROR" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_PAIRS"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_PAIRS"."CAL_ENERGY" IS '#brief=calibration energy (keV)#desc=calibration energy (keV)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_PAIRS"."CHANNEL" IS '#brief=peak centroid channel #desc=peak centroid channel #category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_PAIRS"."CAL_ERROR" IS '#brief=uncertainty of channel#desc=Calibration energy.#category=#ext=#na=#range=#unit=keV';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_ENERGY_PAIRS"  IS '#category=Automatic Processing#desc=The gards_energy_pairs table contains energy calibration pairs information associated with the gamma axis of the spectrum.';
 
--------------------------------------------------------
--  DDL for Table GARDS_ENERGY_PAIRS_ORIG
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_ENERGY_PAIRS_ORIG" 
   (	"SAMPLE_ID" NUMBER, 
	"CAL_ENERGY" NUMBER, 
	"CHANNEL" NUMBER, 
	"CAL_ERROR" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_PAIRS_ORIG"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_PAIRS_ORIG"."CAL_ENERGY" IS '#brief=calibration energy (keV)#desc=calibration energy (keV)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_PAIRS_ORIG"."CHANNEL" IS '#brief=peak centroid channel #desc=peak centroid channel #category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_PAIRS_ORIG"."CAL_ERROR" IS '#brief=uncertainty of channel#desc=Calibration energy.#category=#ext=#na=#range=#unit=keV';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ENERGY_PAIRS_ORIG"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_ENERGY_PAIRS_ORIG"  IS '#category=Automatic Processing#desc=The gards_energy_pairs_orig table contains energy calibration pairs information associated with the gamma axis of the spectrum.  These values are as specified in the PHD file.';
 
--------------------------------------------------------
--  DDL for Table GARDS_ENERGY_PAIRS_TEMP
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_ENERGY_PAIRS_TEMP" 
   (	"SAMPLE_ID" NUMBER, 
	"CAL_ENERGY" NUMBER, 
	"CHANNEL" NUMBER, 
	"CAL_ERROR" NUMBER
   ) ;
 
--------------------------------------------------------
--  DDL for Table GARDS_FLAGS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_FLAGS" 
   (	"FLAG_ID" NUMBER(8,0), 
	"NAME" VARCHAR2(32), 
	"THRESHOLD" NUMBER, 
	"UNITS" VARCHAR2(16), 
	"TEST" VARCHAR2(8), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_FLAGS"."FLAG_ID" IS '#brief=unique identifier for an event screening test#desc=unique identifier for an event screening test#category=#ext=i8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_FLAGS"."NAME" IS '#brief=name of the event screening test#desc=Test name.#category=#ext=a32#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_FLAGS"."THRESHOLD" IS '#brief=value against which the results in the test column are compared#desc=value against which the results in the test column are compared#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_FLAGS"."UNITS" IS '#brief=units of the event screening test#desc=units of the event screening test#category=#ext=a16#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_FLAGS"."TEST" IS '#brief=calculated result of the test; this value is compared to the threshold value (examples are <, = , >, >=)#desc=calculated result of the test; this value is compared to the threshold value (examples are <, = , >, >=)#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_FLAGS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_FLAGS"  IS '#category=Automatic Processing#desc=The gards_flags table contains the name and thresholds for each of the tests run during rms_DBflags.';
 
--------------------------------------------------------
--  DDL for Table GARDS_FPE
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_FPE" 
   (	"FPID" NUMBER, 
	"REVID" NUMBER, 
	"DTG" DATE, 
	"SAMPLE_ID" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_FPE"."FPID" IS '#brief=unique fission product identifier#desc=unique fission product identifier#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_FPE"."REVID" IS '#brief=revision number#desc=revision number#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_FPE"."DTG" IS '#brief=data product generation date#desc=data product generation date#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_FPE"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_FPE"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_FPE"  IS '#category=Automatic Processing#desc=The gards_fpe table contains one record for each sample associated with a fission product event.';
 
--------------------------------------------------------
--  DDL for Table GARDS_IRF
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_IRF" 
   (	"DETECTOR_ID" NUMBER, 
	"ENERGY" NUMBER, 
	"IRF" NUMBER, 
	"IRF_ERROR" NUMBER, 
	"NUCLIDE_NAME" VARCHAR2(8), 
	"SUM_CORR" NUMBER, 
	"MODDATE" DATE DEFAULT SYSDATE, 
	"BEGIN_DATE" DATE, 
	"END_DATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_IRF"."DETECTOR_ID" IS '#brief=unique detector identifier#desc=unique detector identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_IRF"."ENERGY" IS '#brief=energy#desc=energy#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_IRF"."IRF" IS '#brief=isotope response function#desc=isotope response function#category=#ext=g17.5#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_IRF"."IRF_ERROR" IS '#brief=level of confidence#desc=level of confidence#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_IRF"."NUCLIDE_NAME" IS '#brief=nuclide name#desc=nuclide name#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_IRF"."SUM_CORR" IS '#brief=sum of the correlation#desc=sum of the correlation#category=#ext=f10.8#na=NOT ALLOWED#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_IRF"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_IRF"."BEGIN_DATE" IS '#brief=start date of bound applicability#desc=start date of bound applicability#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_IRF"."END_DATE" IS '#brief=end date of bound applicability#desc=end date of bound applicability#category=#ext=a21#na=01-Jan-3000#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_IRF"  IS '#category=Automatic Processing#desc=Thegards_irf table contains the isotope response function, its error and the summing corrections as a function of the energy for a given Nuclide and a given Detector.';
 
--------------------------------------------------------
--  DDL for Table GARDS_IRF_TT
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_IRF_TT" 
   (	"DETECTOR_ID" NUMBER, 
	"ENERGY" NUMBER, 
	"IRF" NUMBER, 
	"IRF_ERROR" NUMBER, 
	"NUCLIDE_NAME" VARCHAR2(8), 
	"SUM_CORR" NUMBER
   ) ;
 
--------------------------------------------------------
--  DDL for Table GARDS_LAB_CATEGORY_DESCRIPTION
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_LAB_CATEGORY_DESCRIPTION" 
   (	"LAB_SAMPLE_CATEGORY" VARCHAR2(2), 
	"DESCRIPTION" VARCHAR2(256), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_LAB_CATEGORY_DESCRIPTION"."LAB_SAMPLE_CATEGORY" IS '#brief=report sample category (A|B|C|D|E)#desc=report sample category (A|B|C|D|E)#category=#ext=a2#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_LAB_CATEGORY_DESCRIPTION"."DESCRIPTION" IS '#brief=description of the lab_sample_category#desc=description of the lab_sample_category#category=#ext=a256#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_LAB_CATEGORY_DESCRIPTION"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_LAB_CATEGORY_DESCRIPTION"  IS '#category=Automatic Processing#desc=the gards_lab_category_description table describes the different sample categories that can be sent to the IDC.';
 
--------------------------------------------------------
--  DDL for Table GARDS_MDAS2REPORT
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_MDAS2REPORT" 
   (	"NAME" VARCHAR2(8), 
	"TYPE" VARCHAR2(16), 
	"MDA_MIN" NUMBER, 
	"MDA_MAX" NUMBER, 
	"SAMPLE_TYPE" VARCHAR2(2), 
	"DTG_BEGIN" DATE, 
	"DTG_END" DATE, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_MDAS2REPORT"."NAME" IS '#brief=nuclide name #desc=Nuclide name.#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_MDAS2REPORT"."TYPE" IS '#brief=nuclide type: ACTIVATION, #desc=Nuclide type. Choices are: ACTIVATION, COSMIC, FISSION(G), FISSION(P), or NATURAL.#category=#ext=a16#na=#range=type IN {ACTIVATION, COSMIC, FISSION(G), FISSION(P), NATURAL}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_MDAS2REPORT"."MDA_MIN" IS '#brief=minimum bound for MDA range#desc=minimum bound for MDA range#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_MDAS2REPORT"."MDA_MAX" IS '#brief=maximum bound for MDA range#desc=maximum bound for MDA range#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_MDAS2REPORT"."SAMPLE_TYPE" IS '#brief=sample type#desc=sample type#category=#ext=a2#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_MDAS2REPORT"."DTG_BEGIN" IS '#brief=start date of bound applicability#desc=start date of bound applicability#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_MDAS2REPORT"."DTG_END" IS '#brief=end date of bound applicability#desc=end date of bound applicability#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_MDAS2REPORT"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_MDAS2REPORT"  IS '#category=Automatic Processing#desc=The gards_mdas2report table contains the list of nuclides which have their minimum detectable activities reported in radionuclide reports.';
 
--------------------------------------------------------
--  DDL for Table GARDS_NIC
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_NIC" 
   (	"SAMPLE_ID" NUMBER, 
	"STATION_ID" NUMBER, 
	"NAME" VARCHAR2(8), 
	"DTG" DATE, 
	"CATEGORY" NUMBER, 
	"CENTRAL_VALUE" NUMBER, 
	"DEL" NUMBER, 
	"UPPER_LIM" NUMBER, 
	"LOWER_LIM" NUMBER, 
	"SAMPLE_STATUS" VARCHAR2(1), 
	"ACTIVITY" NUMBER, 
	"HOLD" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NIC"."SAMPLE_ID" IS '#brief=unique sample identifier#desc=#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NIC"."STATION_ID" IS '#brief=unique station identifier#desc=#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NIC"."NAME" IS '#brief=obsolete#desc=#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NIC"."DTG" IS '#brief=obsolete#desc=#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NIC"."CATEGORY" IS '#brief=obsolete#desc=#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NIC"."CENTRAL_VALUE" IS '#brief=obsolete#desc=#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NIC"."DEL" IS '#brief=obsolete#desc=#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NIC"."UPPER_LIM" IS '#brief=obsolete#desc=#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NIC"."LOWER_LIM" IS '#brief=obsolete#desc=#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NIC"."SAMPLE_STATUS" IS '#brief=obsolete#desc=#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NIC"."ACTIVITY" IS '#brief=obsolete#desc=#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NIC"."HOLD" IS '#brief=obsolete#desc=#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NIC"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=Descriptive#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_NIC"  IS '#category=Automatic Processing#desc=obsolete. Replaced by rmsman.gards_sample_cat.';
 
--------------------------------------------------------
--  DDL for Table GARDS_NOTIFY
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_NOTIFY" 
   (	"EVENT" VARCHAR2(10), 
	"EMAIL_ADDR" VARCHAR2(80), 
	"DESCRIPTION" VARCHAR2(80), 
	"DTG_BEGIN" DATE, 
	"DTG_END" DATE, 
	"POC_ID" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NOTIFY"."EVENT" IS '#brief=type of occurrence (choices are: ALERT, FISS_FOUND, NIC_SIG34, NIC_SIG5, QC_ERROR, QC_WARNING, RADOPSCAL, RMS_ADMIN)#desc=type of occurrence (choices are: ALERT, FISS_FOUND, NIC_SIG34, NIC_SIG5, QC_ERROR, QC_WARNING, RADOPSCAL, RMS_ADMIN)#category=#ext=a10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NOTIFY"."EMAIL_ADDR" IS '#brief=recipient email addresses#desc=recipient email addresses#category=#ext=a80#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NOTIFY"."DESCRIPTION" IS '#brief=general description of occurrence#desc=general description of occurrence#category=#ext=a80#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NOTIFY"."DTG_BEGIN" IS '#brief=notification initialization date#desc=notification initialization date#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NOTIFY"."DTG_END" IS '#brief=notification termination date#desc=Start date of applicability, notification initialization date, or the reporting period.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NOTIFY"."POC_ID" IS '#brief=unique point of contact identifier#desc=unique point of contact identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NOTIFY"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_NOTIFY"  IS '#category=Automatic Processing#desc=The gards_notify table contains contact information for specific events. When the event occurs a message is automatically sent to the email_addr of the specified recipient.';
 
--------------------------------------------------------
--  DDL for Table GARDS_NOTIFY_BAK
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_NOTIFY_BAK" 
   (	"EVENT" VARCHAR2(10), 
	"EMAIL_ADDR" VARCHAR2(80), 
	"DESCRIPTION" VARCHAR2(80), 
	"DTG_BEGIN" DATE, 
	"DTG_END" DATE, 
	"POC_ID" NUMBER, 
	"MODDATE" DATE
   ) ;
 
--------------------------------------------------------
--  DDL for Table GARDS_NUCL2QUANTIFY
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_NUCL2QUANTIFY" 
   (	"NAME" VARCHAR2(8), 
	"DTG_BEGIN" DATE, 
	"DTG_END" DATE, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL2QUANTIFY"."NAME" IS '#brief=nuclide name #desc=Nuclide name.#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL2QUANTIFY"."DTG_BEGIN" IS '#brief=start of reporting period#desc=start of reporting period#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL2QUANTIFY"."DTG_END" IS '#brief=end of reporting period#desc=Start date of applicability, notification initialization date, or the reporting period.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL2QUANTIFY"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_NUCL2QUANTIFY"  IS '#category=Automatic Processing#desc=The gards_nucl2quantify table contains natural radionuclides quantified in radionuclide related reports.';
 
--------------------------------------------------------
--  DDL for Table GARDS_NUCL_IDED
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_NUCL_IDED" 
   (	"SAMPLE_ID" NUMBER, 
	"STATION_ID" NUMBER, 
	"DETECTOR_ID" NUMBER, 
	"NUCLIDE_ID" NUMBER, 
	"NAME" VARCHAR2(8), 
	"TYPE" VARCHAR2(16), 
	"HALFLIFE" VARCHAR2(23), 
	"AVE_ACTIV" NUMBER, 
	"AVE_ACTIV_ERR" NUMBER, 
	"ACTIV_KEY" NUMBER, 
	"ACTIV_KEY_ERR" NUMBER, 
	"MDA" NUMBER, 
	"MDA_ERR" NUMBER, 
	"NID_FLAG" NUMBER, 
	"ACTIV_DECAY" NUMBER, 
	"ACTIV_DECAY_ERR" NUMBER, 
	"COMP_CONFID" NUMBER, 
	"REPORT_MDA" NUMBER, 
	"PD_MOD_FLAG" NUMBER, 
	"CSC_RATIO" NUMBER, 
	"CSC_RATIO_ERR" NUMBER, 
	"CSC_MOD_FLAG" NUMBER, 
	"MODDATE" DATE
   ) ENABLE ROW MOVEMENT ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED"."SAMPLE_ID" IS '#brief=sample identifier #desc=sample identifier #category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED"."STATION_ID" IS '#brief=station identifier #desc=station identifier #category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED"."DETECTOR_ID" IS '#brief=unique detector identifier#desc=unique detector identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED"."NUCLIDE_ID" IS '#brief=nuclide identifier#desc=Flag, nuclide identification indicator.#category=#ext=#na=#range=nid_flag IN {-1, 0, 1, 2}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED"."NAME" IS '#brief=nuclide name Canberra Parameter: CAM_T_NCLNAME #desc=Nuclide name.#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED"."TYPE" IS '#brief=nuclide type (choices are: ACTIVATION, COSMIC, FISSION(G), FISSION(P), or NATURAL) Canberra param: CAM_T_NCLSBHDR#desc=Nuclide type. Choices are: ACTIVATION, COSMIC, FISSION(G), FISSION(P), or NATURAL.#category=#ext=a16#na=#range=type IN {ACTIVATION, COSMIC, FISSION(G), FISSION(P), NATURAL}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED"."HALFLIFE" IS '#brief=half-life in seconds (S), hours (H), days (D), or years (Y) Canberra Parameter: CAM_T_NCLHLFLIFE#desc=half-life in seconds (S), hours (H), days (D), or years (Y) Canberra Parameter: CAM_T_NCLHLFLIFE#category=#ext=a23#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED"."AVE_ACTIV" IS '#brief=average activity for nuclide (mBq/m3) Canberra Parameter: CAM_T_NCLWTMEAN#desc=average activity for nuclide (mBq/m3) Canberra Parameter: CAM_T_NCLWTMEAN#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED"."AVE_ACTIV_ERR" IS '#brief=uncertainty in average activity (mBq/m3) Canberra Parameter: CAM_T_NCLWTMERR#desc=Sample activity concentration of a specific radionuclide calculated by averaging all activity values.#category=#ext=#na=#range=#unit=mBq/m3';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED"."ACTIV_KEY" IS '#brief=key-line activity (mBq/m3) Canberra Parameter: CAM_G_NCLACTVTY#desc=key-line activity (mBq/m3) Canberra Parameter: CAM_G_NCLACTVTY#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED"."ACTIV_KEY_ERR" IS '#brief=uncertainty of key-line activity (mBq/m3) Canberra Parameter: CAM_G_NCLEER#desc=Activity concentration of a radionuclide determined through the analysis of the key gamma photopeak.#category=#ext=#na=#range=#unit=mBq/m3';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED"."MDA" IS '#brief=minimum detectable activity (mBq/m3) Canberra Parameter: CAM_G_NCLMDA#desc=minimum detectable activity (mBq/m3) Canberra Parameter: CAM_G_NCLMDA#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED"."MDA_ERR" IS '#brief=minimum detectable activity uncertainty (mBq/m3) Canberra Parameter: CAM_G_NCLMDAERR#desc=Minimum detectable activity.#category=#ext=#na=#range=mda >= 0.0#unit=mBq/m3 mBq/m3 for gards_roi_concs';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED"."NID_FLAG" IS '#brief=nuclide identification indicator (0 = nuclide was not identified by automated analysis; 1 = nuclide was identified by automated analysis; -1 = nuclide was identified initially by automated analysis but later rejected because the concentration was < 0.0; 2 = nuclide was identified by automated analysis but was removed by the analyst through the Inspectra) Canberra Parameter: CAM_G_NCLFIDENT#desc=nuclide identification indicator (0 = nuclide was not identified by automated analysis; 1 = nuclide was identified by automated analysis; -1 = nuclide was identified initially by automated analysis but later rejected because the concentration was < 0.0; 2 = nuclide was identified by automated analysis but was removed by the analyst through the Inspectra) Canberra Parameter: CAM_G_NCLFIDENT#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED"."ACTIV_DECAY" IS '#brief=activity decay factor Canberra Parameter: CAM_G_NCLDECAY#desc=activity decay factor Canberra Parameter: CAM_G_NCLDECAY#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED"."ACTIV_DECAY_ERR" IS '#brief=uncertainty in activity decay Canberra Parameter: CAM_F_NCLDECAYERR#desc=Activity decay factor.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED"."COMP_CONFID" IS '#brief=computed confidence index Canberra Parameter: CAM_F_NCLCONFID#desc=computed confidence index Canberra Parameter: CAM_F_NCLCONFID#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED"."REPORT_MDA" IS '#brief=indicator of whether MDA is to be reported#desc=indicator of whether MDA is to be reported#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED"."PD_MOD_FLAG" IS '#brief=flag indicating whether or not the nuclide''s activity was modified by the parent/daughter calculation. #desc=Flag indicating whether or not the nuclide''s activity was modified by the parent/daughter calculation. A value of 1= nuclide was modified, zero indicates that the nuclide was not modified.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED"."CSC_RATIO" IS '#brief=multiplier used by analysis to update active_key and mda#desc=flag that indicates if cascade summing modified a nuclide: 1 = nuclide was modified, 0 = nuclide was not modified.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED"."CSC_RATIO_ERR" IS '#brief=uncertainty in csc_ratio#desc=multiplier used by analysis to update activ_key and mda.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED"."CSC_MOD_FLAG" IS '#brief=flag that indicates if cascade summing modified a nuclide: 1 = nuclide was modified, 0 = nuclide was not modified#desc=flag that indicates if cascade summing modified a nuclide: 1 = nuclide was modified, 0 = nuclide was not modified#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_NUCL_IDED"  IS '#category=Automatic Processing#desc=The gards_nucl_ided table contains information regarding nuclides identified during interactive review.';
 
--------------------------------------------------------
--  DDL for Table GARDS_NUCL_IDED_ORIG
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_NUCL_IDED_ORIG" 
   (	"SAMPLE_ID" NUMBER, 
	"STATION_ID" NUMBER, 
	"DETECTOR_ID" NUMBER, 
	"NUCLIDE_ID" NUMBER, 
	"NAME" VARCHAR2(8), 
	"TYPE" VARCHAR2(16), 
	"HALFLIFE" VARCHAR2(23), 
	"AVE_ACTIV" NUMBER, 
	"AVE_ACTIV_ERR" NUMBER, 
	"ACTIV_KEY" NUMBER, 
	"ACTIV_KEY_ERR" NUMBER, 
	"MDA" NUMBER, 
	"MDA_ERR" NUMBER, 
	"NID_FLAG" NUMBER, 
	"ACTIV_DECAY" NUMBER, 
	"ACTIV_DECAY_ERR" NUMBER, 
	"COMP_CONFID" NUMBER, 
	"REPORT_MDA" NUMBER, 
	"PD_MOD_FLAG" NUMBER, 
	"CSC_RATIO" NUMBER, 
	"CSC_RATIO_ERR" NUMBER, 
	"CSC_MOD_FLAG" NUMBER, 
	"MODDATE" DATE
   ) ENABLE ROW MOVEMENT ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED_ORIG"."SAMPLE_ID" IS '#brief=sample identifier #desc=sample identifier #category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED_ORIG"."STATION_ID" IS '#brief=station identifier #desc=station identifier #category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED_ORIG"."DETECTOR_ID" IS '#brief=unique detector identifier#desc=unique detector identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED_ORIG"."NUCLIDE_ID" IS '#brief=identification code of associated nuclide #desc=Flag, nuclide identification indicator.#category=#ext=#na=#range=nid_flag IN {-1, 0, 1, 2}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED_ORIG"."NAME" IS '#brief=nuclide name Canberra Parameter: CAM_T_NCLNAME #desc=Nuclide name.#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED_ORIG"."TYPE" IS '#brief=nuclide type (choices are: ACTIVATION, COSMIC, FISSION(G), FISSION(P), or NATURAL) Canberra Parameter: CAM_T_NCLSBHDR#desc=Nuclide type. Choices are: ACTIVATION, COSMIC, FISSION(G), FISSION(P), or NATURAL.#category=#ext=a16#na=#range=type IN {ACTIVATION, COSMIC, FISSION(G), FISSION(P), NATURAL}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED_ORIG"."HALFLIFE" IS '#brief=half-life in seconds (S), hours (H), minutes (M), or years (Y) Canberra Parameter: CAM_T_NCLHLFLIFE#desc=half-life in seconds (S), hours (H), minutes (M), or years (Y) Canberra Parameter: CAM_T_NCLHLFLIFE#category=#ext=a23#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED_ORIG"."AVE_ACTIV" IS '#brief=average activity for nuclide (mBq/m3) Canberra Parameter: CAM_T_NCLWTMEAN#desc=average activity for nuclide (mBq/m3) Canberra Parameter: CAM_T_NCLWTMEAN#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED_ORIG"."AVE_ACTIV_ERR" IS '#brief=uncertainty in average activity (mBq/m3) Canberra Parameter: CAM_T_NUCLWTMERR#desc=Sample activity concentration of a specific radionuclide calculated by averaging all activity values.#category=#ext=#na=#range=#unit=mBq/m3';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED_ORIG"."ACTIV_KEY" IS '#brief=activity of key-line (mBq/m3) Canberra Parameter: CAM_G_NCLACTVTY#desc=activity of key-line (mBq/m3) Canberra Parameter: CAM_G_NCLACTVTY#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED_ORIG"."ACTIV_KEY_ERR" IS '#brief=uncertainty of key-line activity (mBq/m3) Canberra Parameter: CAM_G_NCLERR#desc=Activity concentration of a radionuclide determined through the analysis of the key gamma photopeak.#category=#ext=#na=#range=#unit=mBq/m3';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED_ORIG"."MDA" IS '#brief=minimum detectable activity (mBq/m3) Canberra Parameter: CAM_G_NCLMDA#desc=minimum detectable activity (mBq/m3) Canberra Parameter: CAM_G_NCLMDA#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED_ORIG"."MDA_ERR" IS '#brief=minimum detectable activity error (mBq/m3) Canberra Parameter: CAM_G_NCLMDAERR#desc=Minimum detectable activity.#category=#ext=#na=#range=mda >= 0.0#unit=mBq/m3 mBq/m3 for gards_roi_concs';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED_ORIG"."NID_FLAG" IS '#brief=nuclide identification indicator (0 or 1)#desc=nuclide identification indicator (0 = nuclide was not identified by automated analysis; 1 = nuclide was identified by automated analysis; -1 = nuclide was identified initially by automated analysis but later rejected because the concentration was < 0.0; 2 = nuclide was identified by automated analysis but was removed by the analyst through Inspectra) Canberra Parameter: CAM_G_NCLFIDENT#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED_ORIG"."ACTIV_DECAY" IS '#brief=activity decay factor Canberra Parameter: CAM_G_NCLDECAY#desc=activity decay factor Canberra Parameter: CAM_G_NCLDECAY#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED_ORIG"."ACTIV_DECAY_ERR" IS '#brief=uncertainty of activity decay Canberra Parameter: CAM_F_NCLDECAYERR#desc=Activity decay factor.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED_ORIG"."COMP_CONFID" IS '#brief=computed confidence index Canberra Parameter: CAM_F_NCLCONFID#desc=computed confidence index Canberra Parameter: CAM_F_NCLCONFID#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED_ORIG"."REPORT_MDA" IS '#brief=indicator of whether MDA is to be reported#desc=indicator of whether MDA is to be reported#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED_ORIG"."PD_MOD_FLAG" IS '#brief=flag indicating whether or not the nuclide''s activity was modified by the parent/daughter calculation. #desc=flag indicating whether or not the nuclide''s activity was modified by the parent/daughter calculation. #category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED_ORIG"."CSC_RATIO" IS '#brief=modifier used by analysis to update active_key and mda#desc=modifier used by analysis to update active_key and mda#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED_ORIG"."CSC_RATIO_ERR" IS '#brief=confidence level#desc=confidence level#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED_ORIG"."CSC_MOD_FLAG" IS '#brief=flag indicating whether or not the nuclide''s activity was modified by the cascade summing. #desc=Flag indicating whether or not the nuclide''s activity was modified by the cascade summing. A value of 1= nuclide was modified, zero indicates that the nuclide was not modified.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_IDED_ORIG"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_NUCL_IDED_ORIG"  IS '#category=Automatic Processing#desc=The gards_nucl_ided_orig table contains information regarding nuclides identified during automated analysis.';
 
--------------------------------------------------------
--  DDL for Table GARDS_NUCL_LIB
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_NUCL_LIB" 
   (	"NUCLIDE_ID" NUMBER, 
	"NAME" VARCHAR2(8), 
	"TYPE" VARCHAR2(16), 
	"HALFLIFE_SEC" NUMBER, 
	"HALFLIFE" VARCHAR2(23), 
	"HALFLIFE_ERR" VARCHAR2(23), 
	"NUM_LINES" NUMBER, 
	"MODDATE" DATE, 
	"NUC_COMMENT" VARCHAR2(1500)
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LIB"."NUCLIDE_ID" IS '#brief=nuclide identifier #desc=nuclide identifier #category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LIB"."NAME" IS '#brief=nuclide name#desc=Nuclide name.#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LIB"."TYPE" IS '#brief=nuclide type (ACTIVATION, COSMIC, FISSION(G), FISSION(P), or NATURAL)#desc=Nuclide type. Choices are: ACTIVATION, COSMIC, FISSION(G), FISSION(P), or NATURAL.#category=#ext=a16#na=#range=type IN {ACTIVATION, COSMIC, FISSION(G), FISSION(P), NATURAL}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LIB"."HALFLIFE_SEC" IS '#brief=half-life in seconds#desc=Uncertainty of halflife.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LIB"."HALFLIFE" IS '#brief=half-life#desc=half-life#category=#ext=a23#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LIB"."HALFLIFE_ERR" IS '#brief=uncertainty of half-life#desc=uncertainty of half-life#category=#ext=a23#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LIB"."NUM_LINES" IS '#brief=number of nuclide lines in library#desc=number of nuclide lines in library#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LIB"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LIB"."NUC_COMMENT" IS '#brief=nuclide comment#desc=nuclide comment#category=#ext=a15#na=#range=#unit=';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_NUCL_LIB"  IS '#category=Automatic Processing#desc=The gards_nucl_lib table contains nuclide library information used by the Inspectra when displaying nuclide data for particulate stations.';
 
--------------------------------------------------------
--  DDL for Table GARDS_NUCL_LIB_BACKUP
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_NUCL_LIB_BACKUP" 
   (	"NUCLIDE_ID" NUMBER, 
	"NAME" VARCHAR2(8), 
	"TYPE" VARCHAR2(16), 
	"HALFLIFE_SEC" NUMBER, 
	"HALFLIFE" VARCHAR2(23), 
	"HALFLIFE_ERR" VARCHAR2(23), 
	"NUM_LINES" NUMBER, 
	"MODDATE" DATE, 
	"NUC_COMMENT" VARCHAR2(1500)
   ) ;
 
--------------------------------------------------------
--  DDL for Table GARDS_NUCL_LINES_IDED
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_NUCL_LINES_IDED" 
   (	"SAMPLE_ID" NUMBER, 
	"STATION_ID" NUMBER, 
	"DETECTOR_ID" NUMBER, 
	"NAME" VARCHAR2(8), 
	"ENERGY" NUMBER, 
	"ENERGY_ERR" NUMBER, 
	"ABUNDANCE" NUMBER, 
	"ABUNDANCE_ERR" NUMBER, 
	"PEAK" NUMBER, 
	"ACTIVITY" NUMBER, 
	"ACTIV_ERR" NUMBER, 
	"EFFIC" NUMBER, 
	"EFFIC_ERR" NUMBER, 
	"MDA" NUMBER, 
	"KEY_FLAG" NUMBER, 
	"NUCLIDE_ID" NUMBER, 
	"CSC_RATIO" NUMBER, 
	"CSC_RATIO_ERR" NUMBER, 
	"CSC_MOD_FLAG" NUMBER, 
	"MODDATE" DATE, 
	"ID_PERCENT" NUMBER
   ) ENABLE ROW MOVEMENT ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED"."SAMPLE_ID" IS '#brief=sample identifier #desc=sample identifier #category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED"."STATION_ID" IS '#brief=station identifier #desc=station identifier #category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED"."DETECTOR_ID" IS '#brief=unique detector identifier#desc=unique detector identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED"."NAME" IS '#brief=nuclide name Canberra Parameter: CAM_T_NCLNAME#desc=Nuclide name.#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED"."ENERGY" IS '#brief=line energy (keV) Canberra Parameter: CAM_F_NLENERGY#desc=line energy (keV) Canberra Parameter: CAM_F_NLENERGY#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED"."ENERGY_ERR" IS '#brief=uncertainty in line energy Canberra Parameter: CAM_F_NLENGERR#desc=Line energy.#category=#ext=#na=#range=0 <= energy#unit=keV';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED"."ABUNDANCE" IS '#brief=abundance of line (percent) Canberra Parameter: CAM_F_NLABUN#desc=Abundance of line.#category=#ext=#na=#range=#unit=percent';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED"."ABUNDANCE_ERR" IS '#brief=uncertainty of abundance (percent) Canberra Parameter: CAM_F_NLABUNERR#desc=uncertainty of abundance (percent) Canberra Parameter: CAM_F_NLABUNERR#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED"."PEAK" IS '#brief=peak identifier Canberra Parameter: CAM_L_NLPEAK#desc=peak identifier Canberra Parameter: CAM_L_NLPEAK#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED"."ACTIVITY" IS '#brief=line activity (mBq/m3) Canberra Parameter: CAM_G_NLACTVTY#desc=Line activity.#category=#ext=#na=#range=#unit=mBq/m3';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED"."ACTIV_ERR" IS '#brief=percent uncertainty of line activity Canberra Parameter: CAM_G_NLERR#desc=percent uncertainty of line activity Canberra Parameter: CAM_G_NLERR#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED"."EFFIC" IS '#brief=efficiency at energy Canberra Parameter: CAM_F_NLEFFICIENCY#desc=efficiency at energy Canberra Parameter: CAM_F_NLEFFICIENCY#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED"."EFFIC_ERR" IS '#brief=uncertainty of efficiency Canberra Parameter: CAM_F_NLEFFERR#desc=uncertainty of efficiency Canberra Parameter: CAM_F_NLEFFERR#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED"."MDA" IS '#brief=minimum detectable activity (mBq/m3) Canberra Parameter: CAM_F_NLMDA#desc=minimum detectable activity (mBq/m3) Canberra Parameter: CAM_F_NLMDA#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED"."KEY_FLAG" IS '#brief=key line indicator Canberra Parameter: CAM_V_NLF_KEYLINE#desc=key line indicator Canberra Parameter: CAM_V_NLF_KEYLINE#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED"."NUCLIDE_ID" IS '#brief=nuclide number associated with line number Canberra Parameter: CAM_L_NLNUCL#desc=nuclide number associated with line number Canberra Parameter: CAM_L_NLNUCL#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED"."CSC_RATIO" IS '#brief=multiplier used by analysis to update activ_key and mda#desc=flag that indicates if cascade summing modified a nuclide: 1 = nuclide was modified, 0 = nuclide was not modified.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED"."CSC_RATIO_ERR" IS '#brief=uncertainty in csc_ratio#desc=multiplier used by analysis to update activ_key and mda.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED"."CSC_MOD_FLAG" IS '#brief=flag that indicates if cascade summing modified a nuclide: 1 = nuclide was modified, 0 = nuclide was not modified.#desc=flag that indicates if cascade summing modified a nuclide: 1 = nuclide was modified, 0 = nuclide was not modified.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED"."ID_PERCENT" IS '#brief=nuclide percentage#desc=nuclide percentage#category=#ext=#na=#range=#unit=';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_NUCL_LINES_IDED"  IS '#category=Automatic Processing#desc=The gards_nucl_lines_ided table contains auxiliary information regarding lines identified by interactive review.';
 
--------------------------------------------------------
--  DDL for Table GARDS_NUCL_LINES_IDED_ORIG
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG" 
   (	"SAMPLE_ID" NUMBER, 
	"STATION_ID" NUMBER, 
	"DETECTOR_ID" NUMBER, 
	"NAME" VARCHAR2(8), 
	"ENERGY" NUMBER, 
	"ENERGY_ERR" NUMBER, 
	"ABUNDANCE" NUMBER, 
	"ABUNDANCE_ERR" NUMBER, 
	"PEAK" NUMBER, 
	"ACTIVITY" NUMBER, 
	"ACTIV_ERR" NUMBER, 
	"EFFIC" NUMBER, 
	"EFFIC_ERR" NUMBER, 
	"MDA" NUMBER, 
	"KEY_FLAG" NUMBER, 
	"NUCLIDE_ID" NUMBER, 
	"CSC_RATIO" NUMBER, 
	"CSC_RATIO_ERR" NUMBER, 
	"CSC_MOD_FLAG" NUMBER, 
	"MODDATE" DATE, 
	"ID_PERCENT" NUMBER
   ) ENABLE ROW MOVEMENT ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG"."SAMPLE_ID" IS '#brief=sample identifier #desc=sample identifier #category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG"."STATION_ID" IS '#brief=station identifier #desc=station identifier #category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG"."DETECTOR_ID" IS '#brief=unique detector identifier#desc=unique detector identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG"."NAME" IS '#brief=nuclide name Canberra Parameter: CAM_T_NCLNAME#desc=Nuclide name.#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG"."ENERGY" IS '#brief=line energy (keV) Canberra Parameter: CAM_F_NLENERGY#desc=line energy (keV) Canberra Parameter: CAM_F_NLENERGY#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG"."ENERGY_ERR" IS '#brief=uncertainty of line energy Canberra Parameter: CAM_F_NLENGERR#desc=Line energy.#category=#ext=#na=#range=0 <= energy#unit=keV';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG"."ABUNDANCE" IS '#brief=abundance of line (percent) Canberra Parameter: CAM_F_NLABUN#desc=Abundance of line.#category=#ext=#na=#range=#unit=percent';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG"."ABUNDANCE_ERR" IS '#brief=uncertainty of abundance (percent) Canberra Parameter: CAM_F_NLABUNERR#desc=uncertainty of abundance (percent) Canberra Parameter: CAM_F_NLABUNERR#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG"."PEAK" IS '#brief=peak associated with line Canberra Parameter: CAM_L_NLPEAK#desc=peak associated with line Canberra Parameter: CAM_L_NLPEAK#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG"."ACTIVITY" IS '#brief=line activity (mBq/m3) #desc=line activity (mBq/m3) Canberra Parameter: CAM_G_NLACTVTY#category=#ext=#na=#range=#unit=mBq/m3';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG"."ACTIV_ERR" IS '#brief=percent uncertainty of line activity Canberra Parameter: CAM_G_NLERR#desc=percent uncertainty of line activity Canberra Parameter: CAM_G_NLERR#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG"."EFFIC" IS '#brief=efficiency at energy Canberra Parameter: CAM_F_NLEFFICIENCY#desc=efficiency at energy Canberra Parameter: CAM_F_NLEFFICIENCY#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG"."EFFIC_ERR" IS '#brief=uncertainty of efficiency Canberra Parameter: CAM_F_NLEFFERR#desc=uncertainty of efficiency Canberra Parameter: CAM_F_NLEFFERR#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG"."MDA" IS '#brief=minimum detectable activity (mBq/m3) Canberra Parameter: CAM_F_NLMDA#desc=minimum detectable activity (mBq/m3) Canberra Parameter: CAM_F_NLMDA#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG"."KEY_FLAG" IS '#brief=key line indicator Canberra Parameter: CAM_V_NLF_KEYLINE#desc=key line indicator Canberra Parameter: CAM_V_NLF_KEYLINE#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG"."NUCLIDE_ID" IS '#brief=nuclide number associated with line number Canberra Parameter: CAM_L_NLNUCL#desc=nuclide number associated with line number Canberra Parameter: CAM_L_NLNUCL#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG"."CSC_RATIO" IS '#brief=modifier used by analysis to update active_key and mda#desc=modifier used by analysis to update active_key and mda#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG"."CSC_RATIO_ERR" IS '#brief=confidence level#desc=confidence level#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG"."CSC_MOD_FLAG" IS '#brief=flag indicating whether or not the nuclide activity was modified by the cascade summing. #desc=flag indicating whether or not the nuclide activity was modified by the cascade summing. #category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG"."ID_PERCENT" IS '#brief=nuclide percentage#desc=nuclide percentage#category=#ext=#na=#range=#unit=';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG"  IS '#category=Automatic Processing#desc=The gards_nucl_lines_ided_orig table contains information regarding lines identified during automated analysis.';
 
--------------------------------------------------------
--  DDL for Table GARDS_NUCL_LINES_LIB
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_NUCL_LINES_LIB" 
   (	"NAME" VARCHAR2(8), 
	"ENERGY" NUMBER, 
	"ENERGY_ERR" NUMBER, 
	"ABUNDANCE" NUMBER, 
	"ABUNDANCE_ERR" NUMBER, 
	"KEY_FLAG" NUMBER, 
	"NUCLIDE_ID" NUMBER, 
	"MODDATE" DATE, 
	"LINECOMMENT" VARCHAR2(1500)
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_LIB"."NAME" IS '#brief=nuclide name#desc=Nuclide name.#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_LIB"."ENERGY" IS '#brief=line energy (keV) Canberra Parameter: CAM_F_NLENERGY#desc=line energy (keV) Canberra Parameter: CAM_F_NLENERGY#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_LIB"."ENERGY_ERR" IS '#brief=uncertainty of line energy Canberra Parameter: CAM_F_NLENGERR#desc=Line energy.#category=#ext=#na=#range=0 <= energy#unit=keV';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_LIB"."ABUNDANCE" IS '#brief=abundance of line (percent) Canberra Parameter: CAM_F_NLABUN#desc=Abundance of line.#category=#ext=#na=#range=#unit=percent';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_LIB"."ABUNDANCE_ERR" IS '#brief=uncertainty of abundance (percent) Canberra Parameter: CAM_F_NLABUNERR#desc=uncertainty of abundance (percent) Canberra Parameter: CAM_F_NLABUNERR#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_LIB"."KEY_FLAG" IS '#brief=key line indicator Canberra Parameter: CAM_V_NLF_KEYLINE#desc=key line indicator Canberra Parameter: CAM_V_NLF_KEYLINE#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_LIB"."NUCLIDE_ID" IS '#brief=nuclide number associated with line number Canberra Parameter: CAM_L_NLNUCL#desc=nuclide number associated with line number Canberra Parameter: CAM_L_NLNUCL#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_LIB"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_NUCL_LINES_LIB"."LINECOMMENT" IS '#brief=comment associated with nuclide line#desc=comment associated with nuclide line#category=#ext=a15#na=#range=#unit=';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_NUCL_LINES_LIB"  IS '#category=Automatic Processing#desc=The gards_nucl_lines_lib table contains library information used in particulate nuclide identification process.';
 
--------------------------------------------------------
--  DDL for Table GARDS_NUCL_LINES_LIB_BACKUP
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_NUCL_LINES_LIB_BACKUP" 
   (	"NAME" VARCHAR2(8), 
	"ENERGY" NUMBER, 
	"ENERGY_ERR" NUMBER, 
	"ABUNDANCE" NUMBER, 
	"ABUNDANCE_ERR" NUMBER, 
	"KEY_FLAG" NUMBER, 
	"NUCLIDE_ID" NUMBER, 
	"MODDATE" DATE, 
	"LINECOMMENT" VARCHAR2(1500)
   ) ;
 
--------------------------------------------------------
--  DDL for Table GARDS_PEAKS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_PEAKS" 
   (	"SAMPLE_ID" NUMBER, 
	"PEAK_ID" NUMBER, 
	"CENTROID" NUMBER, 
	"CENTROID_ERR" NUMBER, 
	"ENERGY" NUMBER, 
	"ENERGY_ERR" NUMBER, 
	"LEFT_CHAN" NUMBER, 
	"WIDTH" NUMBER, 
	"BACK_COUNT" NUMBER, 
	"BACK_UNCER" NUMBER, 
	"FWHM" NUMBER, 
	"FWHM_ERR" NUMBER, 
	"AREA" NUMBER, 
	"AREA_ERR" NUMBER, 
	"ORIGINAL_AREA" NUMBER, 
	"ORIGINAL_UNCER" NUMBER, 
	"COUNTS_SEC" NUMBER, 
	"COUNTS_SEC_ERR" NUMBER, 
	"EFFICIENCY" NUMBER, 
	"EFF_ERROR" NUMBER, 
	"BACK_CHANNEL" NUMBER, 
	"IDED" NUMBER, 
	"FITTED" NUMBER, 
	"MULTIPLET" NUMBER, 
	"LC" NUMBER, 
	"PEAK_SIG" NUMBER, 
	"PEAK_TOL" NUMBER, 
	"PSS" NUMBER, 
	"MODDATE" DATE, 
	"DETECTABILITY" NUMBER
   ) ENABLE ROW MOVEMENT ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."SAMPLE_ID" IS '#brief=sample identifier #desc=sample identifier #category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."PEAK_ID" IS '#brief=peak identifier#desc=peak identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."CENTROID" IS '#brief=peak centroid (channels) Canberra Parameter: CAM_F_PSCENTRD#desc=peak centroid (channels) Canberra Parameter: CAM_F_PSCENTRD#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."CENTROID_ERR" IS '#brief=uncertainty of peak centroid Canberra Parameter: CAM_F_PSDCENTRD#desc=Peak centroid energy.#category=#ext=#na=#range=0.0 <= centroid#unit=KeV';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."ENERGY" IS '#brief=energy at peak centroid (keV) Canberra Parameter: CAM_F_PSENERGY#desc=energy at peak centroid (keV) Canberra Parameter: CAM_F_PSENERGY#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."ENERGY_ERR" IS '#brief=uncertainty of energy (keV) Canberra Parameter: CAM_F_PSDENERGY#desc=Line energy.#category=#ext=#na=#range=0 <= energy#unit=keV';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."LEFT_CHAN" IS '#brief=left channel of peak Canberra Parameter: CAM_L_PSLEFT#desc=left channel of peak Canberra Parameter: CAM_L_PSLEFT#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."WIDTH" IS '#brief=width of peak (channels) Canberra Parameter: CAM_L_PSWIDTH#desc=width of peak (channels) Canberra Parameter: CAM_L_PSWIDTH#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."BACK_COUNT" IS '#brief=continuum background counts Canberra Parameter: CAM_F_PSBACKGND#desc=Average number of background channels.#category=#ext=#na=#range=0.0 <= back_channel#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."BACK_UNCER" IS '#brief=uncertainty in continuum background counts Canberra Parameter: CAM_F_PSBACK#desc=uncertainty in continuum background counts Canberra Parameter: CAM_F_PSBACK#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."FWHM" IS '#brief=full width at half maximum Canberra Parameter: CAM_F_PSFWHM#desc=full width at half maximum Canberra Parameter: CAM_F_PSFWHM#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."FWHM_ERR" IS '#brief=uncertainty of full width at half maximum Canberra Parameter: CAM_F_PSDFWHM#desc=Peak width at half the maximum peak height.#category=#ext=#na=#range=0.0 <= fwhm#unit=keV';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."AREA" IS '#brief=peak area (counts) Canberra Parameter: CAM_F_PSAREA#desc=peak area (counts) Canberra Parameter: CAM_F_PSAREA#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."AREA_ERR" IS '#brief=uncertainty of peak area (counts) Canberra Parameter: CAM_F_PSDAREA#desc=uncertainty of peak area (counts) Canberra Parameter: CAM_F_PSDAREA#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."ORIGINAL_AREA" IS '#brief=original peak area (counts) Canberra Parameter: CAM_F_PSORIGAREA#desc=original peak area (counts) Canberra Parameter: CAM_F_PSORIGAREA#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."ORIGINAL_UNCER" IS '#brief=uncertainty of original peak area (counts)#desc=uncertainty of original peak area (counts) Canberra Parameter: CAM_F_PSORIGERR#category=#ext=#na=#range=original_area > 0#unit=counts';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."COUNTS_SEC" IS '#brief=counts per second#desc=counts per second#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."COUNTS_SEC_ERR" IS '#brief=error in counts per second#desc=error in counts per second#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."EFFICIENCY" IS '#brief=efficiency Canberra Parameter: CAM_F_PSEFF#desc=efficiency Canberra Parameter: CAM_F_PSEFF#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."EFF_ERROR" IS '#brief=uncertainty of efficiency Canberra Parameter: CAM_F_PSEFERR#desc=uncertainty of efficiency Canberra Parameter: CAM_F_PSEFERR#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."BACK_CHANNEL" IS '#brief=number of average background channels Canberra Parameter: CAM_F_PSBKCHAN#desc=number of average background channels Canberra Parameter: CAM_F_PSBKCHAN#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."IDED" IS '#brief=peak identification indicator(0 or 1)#desc=peak identification indicator; 1 = peak was associated with a nuclide by the automated analysis, 0 = peak was not associated with a nuclide by the automated analysis (not updated by the ROI interface) Canberra Parameter: CAM_L_PSPKNOWN#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."FITTED" IS '#brief=peak fit indicator Canberra Parameter: CAM_L_PSPPFIT#desc=peak fit indicator Canberra Parameter: CAM_L_PSPPFIT#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."MULTIPLET" IS '#brief=multiplet peak indicator Canberra Parameter: CAM_L_PSPMULT#desc=multiplet peak indicator Canberra Parameter: CAM_L_PSPMULT#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."LC" IS '#brief=critical level for the peak (counts)#desc=critical level for the peak (counts)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."PEAK_SIG" IS '#brief=peak significance, peak area divided by Lc#desc=peak significance, peak area divided by Lc#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."PEAK_TOL" IS '#brief=per peak energy tolerance; approximates the energy tolerance at a given peak#desc=per peak energy tolerance; approximates the energy tolerance at a given peak#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."PSS" IS '#brief=peak search significance parameter Canberra parameter: CAM_F_PSSIGNIF#desc=peak search significance parameter Canberra parameter: CAM_F_PSSIGNIF#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS"."DETECTABILITY" IS '#brief=detectability#desc=detectability#category=#ext=f9.6#na=NULL#range=#unit=';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_PEAKS"  IS '#category=Automatic Processing#desc=The gards_peaks table contains information regarding peaks identified during interactive review.';
 
--------------------------------------------------------
--  DDL for Table GARDS_PEAKS_ORIG
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_PEAKS_ORIG" 
   (	"SAMPLE_ID" NUMBER, 
	"PEAK_ID" NUMBER, 
	"CENTROID" NUMBER, 
	"CENTROID_ERR" NUMBER, 
	"ENERGY" NUMBER, 
	"ENERGY_ERR" NUMBER, 
	"LEFT_CHAN" NUMBER, 
	"WIDTH" NUMBER, 
	"BACK_COUNT" NUMBER, 
	"BACK_UNCER" NUMBER, 
	"FWHM" NUMBER, 
	"FWHM_ERR" NUMBER, 
	"AREA" NUMBER, 
	"AREA_ERR" NUMBER, 
	"ORIGINAL_AREA" NUMBER, 
	"ORIGINAL_UNCER" NUMBER, 
	"COUNTS_SEC" NUMBER, 
	"COUNTS_SEC_ERR" NUMBER, 
	"EFFICIENCY" NUMBER, 
	"EFF_ERROR" NUMBER, 
	"BACK_CHANNEL" NUMBER, 
	"IDED" NUMBER, 
	"FITTED" NUMBER, 
	"MULTIPLET" NUMBER, 
	"LC" NUMBER, 
	"PEAK_SIG" NUMBER, 
	"PEAK_TOL" NUMBER, 
	"PSS" NUMBER, 
	"MODDATE" DATE, 
	"DETECTABILITY" NUMBER
   ) ENABLE ROW MOVEMENT ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."SAMPLE_ID" IS '#brief=sample identifier #desc=sample identifier #category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."PEAK_ID" IS '#brief=peak identifier#desc=peak identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."CENTROID" IS '#brief=peak centroid (channels) Canberra Parameter: CAM_F_PSCENTRD#desc=peak centroid (channels) Canberra Parameter: CAM_F_PSCENTRD#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."CENTROID_ERR" IS '#brief=uncertainty of peak centroid (channels) Canberra Parameter: CAM_F_PSDCENTRD#desc=Peak centroid energy.#category=#ext=#na=#range=0.0 <= centroid#unit=KeV';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."ENERGY" IS '#brief=energy at peak centroid (keV) Canberra Parameter: CAM_F_PSENERGY#desc=energy at peak centroid (keV) Canberra Parameter: CAM_F_PSENERGY#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."ENERGY_ERR" IS '#brief=uncertainty of energy (keV) Canberra Parameter: CAM_F_PSDENERGY#desc=Line energy.#category=#ext=#na=#range=0 <= energy#unit=keV';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."LEFT_CHAN" IS '#brief=left channel of peak Canberra Parameter: CAM_L_PSLEFT#desc=left channel of peak Canberra Parameter: CAM_L_PSLEFT#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."WIDTH" IS '#brief=width of peak (channels) Canberra Parameter: CAM_L_PSWIDTH#desc=width of peak (channels) Canberra Parameter: CAM_L_PSWIDTH#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."BACK_COUNT" IS '#brief=continuum background counts Canberra Parameter: CAM_F_PSBACKGND#desc=Average number of background channels.#category=#ext=#na=#range=0.0 <= back_channel#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."BACK_UNCER" IS '#brief=uncertainty of continuum background counts Canberra Parameter: CAM_F_PSDBACK#desc=uncertainty of continuum background counts Canberra Parameter: CAM_F_PSDBACK#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."FWHM" IS '#brief=full width at half maximum Canberra Parameter: CAM_F_PSFWHM#desc=full width at half maximum Canberra Parameter: CAM_F_PSFWHM#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."FWHM_ERR" IS '#brief=uncertainty of full width at half maximum Canberra Parameter: CAM_PSDFWHM#desc=Peak width at half the maximum peak height.#category=#ext=#na=#range=0.0 <= fwhm#unit=keV';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."AREA" IS '#brief=peak area (counts) Canberra Parameter: CAM_F_PSAREA#desc=peak area (counts) Canberra Parameter: CAM_F_PSAREA#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."AREA_ERR" IS '#brief=uncertainty of peak area (counts) Canberra Parameter: CAM_F_PSDAREA#desc=uncertainty of peak area (counts) Canberra Parameter: CAM_F_PSDAREA#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."ORIGINAL_AREA" IS '#brief=original peak area (counts) Canberra Parameter: CAM_PSORIGAREA#desc=original peak area (counts) Canberra Parameter: CAM_PSORIGAREA#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."ORIGINAL_UNCER" IS '#brief=uncertainty of original peak area (counts) Canberra Parameter: CAM_PSORIGERR#desc=Original peak area.#category=#ext=#na=#range=original_area > 0#unit=counts';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."COUNTS_SEC" IS '#brief=counts per second#desc=counts per second#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."COUNTS_SEC_ERR" IS '#brief=error in counts per second#desc=error in counts per second#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."EFFICIENCY" IS '#brief=efficiency Canberra Parameter: CAM_F_PSEFF#desc=efficiency Canberra Parameter: CAM_F_PSEFF#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."EFF_ERROR" IS '#brief=uncertainty of efficiency Canberra Parameter: CAM_F_PSEFERR#desc=uncertainty of efficiency Canberra Parameter: CAM_F_PSEFERR#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."BACK_CHANNEL" IS '#brief=number of average background channels Canberra Parameter: CAM_L_PSBKCHAN#desc=number of average background channels Canberra Parameter: CAM_L_PSBKCHAN#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."IDED" IS '#brief=peak identification indicator (0 or 1)#desc=peak identification indicator; 1 = peak was associated with a nuclide by the automated analysis, 0 = peak was not associated with a nuclide by the automated analysis (not updated by the ROI interface) Canberra Parameter: CAM_L_PSPKNOWN#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."FITTED" IS '#brief=peak fit indicator Canberra Parameter: CAM_F_PSPPFIT#desc=peak fit indicator Canberra Parameter: CAM_F_PSPPFIT#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."MULTIPLET" IS '#brief=multiplet peak indicator Canberra Parameter: CAM_PSPMULT#desc=multiplet peak indicator Canberra Parameter: CAM_PSPMULT#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."LC" IS '#brief=critical level for the peak (counts)#desc=critical level for the peak (counts)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."PEAK_SIG" IS '#brief=peak significance, peak area divided by Lc#desc=peak significance, peak area divided by Lc#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."PEAK_TOL" IS '#brief=per peak energy tolerance; approximates the energy tolerance at a given peak#desc=per peak energy tolerance; approximates the energy tolerance at a given peak#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."PSS" IS '#brief=peak search significance parameter Canberra parameter: CAM_F_PSSIGNIF#desc=peak search significance parameter Canberra parameter: CAM_F_PSSIGNIF#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PEAKS_ORIG"."DETECTABILITY" IS '#brief=detectability#desc=detectability#category=#ext=f9.6#na=NULL#range=#unit=';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_PEAKS_ORIG"  IS '#category=Automatic Processing#desc=The gards_peaks_orig table contains information regarding peaks identified during automated analysis.';
 
--------------------------------------------------------
--  DDL for Table GARDS_PERMISSIONS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_PERMISSIONS" 
   (	"PERMISSION_ID" NUMBER, 
	"PERMISSION_NAME" VARCHAR2(30), 
	"DB_NAME" VARCHAR2(35), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PERMISSIONS"."PERMISSION_ID" IS '#brief=unique permission identifier#desc=unique permission identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PERMISSIONS"."PERMISSION_NAME" IS '#brief=string name of a permission#desc=Permission identifier.#category=#ext=a30#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PERMISSIONS"."DB_NAME" IS '#brief=name of corresponding role in the database#desc=name of corresponding role in the database#category=#ext=a35#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PERMISSIONS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_PERMISSIONS"  IS '#category=Automatic Processing#desc=The gards_permissions table contains a list of permissions that can be manipulated by the MAR tool. ';
 
--------------------------------------------------------
--  DDL for Table GARDS_POC
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_POC" 
   (	"POCID" NUMBER, 
	"EMAIL_ADDRESS" VARCHAR2(50), 
	"FIRST_NAME" VARCHAR2(20), 
	"LAST_NAME" VARCHAR2(50), 
	"TELEPHONE" VARCHAR2(20), 
	"ADDRESS" VARCHAR2(500), 
	"ADDITIONAL_INFO" VARCHAR2(500), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_POC"."POCID" IS '#brief=unique point of contact identifier#desc=unique point of contact identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_POC"."EMAIL_ADDRESS" IS '#brief=email address of point of contact#desc=email address of point of contact#category=#ext=a50#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_POC"."FIRST_NAME" IS '#brief=first name of point of contact#desc=first name of point of contact#category=#ext=a20#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_POC"."LAST_NAME" IS '#brief=last name of point of contact#desc=last name of point of contact#category=#ext=a50#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_POC"."TELEPHONE" IS '#brief=telephone number of point of contact#desc=telephone number of point of contact#category=#ext=a20#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_POC"."ADDRESS" IS '#brief=address of point of contact#desc=Additional information for a contact. This column includes information such as full name, title, company or university name, country, and so on.#category=#ext=a500#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_POC"."ADDITIONAL_INFO" IS '#brief=additional information for point of contact#desc=additional information for point of contact#category=#ext=a500#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_POC"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_POC"  IS '#category=Automatic Processing#desc=The gards_poc table contains information for radionuclide monitoring system points of contact (POC).';
 
--------------------------------------------------------
--  DDL for Table GARDS_PROCESSING_ERRORS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_PROCESSING_ERRORS" 
   (	"RMS_ID" NUMBER, 
	"SAMPLE_REF_ID" VARCHAR2(32), 
	"MSG_ID" NUMBER, 
	"FILENAME" VARCHAR2(512), 
	"STATION_CODE" VARCHAR2(5), 
	"DETECTOR_CODE" VARCHAR2(9), 
	"DATA_TYPE" VARCHAR2(12), 
	"ERROR_TEXT" VARCHAR2(2048), 
	"ENTRY_DATE" DATE, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROCESSING_ERRORS"."RMS_ID" IS '#brief=sequence number of associated data type (e.g., RMSSOH, SAMPLEPHD, etc.). If SAMPLEPHD, the sequence refers to a sample_id; if RMSSOH, the RMS ID refers to an soh_id.#desc=sequence number of associated data type (e.g., RMSSOH, SAMPLEPHD, etc.). If SAMPLEPHD, the sequence refers to a sample_id; if RMSSOH, the RMS ID refers to an soh_id.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROCESSING_ERRORS"."SAMPLE_REF_ID" IS '#brief=sample reference identification#desc=sample reference identification#category=#ext=a32#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROCESSING_ERRORS"."MSG_ID" IS '#brief=message identifier#desc=message identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROCESSING_ERRORS"."FILENAME" IS '#brief=import message filename#desc=import message filename#category=#ext=a51#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROCESSING_ERRORS"."STATION_CODE" IS '#brief=station code parsed from import message#desc=station code parsed from import message#category=#ext=a5#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROCESSING_ERRORS"."DETECTOR_CODE" IS '#brief=detector code parsed from import message#desc=detector code parsed from import message#category=#ext=a9#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROCESSING_ERRORS"."DATA_TYPE" IS '#brief=data type parsed from message header (e.g., RMSSOH, MET, SAMPLEPHD, etc.)#desc=data type parsed from message header (e.g., RMSSOH, MET, SAMPLEPHD, etc.)#category=#ext=a12#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROCESSING_ERRORS"."ERROR_TEXT" IS '#brief=text associated with the error#desc=text associated with the error#category=#ext=a20#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROCESSING_ERRORS"."ENTRY_DATE" IS '#brief=date and time of error entry#desc=date and time of error entry#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROCESSING_ERRORS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_PROCESSING_ERRORS"  IS '#category=Automatic Processing#desc=The gards_processing_errors table contains sample information, if applicable, and message information for RMS messages that have failed processing.';
 
--------------------------------------------------------
--  DDL for Table GARDS_PROC_PARAMS_TEMPLATE
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE" 
   (	"STATION_ID" NUMBER, 
	"DETECTOR_ID" NUMBER, 
	"SAMPLE_TYPE" VARCHAR2(2), 
	"DATA_TYPE" CHAR(1), 
	"SPECTRAL_QUALIFIER" VARCHAR2(5), 
	"BEGIN_DATE" DATE, 
	"END_DATE" DATE, 
	"DO_BACK" NUMBER, 
	"BACK_DATA_TYPE" CHAR(1), 
	"NUCLIDE_LIB" VARCHAR2(96), 
	"MDA_LEVEL" NUMBER, 
	"NID_CONFID" NUMBER, 
	"SQUANT_ERR" NUMBER, 
	"BUILDTYPE" VARCHAR2(8), 
	"PEAK_SENSE" NUMBER, 
	"PEAK_START" NUMBER, 
	"PEAK_END" NUMBER, 
	"FWHM_MULT_WIDTH" NUMBER, 
	"LEFT_FWHM_LIM" NUMBER, 
	"RIGHT_FWHM_LIM" NUMBER, 
	"BACK_CHAN" NUMBER, 
	"BACK_TYPE" VARCHAR2(6), 
	"FIT_SINGLETS" NUMBER, 
	"CRIT_LEVEL" NUMBER, 
	"FIX_FWHM" NUMBER, 
	"AREA_REJECT" NUMBER, 
	"MDC_WIDTH" NUMBER, 
	"LC_ABSCISSA" NUMBER, 
	"DO_PD_CALC" NUMBER, 
	"DO_CSC" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."STATION_ID" IS '#brief=station identifier Canberra Parameter: CAM_L_SSPI5#desc=station identifier Canberra Parameter: CAM_L_SSPI5#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."DETECTOR_ID" IS '#brief=detector identifier (relates to gards_detectors.detector_id) Canberra Parameter: CAM_L_SSPI6#desc=detector identifier (relates to gards_detectors.detector_id) Canberra Parameter: CAM_L_SSPI6#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."SAMPLE_TYPE" IS '#brief=type of sample Canberra Parameter: CAM_T_SSPRSTR1#desc=type of sample Canberra Parameter: CAM_T_SSPRSTR1#category=#ext=a2#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."DATA_TYPE" IS '#brief=spectral data type#desc=Type of sample; an uncontaminated crushed blank filter (B), calibration background (C), detector background (D), quality control (Q), or an actual sample (S).#category=#ext=a1#na=#range=data_type IN {B, C, D, Q, S}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."SPECTRAL_QUALIFIER" IS '#brief=indicator of full or preliminary sample#desc=indicator of full or preliminary sample#category=#ext=a5#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."BEGIN_DATE" IS '#brief=initialization date of parameters#desc=initialization date of parameters#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."END_DATE" IS '#brief=termination date of parameters#desc=termination date of parameters#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."DO_BACK" IS '#brief=background subtraction indicator Canberra Parameter: CAM_L_PRNOBACKCOR#desc=background subtraction indicator Canberra Parameter: CAM_L_PRNOBACKCOR#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."BACK_DATA_TYPE" IS '#brief=blank (B), or detector background (D) spectral type#desc=blank (B), or detector background (D) spectral type#category=#ext=a1#na=#range=back_data_type IN {B, D}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."NUCLIDE_LIB" IS '#brief=nuclide library to be used during analysis#desc=nuclide library to be used during analysis#category=#ext=a96#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."MDA_LEVEL" IS '#brief=MDA confidence factor (percent) Canberra Parameter: CAM_F_MDACONFID#desc=MDA confidence factor (percent) Canberra Parameter: CAM_F_MDACONFID#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."NID_CONFID" IS '#brief=NID confidence factor (percent) Canberra Parameter: CAM_F_CONFID#desc=NID confidence factor (percent) Canberra Parameter: CAM_F_CONFID#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."SQUANT_ERR" IS '#brief=error in sample quantity Canberra Parameter: CAM_F_SQUANTERR#desc=Time for which sample was exposed: FULL or PREL (preliminary).#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."BUILDTYPE" IS '#brief=flag for Canberra: activity (NONE), or concentration (BUILD), calculations#desc=flag for Canberra: activity (NONE), or concentration (BUILD), calculations#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."PEAK_SENSE" IS '#brief=peak search sensitivity Canberra Parameter: CAM_F_SENSITIVITY#desc=peak search sensitivity Canberra Parameter: CAM_F_SENSITIVITY#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."PEAK_START" IS '#brief=peak search start (keV) Canberra Parameter: CAM_L_PEAKSTART#desc=peak search start (keV) Canberra Parameter: CAM_L_PEAKSTART#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."PEAK_END" IS '#brief=peak search end (keV) Canberra Parameter: CAM_L_PEAKEND#desc=peak search end (keV) Canberra Parameter: CAM_L_PEAKEND#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."FWHM_MULT_WIDTH" IS '#brief=number of FWHMs to search to determine multiplets Canberra Parameter: CAM_F_PRFWHMPKMULT#desc=number of FWHMs to search to determine multiplets Canberra Parameter: CAM_F_PRFWHMPKMULT#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."LEFT_FWHM_LIM" IS '#brief=left ROI FWHM limit Canberra Parameter: CAM_F_PRFWHMPKLEFT#desc=left ROI FWHM limit Canberra Parameter: CAM_F_PRFWHMPKLEFT#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."RIGHT_FWHM_LIM" IS '#brief=right ROI FWHM limit Canberra Parameter: CAM_F_PRFWHMPKRIGHT#desc=right ROI FWHM limit Canberra Parameter: CAM_F_PRFWHMPKRIGHT#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."BACK_CHAN" IS '#brief=number of continuous channels Canberra Parameter: CAM_L_PRNBKCHN#desc=number of continuous channels Canberra Parameter: CAM_L_PRNBKCHN#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."BACK_TYPE" IS '#brief=background type Canberra Parameter: CAM_T_ROIPSBTYP#desc=background type Canberra Parameter: CAM_T_ROIPSBTYP#category=#ext=a6#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."FIT_SINGLETS" IS '#brief=fit singlets flag, Canberra Parameter: CAM_L_PRFIT#desc=fit singlets flag, Canberra Parameter: CAM_L_PRFIT#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."CRIT_LEVEL" IS '#brief=critical level test indicator, Canberra Parameter: CAM_L_CRITLEVEL#desc=critical level test indicator, Canberra Parameter: CAM_L_CRITLEVEL#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."FIX_FWHM" IS '#brief=fixed FWHM during peak search flag Canberra Parameter: CAM_L_PRFIXFWHM#desc=fixed FWHM during peak search flag Canberra Parameter: CAM_L_PRFIXFWHM#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."AREA_REJECT" IS '#brief=indicatior of whether or not to reject peaks with zero area indicator Canberra Parameter: CAM_L_PRREJECTPEAKS#desc=indicatior of whether or not to reject peaks with zero area indicator Canberra Parameter: CAM_L_PRREJECTPEAKS#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."MDC_WIDTH" IS '#brief=baseline width used for MDA calculation Canberra param: CAM_F_VPWIDTH #desc=baseline width used for MDA calculation Canberra param: CAM_F_VPWIDTH #category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."LC_ABSCISSA" IS '#brief=abscissas of the normal distribution corresponding to a confidence level; a value of 1.645 corresponds to a 95% confidence interval for the peak critical levell #desc=abscissas of the normal distribution corresponding to a confidence level; a value of 1.645 corresponds to a 95% confidence interval for the peak critical levell #category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."DO_PD_CALC" IS '#brief=flag indicates if the parent/daughter calculations should be run; 1 = run calculations, 0 = do not run calculations#desc=flag that indicates how cascade summing should default: 0 = default to off, 1 = default to on.#category=#ext=i1#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."DO_CSC" IS '#brief=flag to turn off cascade summing correction#desc=Flag that indicates whether or not background subtraction should be performed: 1 = yes, 0 = no.#category=#ext=i1#na=#range=do_back IN {0,1}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE"  IS '#category=Automatic Processing#desc=The gards_proc_params_template table is a template data record that contains parameters used by Automatic Analysis process software for peak search and nuclide identification. These parameters are used unless overridden at the command line.';
 
--------------------------------------------------------
--  DDL for Table GARDS_PRODUCT
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_PRODUCT" 
   (	"SAMPLE_ID" NUMBER, 
	"FOFF" NUMBER, 
	"DSIZE" NUMBER, 
	"DIR" VARCHAR2(256), 
	"DFILE" VARCHAR2(32), 
	"AUTHOR" VARCHAR2(30), 
	"REVISION" NUMBER, 
	"TYPEID" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PRODUCT"."SAMPLE_ID" IS '#brief=unique sample identifier#desc=unique sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PRODUCT"."FOFF" IS '#brief=offset into the data file (bytes)#desc=offset into the data file (bytes)#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PRODUCT"."DSIZE" IS '#brief=size of data file in bytes#desc=size of data file in bytes#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PRODUCT"."DIR" IS '#brief=full path to the data file referred to in the DFILE column#desc=full path to the data file referred to in the DFILE column#category=#ext=a256#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PRODUCT"."DFILE" IS '#brief=name of file containing the data#desc=name of file containing the data#category=#ext=a32#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PRODUCT"."AUTHOR" IS '#brief=user name of Radionuclide Officer#desc=user name of Radionuclide Officer#category=#ext=a30#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PRODUCT"."REVISION" IS '#brief=revision identifier#desc=revision identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PRODUCT"."TYPEID" IS '#brief=unique type identifier#desc=unique type identifier#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PRODUCT"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_PRODUCT"  IS '#category=Automatic Processing#desc=The gards_product table temporarily stores radionuclide reviewed products for quality assurance purposes.';
 
--------------------------------------------------------
--  DDL for Table GARDS_PRODUCT_TYPE
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_PRODUCT_TYPE" 
   (	"TYPEID" NUMBER, 
	"PRODTYPE" VARCHAR2(12), 
	"NAME" VARCHAR2(64), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PRODUCT_TYPE"."TYPEID" IS '#brief=unique product type identifier#desc=unique product type identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PRODUCT_TYPE"."PRODTYPE" IS '#brief=product type#desc=product type#category=#ext=a12#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PRODUCT_TYPE"."NAME" IS '#brief=product name#desc=product name#category=#ext=a64#na=NOT ALLOWED#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_PRODUCT_TYPE"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_PRODUCT_TYPE"  IS '#category=Automatic Processing#desc=The gards_product_type table lists the different types of radionuclide reviewed products.';
 
--------------------------------------------------------
--  DDL for Table GARDS_QAT_CONFIG
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_QAT_CONFIG" 
   (	"T_TIME" NUMBER, 
	"MIN_T_TIME" NUMBER, 
	"MAX_T_TIME" NUMBER, 
	"Q_TIME" NUMBER, 
	"POLL_TIME" NUMBER, 
	"ALLOW_RELEASE" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QAT_CONFIG"."T_TIME" IS '#brief=number of minutes after gards_sample_status.entry_date that rms_QAT_auto waits before releasing a sample#desc=number of minutes after gards_sample_status.entry_date that rms_QAT_auto waits before releasing a sample#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QAT_CONFIG"."MIN_T_TIME" IS '#brief=minimum allowable value for t_time#desc=minimum allowable value for t_time#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QAT_CONFIG"."MAX_T_TIME" IS '#brief=maximum allowable value for t_time#desc=maximum allowable value for t_time#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QAT_CONFIG"."Q_TIME" IS '#brief=number of minutes after gards_sample_status.review_date that rms_QAT_auto waits before releasing a sample#desc=number of minutes after gards_sample_status.review_date that rms_QAT_auto waits before releasing a sample#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QAT_CONFIG"."POLL_TIME" IS '#brief=number of minutes rms_QAT sleeps between each database poll#desc=number of minutes rms_QAT sleeps between each database poll#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QAT_CONFIG"."ALLOW_RELEASE" IS '#brief=flag indicating whether or not release is permitted#desc=flag indicating whether or not release is permitted#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QAT_CONFIG"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_QAT_CONFIG"  IS '#category=Automatic Processing#desc=The gards_qat_config table contains q_time and t_time used by rms_QAT_auto; there is only one record in the database.';
 
--------------------------------------------------------
--  DDL for Table GARDS_QAT_NOTIFY
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_QAT_NOTIFY" 
   (	"SAMPLE_ID" NUMBER, 
	"COMMENT_TYPE" NUMBER, 
	"COMMENT_TEXT" VARCHAR2(2048), 
	"NUCL_NAME" VARCHAR2(8), 
	"ENERGY" NUMBER, 
	"DTG" DATE, 
	"AUTHOR" VARCHAR2(30), 
	"RECIPIENT_LIST" VARCHAR2(128), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QAT_NOTIFY"."SAMPLE_ID" IS '#brief=foriegn key#desc=foriegn key#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QAT_NOTIFY"."COMMENT_TYPE" IS '#brief=foriegn key to gards_comments_defs#desc=Text of analyst comments.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QAT_NOTIFY"."COMMENT_TEXT" IS '#brief=text of the comment#desc=text of the comment#category=#ext=a20#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QAT_NOTIFY"."NUCL_NAME" IS '#brief=nuclide name referenced by comment#desc=nuclide name referenced by comment#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QAT_NOTIFY"."ENERGY" IS '#brief=energy (keV) referenced by comment#desc=energy (keV) referenced by comment#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QAT_NOTIFY"."DTG" IS '#brief=date comment was entered#desc=date comment was entered#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QAT_NOTIFY"."AUTHOR" IS '#brief=user name of Radionuclide Officer#desc=user name of Radionuclide Officer#category=#ext=a30#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QAT_NOTIFY"."RECIPIENT_LIST" IS '#brief=comma-separated list of users to whom the notification was sent#desc=comma-separated list of users to whom the notification was sent#category=#ext=a128#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QAT_NOTIFY"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_QAT_NOTIFY"  IS '#category=Automatic Processing#desc=The gards_qat_notify table contains comments created by rms_QAT.';
 
--------------------------------------------------------
--  DDL for Table GARDS_QAT_QUERY_FILTER
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_QAT_QUERY_FILTER" 
   (	"USER_ID" NUMBER, 
	"MIN_SAMPLE_ID" NUMBER, 
	"MAX_SAMPLE_ID" NUMBER, 
	"STATUS_LIST" VARCHAR2(128), 
	"STATION_LIST" VARCHAR2(1024), 
	"INCLUDE_STATIONS" NUMBER, 
	"CATEGORY_LIST" VARCHAR2(32), 
	"REVIEW_CAT" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QAT_QUERY_FILTER"."USER_ID" IS '#brief=foreign key to gards_users#desc=foreign key to gards_users#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QAT_QUERY_FILTER"."MIN_SAMPLE_ID" IS '#brief=foreign key#desc=foreign key#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QAT_QUERY_FILTER"."MAX_SAMPLE_ID" IS '#brief=foreign key#desc=foreign key#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QAT_QUERY_FILTER"."STATUS_LIST" IS '#brief=comma-separated list of statuses#desc=comma-separated list of statuses#category=#ext=a128#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QAT_QUERY_FILTER"."STATION_LIST" IS '#brief=comma-separated list of stations#desc=comma-separated list of stations#category=#ext=a128#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QAT_QUERY_FILTER"."INCLUDE_STATIONS" IS '#brief=flag to include or exclude stations#desc=flag to include or exclude stations#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QAT_QUERY_FILTER"."CATEGORY_LIST" IS '#brief=comma-separated list of categories#desc=comma-separated list of categories#category=#ext=a1024#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QAT_QUERY_FILTER"."REVIEW_CAT" IS '#brief=review category#desc=review category#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QAT_QUERY_FILTER"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_QAT_QUERY_FILTER"  IS '#category=#desc=';
 
--------------------------------------------------------
--  DDL for Table GARDS_QCHISTORY
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_QCHISTORY" 
   (	"STATION_ID" NUMBER, 
	"DETECTOR_ID" NUMBER, 
	"SAMPLE_ID" NUMBER, 
	"STATE" VARCHAR2(128), 
	"LDDATE" DATE, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QCHISTORY"."STATION_ID" IS '#brief=station identifier #desc=station identifier #category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QCHISTORY"."DETECTOR_ID" IS '#brief=unique detector identifier#desc=unique detector identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QCHISTORY"."SAMPLE_ID" IS '#brief=sample identifier #desc=sample identifier #category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QCHISTORY"."STATE" IS '#brief=text results of quality control hypothesis tests#desc=text results of quality control hypothesis tests#category=#ext=a128#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QCHISTORY"."LDDATE" IS '#brief=date of quality control processing#desc=date of quality control processing#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_QCHISTORY"  IS '#category=Automatic Processing#desc=The gards_qchistory table contains output messages from quality control tests for each sample.';
 
--------------------------------------------------------
--  DDL for Table GARDS_QCPARAMS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_QCPARAMS" 
   (	"DETECTOR_ID" NUMBER, 
	"GAINCHANGE" NUMBER, 
	"SDMULT" NUMBER, 
	"WIDTH_ADJ" NUMBER, 
	"AREA_ADJ" NUMBER, 
	"ETOL" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QCPARAMS"."DETECTOR_ID" IS '#brief=unique detector identifier#desc=unique detector identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QCPARAMS"."GAINCHANGE" IS '#brief=gain first difference tolerance#desc=gain first difference tolerance#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QCPARAMS"."SDMULT" IS '#brief=location test standard deviation multiplier#desc=location test standard deviation multiplier#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QCPARAMS"."WIDTH_ADJ" IS '#brief=peak width standard deviation inflation factor#desc=peak width standard deviation inflation factor#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QCPARAMS"."AREA_ADJ" IS '#brief=peak area standard deviation inflation factor#desc=peak area standard deviation inflation factor#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QCPARAMS"."ETOL" IS '#brief=energy tolerance used to match peaks with energies (keV)#desc=energy tolerance used to match peaks with energies (keV)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QCPARAMS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_QCPARAMS"  IS '#category=Automatic Processing#desc=The gards_qcparams table contains parameters for quality control processes.';
 
--------------------------------------------------------
--  DDL for Table GARDS_QCTARGETS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_QCTARGETS" 
   (	"STATION_ID" NUMBER, 
	"DETECTOR_ID" NUMBER, 
	"DTG" DATE, 
	"NAME" VARCHAR2(8), 
	"ENERGY" NUMBER, 
	"MUWIDTH" NUMBER, 
	"MUAREA" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QCTARGETS"."STATION_ID" IS '#brief=station identifier#desc=station identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QCTARGETS"."DETECTOR_ID" IS '#brief=unique detector identifier#desc=unique detector identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QCTARGETS"."DTG" IS '#brief=decay correction reference date#desc=decay correction reference date#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QCTARGETS"."NAME" IS '#brief=nuclide name#desc=Nuclide name.#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QCTARGETS"."ENERGY" IS '#brief=nuclide line energy (keV)#desc=nuclide line energy (keV)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QCTARGETS"."MUWIDTH" IS '#brief=target width for each nuclide line energy (keV)#desc=target width for each nuclide line energy (keV)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QCTARGETS"."MUAREA" IS '#brief=target area for each nuclide line energy (counts)#desc=target area for each nuclide line energy (counts)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QCTARGETS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_QCTARGETS"  IS '#category=Automatic Processing#desc=The gards_qctargets table contains detector-specific target values for the quality control width and area tests.';
 
--------------------------------------------------------
--  DDL for Table GARDS_QC_RESULTS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_QC_RESULTS" 
   (	"SAMPLE_ID" NUMBER(22,0), 
	"TEST_NAME" VARCHAR2(32), 
	"FLAG" CHAR(1), 
	"QC_COMMENT" VARCHAR2(255), 
	"MODDATE" DATE DEFAULT SYSDATE
   ) ;
 
--------------------------------------------------------
--  DDL for Table GARDS_QUERY_RESULTS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_QUERY_RESULTS" 
   (	"RQST_ID" NUMBER, 
	"RQST_STRING" VARCHAR2(100), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QUERY_RESULTS"."RQST_ID" IS '#brief=unique query identifier#desc=unique query identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_QUERY_RESULTS"."RQST_STRING" IS '#brief=output of the user query#desc=Unique query identifier.#category=#ext=a100#na=#range=rqst_id > 0#unit=';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_QUERY_RESULTS"  IS '#category=Automatic Processing#desc=The gards_query_results table contains output of a user-initiated query from the event screening tool.  This table is purged at the end of the request. ';
 
--------------------------------------------------------
--  DDL for Table GARDS_REFLINE_MASTER
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_REFLINE_MASTER" 
   (	"REFPEAK_ENERGY" NUMBER, 
	"DATA_TYPE" CHAR(1), 
	"SPECTRAL_QUALIFIER" VARCHAR2(5), 
	"CALIBRATION_TYPE" VARCHAR2(3), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_REFLINE_MASTER"."REFPEAK_ENERGY" IS '#brief=known reference energy for a nuclide#desc=known reference energy for a nuclide#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_REFLINE_MASTER"."DATA_TYPE" IS '#brief=data type #desc=data type #category=#ext=a1#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_REFLINE_MASTER"."SPECTRAL_QUALIFIER" IS '#brief=spectral qualifier#desc=spectral qualifier#category=#ext=a1#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_REFLINE_MASTER"."CALIBRATION_TYPE" IS '#brief=calibration type#desc=calibration type#category=#ext=a3#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_REFLINE_MASTER"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_REFLINE_MASTER"  IS '#category=Automatic Processing#desc=The gards_refline_master table contains resolution calibration pairs information associated with spectral pulse height data (PHD).';
 
--------------------------------------------------------
--  DDL for Table GARDS_RELEVANT_NUCLIDES
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_RELEVANT_NUCLIDES" 
   (	"NAME" VARCHAR2(8), 
	"TYPE" VARCHAR2(16), 
	"SAMPLE_TYPE" CHAR(1), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RELEVANT_NUCLIDES"."NAME" IS '#brief=name of the nuclide#desc=Nuclide name.#category=#ext=a5#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RELEVANT_NUCLIDES"."TYPE" IS '#brief=nuclide type (choices are: ACTIVATION, COSMIC, FISSION(G), FISSION(P), or NATURAL)#desc=Nuclide type. Choices are: ACTIVATION, COSMIC, FISSION(G), FISSION(P), or NATURAL.#category=#ext=a16#na=#range=type IN {ACTIVATION, COSMIC, FISSION(G), FISSION(P), NATURAL}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RELEVANT_NUCLIDES"."SAMPLE_TYPE" IS '#brief=sample type (P, G, or B)#desc=sample type (P, G, or B)#category=#ext=a1#na=#range=sample_type IN {P, G, B}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RELEVANT_NUCLIDES"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_RELEVANT_NUCLIDES"  IS '#category=Automatic Processing#desc=The gards_relevant_nuclides table contains the list of nuclides determined to be relevant during the identification of radionuclide events.   This table includes the categorization list for particulate samples (CLPS) and the relevant radioxenon isotopes.';
 
--------------------------------------------------------
--  DDL for Table GARDS_RESOLUTION_CAL
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_RESOLUTION_CAL" 
   (	"SAMPLE_ID" NUMBER, 
	"COEFF1" NUMBER, 
	"COEFF2" NUMBER, 
	"COEFF3" NUMBER, 
	"COEFF4" NUMBER, 
	"COEFF5" NUMBER, 
	"COEFF6" NUMBER, 
	"COEFF7" NUMBER, 
	"COEFF8" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_CAL"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_CAL"."COEFF1" IS '#brief=first order calibration coefficient#desc=first order calibration coefficient#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_CAL"."COEFF2" IS '#brief=second order calibration coefficient#desc=second order calibration coefficient#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_CAL"."COEFF3" IS '#brief=third order calibration coefficient#desc=third order calibration coefficient#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_CAL"."COEFF4" IS '#brief=fourth order calibration coefficient#desc=fourth order calibration coefficient#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_CAL"."COEFF5" IS '#brief=fifth order calibration coefficient#desc=fifth order calibration coefficient#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_CAL"."COEFF6" IS '#brief=sixth order calibration coefficient#desc=sixth order calibration coefficient#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_CAL"."COEFF7" IS '#brief=seventh order calibration coefficient#desc=seventh order calibration coefficient#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_CAL"."COEFF8" IS '#brief=eighth order calibration coefficient#desc=eighth order calibration coefficient#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_CAL"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_RESOLUTION_CAL"  IS '#category=Automatic Processing#desc=The gards_resolution_cal table contains resolution calibration coefficients calculated during analysis.';
 
--------------------------------------------------------
--  DDL for Table GARDS_RESOLUTION_CAL_COV
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_RESOLUTION_CAL_COV" 
   (	"SAMPLE_ID" NUMBER(22,0), 
	"ROW_INDEX" NUMBER(10,0), 
	"COL_INDEX" NUMBER(10,0), 
	"MODDATE" DATE DEFAULT SYSDATE, 
	"COEFF" FLOAT(22)
   ) ;
 
   COMMENT ON TABLE "RMSMAN"."GARDS_RESOLUTION_CAL_COV"  IS '#category=Automatic Processing#desc=gards resolution cal cov';
 
--------------------------------------------------------
--  DDL for Table GARDS_RESOLUTION_CAL_ORIG
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_RESOLUTION_CAL_ORIG" 
   (	"SAMPLE_ID" NUMBER(8,0), 
	"COEFF1" NUMBER(8,0), 
	"COEFF2" NUMBER(8,0), 
	"COEFF3" NUMBER(8,0), 
	"COEFF4" NUMBER(8,0), 
	"COEFF5" NUMBER(8,0), 
	"COEFF6" NUMBER(8,0), 
	"COEFF7" NUMBER(8,0), 
	"COEFF8" NUMBER(8,0), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_CAL_ORIG"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=i8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_CAL_ORIG"."COEFF1" IS '#brief=first order calibration coefficient#desc=first order calibration coefficient#category=#ext=i8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_CAL_ORIG"."COEFF2" IS '#brief=second order calibration coefficient#desc=second order calibration coefficient#category=#ext=i8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_CAL_ORIG"."COEFF3" IS '#brief=third order calibration coefficient#desc=third order calibration coefficient#category=#ext=i8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_CAL_ORIG"."COEFF4" IS '#brief=fourth order calibration coefficient#desc=fourth order calibration coefficient#category=#ext=i8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_CAL_ORIG"."COEFF5" IS '#brief=fifth order calibration coefficient#desc=fifth order calibration coefficient#category=#ext=i8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_CAL_ORIG"."COEFF6" IS '#brief=sixth order calibration coefficient#desc=sixth order calibration coefficient#category=#ext=i8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_CAL_ORIG"."COEFF7" IS '#brief=seventh order calibration coefficient#desc=seventh order calibration coefficient#category=#ext=i8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_CAL_ORIG"."COEFF8" IS '#brief=eighth order calibration coefficient#desc=eighth order calibration coefficient#category=#ext=i8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_CAL_ORIG"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_RESOLUTION_CAL_ORIG"  IS '#category=Automatic Processing#desc=The gards_resolution_cal_orig table contains the original resolution calibration coefficients calculated during analysis.';
 
--------------------------------------------------------
--  DDL for Table GARDS_RESOLUTION_PAIRS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_RESOLUTION_PAIRS" 
   (	"SAMPLE_ID" NUMBER, 
	"RES_ENERGY" NUMBER, 
	"RESOLUTION" NUMBER, 
	"RES_ERROR" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_PAIRS"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_PAIRS"."RES_ENERGY" IS '#brief=resolution energy (keV)#desc=resolution energy (keV)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_PAIRS"."RESOLUTION" IS '#brief=resolution (keV)#desc=Uncertainty of resolution.#category=#ext=#na=#range=0.0 < res_error#unit=keV';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_PAIRS"."RES_ERROR" IS '#brief=error in resolution (keV)#desc=Resolution energy.#category=#ext=#na=#range=0.0 < res_energy#unit=keV';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_RESOLUTION_PAIRS"  IS '#category=Automatic Processing#desc=The gards_resolution_pairs table contains resolution calibration pairs information associated with spectral PHD.';
 
--------------------------------------------------------
--  DDL for Table GARDS_RESOLUTION_PAIRS_ORIG
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_RESOLUTION_PAIRS_ORIG" 
   (	"SAMPLE_ID" NUMBER, 
	"RES_ENERGY" NUMBER, 
	"RESOLUTION" NUMBER, 
	"RES_ERROR" NUMBER, 
	"MODDATE" DATE
   ) ENABLE ROW MOVEMENT ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_PAIRS_ORIG"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_PAIRS_ORIG"."RES_ENERGY" IS '#brief=resolution energy (keV)#desc=resolution energy (keV)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_PAIRS_ORIG"."RESOLUTION" IS '#brief=resolution (keV)#desc=Uncertainty of resolution.#category=#ext=#na=#range=0.0 < res_error#unit=keV';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_PAIRS_ORIG"."RES_ERROR" IS '#brief=error in resolution (keV)#desc=Resolution energy.#category=#ext=#na=#range=0.0 < res_energy#unit=keV';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_RESOLUTION_PAIRS_ORIG"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_RESOLUTION_PAIRS_ORIG"  IS '#category=Automatic Processing#desc=The gards_resolution_pairs_orig table contains the original resolution calibration pairs information associated with spectral PHD.';
 
--------------------------------------------------------
--  DDL for Table GARDS_ROI_CHANNELS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_ROI_CHANNELS" 
   (	"SAMPLE_ID" NUMBER, 
	"ROI" NUMBER, 
	"B_CHAN_START" NUMBER, 
	"B_CHAN_STOP" NUMBER, 
	"G_CHAN_START" NUMBER, 
	"G_CHAN_STOP" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_CHANNELS"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_CHANNELS"."ROI" IS '#brief=ROI identifier#desc=ROI identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_CHANNELS"."B_CHAN_START" IS '#brief=beta boundary start channel#desc=beta boundary start channel#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_CHANNELS"."B_CHAN_STOP" IS '#brief=beta boundary stop channel#desc=Beta boundary start channel.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_CHANNELS"."G_CHAN_START" IS '#brief=gamma boundary start channel#desc=gamma boundary start channel#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_CHANNELS"."G_CHAN_STOP" IS '#brief=gamma boundary stop channel#desc=Gamma boundary start channel.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_CHANNELS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_ROI_CHANNELS"  IS '#category=Automatic Processing#desc=The gards_roi_channels table contains the ROI boundaries in channel units that are calculated in rms_xanalyze.';
 
--------------------------------------------------------
--  DDL for Table GARDS_ROI_CONCS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_ROI_CONCS" 
   (	"SAMPLE_ID" NUMBER, 
	"ROI" NUMBER, 
	"ACTIVITY" NUMBER, 
	"ACTIV_ERR" NUMBER, 
	"MDA" NUMBER, 
	"NID_FLAG" NUMBER, 
	"REPORT_MDA" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_CONCS"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_CONCS"."ROI" IS '#brief=ROI identifier#desc=ROI identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_CONCS"."ACTIVITY" IS '#brief=activity per unit volume air (mBq/m3)#desc=activity per unit volume air (mBq/m3)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_CONCS"."ACTIV_ERR" IS '#brief=uncertainty of activity (mBq/m3)#desc=uncertainty of activity (mBq/m3)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_CONCS"."MDA" IS '#brief=minimum detectable activity (mBq/m3)#desc=minimum detectable activity (mBq/m3)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_CONCS"."NID_FLAG" IS '#brief=nuclide identification indicator (0,1 or 2)#desc=nuclide identification indicator (0 = nuclide was not identified by automated analysis; 1 = nuclide was identified by automated analysis; -1 = nuclide was identified initially by automated analysis but later rejected because the concentration was <0.0; 2 = nuclide was identified by automated analysis but was removed by the analyst through the Inspectra)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_CONCS"."REPORT_MDA" IS '#brief=indicator of whether MDA is to be reported#desc=indicator of whether MDA is to be reported#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_CONCS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_ROI_CONCS"  IS '#category=Automatic Processing#desc=The gards_roi_concs table contains information regarding the concentration of each identified nuclide that is calculated in rms_xanalyze.';
 
--------------------------------------------------------
--  DDL for Table GARDS_ROI_COUNTS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_ROI_COUNTS" 
   (	"SAMPLE_ID" NUMBER, 
	"ROI" NUMBER, 
	"GROSS" NUMBER, 
	"GROSS_ERR" NUMBER, 
	"COMPTON" NUMBER, 
	"COMPTON_ERR" NUMBER, 
	"INTERFERENCE" NUMBER, 
	"INTERFERENCE_ERR" NUMBER, 
	"MEMORY" NUMBER, 
	"MEMORY_ERR" NUMBER, 
	"DETECTOR_BACK" NUMBER, 
	"DETECTOR_BACK_ERR" NUMBER, 
	"NET" NUMBER, 
	"NET_ERR" NUMBER, 
	"LC" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_COUNTS"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_COUNTS"."ROI" IS '#brief=ROI identifier#desc=ROI identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_COUNTS"."GROSS" IS '#brief=counts in ROI before processing#desc=counts in ROI before processing#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_COUNTS"."GROSS_ERR" IS '#brief=uncertainty of gross (counts)#desc=Counts in ROI before processing.#category=#ext=#na=#range=#unit=counts';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_COUNTS"."COMPTON" IS '#brief=compton continuum background counts#desc=compton continuum background counts#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_COUNTS"."COMPTON_ERR" IS '#brief=uncertainty of compton (counts)#desc=Compton continuum background counts.#category=#ext=#na=#range=#unit=counts';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_COUNTS"."INTERFERENCE" IS '#brief=counts from interference nuclides#desc=counts from interference nuclides#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_COUNTS"."INTERFERENCE_ERR" IS '#brief=uncertainty of interference (counts)#desc=Counts from interference nuclides.#category=#ext=#na=#range=#unit=counts';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_COUNTS"."MEMORY" IS '#brief=gas background counts#desc=gas background counts#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_COUNTS"."MEMORY_ERR" IS '#brief=uncertainty of memory (counts)#desc=Gas background (that is, "memory effect") counts.#category=#ext=#na=#range=#unit=counts';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_COUNTS"."DETECTOR_BACK" IS '#brief=detector background counts#desc=detector background counts#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_COUNTS"."DETECTOR_BACK_ERR" IS '#brief=uncertainty of detector_back (counts)#desc=Detector background counts.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_COUNTS"."NET" IS '#brief=counts in ROI after processing#desc=counts in ROI after processing#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_COUNTS"."NET_ERR" IS '#brief=uncertainty of net (counts)#desc=Counts in ROI after processing.#category=#ext=#na=#range=#unit=counts';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_COUNTS"."LC" IS '#brief=critical level (counts)#desc=critical level (counts)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_COUNTS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_ROI_COUNTS"  IS '#category=Automatic Processing#desc=The gards_roi_counts table contains information regarding the counts that are calculated in rms_xanalyze for each ROI.';
 
--------------------------------------------------------
--  DDL for Table GARDS_ROI_LIB
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_ROI_LIB" 
   (	"ROI" NUMBER, 
	"NAME" VARCHAR2(8), 
	"HALFLIFE" VARCHAR2(23), 
	"HALFLIFE_ERR" VARCHAR2(23), 
	"HALFLIFE_SEC" NUMBER, 
	"ABUNDANCE" NUMBER, 
	"ABUNDANCE_ERR" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_LIB"."ROI" IS '#brief=unique ROI identifier#desc=unique ROI identifier#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_LIB"."NAME" IS '#brief=nuclide associated with ROI#desc=Nuclide name.#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_LIB"."HALFLIFE" IS '#brief=half-life of the nuclide#desc=half-life of the nuclide#category=#ext=a23#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_LIB"."HALFLIFE_ERR" IS '#brief=uncertainty of halflife#desc=uncertainty of halflife#category=#ext=a23#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_LIB"."HALFLIFE_SEC" IS '#brief=numerical half-life in seconds#desc=Uncertainty of halflife.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_LIB"."ABUNDANCE" IS '#brief=intensity of b-g coincidence event#desc=intensity of b-g coincidence event#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_LIB"."ABUNDANCE_ERR" IS '#brief=uncertainty of abundance#desc=uncertainty of abundance#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_LIB"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_ROI_LIB"  IS '#category=Automatic Processing#desc=The gards_roi_lib table relates each ROI to a specific nuclide.  The table also contains nuclide properties used in nuclide quantification.';
 
--------------------------------------------------------
--  DDL for Table GARDS_ROI_LIMITS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_ROI_LIMITS" 
   (	"SAMPLE_ID" NUMBER, 
	"ROI" NUMBER, 
	"B_ENERGY_START" NUMBER, 
	"B_ENERGY_STOP" NUMBER, 
	"G_ENERGY_START" NUMBER, 
	"G_ENERGY_STOP" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_LIMITS"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_LIMITS"."ROI" IS '#brief=ROI identifier#desc=ROI identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_LIMITS"."B_ENERGY_START" IS '#brief=beta boundary start energy (keV)#desc=beta boundary start energy (keV)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_LIMITS"."B_ENERGY_STOP" IS '#brief=beta boundary stop energy (keV)#desc=Beta boundary start energy.#category=#ext=#na=#range=#unit=keV';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_LIMITS"."G_ENERGY_START" IS '#brief=gamma boundary start energy (keV)#desc=gamma boundary start energy (keV)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_LIMITS"."G_ENERGY_STOP" IS '#brief=gamma boundary stop energy (keV)#desc=Gamma boundary start energy.#category=#ext=#na=#range=#unit=keV';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROI_LIMITS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_ROI_LIMITS"  IS '#category=Automatic Processing#desc=The gards_roi_limits table contains the ROI boundaries in energy units as specified in the PHD file.';
 
--------------------------------------------------------
--  DDL for Table GARDS_ROI_LIMITS_TEMP
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_ROI_LIMITS_TEMP" 
   (	"SAMPLE_ID" NUMBER, 
	"ROI" NUMBER, 
	"B_ENERGY_START" NUMBER, 
	"B_ENERGY_STOP" NUMBER, 
	"G_ENERGY_START" NUMBER, 
	"G_ENERGY_STOP" NUMBER, 
	"MODDATE" DATE
   ) ;
 
--------------------------------------------------------
--  DDL for Table GARDS_ROLES
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_ROLES" 
   (	"ROLE_ID" NUMBER, 
	"ROLE_NAME" VARCHAR2(30), 
	"DB_NAME" VARCHAR2(35), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROLES"."ROLE_ID" IS '#brief=unique role identifier#desc=unique role identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROLES"."ROLE_NAME" IS '#brief=string name of a role#desc=Role identifier.#category=#ext=a30#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROLES"."DB_NAME" IS '#brief=name of corresponding database role#desc=name of corresponding database role#category=#ext=a35#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROLES"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_ROLES"  IS '#category=Automatic Processing#desc=The gards_roles table contains the list of roles that can be manipulated by the MAR tools.';
 
--------------------------------------------------------
--  DDL for Table GARDS_ROLES_PERMISSIONS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_ROLES_PERMISSIONS" 
   (	"ROLE_ID" NUMBER, 
	"PERMISSION_ID" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROLES_PERMISSIONS"."ROLE_ID" IS '#brief=role identifier#desc=role identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_ROLES_PERMISSIONS"."PERMISSION_ID" IS '#brief=permission identifier#desc=permission identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_ROLES_PERMISSIONS"  IS '#category=Automatic Processing#desc=The gards_roles_permissions table contains a mapping of which permissions are assigned to which roles.';
 
--------------------------------------------------------
--  DDL for Table GARDS_SAMPLE_AUX_TEMP
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_SAMPLE_AUX_TEMP" 
   (	"SAMPLE_ID" NUMBER, 
	"SAMPLE_REF_ID" VARCHAR2(32), 
	"MEASUREMENT_ID" VARCHAR2(31), 
	"BKGD_MEASUREMENT_ID" VARCHAR2(31), 
	"SAMPLE_HEIGHT" NUMBER, 
	"CALIBRATION_DTG" DATE, 
	"MSG_ID" NUMBER, 
	"ARCHIVE_BOTTLE_ID" CHAR(2), 
	"GAS_BKGD_MEASUREMENT_ID" VARCHAR2(31), 
	"XE_COLLECT_YIELD" NUMBER, 
	"XE_COLLECT_YIELD_ERR" NUMBER, 
	"XE_VOLUME" NUMBER, 
	"XE_VOLUME_ERR" NUMBER, 
	"SAMPLE_DIAMETER" NUMBER, 
	"MODDATE" DATE
   ) ;
 
--------------------------------------------------------
--  DDL for Table GARDS_SAMPLE_CAT
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_SAMPLE_CAT" 
   (	"SAMPLE_ID" NUMBER, 
	"NAME" VARCHAR2(8), 
	"METHOD_ID" NUMBER, 
	"CATEGORY" NUMBER, 
	"UPPER_BOUND" NUMBER, 
	"LOWER_BOUND" NUMBER, 
	"CENTRAL_VALUE" NUMBER, 
	"DELTA" NUMBER, 
	"ACTIVITY" NUMBER, 
	"HOLD" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_CAT"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_CAT"."NAME" IS '#brief=nuclide name#desc=Nuclide name.#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_CAT"."METHOD_ID" IS '#brief=method identifier#desc=method identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_CAT"."CATEGORY" IS '#brief=categorization level#desc=categorization level#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_CAT"."UPPER_BOUND" IS '#brief=upper limit of the amount of a nuclide that can be acceptably found#desc=upper limit of the amount of a nuclide that can be acceptably found#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_CAT"."LOWER_BOUND" IS '#brief=lower limit of the amount of a nuclide that can be acceptably found#desc=lower limit of the amount of a nuclide that can be acceptably found#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_CAT"."CENTRAL_VALUE" IS '#brief=current estimate of the level of the random process#desc=current estimate of the level of the random process#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_CAT"."DELTA" IS '#brief=value of a variable used in bounds estimation (EWMA algorithm)#desc=value of a variable used in bounds estimation (EWMA algorithm)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_CAT"."ACTIVITY" IS '#brief=relates to gards_nucl_ided.activ_key#desc=Line activity.#category=#ext=#na=#range=#unit=mBq/m3';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_CAT"."HOLD" IS '#brief=flag that hold categorization bounds fixed and does not update values (0 = proceed, 1 = wait)#desc=flag that hold categorization bounds fixed and does not update values (0 = proceed, 1 = wait)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_CAT"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_SAMPLE_CAT"  IS '#category=Automatic Processing#desc=The gards_sample_cat table contains the most recent categorization values from either automatic or manual processing.';
 
--------------------------------------------------------
--  DDL for Table GARDS_SAMPLE_DATA
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_SAMPLE_DATA" 
   (	"SITE_DET_CODE" CHAR(15), 
	"SAMPLE_ID" NUMBER, 
	"STATION_ID" NUMBER, 
	"DETECTOR_ID" NUMBER, 
	"INPUT_FILE_NAME" VARCHAR2(256), 
	"SAMPLE_TYPE" CHAR(1), 
	"DATA_TYPE" CHAR(1), 
	"GEOMETRY" VARCHAR2(17), 
	"SPECTRAL_QUALIFIER" VARCHAR2(5), 
	"TRANSMIT_DTG" DATE, 
	"COLLECT_START" DATE, 
	"COLLECT_STOP" DATE, 
	"ACQUISITION_START" DATE, 
	"ACQUISITION_STOP" DATE, 
	"ACQUISITION_REAL_SEC" NUMBER, 
	"ACQUISITION_LIVE_SEC" NUMBER, 
	"QUANTITY" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_DATA"."SITE_DET_CODE" IS '#brief=station code concatenated with detector code#desc=station code concatenated with detector code#category=#ext=a15#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_DATA"."SAMPLE_ID" IS '#brief=unique sample identifier#desc=unique sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_DATA"."STATION_ID" IS '#brief=unique station identifier#desc=Station code.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_DATA"."DETECTOR_ID" IS '#brief=unique detector identifier#desc=unique detector identifier#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_DATA"."INPUT_FILE_NAME" IS '#brief=input data filename#desc=input data filename#category=#ext=a256#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_DATA"."SAMPLE_TYPE" IS '#brief=sample type (P, G, or B)#desc=sample type (P, G, or B)#category=#ext=a1#na=#range=sample_type IN {P, G, B}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_DATA"."DATA_TYPE" IS '#brief=type of sample; an uncontaminated crushed blank filter (B), calibration background (C), detector background (D), quality control (Q), or an actual sample (S).#desc=Type of sample; an uncontaminated crushed blank filter (B), calibration background (C), detector background (D), quality control (Q), or an actual sample (S).#category=#ext=a1#na=#range=data_type IN {B, C, D, Q, S}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_DATA"."GEOMETRY" IS '#brief=sample geometry Canberra param: CAM_T_GEOMETRY#desc=sample geometry Canberra param: CAM_T_GEOMETRY#category=#ext=a17#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_DATA"."SPECTRAL_QUALIFIER" IS '#brief=time for which the sample was exposed: FULL or PREL (preliminary)#desc=time for which the sample was exposed: FULL or PREL (preliminary)#category=#ext=a5#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_DATA"."TRANSMIT_DTG" IS '#brief=transmit date time group#desc=transmit date time group#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_DATA"."COLLECT_START" IS '#brief=collection start date#desc=collection start time Canberra param: CAM_X_SDEPOSIT#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_DATA"."COLLECT_STOP" IS '#brief=collection stop time Canberra param: CAM_X_STIME#desc=Date of sample collection commencement.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_DATA"."ACQUISITION_START" IS '#brief=acquisition start time#desc=Time difference between acquisition_stop and acquisition_start.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_DATA"."ACQUISITION_STOP" IS '#brief=acquisition stop time#desc=Date of detector count commencement.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_DATA"."ACQUISITION_REAL_SEC" IS '#brief=difference between acquisition stop and acquisition start (seconds)#desc=Total time a detectors input gate is open for processing pulses.#category=#ext=#na=#range=#unit=seconds';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_DATA"."ACQUISITION_LIVE_SEC" IS '#brief=active detection time (seconds)#desc=active detection time (seconds)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_DATA"."QUANTITY" IS '#brief=air volume sampled (m3)#desc=Air volume sampled.#category=#ext=#na=#range=#unit=m3';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_DATA"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_SAMPLE_DATA"  IS '#category=Automatic Processing#desc=The gards_sample_data table contains header data from PHD messages.';
 
--------------------------------------------------------
--  DDL for Table GARDS_SAMPLE_FLAGS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_SAMPLE_FLAGS" 
   (	"SAMPLE_ID" NUMBER, 
	"FLAG_ID" NUMBER, 
	"RESULT" NUMBER, 
	"VALUE" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_FLAGS"."SAMPLE_ID" IS '#brief=sample identifier #desc=sample identifier #category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_FLAGS"."FLAG_ID" IS '#brief=flag identifier #desc=flag identifier #category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_FLAGS"."RESULT" IS '#brief=indicator of whether or not the test passed#desc=indicator of whether or not the test passed#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_FLAGS"."VALUE" IS '#brief=threshold value used for the test#desc=Threshold value for the test.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_FLAGS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_SAMPLE_FLAGS"  IS '#category=Automatic Processing#desc=The gards_sample_flags table contains the results of the rms_DBflags analysis for each sample.';
 
--------------------------------------------------------
--  DDL for Table GARDS_SAMPLE_PROC_PARAMS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS" 
   (	"SAMPLE_ID" NUMBER, 
	"DO_BACK" NUMBER, 
	"BACK_DATA_TYPE" CHAR(1), 
	"BACK_SAMPLE_ID" NUMBER, 
	"NUCLIDE_LIB" VARCHAR2(96), 
	"ENERGY_TOL" NUMBER, 
	"MDA_LEVEL" NUMBER, 
	"NID_CONFID" NUMBER, 
	"SQUANT_ERR" NUMBER, 
	"BUILDTYPE" VARCHAR2(8), 
	"PEAK_SENSE" NUMBER, 
	"PEAK_START" NUMBER, 
	"PEAK_END" NUMBER, 
	"FWHM_MULT_WIDTH" NUMBER, 
	"LEFT_FWHM_LIM" NUMBER, 
	"RIGHT_FWHM_LIM" NUMBER, 
	"BACK_CHAN" NUMBER, 
	"BACK_TYPE" VARCHAR2(6), 
	"FIT_SINGLETS" NUMBER, 
	"CRIT_LEVEL" NUMBER, 
	"FIX_FWHM" NUMBER, 
	"AREA_REJECT" NUMBER, 
	"MDC_WIDTH" NUMBER, 
	"LC_ABSCISSA" NUMBER, 
	"DO_PD_CALC" NUMBER, 
	"DO_CSC" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."DO_BACK" IS '#brief=background subtraction indicator Canberra Parameter: CAM_L_PRNOBACKCOR#desc=background subtraction indicator Canberra Parameter: CAM_L_PRNOBACKCOR#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."BACK_DATA_TYPE" IS '#brief=data type used for background subtraction; blank (B), or detector background (D)#desc=data type used for background subtraction; blank (B), or detector background (D)#category=#ext=a1#na=#range=back_data_type IN {B, D}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."BACK_SAMPLE_ID" IS '#brief=sample identifier for sample used in background subtraction#desc=Parameter that designates the PHD type to be used for a background subtraction (controlled by the do_back column): B indicates BLANKPHD and D indicates DETBKPHD.#category=#ext=#na=#range=back_data_type IN {B, D}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."NUCLIDE_LIB" IS '#brief=nuclide library to be used during analysis Canberra Parameter: CAM_T_EXPLIB#desc=nuclide library to be used during analysis Canberra Parameter: CAM_T_EXPLIB#category=#ext=a96#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."ENERGY_TOL" IS '#brief=tolerence for nuclide identification Canberra Parameter: CAM_F_TOLERANCE#desc=tolerence for nuclide identification Canberra Parameter: CAM_F_TOLERANCE#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."MDA_LEVEL" IS '#brief=MDA confidence factor Canberra Parameter: CAM_F_MDACONFID#desc=MDA confidence factor Canberra Parameter: CAM_F_MDACONFID#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."NID_CONFID" IS '#brief=NID confidence factor Canberra Parameter: CAM_F_CONFID#desc=NID confidence factor Canberra Parameter: CAM_F_CONFID#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."SQUANT_ERR" IS '#brief=uncertainty of sample quantity (m3) Canberra param: CAM_F_SQUANTERR (No longer used in processing)#desc=uncertainty of sample quantity (m3) Canberra param: CAM_F_SQUANTERR (No longer used in processing)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."BUILDTYPE" IS '#brief=flag for Canberra: activity (NONE), or concentration (BUILD), calculations#desc=flag for Canberra: activity (NONE), or concentration (BUILD), calculations#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."PEAK_SENSE" IS '#brief=peak search sensitivity Canberra param: CAM_F_SENSITIVITY#desc=peak search sensitivity Canberra param: CAM_F_SENSITIVITY#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."PEAK_START" IS '#brief=peak search start (keV) Canberra param: CAM_L_PEAKSTART#desc=peak search start (keV) Canberra param: CAM_L_PEAKSTART#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."PEAK_END" IS '#brief=peak search end (keV) Canberra param: CAM_L_PEAKEND#desc=peak search end (keV) Canberra param: CAM_L_PEAKEND#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."FWHM_MULT_WIDTH" IS '#brief=number of FWHMs to search to determine multiplets Canberra param: CAM_F_PRFWHMPKMULT#desc=number of FWHMs to search to determine multiplets Canberra param: CAM_F_PRFWHMPKMULT#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."LEFT_FWHM_LIM" IS '#brief=left ROI FWHM limit Canberra param: CAM_F_PRFWHMPKLEFT#desc=left ROI FWHM limit Canberra param: CAM_F_PRFWHMPKLEFT#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."RIGHT_FWHM_LIM" IS '#brief=right ROI FWHM limit Canberra param: CAM_F_PRFWHMPKRIGHT#desc=right ROI FWHM limit Canberra param: CAM_F_PRFWHMPKRIGHT#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."BACK_CHAN" IS '#brief=number of continuous channels Canberra param: CAM_L_PRNBKCHN#desc=number of continuous channels Canberra param: CAM_L_PRNBKCHN#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."BACK_TYPE" IS '#brief=background type: LINEAR or STEP Canberra param: CAM_T_ROIPSBTYP#desc=sample_id of the most recent background count. This count is used for background subtraction when the background subtraction function is ON.#category=#ext=a6#na=#range=0 <= back_sample_id#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."FIT_SINGLETS" IS '#brief=fit singlets flag Canberra param: CAM_L_PRFIT#desc=fit singlets flag Canberra param: CAM_L_PRFIT#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."CRIT_LEVEL" IS '#brief=critical level test indicator Canberra param: CAM_L_CRITLEVEL#desc=critical level test indicator Canberra param: CAM_L_CRITLEVEL#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."FIX_FWHM" IS '#brief=fixed FWHM during peak search flag Canberra param: CAM_L_PRFIXFWHM#desc=fixed FWHM during peak search flag Canberra param: CAM_L_PRFIXFWHM#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."AREA_REJECT" IS '#brief=reject peaks with zero area indicator Canberra param: CAM_L_PRREJECTPEAKS#desc=reject peaks with zero area indicator Canberra param: CAM_L_PRREJECTPEAKS#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."MDC_WIDTH" IS '#brief=baseline width used for MDA calculation Canberra param: CAM_F_VPWIDTH #desc=baseline width used for MDA calculation Canberra param: CAM_F_VPWIDTH #category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."LC_ABSCISSA" IS '#brief=abscissas of the normal distribution corresponding to a confidence level; a value of 1.645 corresponds to a 95% confidence interval for the peak critical level #desc=abscissas of the normal distribution corresponding to a confidence level; a value of 1.645 corresponds to a 95% confidence interval for the peak critical level #category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."DO_PD_CALC" IS '#brief=flag that indicates if the parent/daughter calculations were run for a particular sample; 1 = calculations were run, 0 = calculations were not run #desc=flag that indicates how cascade summing should default: 0 = defaul to off, 1 = default to on.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."DO_CSC" IS '#brief=flag indicating if cascade summing was turned on/off during analysis#desc=Flag that indicates whether or not background subtraction should be performed: 1 = yes, 0 = no.#category=#ext=#na=#range=do_back IN {0,1}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS"  IS '#category=Automatic Processing#desc=The gards_sample_proc_params table contains specific processing parameters to be used for a particular spectral analysis; the table contains a combination of values from gards_proc_params_template and values entered at the command line.';
 
--------------------------------------------------------
--  DDL for Table GARDS_SAMPLE_RATIOS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_SAMPLE_RATIOS" 
   (	"SAMPLE_ID" NUMBER, 
	"RATIO_ID" VARCHAR2(15), 
	"UPPER_ROI_NUMBER" NUMBER, 
	"LOWER_ROI_NUMBER" NUMBER, 
	"COUNT_RATIO" NUMBER, 
	"COUNT_RATIO_ERR" NUMBER, 
	"MODDATE" DATE
   ) ENABLE ROW MOVEMENT ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_RATIOS"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_RATIOS"."RATIO_ID" IS '#brief=ratio identifier#desc=ratio identifier#category=#ext=a15#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_RATIOS"."UPPER_ROI_NUMBER" IS '#brief=ROI number associated with the upper ROI#desc=ROI number associated with the upper ROI#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_RATIOS"."LOWER_ROI_NUMBER" IS '#brief=ROI number associated with the lower ROI#desc=ROI number associated with the lower ROI#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_RATIOS"."COUNT_RATIO" IS '#brief=ratio of the upper ROI counts to lower ROI counts#desc=ratio of the upper ROI counts to lower ROI counts#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_RATIOS"."COUNT_RATIO_ERR" IS '#brief=uncertainty of count_ratio#desc=Ratio of upper ROI counts to lower ROI counts.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_RATIOS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_SAMPLE_RATIOS"  IS '#category=Automatic Processing#desc=The gards_sample_ratios table contains the amount of overlap between each ROI as specified in the PHD file.';
 
--------------------------------------------------------
--  DDL for Table GARDS_SAMPLE_RATIOS_TEMP
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_SAMPLE_RATIOS_TEMP" 
   (	"SAMPLE_ID" NUMBER, 
	"RATIO_ID" VARCHAR2(15), 
	"UPPER_ROI_NUMBER" NUMBER, 
	"LOWER_ROI_NUMBER" NUMBER, 
	"COUNT_RATIO" NUMBER, 
	"COUNT_RATIO_ERR" NUMBER, 
	"MODDATE" DATE
   ) ;
 
--------------------------------------------------------
--  DDL for Table GARDS_SAMPLE_STATUS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_SAMPLE_STATUS" 
   (	"SAMPLE_ID" NUMBER, 
	"ENTRY_DATE" DATE, 
	"CNF_BEGIN_DATE" DATE, 
	"CNF_END_DATE" DATE, 
	"REVIEW_DATE" DATE, 
	"REVIEW_TIME" NUMBER, 
	"ANALYST" VARCHAR2(30), 
	"STATUS" CHAR(1), 
	"CATEGORY" NUMBER, 
	"AUTO_CATEGORY" NUMBER, 
	"RELEASE_DATE" DATE, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_STATUS"."SAMPLE_ID" IS '#brief=sample identifier #desc=sample identifier #category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_STATUS"."ENTRY_DATE" IS '#brief=date sample was entered into database#desc=date sample was entered into database#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_STATUS"."CNF_BEGIN_DATE" IS '#brief=date when last analysis began#desc=date when last analysis began#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_STATUS"."CNF_END_DATE" IS '#brief=date when last analysis ended#desc=Date when last analysis began.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_STATUS"."REVIEW_DATE" IS '#brief=date sample was last reviewed #desc=date sample was last reviewed #category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_STATUS"."REVIEW_TIME" IS '#brief=amount of time to review sample (minutes) (no longer automatically updated)#desc=Date sample was last reviewed.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_STATUS"."ANALYST" IS '#brief=name of analyst who reviewed sample#desc=name of analyst who reviewed sample#category=#ext=a30#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_STATUS"."STATUS" IS '#brief=current processing status of sample.#desc=current processing status of sample. Some possible values are: A- analyzed, P- processed, R- reviewed, U- unprocessed, V- viewed, F  xxx, D  xxx, B  xxx, Z - xxx#category=#ext=a1#na=#range=status IN {A, P, R, U, V, F, D, B, Z}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_STATUS"."CATEGORY" IS '#brief=sample categorization level after interactive analysis#desc=sample categorization level after interactive analysis#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_STATUS"."AUTO_CATEGORY" IS '#brief=sample categorization level after automated analysis#desc=sample categorization level after automated analysis#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_STATUS"."RELEASE_DATE" IS '#brief=release date#desc=release date#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_STATUS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_SAMPLE_STATUS"  IS '#category=Automatic Processing#desc=The gards_sample_status table contains spectral processing historical data.';
 
--------------------------------------------------------
--  DDL for Table GARDS_SAMPLE_UPDATE_PARAMS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_SAMPLE_UPDATE_PARAMS" 
   (	"SAMPLE_ID" NUMBER, 
	"MRP_USED" NUMBER, 
	"MRP_SAMPLE_ID" NUMBER, 
	"GAINSHIFT" NUMBER, 
	"ZEROSHIFT" NUMBER, 
	"AREA_LIM" NUMBER, 
	"USE_WEIGHT" NUMBER, 
	"USE_MULT" NUMBER, 
	"F_LINEAR" NUMBER, 
	"BOOTSTRAP" NUMBER, 
	"MIN_LOOKUP" NUMBER, 
	"RER_INTERCEPT" NUMBER, 
	"RER_SLOPE" NUMBER, 
	"ECR_SLOPE" NUMBER, 
	"DO_RERU" NUMBER, 
	"RER_MRP_USED" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_UPDATE_PARAMS"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_UPDATE_PARAMS"."MRP_USED" IS '#brief=indicator of whether or not the Most Recent Prior (MRP) sample should be used#desc=Column that lists the sample_id of the MRP sample in the event that the mrp_used flag has been set to 1.#category=#ext=#na=#range=mrp_sample_id >= 0#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_UPDATE_PARAMS"."MRP_SAMPLE_ID" IS '#brief=the sample_id of the MRP sample to be used#desc=the sample_id of the MRP sample to be used#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_UPDATE_PARAMS"."GAINSHIFT" IS '#brief=gain change for matching, percent (typically 0.1)#desc=gain change for matching, percent (typically 0.1)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_UPDATE_PARAMS"."ZEROSHIFT" IS '#brief=zero change for matching, channels (typically 1)#desc=Change in channel number at 0 keV between one spectrum and the previous spectrum.#category=#ext=#na=#range=zeroshift >= 0.0 #unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_UPDATE_PARAMS"."AREA_LIM" IS '#brief=minimum peak area for inclusion in matching (counts)#desc=minimum peak area for inclusion in matching (counts)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_UPDATE_PARAMS"."USE_WEIGHT" IS '#brief=0/1 flag for use of weights in ECR updating (typically 1)#desc=0/1 flag for use of weights in ECR updating (typically 1)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_UPDATE_PARAMS"."USE_MULT" IS '#brief=0/1 flag for use of multiplets in ECR updating (typically 1)#desc=0/1 flag for use of multiplets in ECR updating (typically 1)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_UPDATE_PARAMS"."F_LINEAR" IS '#brief=0/1 flag for forcing ECR to be first-order (typically 0)#desc=0/1 flag for forcing ECR to be first-order (typically 0)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_UPDATE_PARAMS"."BOOTSTRAP" IS '#brief=0/1 flag for ignoring prior ECR/ resolution versus energy regression (RER) (typically 0)#desc=0/1 flag for ignoring prior ECR/ resolution versus energy regression (RER) (typically 0)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_UPDATE_PARAMS"."MIN_LOOKUP" IS '#brief=minimum library lookup tolerance, keV (typically 0.2)#desc=minimum library lookup tolerance, keV (typically 0.2)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_UPDATE_PARAMS"."RER_INTERCEPT" IS '#brief=default RER intercept (typically 1.2)#desc=default RER intercept (typically 1.2)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_UPDATE_PARAMS"."RER_SLOPE" IS '#brief=default RER coeff (typically 0.03) #desc=Default RER intercept to be used during calculations.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_UPDATE_PARAMS"."ECR_SLOPE" IS '#brief=default ECR slope#desc=default ECR slope#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_UPDATE_PARAMS"."DO_RERU" IS '#brief=flag that indicates if a resolution update was performed#desc=flag that indicates if a resolution update was performed#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_UPDATE_PARAMS"."RER_MRP_USED" IS '#brief=indicates what RER was chosen during analysis#desc=indicates what RER was chosen during analysis#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_UPDATE_PARAMS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_SAMPLE_UPDATE_PARAMS"  IS '#category=Automatic Processing#desc=The gards_sample_update_params table holds the actual parameters used for energy calibration updating during analysis. This table may contain a combination of defaults from gards_update_params_template and values from the command line.';
 
--------------------------------------------------------
--  DDL for Table GARDS_SAMPLE_XE_PROC_PARAMS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_SAMPLE_XE_PROC_PARAMS" 
   (	"SAMPLE_ID" NUMBER, 
	"ROI" NUMBER, 
	"LC_ABSCISSA" NUMBER, 
	"BETA_ECR_ORDER" NUMBER, 
	"GAMMA_ECR_ORDER" NUMBER, 
	"COMPTON" NUMBER, 
	"DET_BACK_USED" NUMBER, 
	"GAS_BACK_USED" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_XE_PROC_PARAMS"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_XE_PROC_PARAMS"."ROI" IS '#brief=ROI identifier#desc=ROI identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_XE_PROC_PARAMS"."LC_ABSCISSA" IS '#brief=abscissa of the normal distribution corresponding to a confidence level#desc=abscissa of the normal distribution corresponding to a confidence level#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_XE_PROC_PARAMS"."BETA_ECR_ORDER" IS '#brief=determines whether the beta ECR is linear, quadratic, or manually defined#desc=determines whether the beta ECR is linear, quadratic, or manually defined#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_XE_PROC_PARAMS"."GAMMA_ECR_ORDER" IS '#brief=determines whether the gamma ECR is linear, quadratic, or manually defined#desc=determines whether the gamma ECR is linear, quadratic, or manually defined#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_XE_PROC_PARAMS"."COMPTON" IS '#brief=number of compton channels#desc=number of compton channels#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_XE_PROC_PARAMS"."DET_BACK_USED" IS '#brief=determines whether the detector background is in use or not (1 = YES, 0 = NO)#desc=determines whether the detector background is in use or not (1 = YES, 0 = NO)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_XE_PROC_PARAMS"."GAS_BACK_USED" IS '#brief=determines whether the gas background is in use or not (1 = YES, 0 = NO)#desc=Determines whether the gamma ecr is linear, quadratic, or manually defined; 1 = linear, 2 = quadratic, 3 = manual (ecr is set on command line).#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SAMPLE_XE_PROC_PARAMS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_SAMPLE_XE_PROC_PARAMS"  IS '#category=Automatic Processing#desc=The gards_sample_xe_proc_params table contains specific processing parameters to be used for a particular spectral analysis.';
 
--------------------------------------------------------
--  DDL for Table GARDS_SOH_CODE
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_SOH_CODE" 
   (	"PARAM" VARCHAR2(30), 
	"PARAM_CODE" NUMBER, 
	"PARAM_DISPLAY" VARCHAR2(30), 
	"PARAM_DISPLAY_FLAG" NUMBER, 
	"DISPLAY_STATION" NUMBER, 
	"DISPLAY_DETECTOR" NUMBER, 
	"UNIT" VARCHAR2(32), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SOH_CODE"."PARAM" IS '#brief=SOH parameter name#desc=SOH parameter name#category=#ext=a30#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SOH_CODE"."PARAM_CODE" IS '#brief=SOH parameter code#desc=SOH parameter name.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SOH_CODE"."PARAM_DISPLAY" IS '#brief=text of the parameter to be displayed in Trendvue #desc=SOH parameter code.#category=#ext=a30#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SOH_CODE"."PARAM_DISPLAY_FLAG" IS '#brief=flag indicating whether or not a particular parameter is diaplayed#desc=flag indicating whether or not a particular parameter is diaplayed#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SOH_CODE"."DISPLAY_STATION" IS '#brief=flag indicating whether (1) or not (0) stations will appear in the Trendvue dialog box#desc=Flag indicating if the SOH parameter is associated with a detector; 1 = the parameter is associated with a detector and Trendvue should allow users to query by detector, 0 = the parameter is station only and no detectors will appear in the Trendvue dialog box.#category=#ext=i1#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SOH_CODE"."DISPLAY_DETECTOR" IS '#brief=flag indicating whether (1) or not (0) detectors will appear in the Trendvue dialog box#desc=1 or 0; if 1, then the parameter is associated with a detector and Trendvue will allow users to query by detector; if it is 0, then this parameter is station only and no detectors will appear in the Trendvue dialog box#category=#ext=i1#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SOH_CODE"."UNIT" IS '#brief=unit that the parameter is stored in#desc=unit that the parameter is stored in#category=#ext=a32#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_SOH_CODE"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_SOH_CODE"  IS '#category=Automatic Processing#desc=The gards_soh_code table contains all state of health (SOH) parameter names and their codes.';
 
--------------------------------------------------------
--  DDL for Table GARDS_STADET
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_STADET" 
   (	"STATION_ID" NUMBER, 
	"DETECTOR_ID" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STADET"."STATION_ID" IS '#brief=unique station identifier#desc=Station code.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STADET"."DETECTOR_ID" IS '#brief=unique detector identifier#desc=unique detector identifier#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STADET"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_STADET"  IS '#category=Automatic Processing#desc=The gards_stadet table contains a complete list of all station/detector identifier code combinations. The entries in this table are generated via a trigger on the gards_sample_data table.';
 
--------------------------------------------------------
--  DDL for Table GARDS_STATIONS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_STATIONS" 
   (	"STATION_ID" NUMBER, 
	"STATION_CODE" VARCHAR2(5), 
	"COUNTRY_CODE" VARCHAR2(2), 
	"TYPE" VARCHAR2(6), 
	"DESCRIPTION" VARCHAR2(40), 
	"LAT" NUMBER, 
	"LON" NUMBER, 
	"ELEVATION" NUMBER, 
	"DATE_BEGIN" DATE, 
	"DATE_END" DATE, 
	"STATUS" VARCHAR2(2), 
	"POCID" NUMBER, 
	"SPLIT_STATION" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATIONS"."STATION_ID" IS '#brief=unique station identifier#desc=Station code.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATIONS"."STATION_CODE" IS '#brief=station code#desc=station code#category=#ext=a5#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATIONS"."COUNTRY_CODE" IS '#brief=country code of site#desc=country code of site#category=#ext=a2#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATIONS"."TYPE" IS '#brief=station type#desc=Brief description of detector or station.#category=#ext=a6#na=#range=ASCII characters#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATIONS"."DESCRIPTION" IS '#brief=description of station#desc=Description of the code, detector, or station.#category=#ext=a40#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATIONS"."LAT" IS '#brief=latitude (degrees)#desc=latitude (degrees)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATIONS"."LON" IS '#brief=longitude (degrees)#desc=longitude (degrees)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATIONS"."ELEVATION" IS '#brief=elevation (m)#desc=elevation (m)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATIONS"."DATE_BEGIN" IS '#brief=station initialization date#desc=station initialization date#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATIONS"."DATE_END" IS '#brief=station decommissioning date#desc=Station/Detector initialization date.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATIONS"."STATUS" IS '#brief=status of station, if NULL then station is fully operational otherwise the status is I #desc=Status of station: if NULL, then station is fully operational, otherwise status is I.#category=#ext=a2#na=#range=status IN {I}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATIONS"."POCID" IS '#brief=point of contact identifier#desc=point of contact identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATIONS"."SPLIT_STATION" IS '#brief=flag indicating whether or not station is split#desc=flag indicating whether or not station is split#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATIONS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_STATIONS"  IS '#category=Automatic Processing#desc=The gards_stations table contains a station overview and station characteristics.';
 
--------------------------------------------------------
--  DDL for Table GARDS_STATIONS_SCHEDULE
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_STATIONS_SCHEDULE" 
   (	"STATION_ID" NUMBER, 
	"BEGIN_DATE" DATE, 
	"END_DATE" DATE, 
	"CODE" CHAR(5), 
	"TEMPORAL_VALUE" NUMBER, 
	"TEMPORAL_UNIT" CHAR(5), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATIONS_SCHEDULE"."STATION_ID" IS '#brief=unique station identifier#desc=Station code.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATIONS_SCHEDULE"."BEGIN_DATE" IS '#brief=initial date of schedule#desc=initial date of schedule#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATIONS_SCHEDULE"."END_DATE" IS '#brief=final date of schedule#desc=final date of schedule#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATIONS_SCHEDULE"."CODE" IS '#brief=code symbol SCHEDULE as found in the gards_codes table. SF_GP for full sample grace period or SPHDF for full sample PHD#desc=code symbol SCHEDULE as found in the gards_codes table. SF_GP for full sample grace period or SPHDF for full sample PHD#category=#ext=a5#na=#range=code IN {SF_GP, SPHDF}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATIONS_SCHEDULE"."TEMPORAL_VALUE" IS '#brief=expected station schedule period#desc=Units for schedule period - currently only the value DAYS is supported.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATIONS_SCHEDULE"."TEMPORAL_UNIT" IS '#brief=units for schedule period - currently only the value DAYS is supported#desc=units for schedule period - currently only the value DAYS is supported#category=#ext=a5#na=#range=temporal_unit IN {DAYS}#unit=days';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATIONS_SCHEDULE"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_STATIONS_SCHEDULE"  IS '#category=Automatic Processing#desc=The gards_stations_schedule table contains schedule descriptions for stations reporting to a data center.';
 
--------------------------------------------------------
--  DDL for Table GARDS_STATION_ASSIGNMENTS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_STATION_ASSIGNMENTS" 
   (	"STATION_ID" NUMBER, 
	"USER_ID" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATION_ASSIGNMENTS"."STATION_ID" IS '#brief=unique station identifier#desc=Station code.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATION_ASSIGNMENTS"."USER_ID" IS '#brief=user identifier#desc=user identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATION_ASSIGNMENTS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_STATION_ASSIGNMENTS"  IS '#category=Automatic Processing#desc=The gards_station_assignments table contains a mapping of which stations are assigned to which users.';
 
--------------------------------------------------------
--  DDL for Table GARDS_STATUS_HISTORY
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_STATUS_HISTORY" 
   (	"SAMPLE_ID" NUMBER, 
	"USER_NAME" VARCHAR2(30), 
	"OLD_STATUS" CHAR(1), 
	"NEW_STATUS" CHAR(1), 
	"DTG" DATE, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATUS_HISTORY"."SAMPLE_ID" IS '#brief=foriegn key#desc=foriegn key#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATUS_HISTORY"."USER_NAME" IS '#brief=user name#desc=user name#category=#ext=a30#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATUS_HISTORY"."OLD_STATUS" IS '#brief=sample_status before change#desc=sample_status before change#category=#ext=a1#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATUS_HISTORY"."NEW_STATUS" IS '#brief=sample_status after change#desc=sample_status after change#category=#ext=a1#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATUS_HISTORY"."DTG" IS '#brief=date of change#desc=date of change#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_STATUS_HISTORY"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_STATUS_HISTORY"  IS '#category=Automatic Processing#desc=The gards_status_history table contains a list of changes in gards_sample_stations.status for reviewed samples.';
 
--------------------------------------------------------
--  DDL for Table GARDS_TOTAL_EFFIC
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_TOTAL_EFFIC" 
   (	"SAMPLE_ID" NUMBER, 
	"EFFIC_ENERGY" NUMBER, 
	"EFFICIENCY" NUMBER, 
	"EFFIC_ERROR" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_TOTAL_EFFIC"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_TOTAL_EFFIC"."EFFIC_ENERGY" IS '#brief=efficiency energy (keV)#desc=efficiency energy (keV)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_TOTAL_EFFIC"."EFFICIENCY" IS '#brief=efficiency#desc=Uncertainty of efficiency.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_TOTAL_EFFIC"."EFFIC_ERROR" IS '#brief=uncertainty of efficiency#desc=uncertainty of efficiency#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_TOTAL_EFFIC"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_TOTAL_EFFIC"  IS '#category=Automatic Processing#desc=The gards_total_effic table contains detector  total efficiency data as specified in the PHD file.';
 
--------------------------------------------------------
--  DDL for Table GARDS_TRENDVUE
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_TRENDVUE" 
   (	"SESSION_ID" NUMBER, 
	"DATE_VALUE" DATE, 
	"NUM_VALUE1" NUMBER, 
	"NUM_VALUE2" NUMBER, 
	"NUM_VALUE3" NUMBER, 
	"NUM_VALUE4" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_TRENDVUE"."SESSION_ID" IS '#brief=unique session identifier#desc=unique session identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_TRENDVUE"."DATE_VALUE" IS '#brief=date of the Trendvue plot#desc=date of the Trendvue plot#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_TRENDVUE"."NUM_VALUE1" IS '#brief=first plot value#desc=First plot value.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_TRENDVUE"."NUM_VALUE2" IS '#brief=second plot value#desc=Second plot value.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_TRENDVUE"."NUM_VALUE3" IS '#brief=third plot value#desc=Third plot value.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_TRENDVUE"."NUM_VALUE4" IS '#brief=fourth plot value#desc=Fourth plot value.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_TRENDVUE"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_TRENDVUE"  IS '#category=Automatic Processing#desc=The gards_trendvue table contains data produced by the Trendvue application and is purged at the end of each session.';
 
--------------------------------------------------------
--  DDL for Table GARDS_UPDATE_PARAMS_TEMPLATE
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_UPDATE_PARAMS_TEMPLATE" 
   (	"DETECTOR_ID" NUMBER, 
	"GAINSHIFT" NUMBER, 
	"ZEROSHIFT" NUMBER, 
	"AREA_LIM" NUMBER, 
	"USE_WEIGHT" NUMBER, 
	"USE_MULT" NUMBER, 
	"F_LINEAR" NUMBER, 
	"BOOTSTRAP" NUMBER, 
	"MIN_LOOKUP" NUMBER, 
	"RER_INTERCEPT" NUMBER, 
	"RER_SLOPE" NUMBER, 
	"DO_RERU" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_UPDATE_PARAMS_TEMPLATE"."DETECTOR_ID" IS '#brief=unique detector identifier#desc=unique detector identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_UPDATE_PARAMS_TEMPLATE"."GAINSHIFT" IS '#brief=gain change for matching, percent (typically 0.1)#desc=gain change for matching, percent (typically 0.1)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_UPDATE_PARAMS_TEMPLATE"."ZEROSHIFT" IS '#brief=zero change for matching, channels (typically 1)#desc=Change in channel number at 0 keV between one spectrum and the previous spectrum.#category=#ext=#na=#range=zeroshift >= 0.0 #unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_UPDATE_PARAMS_TEMPLATE"."AREA_LIM" IS '#brief=minimum peak area for inclusion in matching (counts)#desc=minimum peak area for inclusion in matching (counts)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_UPDATE_PARAMS_TEMPLATE"."USE_WEIGHT" IS '#brief=0/1 flag for use of weights in ECR updating (typically 1)#desc=0/1 flag for use of weights in ECR updating (typically 1)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_UPDATE_PARAMS_TEMPLATE"."USE_MULT" IS '#brief=0/1 flag for use of multiplets in ECR updating (typically 1)#desc=0/1 flag for use of multiplets in ECR updating (typically 1)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_UPDATE_PARAMS_TEMPLATE"."F_LINEAR" IS '#brief=0/1 flag for forcing ECR to be first-order (typically 0)#desc=0/1 flag for forcing ECR to be first-order (typically 0)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_UPDATE_PARAMS_TEMPLATE"."BOOTSTRAP" IS '#brief=0/1 flag for ignoring prior ECR/RER (typically 0)#desc=0/1 flag for ignoring prior ECR/RER (typically 0)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_UPDATE_PARAMS_TEMPLATE"."MIN_LOOKUP" IS '#brief=minimum library lookup tolerance, keV (typically 0.2)#desc=minimum library lookup tolerance, keV (typically 0.2)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_UPDATE_PARAMS_TEMPLATE"."RER_INTERCEPT" IS '#brief=default RER intercept (typically 1.2)#desc=default RER intercept (typically 1.2)#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_UPDATE_PARAMS_TEMPLATE"."RER_SLOPE" IS '#brief=default RER slope (typically 0.03)#desc=Default RER intercept to be used during calculations.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_UPDATE_PARAMS_TEMPLATE"."DO_RERU" IS '#brief=0/1 flag that indicates whether or not a resolution update should be performed#desc=0/1 flag that indicates whether or not a resolution update should be performed#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_UPDATE_PARAMS_TEMPLATE"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_UPDATE_PARAMS_TEMPLATE"  IS '#category=Automatic Processing#desc=The gards_update_params_template table holds the default parameters used for energy calibration updating during analysis; these values can be overridden at the command line.';
 
--------------------------------------------------------
--  DDL for Table GARDS_UPDATE_REFLINES
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_UPDATE_REFLINES" 
   (	"STATION_ID" NUMBER, 
	"DETECTOR_ID" NUMBER, 
	"REFPEAK_ENERGY" NUMBER, 
	"DATA_TYPE" CHAR(1), 
	"SPECTRAL_QUALIFIER" VARCHAR2(5), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_UPDATE_REFLINES"."STATION_ID" IS '#brief=unique station identifier#desc=Station code.#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_UPDATE_REFLINES"."DETECTOR_ID" IS '#brief=unique detector identifier#desc=unique detector identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_UPDATE_REFLINES"."REFPEAK_ENERGY" IS '#brief=known reference energy for a nuclide#desc=known reference energy for a nuclide#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_UPDATE_REFLINES"."DATA_TYPE" IS '#brief=type of sample; an uncontaminated crushed blank filter (B), calibration background (C), detector background (D), quality control (Q), or an actual sample (S)#desc=Type of sample; an uncontaminated crushed blank filter (B), calibration background (C), detector background (D), quality control (Q), or an actual sample (S).#category=#ext=a1#na=#range=data_type IN {B, C, D, Q, S}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_UPDATE_REFLINES"."SPECTRAL_QUALIFIER" IS '#brief=time for which the sample was exposed: FULL or PREL (preliminary)#desc=time for which the sample was exposed: FULL or PREL (preliminary)#category=#ext=a5#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_UPDATE_REFLINES"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_UPDATE_REFLINES"  IS '#category=Automatic Processing#desc=The gards_update_reflines table contains the energies of the reference lines used in the ECR/RER updating functions.';
 
--------------------------------------------------------
--  DDL for Table GARDS_USERENV
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_USERENV" 
   (	"NAME" VARCHAR2(40), 
	"VALUE" VARCHAR2(256), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_USERENV"."NAME" IS '#brief=variable name#desc=variable name#category=#ext=a40#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_USERENV"."VALUE" IS '#brief=variable value#desc=variable value#category=#ext=a256#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_USERENV"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_USERENV"  IS '#category=Automatic Processing#desc=The gards_userenv table contains configurable environment variables used by the Automatic Processing software.';
 
--------------------------------------------------------
--  DDL for Table GARDS_USERS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_USERS" 
   (	"USER_ID" NUMBER, 
	"USER_NAME" VARCHAR2(30), 
	"ASSIGNABLE" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_USERS"."USER_ID" IS '#brief=unique user identifier#desc=unique user identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_USERS"."USER_NAME" IS '#brief=string name for a user database login name#desc=User identifier.#category=#ext=a30#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_USERS"."ASSIGNABLE" IS '#brief=1 = user can be assigned stations for review or 0 = user not to be assigned stations#desc=1 = user can be assigned stations for review or 0 = user not to be assigned stations#category=#ext=i1#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_USERS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_USERS"  IS '#category=Interactive Analysis#desc=Contains details of radionuclide-related personnel.';
 
--------------------------------------------------------
--  DDL for Table GARDS_USERS_ROLES
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_USERS_ROLES" 
   (	"USER_ID" NUMBER, 
	"ROLE_ID" NUMBER, 
	"DEFAULT_ROLE" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_USERS_ROLES"."USER_ID" IS '#brief=user identifier#desc=user identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_USERS_ROLES"."ROLE_ID" IS '#brief=role identifier#desc=role identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_USERS_ROLES"."DEFAULT_ROLE" IS '#brief=integer representation of the default role name to be assigned to the user#desc=integer representation of the default role name to be assigned to the user#category=#ext=#na=#range=#unit=';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_USERS_ROLES"  IS '#category=Automatic Processing#desc=The gards_users_roles table contains a mapping of which roles are assigned to which user.';
 
--------------------------------------------------------
--  DDL for Table GARDS_USER_COMMENTS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_USER_COMMENTS" 
   (	"SAMPLE_ID" NUMBER, 
	"COMMENT_ID" NUMBER, 
	"COMMENT_TEXT" VARCHAR2(2048), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_USER_COMMENTS"."SAMPLE_ID" IS '#brief=sample identifier#desc=sample identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_USER_COMMENTS"."COMMENT_ID" IS '#brief=comment identifier #desc=comment identifier #category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_USER_COMMENTS"."COMMENT_TEXT" IS '#brief=free-form user comments#desc=Unique comment identifier.#category=#ext=a2048#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_USER_COMMENTS"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_USER_COMMENTS"  IS '#category=Automatic Processing#desc=The gards_user_comments table contains text associated with user-defined comments.';
 
--------------------------------------------------------
--  DDL for Table GARDS_XE_NUCL_LIB
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_XE_NUCL_LIB" 
   (	"NUCLIDE_ID" NUMBER, 
	"NAME" VARCHAR2(8), 
	"TYPE" VARCHAR2(16), 
	"HALFLIFE_SEC" NUMBER, 
	"HALFLIFE" VARCHAR2(23), 
	"HALFLIFE_ERR" VARCHAR2(23), 
	"NUM_LINES" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_XE_NUCL_LIB"."NUCLIDE_ID" IS '#brief=nuclide identifier#desc=nuclide identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_XE_NUCL_LIB"."NAME" IS '#brief=nuclide name#desc=Nuclide name.#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_XE_NUCL_LIB"."TYPE" IS '#brief=nuclide type; choices are: #desc=Nuclide type. Choices are: ACTIVATION, COSMIC, FISSION(G), FISSION(P), or NATURAL.#category=#ext=a16#na=#range=type IN {ACTIVATION, COSMIC, FISSION(G), FISSION(P), NATURAL}#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_XE_NUCL_LIB"."HALFLIFE_SEC" IS '#brief=half life in seconds#desc=half life in seconds#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_XE_NUCL_LIB"."HALFLIFE" IS '#brief=half life#desc=half life#category=#ext=a23#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_XE_NUCL_LIB"."HALFLIFE_ERR" IS '#brief=level of confidence#desc=level of confidence#category=#ext=a23#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_XE_NUCL_LIB"."NUM_LINES" IS '#brief=number of lines#desc=number of lines#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_XE_NUCL_LIB"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_XE_NUCL_LIB"  IS '#category=Automatic Processing#desc=The gards_xe_nucl_lib table contains nuclide library information used by the Inspectra when displaying nuclide data for gamma spectroscopy noble gas stations.';
 
--------------------------------------------------------
--  DDL for Table GARDS_XE_NUCL_LINES_LIB
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_XE_NUCL_LINES_LIB" 
   (	"NAME" VARCHAR2(8), 
	"ENERGY" NUMBER, 
	"ENERGY_ERR" NUMBER, 
	"ABUNDANCE" NUMBER, 
	"ABUNDANCE_ERR" NUMBER, 
	"KEY_FLAG" NUMBER, 
	"NUCLIDE_ID" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_XE_NUCL_LINES_LIB"."NAME" IS '#brief=nuclide name#desc=Nuclide name.#category=#ext=a8#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_XE_NUCL_LINES_LIB"."ENERGY" IS '#brief=line energy (keV) Canberra parameter: CAM_F_NLENERGY#desc=line energy (keV) Canberra parameter: CAM_F_NLENERGY#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_XE_NUCL_LINES_LIB"."ENERGY_ERR" IS '#brief=uncertainty of line energy Canberra parameter: CAM_F_NLENGERR#desc=Line energy.#category=#ext=#na=#range=0 <= energy#unit=keV';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_XE_NUCL_LINES_LIB"."ABUNDANCE" IS '#brief=abundance of line (percent) Canberra parameter: CAM_F_NLABUN #desc=Abundance of line.#category=#ext=#na=#range=#unit=percent';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_XE_NUCL_LINES_LIB"."ABUNDANCE_ERR" IS '#brief=uncertainty of abundance (percent) Canberra parameter: CAM_F_NLABUNERR#desc=uncertainty of abundance (percent) Canberra parameter: CAM_F_NLABUNERR#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_XE_NUCL_LINES_LIB"."KEY_FLAG" IS '#brief=key line indicator Canberra parameter: CAM_L_NLFKEYLINE #desc=key line indicator Canberra parameter: CAM_L_NLFKEYLINE #category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_XE_NUCL_LINES_LIB"."NUCLIDE_ID" IS '#brief=nuclide identifier Canberra parameter: CAM_L_NLNUCL#desc=nuclide identifier Canberra parameter: CAM_L_NLNUCL#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_XE_NUCL_LINES_LIB"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_XE_NUCL_LINES_LIB"  IS '#category=Automatic Processing#desc=The gards_xe_nucl_lines_lib table contains nuclide library information for specific lines of a nuclide and is used by the Inspectra when displaying nuclide data for gamma spectroscopy noble gas stations.';
 
--------------------------------------------------------
--  DDL for Table GARDS_XE_PROC_PARAMS_TEMPLATE
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_XE_PROC_PARAMS_TEMPLATE" 
   (	"DETECTOR_ID" NUMBER, 
	"ROI" NUMBER, 
	"LC_ABSCISSA" NUMBER, 
	"BETA_ECR_ORDER" NUMBER, 
	"GAMMA_ECR_ORDER" NUMBER, 
	"COMPTON" NUMBER, 
	"DET_BACK_USED" NUMBER, 
	"GAS_BACK_USED" NUMBER, 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_XE_PROC_PARAMS_TEMPLATE"."DETECTOR_ID" IS '#brief=unique detector identifier#desc=unique detector identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_XE_PROC_PARAMS_TEMPLATE"."ROI" IS '#brief=ROI identifier#desc=ROI identifier#category=#ext=i10#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_XE_PROC_PARAMS_TEMPLATE"."LC_ABSCISSA" IS '#brief=abscissa of the normal distribution corresponding to a confidence level#desc=abscissa of the normal distribution corresponding to a confidence level#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_XE_PROC_PARAMS_TEMPLATE"."BETA_ECR_ORDER" IS '#brief=determines whether the beta ECR is linear, quadratic, or manually defined#desc=determines whether the beta ECR is linear, quadratic, or manually defined#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_XE_PROC_PARAMS_TEMPLATE"."GAMMA_ECR_ORDER" IS '#brief=determines whether the gamma ECR is linear, quadratic or manually defined#desc=determines whether the gamma ECR is linear, quadratic or manually defined#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_XE_PROC_PARAMS_TEMPLATE"."COMPTON" IS '#brief=number of compton channels#desc=number of compton channels#category=#ext=#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_XE_PROC_PARAMS_TEMPLATE"."DET_BACK_USED" IS '#brief=determines whether the detector background is in use or not (1 = YES, 0 = NO)#desc=determines whether the detector background is in use or not (1 = YES, 0 = NO)#category=#ext=i1#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_XE_PROC_PARAMS_TEMPLATE"."GAS_BACK_USED" IS '#brief=determines whether the gas background is in use or not (1 = YES, 0 = NO)#desc=Determines whether the gamma ecr is linear, quadratic, or manually defined; 1 = linear, 2 = quadratic, 3 = manual (ecr is set on command line).#category=#ext=i1#na=#range=#unit=';
 
   COMMENT ON COLUMN "RMSMAN"."GARDS_XE_PROC_PARAMS_TEMPLATE"."MODDATE" IS '#brief=date/time at which the row was last modified#desc=The date/time at which the row was last modified.#category=#ext=a21#na=NOT ALLOWED#range=any valid ORACLE date#unit=Date';
 
   COMMENT ON TABLE "RMSMAN"."GARDS_XE_PROC_PARAMS_TEMPLATE"  IS '#category=Automatic Processing#desc=The gards_xe_proc_params_template table contains the information used for nuclide identification.';
 
--------------------------------------------------------
--  DDL for Table GARDS_XE_REFLINE_MASTER
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_XE_REFLINE_MASTER" 
   (	"REFPEAK_ENERGY" NUMBER, 
	"DATA_TYPE" CHAR(1), 
	"SPECTRAL_QUALIFIER" VARCHAR2(5), 
	"CALIBRATION_TYPE" VARCHAR2(3), 
	"MODDATE" DATE
   ) ;
 
--------------------------------------------------------
--  DDL for Table GARDS_XE_RESULTS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."GARDS_XE_RESULTS" 
   (	"SAMPLE_ID" NUMBER, 
	"METHOD_ID" NUMBER, 
	"NUCLIDE_ID" NUMBER, 
	"CONC" FLOAT(126), 
	"CONC_ERR" FLOAT(126), 
	"MDC" FLOAT(126), 
	"MDI" FLOAT(126), 
	"NID_FLAG" NUMBER, 
	"LC" FLOAT(126), 
	"LD" FLOAT(126), 
	"SAMPLE_ACT" FLOAT(126), 
	"COV_XE_131M" FLOAT(126), 
	"COV_XE_133M" FLOAT(126), 
	"COV_XE_133" FLOAT(126), 
	"COV_XE_135" FLOAT(126), 
	"COV_RADON" FLOAT(126), 
	"MODDATE" DATE
   ) ;
 
   COMMENT ON TABLE "RMSMAN"."GARDS_XE_RESULTS"  IS '#category=Automatic Processing#desc=gards xe results';
 
--------------------------------------------------------
--  DDL for Table JAVA$CLASS$MD5$TABLE
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."JAVA$CLASS$MD5$TABLE" 
   (	"NAME" VARCHAR2(200), 
	"MD5" RAW(16)
   ) ;
 
--------------------------------------------------------
--  DDL for Table JAVA$OPTIONS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."JAVA$OPTIONS" 
   (	"WHAT" VARCHAR2(128), 
	"OPT" VARCHAR2(20), 
	"VALUE" VARCHAR2(128)
   ) ;
 
--------------------------------------------------------
--  DDL for Table R2_RMS_SPECTRUM_LOG
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."R2_RMS_SPECTRUM_LOG" 
   (	"COMMENT_ID" NUMBER, 
	"ANALYST" VARCHAR2(15), 
	"SPECTRUM_ID" NUMBER, 
	"COMMENT_DATE" DATE, 
	"COMMENT_TYPE" VARCHAR2(15)
   ) ;
 
--------------------------------------------------------
--  DDL for Table R2_RMS_TYPE2
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."R2_RMS_TYPE2" 
   (	"SPECTRUM_ID" NUMBER, 
	"ANALYST" VARCHAR2(15), 
	"TYPE2_ENERGY" NUMBER, 
	"TYPE2_NUCLIDE" VARCHAR2(30), 
	"COMMENT_DATE" DATE
   ) ;
 
   COMMENT ON TABLE "RMSMAN"."R2_RMS_TYPE2"  IS '#category=Manual Processing#desc=The R2_RMS_TYPE2 table contains the type 2 lines found during review  for a given sample_id';
 
--------------------------------------------------------
--  DDL for Table RMS_COMPARE_SAMPLES
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."RMS_COMPARE_SAMPLES" 
   (	"SAMPLE_ID" NUMBER
   ) ;
 
--------------------------------------------------------
--  DDL for Table RMS_PURGE_DIFFS
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."RMS_PURGE_DIFFS" 
   (	"SAMPLE_ID" NUMBER
   ) ;
 
--------------------------------------------------------
--  DDL for Table RMS_PURGE_SAMPLES
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."RMS_PURGE_SAMPLES" 
   (	"SAMPLE_ID" NUMBER
   ) ;
 
--------------------------------------------------------
--  DDL for Table TETABLE
--------------------------------------------------------

  CREATE TABLE "RMSMAN"."TETABLE" 
   (	"INX" NUMBER(*,0), 
	"TEXT" VARCHAR2(30)
   ) ;
 
--------------------------------------------------------
--  Constraints for Table CREATE$JAVA$LOB$TABLE
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."CREATE$JAVA$LOB$TABLE" ADD UNIQUE ("NAME") ENABLE;
 
--------------------------------------------------------
--  Constraints for Table GARDS_AUX_LINES_LIB
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_AUX_LINES_LIB" ADD CONSTRAINT "UQ_AUX_LNS_LIB" UNIQUE ("NAME", "ENERGY", "ABUNDANCE_ACT") ENABLE;
 
--------------------------------------------------------
--  Constraints for Table GARDS_BG_CONFIG_PARAMS_TEMP
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_BG_CONFIG_PARAMS_TEMP" MODIFY ("DETECTOR_ID" NOT NULL ENABLE);
 
--------------------------------------------------------
--  Constraints for Table GARDS_BG_ENERGY_CAL
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_BG_ENERGY_CAL" ADD PRIMARY KEY ("SAMPLE_ID") ENABLE;
 
--------------------------------------------------------
--  Constraints for Table GARDS_BG_ISOTOPE_CONCS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_BG_ISOTOPE_CONCS" MODIFY ("SAMPLE_ID" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_BG_ISOTOPE_CONCS" MODIFY ("NUCLIDE_ID" NOT NULL ENABLE);
 
--------------------------------------------------------
--  Constraints for Table GARDS_BG_PROC_PARAMS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_BG_PROC_PARAMS" MODIFY ("SAMPLE_ID" NOT NULL ENABLE);
 
--------------------------------------------------------
--  Constraints for Table GARDS_BG_QC_RESULT
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_BG_QC_RESULT" MODIFY ("SAMPLE_ID" NOT NULL ENABLE);
 
--------------------------------------------------------
--  Constraints for Table GARDS_BG_ROI_COUNTS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_BG_ROI_COUNTS" MODIFY ("SAMPLE_ID" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_BG_ROI_COUNTS" MODIFY ("ROI" NOT NULL ENABLE);
 
--------------------------------------------------------
--  Constraints for Table GARDS_BG_STD_SPECTRA_RESULT
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_BG_STD_SPECTRA_RESULT" MODIFY ("SAMPLE_ID" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_BG_STD_SPECTRA_RESULT" MODIFY ("STD_SPECTRA_ID" NOT NULL ENABLE);
 
--------------------------------------------------------
--  Constraints for Table GARDS_CAT_CRITERIA_TESTS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_CAT_CRITERIA_TESTS" ADD CONSTRAINT "PK_CAT_CRIT_TEST_ID" PRIMARY KEY ("TEST_ID") ENABLE;
 
  ALTER TABLE "RMSMAN"."GARDS_CAT_CRITERIA_TESTS" MODIFY ("TEST_CODE" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_CAT_CRITERIA_TESTS" MODIFY ("TEST_NAME" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_CAT_CRITERIA_TESTS" MODIFY ("ACTIVE_FLAG" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_CAT_CRITERIA_TESTS" ADD CONSTRAINT "UQ_CAT_CRIT_TEST_CODE" UNIQUE ("TEST_CODE") ENABLE;
 
--------------------------------------------------------
--  Constraints for Table GARDS_COMMENTS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_COMMENTS" ADD CONSTRAINT "PK_COMMENTS" PRIMARY KEY ("COMMENT_ID") ENABLE;
 
--------------------------------------------------------
--  Constraints for Table GARDS_COMMENTS_DEFS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_COMMENTS_DEFS" ADD CONSTRAINT "PK_COMMENTS_DEF" PRIMARY KEY ("COMMENT_TYPE") ENABLE;
 
--------------------------------------------------------
--  Constraints for Table GARDS_CSC_MODCOEFF_LIB
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_CSC_MODCOEFF_LIB" ADD CONSTRAINT "PK_CSC_MODCOEFF" PRIMARY KEY ("DETECTOR_ID", "NAME", "ENERGY") ENABLE;
 
--------------------------------------------------------
--  Constraints for Table GARDS_DETECTORS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_DETECTORS" ADD CONSTRAINT "PK_DETECTORS" PRIMARY KEY ("DETECTOR_ID") ENABLE;
 
  ALTER TABLE "RMSMAN"."GARDS_DETECTORS" ADD CONSTRAINT "UQ_DETECTORS" UNIQUE ("DETECTOR_CODE") ENABLE;
 
--------------------------------------------------------
--  Constraints for Table GARDS_DIST_SAMPLE_QUEUE
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_DIST_SAMPLE_QUEUE" ADD CONSTRAINT "PK_DIST_SAMPLE_QUEUE" PRIMARY KEY ("SAMPLE_ID") ENABLE;
 
--------------------------------------------------------
--  Constraints for Table GARDS_FLAGS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_FLAGS" ADD PRIMARY KEY ("FLAG_ID") ENABLE;
 
--------------------------------------------------------
--  Constraints for Table GARDS_NOTIFY
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_NOTIFY" MODIFY ("EVENT" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_NOTIFY" MODIFY ("DTG_BEGIN" NOT NULL ENABLE);
 
--------------------------------------------------------
--  Constraints for Table GARDS_NUCL_IDED
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_NUCL_IDED" ADD CONSTRAINT "PK_NUCL_IDED" PRIMARY KEY ("SAMPLE_ID", "NAME") ENABLE;
 
  ALTER TABLE "RMSMAN"."GARDS_NUCL_IDED" MODIFY ("SAMPLE_ID" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_NUCL_IDED" MODIFY ("STATION_ID" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_NUCL_IDED" MODIFY ("DETECTOR_ID" NOT NULL ENABLE);
 
--------------------------------------------------------
--  Constraints for Table GARDS_NUCL_IDED_ORIG
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_NUCL_IDED_ORIG" ADD CONSTRAINT "PK_NUCL_IDED_ORIG" PRIMARY KEY ("SAMPLE_ID", "NAME") ENABLE;
 
  ALTER TABLE "RMSMAN"."GARDS_NUCL_IDED_ORIG" MODIFY ("SAMPLE_ID" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_NUCL_IDED_ORIG" MODIFY ("STATION_ID" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_NUCL_IDED_ORIG" MODIFY ("DETECTOR_ID" NOT NULL ENABLE);
 
--------------------------------------------------------
--  Constraints for Table GARDS_NUCL_LINES_IDED
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_NUCL_LINES_IDED" MODIFY ("SAMPLE_ID" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_NUCL_LINES_IDED" MODIFY ("STATION_ID" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_NUCL_LINES_IDED" MODIFY ("DETECTOR_ID" NOT NULL ENABLE);
 
--------------------------------------------------------
--  Constraints for Table GARDS_NUCL_LINES_IDED_ORIG
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG" MODIFY ("SAMPLE_ID" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG" MODIFY ("STATION_ID" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG" MODIFY ("DETECTOR_ID" NOT NULL ENABLE);
 
--------------------------------------------------------
--  Constraints for Table GARDS_PROC_PARAMS_TEMPLATE
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE" ADD CONSTRAINT "CK_TEMPL_DO_CSC" CHECK (do_csc in (0,1,2)) ENABLE;
 
--------------------------------------------------------
--  Constraints for Table GARDS_POC
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_POC" ADD CONSTRAINT "PK_POC" PRIMARY KEY ("POCID") ENABLE;
 
  ALTER TABLE "RMSMAN"."GARDS_POC" MODIFY ("EMAIL_ADDRESS" NOT NULL ENABLE);
 
--------------------------------------------------------
--  Constraints for Table GARDS_PERMISSIONS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_PERMISSIONS" ADD CONSTRAINT "PK_PERMISSIONS" PRIMARY KEY ("PERMISSION_ID") ENABLE;
 
  ALTER TABLE "RMSMAN"."GARDS_PERMISSIONS" MODIFY ("PERMISSION_NAME" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_PERMISSIONS" MODIFY ("DB_NAME" NOT NULL ENABLE);
 
--------------------------------------------------------
--  Constraints for Table GARDS_SAMPLE_PROC_PARAMS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS" ADD CONSTRAINT "CK_DO_CSC" CHECK (do_csc in (0,1,2)) ENABLE;
 
--------------------------------------------------------
--  Constraints for Table GARDS_SAMPLE_DATA
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_SAMPLE_DATA" ADD CONSTRAINT "PK_SAMPLE_DATA" PRIMARY KEY ("SAMPLE_ID") ENABLE;
 
  ALTER TABLE "RMSMAN"."GARDS_SAMPLE_DATA" ADD CONSTRAINT "UQ_SAMPLE_DATA" UNIQUE ("STATION_ID", "DETECTOR_ID", "SPECTRAL_QUALIFIER", "COLLECT_STOP", "ACQUISITION_STOP", "TRANSMIT_DTG") ENABLE;
 
--------------------------------------------------------
--  Constraints for Table GARDS_SAMPLE_CAT
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_SAMPLE_CAT" MODIFY ("NAME" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_SAMPLE_CAT" MODIFY ("SAMPLE_ID" NOT NULL ENABLE);
 
--------------------------------------------------------
--  Constraints for Table GARDS_ROLES
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_ROLES" ADD CONSTRAINT "PK_ROLES" PRIMARY KEY ("ROLE_ID") ENABLE;
 
  ALTER TABLE "RMSMAN"."GARDS_ROLES" MODIFY ("ROLE_NAME" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_ROLES" MODIFY ("DB_NAME" NOT NULL ENABLE);
 
--------------------------------------------------------
--  Constraints for Table GARDS_SAMPLE_STATUS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_SAMPLE_STATUS" ADD CONSTRAINT "PK_SAMPLE_STATUS" PRIMARY KEY ("SAMPLE_ID") ENABLE;
 
--------------------------------------------------------
--  Constraints for Table GARDS_SAMPLE_XE_PROC_PARAMS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_SAMPLE_XE_PROC_PARAMS" ADD CONSTRAINT "S_XE_PP_BACK_USED" CHECK (det_back_used in (0,1)    AND gas_back_used   in (0,1)) ENABLE;
 
  ALTER TABLE "RMSMAN"."GARDS_SAMPLE_XE_PROC_PARAMS" ADD CONSTRAINT "S_XE_PP_ECR" CHECK (beta_ecr_order in (1,2,3) AND gamma_ecr_order in (1,2,3)) ENABLE;
 
--------------------------------------------------------
--  Constraints for Table GARDS_STADET
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_STADET" ADD CONSTRAINT "PK_STADET" PRIMARY KEY ("STATION_ID", "DETECTOR_ID") ENABLE;
 
--------------------------------------------------------
--  Constraints for Table GARDS_STATIONS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_STATIONS" ADD CONSTRAINT "CK_STATIONS_SPLIT" CHECK (split_station in (1, 0)) ENABLE;
 
  ALTER TABLE "RMSMAN"."GARDS_STATIONS" ADD CONSTRAINT "PK_STATIONS" PRIMARY KEY ("STATION_ID") ENABLE;
 
  ALTER TABLE "RMSMAN"."GARDS_STATIONS" ADD CONSTRAINT "UQ_STATIONS" UNIQUE ("STATION_CODE") ENABLE;
 
--------------------------------------------------------
--  Constraints for Table GARDS_USERENV
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_USERENV" MODIFY ("NAME" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_USERENV" MODIFY ("VALUE" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_USERENV" ADD CONSTRAINT "UQ_USERENV" UNIQUE ("NAME") ENABLE;
 
--------------------------------------------------------
--  Constraints for Table GARDS_USERS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_USERS" ADD CONSTRAINT "CK_USERS_ASSIGN" CHECK (assignable in (-1, 0, 1)) ENABLE;
 
  ALTER TABLE "RMSMAN"."GARDS_USERS" ADD CONSTRAINT "PK_USERS" PRIMARY KEY ("USER_ID") ENABLE;
 
  ALTER TABLE "RMSMAN"."GARDS_USERS" MODIFY ("USER_NAME" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_USERS" MODIFY ("ASSIGNABLE" NOT NULL ENABLE);
 
--------------------------------------------------------
--  Constraints for Table GARDS_SOH_CODE
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_SOH_CODE" ADD CONSTRAINT "PK_SOH_CODE" PRIMARY KEY ("PARAM") ENABLE;
 
--------------------------------------------------------
--  Constraints for Table JAVA$CLASS$MD5$TABLE
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."JAVA$CLASS$MD5$TABLE" ADD UNIQUE ("NAME") ENABLE;
 
--------------------------------------------------------
--  Constraints for Table GARDS_XE_PROC_PARAMS_TEMPLATE
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_XE_PROC_PARAMS_TEMPLATE" ADD CONSTRAINT "XE_PPT_BETA_GAMMA_ECR" CHECK (beta_ecr_order in (1,2,3) AND gamma_ecr_order in (1,2,3)) ENABLE;
 
  ALTER TABLE "RMSMAN"."GARDS_XE_PROC_PARAMS_TEMPLATE" ADD CONSTRAINT "XE_PPT_DT_BCK_USED" CHECK (det_back_used in (0,1) AND gas_back_used in (0,1)) ENABLE;
 
--------------------------------------------------------
--  Constraints for Table GARDS_IRF
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_IRF" MODIFY ("DETECTOR_ID" NOT NULL ENABLE);
 
--------------------------------------------------------
--  Constraints for Table R2_RMS_SPECTRUM_LOG
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."R2_RMS_SPECTRUM_LOG" MODIFY ("COMMENT_ID" NOT NULL ENABLE);
 
--------------------------------------------------------
--  Constraints for Table GARDS_XE_RESULTS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_XE_RESULTS" MODIFY ("SAMPLE_ID" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_XE_RESULTS" MODIFY ("METHOD_ID" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_XE_RESULTS" MODIFY ("NUCLIDE_ID" NOT NULL ENABLE);
 
--------------------------------------------------------
--  Constraints for Table GARDS_BG_CONFIG_PARAMS_ORI
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_BG_CONFIG_PARAMS_ORI" MODIFY ("DETECTOR_ID" NOT NULL ENABLE);
 
--------------------------------------------------------
--  Constraints for Table GARDS_BG_CONFIG_PARAMS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_BG_CONFIG_PARAMS" MODIFY ("DETECTOR_ID" NOT NULL ENABLE);
 
--------------------------------------------------------
--  Constraints for Table GARDS_NOTIFY_BAK
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_NOTIFY_BAK" MODIFY ("EVENT" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_NOTIFY_BAK" MODIFY ("DTG_BEGIN" NOT NULL ENABLE);
 
--------------------------------------------------------
--  Constraints for Table GARDS_IRF_TT
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_IRF_TT" MODIFY ("DETECTOR_ID" NOT NULL ENABLE);
 
--------------------------------------------------------
--  Constraints for Table GARDS_BASELINE
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_BASELINE" MODIFY ("DATA_TYPE" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_BASELINE" MODIFY ("INDEX_NO" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_BASELINE" MODIFY ("MULT" NOT NULL ENABLE);
 
  ALTER TABLE "RMSMAN"."GARDS_BASELINE" MODIFY ("NO_OF_LOOPS" NOT NULL ENABLE);
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_RESOLUTION_CAL_COV
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_RESOLUTION_CAL_COV" ADD CONSTRAINT "FK_RESOLUTION_CAL_COV" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_ENERGY_CAL_COV
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_ENERGY_CAL_COV" ADD CONSTRAINT "FK_ENERGY_CAL_COV" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_BG_EFFICIENCY_PAIRS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_BG_EFFICIENCY_PAIRS" ADD CONSTRAINT "FK_BG_EFFICIENCY_PAIRS" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_BG_ENERGY_CAL
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_BG_ENERGY_CAL" ADD CONSTRAINT "FK_BG_EN_CAL_SID" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_B_ENERGY_PAIRS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_B_ENERGY_PAIRS" ADD CONSTRAINT "FK_B_ENERGY_PAIRS" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_B_ENERGY_PAIRS_ORIG
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_B_ENERGY_PAIRS_ORIG" ADD CONSTRAINT "FK_B_ENERGY_PAIRS_ORIG" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_B_RESOLUTION_PAIRS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_B_RESOLUTION_PAIRS" ADD CONSTRAINT "FK_B_RESOLUTION_PAIRS" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_B_RESOLUTION_PAIRS_ORIG
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_B_RESOLUTION_PAIRS_ORIG" ADD CONSTRAINT "FK_B_RESOLUTION_PAIRS_ORIG" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_CAT_TEMPLATE
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_CAT_TEMPLATE" ADD CONSTRAINT "FK_DETECTOR" FOREIGN KEY ("DETECTOR_ID")
	  REFERENCES "RMSMAN"."GARDS_DETECTORS" ("DETECTOR_ID") ENABLE;
 
  ALTER TABLE "RMSMAN"."GARDS_CAT_TEMPLATE" ADD CONSTRAINT "FK_STATION" FOREIGN KEY ("STATION_ID")
	  REFERENCES "RMSMAN"."GARDS_STATIONS" ("STATION_ID") ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_COMMENTS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_COMMENTS" ADD CONSTRAINT "FK_COMMENTS" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_CSC_MODCOEFF_LIB
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_CSC_MODCOEFF_LIB" ADD CONSTRAINT "FK_CSC_MODCFF_LIB" FOREIGN KEY ("DETECTOR_ID")
	  REFERENCES "RMSMAN"."GARDS_DETECTORS" ("DETECTOR_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_DIST_SAMPLE_QUEUE
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_DIST_SAMPLE_QUEUE" ADD CONSTRAINT "FK_DIST_SAMPLE_QUEUE" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_EFFICIENCY_CAL
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_EFFICIENCY_CAL" ADD CONSTRAINT "FK_EFFICIENCY_CAL" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_EFFICIENCY_PAIRS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_EFFICIENCY_PAIRS" ADD CONSTRAINT "FK_EFFICIENCY_PAIRS" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_ENERGY_CAL
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_ENERGY_CAL" ADD CONSTRAINT "FK_ENERGY_CAL" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_ENERGY_CAL_ORIG
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_ENERGY_CAL_ORIG" ADD CONSTRAINT "FK_ENERGY_CAL_ORIG" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_ENERGY_PAIRS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_ENERGY_PAIRS" ADD CONSTRAINT "FK_ENERGY_PAIRS" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_ENERGY_PAIRS_ORIG
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_ENERGY_PAIRS_ORIG" ADD CONSTRAINT "FK_ENERGY_PAIRS_ORIG" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_FPE
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_FPE" ADD CONSTRAINT "FK_FPE" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_NIC
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_NIC" ADD CONSTRAINT "FK_NIC" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_NOTIFY
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_NOTIFY" ADD CONSTRAINT "FK_NOTIFY_POC" FOREIGN KEY ("POC_ID")
	  REFERENCES "RMSMAN"."GARDS_POC" ("POCID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_NUCL_IDED
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_NUCL_IDED" ADD CONSTRAINT "FK_NUCL_IDED" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_NUCL_IDED_ORIG
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_NUCL_IDED_ORIG" ADD CONSTRAINT "FK_NUCL_IDED_ORIG" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_NUCL_LINES_IDED
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_NUCL_LINES_IDED" ADD CONSTRAINT "FK_NUCL_LINES_IDED" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_NUCL_LINES_IDED_ORIG
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG" ADD CONSTRAINT "FK_NUCL_LINES_IDED_ORIG" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_QCHISTORY
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_QCHISTORY" ADD CONSTRAINT "FK_QCHISTORY" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_PROC_PARAMS_TEMPLATE
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE" ADD CONSTRAINT "FK_PPTEMPL_DET" FOREIGN KEY ("DETECTOR_ID")
	  REFERENCES "RMSMAN"."GARDS_DETECTORS" ("DETECTOR_ID") ON DELETE CASCADE ENABLE;
 
  ALTER TABLE "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE" ADD CONSTRAINT "FK_PPTEMPL_STA" FOREIGN KEY ("STATION_ID")
	  REFERENCES "RMSMAN"."GARDS_STATIONS" ("STATION_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_QCTARGETS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_QCTARGETS" ADD CONSTRAINT "FK_QCTARGS_DET" FOREIGN KEY ("DETECTOR_ID")
	  REFERENCES "RMSMAN"."GARDS_DETECTORS" ("DETECTOR_ID") ON DELETE CASCADE ENABLE;
 
  ALTER TABLE "RMSMAN"."GARDS_QCTARGETS" ADD CONSTRAINT "FK_QCTARGS_STA" FOREIGN KEY ("STATION_ID")
	  REFERENCES "RMSMAN"."GARDS_STATIONS" ("STATION_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_QCPARAMS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_QCPARAMS" ADD CONSTRAINT "FK_QCPARAMS_DET" FOREIGN KEY ("DETECTOR_ID")
	  REFERENCES "RMSMAN"."GARDS_DETECTORS" ("DETECTOR_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_PEAKS_ORIG
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_PEAKS_ORIG" ADD CONSTRAINT "FK_PEAKS_ORIG" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_PEAKS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_PEAKS" ADD CONSTRAINT "FK_PEAKS" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_RESOLUTION_CAL_ORIG
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_RESOLUTION_CAL_ORIG" ADD CONSTRAINT "FK_RESOLUTION_CAL_ORIG" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_RESOLUTION_PAIRS_ORIG
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_RESOLUTION_PAIRS_ORIG" ADD CONSTRAINT "FK_RESOLUTION_PAIRS_ORIG" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_ROI_CONCS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_ROI_CONCS" ADD CONSTRAINT "FK_ROI_CONCS" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_SAMPLE_RATIOS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_SAMPLE_RATIOS" ADD CONSTRAINT "FK_SAMPLE_RATIOS" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_SAMPLE_PROC_PARAMS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS" ADD CONSTRAINT "FK_SAMPLE_PROC_PARAMS" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_SAMPLE_FLAGS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_SAMPLE_FLAGS" ADD CONSTRAINT "FK_SAMPLE_FLAGS" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_SAMPLE_CAT
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_SAMPLE_CAT" ADD CONSTRAINT "FK_SAMP_ID" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_ROLES_PERMISSIONS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_ROLES_PERMISSIONS" ADD FOREIGN KEY ("PERMISSION_ID")
	  REFERENCES "RMSMAN"."GARDS_PERMISSIONS" ("PERMISSION_ID") ON DELETE CASCADE ENABLE;
 
  ALTER TABLE "RMSMAN"."GARDS_ROLES_PERMISSIONS" ADD FOREIGN KEY ("ROLE_ID")
	  REFERENCES "RMSMAN"."GARDS_ROLES" ("ROLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_SAMPLE_UPDATE_PARAMS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_SAMPLE_UPDATE_PARAMS" ADD CONSTRAINT "FK_SAMPLE_UPDATE_PARAMS" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_SAMPLE_STATUS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_SAMPLE_STATUS" ADD CONSTRAINT "FK_SAMPLE_STATUS" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_ROI_LIMITS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_ROI_LIMITS" ADD CONSTRAINT "FK_ROI_LIMITS" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_ROI_COUNTS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_ROI_COUNTS" ADD CONSTRAINT "FK_ROI_COUNTS" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_ROI_CHANNELS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_ROI_CHANNELS" ADD CONSTRAINT "FK_ROI_CHANNELS" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_RESOLUTION_PAIRS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_RESOLUTION_PAIRS" ADD CONSTRAINT "FK_RESOLUTION_PAIRS" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_RESOLUTION_CAL
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_RESOLUTION_CAL" ADD CONSTRAINT "FK_RESOLUTION_CAL" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_SAMPLE_XE_PROC_PARAMS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_SAMPLE_XE_PROC_PARAMS" ADD CONSTRAINT "FK_SAMPLE_XE_PROC_PARAMS" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_STADET
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_STADET" ADD CONSTRAINT "FK_STADET_DET" FOREIGN KEY ("DETECTOR_ID")
	  REFERENCES "RMSMAN"."GARDS_DETECTORS" ("DETECTOR_ID") ON DELETE CASCADE ENABLE;
 
  ALTER TABLE "RMSMAN"."GARDS_STADET" ADD CONSTRAINT "FK_STADET_STA" FOREIGN KEY ("STATION_ID")
	  REFERENCES "RMSMAN"."GARDS_STATIONS" ("STATION_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_STATION_ASSIGNMENTS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_STATION_ASSIGNMENTS" ADD CONSTRAINT "FK_STA_ASSIGN_STAID" FOREIGN KEY ("STATION_ID")
	  REFERENCES "RMSMAN"."GARDS_STATIONS" ("STATION_ID") ON DELETE CASCADE ENABLE;
 
  ALTER TABLE "RMSMAN"."GARDS_STATION_ASSIGNMENTS" ADD CONSTRAINT "FK_STA_ASSIGN_USRID" FOREIGN KEY ("USER_ID")
	  REFERENCES "RMSMAN"."GARDS_USERS" ("USER_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_TOTAL_EFFIC
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_TOTAL_EFFIC" ADD CONSTRAINT "FK_TOTAL_EFFIC" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_UPDATE_PARAMS_TEMPLATE
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_UPDATE_PARAMS_TEMPLATE" ADD CONSTRAINT "FK_UPD_PARAMS_TMPL" FOREIGN KEY ("DETECTOR_ID")
	  REFERENCES "RMSMAN"."GARDS_DETECTORS" ("DETECTOR_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_USERS_ROLES
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_USERS_ROLES" ADD CONSTRAINT "FK_ROLE_ID" FOREIGN KEY ("ROLE_ID")
	  REFERENCES "RMSMAN"."GARDS_ROLES" ("ROLE_ID") ON DELETE CASCADE ENABLE;
 
  ALTER TABLE "RMSMAN"."GARDS_USERS_ROLES" ADD CONSTRAINT "FK_USER_ID" FOREIGN KEY ("USER_ID")
	  REFERENCES "RMSMAN"."GARDS_USERS" ("USER_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_USER_COMMENTS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_USER_COMMENTS" ADD CONSTRAINT "FK_USER_COMMENTS" FOREIGN KEY ("COMMENT_ID")
	  REFERENCES "RMSMAN"."GARDS_COMMENTS" ("COMMENT_ID") ON DELETE CASCADE ENABLE;
 
  ALTER TABLE "RMSMAN"."GARDS_USER_COMMENTS" ADD CONSTRAINT "FK_USER_COMMENTS_SID" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_UPDATE_REFLINES
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_UPDATE_REFLINES" ADD CONSTRAINT "FK_UPD_REFLINES_DET" FOREIGN KEY ("DETECTOR_ID")
	  REFERENCES "RMSMAN"."GARDS_DETECTORS" ("DETECTOR_ID") ON DELETE CASCADE ENABLE;
 
  ALTER TABLE "RMSMAN"."GARDS_UPDATE_REFLINES" ADD CONSTRAINT "FK_UPD_REFLINES_STA" FOREIGN KEY ("STATION_ID")
	  REFERENCES "RMSMAN"."GARDS_STATIONS" ("STATION_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_STATIONS_SCHEDULE
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_STATIONS_SCHEDULE" ADD CONSTRAINT "FK_STA_SCHEDULE_STAID" FOREIGN KEY ("STATION_ID")
	  REFERENCES "RMSMAN"."GARDS_STATIONS" ("STATION_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_XE_PROC_PARAMS_TEMPLATE
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_XE_PROC_PARAMS_TEMPLATE" ADD CONSTRAINT "XE_PPT_DET" FOREIGN KEY ("DETECTOR_ID")
	  REFERENCES "RMSMAN"."GARDS_DETECTORS" ("DETECTOR_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_IRF
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_IRF" ADD CONSTRAINT "FK_IRF" FOREIGN KEY ("DETECTOR_ID")
	  REFERENCES "RMSMAN"."GARDS_DETECTORS" ("DETECTOR_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_QC_RESULTS
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_QC_RESULTS" ADD CONSTRAINT "FK_QC_RESULTS" FOREIGN KEY ("SAMPLE_ID")
	  REFERENCES "RMSMAN"."GARDS_SAMPLE_DATA" ("SAMPLE_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  Ref Constraints for Table GARDS_BASELINE
--------------------------------------------------------

  ALTER TABLE "RMSMAN"."GARDS_BASELINE" ADD CONSTRAINT "FK_BASELINE" FOREIGN KEY ("DETECTOR_ID")
	  REFERENCES "RMSMAN"."GARDS_DETECTORS" ("DETECTOR_ID") ON DELETE CASCADE ENABLE;
 
--------------------------------------------------------
--  DDL for Synonymn FILEPRODUCT
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."FILEPRODUCT" FOR "IDCX"."FILEPRODUCT";
 
--------------------------------------------------------
--  DDL for Synonymn FPDESCRIPTION
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."FPDESCRIPTION" FOR "IDCX"."FPDESCRIPTION";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_ALERTS
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_ALERTS" FOR "RMSAUTO"."GARDS_ALERTS";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_BG_DETECTOR_STD_SPECTRA
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_BG_DETECTOR_STD_SPECTRA" FOR "RMSAUTO"."GARDS_BG_DETECTOR_STD_SPECTRA";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_BG_STD_SPECTRA
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_BG_STD_SPECTRA" FOR "RMSAUTO"."GARDS_BG_STD_SPECTRA";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_DATA_LOG
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_DATA_LOG" FOR "RMSAUTO"."GARDS_DATA_LOG";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_ENVIRONMENT
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_ENVIRONMENT" FOR "RMSAUTO"."GARDS_ENVIRONMENT";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_HISTOGRAM
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_HISTOGRAM" FOR "RMSAUTO"."GARDS_HISTOGRAM";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_INTERVAL
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_INTERVAL" FOR "RMSAUTO"."GARDS_INTERVAL";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_MET_DATA
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_MET_DATA" FOR "RMSAUTO"."GARDS_MET_DATA";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_READ_SAMPLE_CAT
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_READ_SAMPLE_CAT" FOR "RMSMAN"."GARDS_SAMPLE_CAT";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_READ_SAMPLE_STATUS
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_READ_SAMPLE_STATUS" FOR "RMSMAN"."GARDS_SAMPLE_STATUS";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_RECEIPT_LOG
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_RECEIPT_LOG" FOR "RMSAUTO"."GARDS_RECEIPT_LOG";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_RLR
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_RLR" FOR "RMSAUTO"."GARDS_RLR";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_RLR_CONCLUSIONS
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_RLR_CONCLUSIONS" FOR "RMSAUTO"."GARDS_RLR_CONCLUSIONS";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_RLR_OBJECTIVE
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_RLR_OBJECTIVE" FOR "RMSAUTO"."GARDS_RLR_OBJECTIVE";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_RLR_RATIOS
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_RLR_RATIOS" FOR "RMSAUTO"."GARDS_RLR_RATIOS";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_RLR_RESULTS
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_RLR_RESULTS" FOR "RMSAUTO"."GARDS_RLR_RESULTS";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_RLR_SSREB
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_RLR_SSREB" FOR "RMSAUTO"."GARDS_RLR_SSREB";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_SAMPLE_AUX
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_SAMPLE_AUX" FOR "RMSAUTO"."GARDS_SAMPLE_AUX";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_SAMPLE_CERT
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_SAMPLE_CERT" FOR "RMSAUTO"."GARDS_SAMPLE_CERT";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_SAMPLE_CERT_LINES
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_SAMPLE_CERT_LINES" FOR "RMSAUTO"."GARDS_SAMPLE_CERT_LINES";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_SAMPLE_DESCRIPTION
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_SAMPLE_DESCRIPTION" FOR "RMSAUTO"."GARDS_SAMPLE_DESCRIPTION";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_SOH_CHAR_DATA
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_SOH_CHAR_DATA" FOR "RMSAUTO"."GARDS_SOH_CHAR_DATA";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_SOH_HEADER
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_SOH_HEADER" FOR "RMSAUTO"."GARDS_SOH_HEADER";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_SOH_NUM_DATA
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_SOH_NUM_DATA" FOR "RMSAUTO"."GARDS_SOH_NUM_DATA";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_SOH_SENSOR_DATA
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_SOH_SENSOR_DATA" FOR "RMSAUTO"."GARDS_SOH_SENSOR_DATA";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_SPECTRUM
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_SPECTRUM" FOR "RMSAUTO"."GARDS_SPECTRUM";
 
--------------------------------------------------------
--  DDL for Synonymn GARDS_WRITE_SAMPLE_CAT
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GARDS_WRITE_SAMPLE_CAT" FOR "RMSMAN"."GARDS_SAMPLE_CAT";
 
--------------------------------------------------------
--  DDL for Synonymn GBEPO
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GBEPO" FOR "RMSMAN"."GARDS_B_ENERGY_PAIRS_ORIG";
 
--------------------------------------------------------
--  DDL for Synonymn GBGEP
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GBGEP" FOR "RMSMAN"."GARDS_BG_EFFICIENCY_PAIRS";
 
--------------------------------------------------------
--  DDL for Synonymn GBRP
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GBRP" FOR "RMSMAN"."GARDS_B_RESOLUTION_PAIRS";
 
--------------------------------------------------------
--  DDL for Synonymn GBRPO
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GBRPO" FOR "RMSMAN"."GARDS_B_RESOLUTION_PAIRS_ORIG";
 
--------------------------------------------------------
--  DDL for Synonymn GCCT
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GCCT" FOR "RMSMAN"."GARDS_CAT_CRITERIA_TESTS";
 
--------------------------------------------------------
--  DDL for Synonymn GNLIO
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GNLIO" FOR "RMSMAN"."GARDS_NUCL_LINES_IDED_ORIG";
 
--------------------------------------------------------
--  DDL for Synonymn GPPT
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GPPT" FOR "RMSMAN"."GARDS_PROC_PARAMS_TEMPLATE";
 
--------------------------------------------------------
--  DDL for Synonymn GRCO
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GRCO" FOR "RMSMAN"."GARDS_RESOLUTION_CAL_ORIG";
 
--------------------------------------------------------
--  DDL for Synonymn GRPO
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GRPO" FOR "RMSMAN"."GARDS_RESOLUTION_PAIRS_ORIG";
 
--------------------------------------------------------
--  DDL for Synonymn GSD
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GSD" FOR "RMSMAN"."GARDS_SAMPLE_DATA";
 
--------------------------------------------------------
--  DDL for Synonymn GSPP
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GSPP" FOR "RMSMAN"."GARDS_SAMPLE_PROC_PARAMS";
 
--------------------------------------------------------
--  DDL for Synonymn GSS
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GSS" FOR "RMSMAN"."GARDS_SAMPLE_STATUS";
 
--------------------------------------------------------
--  DDL for Synonymn GSTA
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GSTA" FOR "RMSMAN"."GARDS_STATION_ASSIGNMENTS";
 
--------------------------------------------------------
--  DDL for Synonymn GSUP
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GSUP" FOR "RMSMAN"."GARDS_SAMPLE_UPDATE_PARAMS";
 
--------------------------------------------------------
--  DDL for Synonymn GSXPP
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GSXPP" FOR "RMSMAN"."GARDS_SAMPLE_XE_PROC_PARAMS";
 
--------------------------------------------------------
--  DDL for Synonymn GUPT
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GUPT" FOR "RMSMAN"."GARDS_UPDATE_PARAMS_TEMPLATE";
 
--------------------------------------------------------
--  DDL for Synonymn GXPPT
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."GXPPT" FOR "RMSMAN"."GARDS_XE_PROC_PARAMS_TEMPLATE";
 
--------------------------------------------------------
--  DDL for Synonymn INTERVAL
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."INTERVAL" FOR "RMSMAN"."GARDS_INTERVAL";
 
--------------------------------------------------------
--  DDL for Synonymn LASTID
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."LASTID" FOR "IDCX"."LASTID";
 
--------------------------------------------------------
--  DDL for Synonymn MSGDISC
--------------------------------------------------------

  CREATE OR REPLACE SYNONYM "RMSMAN"."MSGDISC" FOR "IDCX"."MSGDISC";
 