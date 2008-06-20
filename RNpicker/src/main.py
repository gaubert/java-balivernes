import logging
import logging.handlers

import common.utils
from db.connections import DatabaseConnector
from renderers.rawrenderer import DBRawRenderer

def myBasicLoggingConfig():
    """
    Do basic configuration for the logging system by creating a
    StreamHandler with a default Formatter and adding it to the
    root logger.
    """
    if len(logging.root.handlers) == 0:
        hdlr = logging.handlers.RotatingFileHandler("/tmp/logging.log", "a", 5000000, 4)
        # fmt = logging.Formatter(logging.BASIC_FORMAT)
        fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        hdlr.setFormatter(fmt)
        logging.root.addHandler(hdlr)
        
 
if __name__ == '__main__':

   myBasicLoggingConfig()  
   print "Hello"
   log = logging.getLogger("ROOT")
   log.setLevel(logging.DEBUG)
   log.info("Start")
   
   conf = common.utils.Conf.get_conf()
   url = conf.get("DatabaseAccess","url")
   
   print "URL=%s"%(url)
   
   
   
   # create DB connector
   conn = DatabaseConnector('oracle://aubert:ernest25@idcdev')
   
   conn.connect()
   
   # create raw Renderer
   renderer = DBRawRenderer(conn)
   
   renderer.render('GARDS_SAMPLE_DATA')
   
   print "Bye"