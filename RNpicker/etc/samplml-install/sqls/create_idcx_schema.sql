
----------------------------------------------------------------------
--- Create from IDCX
----------------------------------------------------------------------

  CREATE TABLE FILEPRODUCT
  (
    FPID         NUMBER(10) NOT NULL ENABLE,
    TYPEID       NUMBER(10),
    DIR          VARCHAR2(64),
    DFILE        VARCHAR2(32),
    FOFF         NUMBER(10),
    DSIZE        NUMBER(10),
    TIME         FLOAT(53),
    ENDTIME      FLOAT(53),
    STA          VARCHAR2(6),
    CHAN         VARCHAR2(8),
    AUTHOR       VARCHAR2(16),
    VERSION      FLOAT(53),
    REVISION     NUMBER(4),
    OBSOLETE     NUMBER(1),
    LDDATE       DATE
  ) ;

  CREATE TABLE FPDESCRIPTION
  (
    TYPEID       NUMBER(10) NOT NULL ENABLE,
    PRODTYPE     VARCHAR2(12),
    NAME         VARCHAR2(64),
    MSGDTYPE     VARCHAR2(16),
    MSGDFORMAT   VARCHAR2(8),
    HEADER_FPID  NUMBER(10),
    LDDATE       DATE
  ) ;
