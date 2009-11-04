'''
Created on Nov 2, 2009

@author: guillaume.aubert@ctbto.org
'''

from time import time as _time
from sql_queue import SQLQueue
from tokyo_queue import TokyoCabinetQueue
from collections import deque
import uuid

class Empty(Exception):
    "Exception raised by Queue.get(block=0)/get_nowait()."
    pass

class Full(Exception):
    "Exception raised by Queue.put(block=0)/put_nowait()."
    pass

class Queue:
    """Create a queue object with a given maximum size.

    If maxsize is <= 0, the queue size is infinite.
    """
    def __init__(self, maxsize=0):
        try:
            import threading
        except ImportError:
            import dummy_threading as threading
        self.maxsize = maxsize
        self._init(maxsize)
        # mutex must be held whenever the queue is mutating.  All methods
        # that acquire mutex must release it before returning.  mutex
        # is shared between the three conditions, so acquiring and
        # releasing the conditions also acquires and releases mutex.
        self.mutex = threading.Lock()
        # Notify not_empty whenever an item is added to the queue; a
        # thread waiting to get is notified then.
        self.not_empty = threading.Condition(self.mutex)
        # Notify not_full whenever an item is removed from the queue;
        # a thread waiting to put is notified then.
        self.not_full = threading.Condition(self.mutex)
        # Notify all_tasks_done whenever the number of unfinished tasks
        # drops to zero; thread waiting to join() is notified to resume
        self.all_tasks_done = threading.Condition(self.mutex)
        
        self.unfinished_tasks = self.qsize()

    def task_done(self):
        """Indicate that a formerly enqueued task is complete.

        Used by Queue consumer threads.  For each get() used to fetch a task,
        a subsequent call to task_done() tells the queue that the processing
        on the task is complete.

        If a join() is currently blocking, it will resume when all items
        have been processed (meaning that a task_done() call was received
        for every item that had been put() into the queue).

        Raises a ValueError if called more times than there were items
        placed in the queue.
        """
        self.all_tasks_done.acquire()
        try:
            unfinished = self.unfinished_tasks - 1
            if unfinished <= 0:
                if unfinished < 0:
                    raise ValueError('task_done() called too many times')
                self.all_tasks_done.notifyAll()
            self.unfinished_tasks = unfinished
        finally:
            self.all_tasks_done.release()

    def join(self):
        """Blocks until all items in the Queue have been gotten and processed.

        The count of unfinished tasks goes up whenever an item is added to the
        queue. The count goes down whenever a consumer thread calls task_done()
        to indicate the item was retrieved and all work on it is complete.

        When the count of unfinished tasks drops to zero, join() unblocks.
        """
        self.all_tasks_done.acquire()
        try:
            while self.unfinished_tasks:
                self.all_tasks_done.wait()
        finally:
            self.all_tasks_done.release()

    def qsize(self):
        """Return the approximate size of the queue (not reliable!)."""
        self.mutex.acquire()
        n = self._qsize()
        self.mutex.release()
        return n

    def empty(self):
        """Return True if the queue is empty, False otherwise (not reliable!)."""
        self.mutex.acquire()
        n = not self._qsize()
        self.mutex.release()
        return n

    def full(self):
        """Return True if the queue is full, False otherwise (not reliable!)."""
        self.mutex.acquire()
        n = 0 < self.maxsize == self._qsize()
        self.mutex.release()
        return n

    def put(self, item, block=True, timeout=None):
        """Put an item into the queue.

        If optional args 'block' is true and 'timeout' is None (the default),
        block if necessary until a free slot is available. If 'timeout' is
        a positive number, it blocks at most 'timeout' seconds and raises
        the Full exception if no free slot was available within that time.
        Otherwise ('block' is false), put an item on the queue if a free slot
        is immediately available, else raise the Full exception ('timeout'
        is ignored in that case).
        """
        self.not_full.acquire()
        try:
            if self.maxsize > 0:
                if not block:
                    if self._qsize() == self.maxsize:
                        raise Full
                elif timeout is None:
                    while self._qsize() == self.maxsize:
                        self.not_full.wait()
                elif timeout < 0:
                    raise ValueError("'timeout' must be a positive number")
                else:
                    endtime = _time() + timeout
                    while self._qsize() == self.maxsize:
                        remaining = endtime - _time()
                        if remaining <= 0.0:
                            raise Full
                        self.not_full.wait(remaining)
            self._put(item)
            self.unfinished_tasks += 1
            self.not_empty.notify()
        finally:
            self.not_full.release()

    def put_nowait(self, item):
        """Put an item into the queue without blocking.

        Only enqueue the item if a free slot is immediately available.
        Otherwise raise the Full exception.
        """
        return self.put(item, False)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.

        If optional args 'block' is true and 'timeout' is None (the default),
        block if necessary until an item is available. If 'timeout' is
        a positive number, it blocks at most 'timeout' seconds and raises
        the Empty exception if no item was available within that time.
        Otherwise ('block' is false), return an item if one is immediately
        available, else raise the Empty exception ('timeout' is ignored
        in that case).
        """
        self.not_empty.acquire()
        try:
            if not block:
                if not self._qsize():
                    raise Empty
            elif timeout is None:
                while not self._qsize():
                    self.not_empty.wait()
            elif timeout < 0:
                raise ValueError("'timeout' must be a positive number")
            else:
                endtime = _time() + timeout
                while not self._qsize():
                    remaining = endtime - _time()
                    if remaining <= 0.0:
                        raise Empty
                    self.not_empty.wait(remaining)
            item = self._get()
            self.not_full.notify()
            return item
        finally:
            self.not_empty.release()

    def get_nowait(self):
        """Remove and return an item from the queue without blocking.

        Only get an item if one is immediately available. Otherwise
        raise the Empty exception.
        """
        return self.get(False)

    # Override these methods to implement other queue organizations
    # (e.g. stack or priority queue).
    # These will only be called with appropriate locks held

    # Initialize the queue representation
    def _init(self, maxsize):
        self.queue = deque()

    def _qsize(self, len=len):
        return len(self.queue)

    # Put a new item in the queue
    def _put(self, item):
        self.queue.append(item)

    # Get an item from the queue
    def _get(self):
        return self.queue.popleft()
    
class NMSQueueItemSet():
    """ Set of Items retireved from the Queue """
    
    def __init__(self, a_db_cusror):
        """ constructor """
        
        self._db_cusror = a_db_cusror
        
    def __iter__(self):
        """ support iterable interface """
        return self
        
    def next(self):
        
        row = self._db_cusror.fetchone()
         
        if row:
            return NMSQueueItem(row[1], None, row[0], row[2], row[3])
        else:
            raise StopIteration()

class NMSQueueItem():
    """ Item internal to the Queue """
    
    def __init__(self, a_priority, a_data, a_uuid = None, a_status = None, a_insertion_date = None):
        
        self._priority       = a_priority
        self._data           = a_data
        self._uuid           = a_uuid
        self._status         = "ACTIVE" if not a_status else a_status
        self._insertion_date = a_insertion_date
    
    def set_uuid(self):
        if not self._uuid:
            self._uuid = uuid.uuid1()
    
    def __str__(self):
        return "NMSQueueItem: priority = %s, uuid = %s, status = %s, insertion_date = %s" %(self._priority, self._uuid, self._status, self._insertion_date)
    
    @property
    def uuid(self):
        return self._uuid
    
    @property
    def priority(self):
        return self._priority
    
    @property
    def data(self):
        return self._data
    
    @property
    def status(self):
        return self._status
    
    def insertion_date(self):
        return self._insertion_date

class NMSQueue(Queue):
    """Create a queue object with a given maximum size.

    """
    # Override these methods to implement other queue organizations
    # (e.g. stack or priority queue).
    # These will only be called with appropriate locks held

    # Initialize the queue representation
    def _init(self, maxsize):
        self.queue = TokyoCabinetQueue()

    def _qsize(self, len=len):
        return self.queue.size()

    # Put a new item in the queue
    def _put(self, item):
        
        t = type(item)
        
        if t.__name__=='instance':
            if item.__class__.__name__== 'NMSQueueItem':
                item.set_uuid()
        
                self.queue.put(item)
        else:
           raise Exception("This queue only accepts NMSQueueItem. Found a %s" % (t)) 

    # Get an item from the queue
    def _get(self):
        row = self.queue.pop()
        return NMSQueueItem(row[1], None, row[0], row[2], row[3])
    
    #operating, visitor interface
    def get_item(self,uuid):
        """ Return an item that has the following id """
        row = self.queue.get_from_uuid(uuid)
        return NMSQueueItem(row[1], None, row[0], row[2], row[3])
    
    def delete_item(self,uuid):
        """ delete an item from the queue """
        self.queue.delete_from_uuid(uuid)
    
    def get_items_with_priority(self, a_beg_priority, a_end_priority, a_beg_offset, a_end_offset):
        """ Return items with priority """
        
        db_cursor = self.queue.get_from_priority_range(a_beg_priority, a_end_priority, a_beg_offset, a_end_offset)
        return NMSQueueItemSet(db_cursor)
    
    def change_item_status(self,a_uuid, a_status):
        """ Change item status """
        self.queue.change_status(a_uuid,a_status)   
        
    
    #Visitor interface
    
    