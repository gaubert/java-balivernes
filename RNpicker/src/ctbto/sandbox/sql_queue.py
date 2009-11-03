'''
Created on Nov 3, 2009

@author: guillaume.aubert@ctbto.org
'''

import sqlalchemy
import datetime


class SQLQueue(object):
    """Create support for Queue in SQL """
    
    def __init__(self):
        """ constructor """
        
        self._sql_engine  = sqlalchemy.create_engine('sqlite:////tmp/queue_db.db')
        self._sql_conn    = self._sql_engine.connect()
        self._metadata    = sqlalchemy.MetaData()
        self._queue_table = None
        
        self._init_db()
        
        
    def _init_db(self):
        """ create queue table if necessary """
        
        self._queue_table = sqlalchemy.Table('queue', self._metadata,
                                       sqlalchemy.Column('q_item_id',        sqlalchemy.String(60), primary_key = True, unique = True, nullable = False),
                                       sqlalchemy.Column('q_priority',       sqlalchemy.Integer, index=True, nullable = False),
                                       sqlalchemy.Column('q_status',         sqlalchemy.String(30), nullable = False),
                                       sqlalchemy.Column('q_insertion_time', sqlalchemy.DateTime(), nullable = False)
                                      )
        
        # multi-col index on col3, col4
        sqlalchemy.Index('idx_priority_insertion_time', self._queue_table.c.q_priority, self._queue_table.c.q_insertion_time)

        self._queue_table.create(bind=self._sql_engine, checkfirst=True)
    
    def put(self, nms_queue_item):
        """ add one element in queue """
        
        table = self._queue_table
        
        uuid     = nms_queue_item.uuid
        priority = nms_queue_item.priority
        status   = nms_queue_item.status
        time     = datetime.datetime.now()
        
        #TODO Add transactions
        ins = self._queue_table.insert().values(q_item_id = str(uuid), q_priority = priority, q_status = status, q_insertion_time = time)
        
        print("\nins = %s\n. params = %s" % (ins, ins.compile().params))
        
        self._sql_conn.execute(ins)
    
    def pop(self):
        """ return the item with the highest priority and remove it from the queue """
                
        req  = self._queue_table.select().order_by(self._queue_table.c.q_priority.desc(),self._queue_table.c.q_insertion_time.asc()).limit(1)
        row = self._sql_conn.execute(req).fetchone()
        
        if row:
            id = row.q_item_id
            self._sql_conn.execute(self._queue_table.delete().where(self._queue_table.c.q_item_id == id))
        
        return row
    
    def size(self):
        """ return the size of th queue """
        
        sel = sqlalchemy.select([sqlalchemy.func.count(self._queue_table.c.q_item_id)])
        
        return self._sql_conn.execute(sel).scalar()
    
    def get(self):
        """ return the item with the highest priority """
        
        req = self._queue_table.select().order_by(self._queue_table.c.q_priority.desc(),self._queue_table.c.q_insertion_time.asc()).limit(1)
        
        return self._sql_conn.execute(req).fetchone()

    def get_all(self):
        
        req = self._queue_table.select().order_by(self._queue_table.c.q_priority.desc(),self._queue_table.c.q_insertion_time.asc())
        
        return self._sql_conn.execute(req).fetchall()
