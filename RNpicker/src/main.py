import logging
import logging.handlers
from StringIO import StringIO

import common.utils
import common.xml_utils
from db.datafetchers import DBDataFetcher
from db.connections import DatabaseConnector
from renderers.SAMPMLrendererv1 import ParticulateRenderer



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
   
   conf = common.utils.Conf.get_instance()
   url = conf.get("DatabaseAccess","url")
   
   print "URL=%s"%(url)
   
   # create DB connector
   conn = DatabaseConnector(url)
   
   conn.connect()
   
   # fetchnoble gas data
   #fetcher = DBDataFetcher.getDataFetcher(conn,"216061")
   
    # fetchnoble particulate
   fetcher = DBDataFetcher.getDataFetcher(conn,"153961")
   
   fetcher.fetch()
   
   renderer = ParticulateRenderer(fetcher)
   
   xmlStr = renderer.asXmlStr()
   
   common.xml_utils.pretty_print_xml(StringIO(xmlStr),"/tmp/subs-template.xml")
     
   print "Bye"