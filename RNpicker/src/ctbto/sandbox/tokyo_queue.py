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
    DATA       = "data"
    
    def __init__(self):
        """ constructor """
        
        self._db = table.Table()
        self._db.open('/tmp/test1.tct', table.TDBOWRITER | table.TDBOCREAT)
        
        self._init_db()
        
    def _init_db(self):
        """ create queue table if necessary """
        
        # create index
        self._db.setindex('uuid'                , table.TDBITLEXICAL)
        self._db.setindex('priority'            , table.TDBITLEXICAL)
        self._db.setindex('insertion_time'      , table.TDBITLEXICAL)
        self._db.setindex('priority_insert_time', table.TDBITLEXICAL)
    
    def put(self, a_dict_item):
        """ add one element in queue """
        
        klass = self.__class__
        
        the_uuid   = a_dict_item[klass.UUID]
        dummy      = a_dict_item.get(klass.TIME, None)
        the_time   = time.time() if not dummy else dummy
        
        the_prio_time = "%s|%s" %(a_dict_item[klass.PRIORITY], the_time)
        
        s = str( a_dict_item[klass.TIME] )
        
        the_dict = { klass.UUID        : str( a_dict_item[klass.UUID] ) ,\
                                    klass.PRIORITY    : str( a_dict_item[klass.PRIORITY] ),\
                                    klass.STATUS      : str( a_dict_item[klass.STATUS] ),\
                                    klass.TIME        : str( the_time ),\
                                    klass.PRIO_TIME   : the_prio_time }
        
        self._db[str(the_uuid)] = the_dict
        
        print('\ninserted %s\n' % (the_dict) )

    
    def pop(self):
        """ return the item with the highest priority and remove it from the queue """
        
        klass = self.__class__
        
        q = self._db.query()
        
        # table.TDBQCSTRBW 
        q.setorder( self.__class__.PRIO_TIME, table.TDBQCSTRBW) 
        
        #first param is max, second is skip
        q.setlimit(1, 0)   
            
        res = q.search()
        
        row = self._db[res[0]]
        
        self._db.out(res[0])
         
        return row
    
    def size(self):
        """ return the size of th queue """
        return len(self._db)
