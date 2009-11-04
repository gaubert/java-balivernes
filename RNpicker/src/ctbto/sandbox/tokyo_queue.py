'''
Created on Nov 4, 2009

@author: guillaume.aubert@ctbto.org
'''

from tokyocabinet import table
import time


class TokyoCabinetQueue(object):
    """Create support for Queue in SQL """
    
    UUID       = "uuid"
    PRIORITY   = "priority"
    STATUS     = "status"
    TIME       = "insertion_time"
    PRIO_TIME  = "prio_time"
    
    def __init__(self):
        """ constructor """
        
        self._db = table.Table()
        self._db.open('/tmp/test.tct', table.TDBOWRITER | table.TDBOCREAT)
        
        self._init_db()
        
    def _init_db(self):
        """ create queue table if necessary """
        
        # create index
        self._db.setindex('uuid'                , table.TDBITLEXICAL)
        self._db.setindex('priority'            , table.TDBITLEXICAL)
        self._db.setindex('insertion_time'      , table.TDBITLEXICAL)
        self._db.setindex('priority_insert_time', table.TDBITLEXICAL)
    
    def put(self, nms_queue_item):
        """ add one element in queue """
        
        klass = self.__class__
        
        the_uuid      = nms_queue_item.uuid
        the_time      = time.time()
        
        print('\ninsert %s\n' % (nms_queue_item))
        
        the_prio_time = "%d_%d" %(nms_queue_item.priority, the_time)
        
        self._db[str(the_uuid)] = { klass.UUID        : str(the_uuid) ,\
                               klass.PRIORITY    : str(nms_queue_item.priority),\
                               klass.STATUS      : str(nms_queue_item.status),\
                               klass.TIME        : str(the_time),\
                               klass.PRIO_TIME   : the_prio_time }

    
    def pop(self):
        """ return the item with the highest priority and remove it from the queue """
        q = self._db.query()
        q.setorder( self.__class__.PRIO_TIME, table.TDBQCSTREQ) 
        #first param is max, second is skip
        q.setlimit(1, 0)   
            
        res = q.search()
        
        row = self._db[res[0]]
        
        self._db.out(res[0])
        
        return row
    
    def size(self):
        """ return the size of th queue """
        return len(self._db)
