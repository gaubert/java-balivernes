import logging
import logging.handlers
from lxml import etree
from StringIO import StringIO

import common.utils
from db.datafetchers import DBDataFetcher
from db.connections import DatabaseConnector
from renderers.SAMPMLrendererv1 import ParticulateRenderer
import sandbox.xmlpp


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
  
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level+1)
            if not e.tail or not e.tail.strip():
                e.tail = i + "  "
        if not e.tail or not e.tail.strip():
            e.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

        
 
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
   
   # fetchnoble gas data
   #fetcher = DBDataFetcher.getDataFetcher(conn,"216061")
   
    # fetchnoble particulate
   fetcher = DBDataFetcher.getDataFetcher(conn,"153961")
   
   fetcher.fetch()
   
   renderer = ParticulateRenderer(fetcher)
   
   xmlStr = renderer.asXmlStr()
   
   f = StringIO(xmlStr)
   
   tree = etree.parse(f)
   
   transform = etree.XSLT(etree.parse(open("/home/aubert/ecmwf/workspace/RNpicker/etc/ext/pretty-print.xslt")))
   
   result = transform(tree)
   
   common.utils.printInFile(str(result),"/tmp/subs-template.xml")
     
   print "Bye"