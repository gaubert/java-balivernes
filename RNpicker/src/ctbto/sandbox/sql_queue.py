'''
Created on Nov 3, 2009

@author: guillaume.aubert@ctbto.org
'''

import sqlalchemy
import datetime


class SQLQueue(object):
    """Create support for Queue in SQL """
    
    UUID       = "uuid"
    PRIORITY   = "priority"
    STATUS     = "status"
    TIME       = "insertion_time"
    PRIO_TIME  = "prio_time"
    DATA       = "data"
    
    def __init__(self):
        """ constructor """
        
        # to pass parameters: 'sqlite:////tmp/queue_db.db?check_same_thread=False
        self._sql_engine  = sqlalchemy.create_engine('sqlite:////tmp/queue_db.db?check_same_thread=False', poolclass=sqlalchemy.pool.NullPool )
        #self._sql_conn    = self._sql_engine.connect()
        self._metadata    = sqlalchemy.MetaData()
        self._queue_table = None
        
        self._init_db()
        
    
    def _execute_req(self, request):
        """ execute a request on the connection. 
            This is necessary for sqlite as the connection cannot be maintained in mutliple threads 
        """
        
        conn = self._sql_engine.connect()
        
        return conn.execute(request)
    
        
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
    
    def put(self, a_dict_item):
        """ add one element in queue """
        
        klass = self.__class__
        
        table = self._queue_table
        
        uuid     = a_dict_item[klass.UUID]
        priority = a_dict_item[klass.PRIORITY]
        status   = a_dict_item[klass.STATUS]
        time     = datetime.datetime.now()
        
        #TODO Add transactions
        ins = self._queue_table.insert().values(q_item_id = str(uuid), q_priority = priority, q_status = status, q_insertion_time = time)
        
        self._execute_req(ins)

    
    def pop(self):
        """ return the item with the highest priority and remove it from the queue """
         
        klass = self.__class__     
         
        req  = self._queue_table.select().where(self._queue_table.c.q_status == 'ACTIVE').order_by(self._queue_table.c.q_priority.desc(),self._queue_table.c.q_insertion_time.asc()).limit(1)
        row  = self._execute_req(req).fetchone()
        
        if row:
            id = row.q_item_id
            self._execute_req(self._queue_table.delete().where(self._queue_table.c.q_item_id == id))
        
        
        
        return { klass.UUID : row.q_item_id, klass.PRIORITY : row.q_priority, klass.STATUS : row.q_status, klass.TIME : row.q_insertion_time, klass.DATA : None }
    
    def size(self):
        """ return the size of th queue """
        
        sel = sqlalchemy.select([sqlalchemy.func.count(self._queue_table.c.q_item_id)])
        
        return self._execute_req(sel).scalar()
    
    def get(self):
        """ return the item with the highest priority """
        
        req = self._queue_table.select().order_by(self._queue_table.c.q_priority.desc(),self._queue_table.c.q_insertion_time.asc()).limit(1)
        
        return self._execute_req(req).fetchone()

    def get_from_priority_range(self, a_beg_priority, a_end_priority, a_beg_offset, a_end_offset):
        """ return a cursor on all item """
        req = self._queue_table.select().where( (self._queue_table.c.q_priority >= a_beg_priority) & (self._queue_table.c.q_priority <= a_end_priority) )\
                                        .order_by(self._queue_table.c.q_priority.desc(),self._queue_table.c.q_insertion_time.asc())\
                                        .offset(a_beg_offset).limit( (a_end_offset - a_beg_offset) + 1)
        
        return self._execute_req(req)
    
    def get_from_insertion_time_range(self, a_beg_date, a_end_date, a_beg_offset, a_end_offset):
        """ return a cursor on all item """
        req = self._queue_table.select().where( (self._queue_table.c.q_insertion_time >= a_beg_priority) & (self._queue_table.c.q_insertion_time <= a_end_priority) )\
                                        .order_by(self._queue_table.c.q_priority.desc(),self._queue_table.c.q_insertion_time.asc())\
                                        .offset(a_beg_offset).limit( (a_end_offset - a_beg_offset) + 1)
        
        return self._execute_req(req)
    
    def get_from_uuid(self, a_uuid):
        """ return the row with given uuid """
        req = self._queue_table.select().where(self._queue_table.c.q_item_id == a_uuid)
        
        return self._execute_req(req).fetchone()
    
    def delete_from_uuid(self, a_uuid):
        """ delete from a uuid """
        req = self._queue_table.delete().where(self._queue_table.c.q_item_id == a_uuid)
        
        return self._execute_req(req)
    
    def change_status(self, a_uuid, a_status):
        """ change the status of an item """
        
        req = self._queue_table.update().where(self._queue_table.c.q_item_id == a_uuid).values(q_status = a_status)
        return self._execute_req(req)
    
    def change_priority(self, a_uuid, a_priority):
        """ change the status of an item """
        
        req = self._queue_table.update().where(self._queue_table.c.q_item_id == a_uuid).values(q_priority = a_priority)
        return self._execute_req(req)
