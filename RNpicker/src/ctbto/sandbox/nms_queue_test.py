'''
Created on Nov 02, 2009

Unit tests for NMSQueue

@author: guillaume.aubert@ctbto.org
'''

from unittest import TestCase,TestLoader,TextTestRunner
import pickle
import os
import datetime
import time
import pprint


from nms_queue   import NMSQueue, NMSQueueItem
from sql_queue   import SQLQueue
from tokyo_queue import TokyoCabinetQueue

from threading   import Thread

workers   = []
producers = []

class Worker(Thread):
   
    def __init__ (self, name, queue):
        Thread.__init__(self)
        self.name    = name
        self.queue   = queue
        self.status  = "stopped"
        self.timeout = 3
   
    def run(self):
    
        self.status = "running"
    
        while self.status == "running":
                item = self.queue.get(self.timeout)
                
                if item:
                    print("[Worker %s] consumed %s" % (self.name, item))
                    self.queue.task_done()
                else:
                    print("[Worker %s] just wake up\n" % (self.name))
                
                item = None
                
            
        print("[Worker %s] job finished. Bye")
    
    def change_status(self, value):
        
        print("[Worker %s] Set status to %s" %(self.name, value))
        
        self.status = value
        
class Producer(Thread):
   
    def __init__ (self, name, queue, nb_messages):
      Thread.__init__(self)
      
      self.name    = name
      self.queue   = queue
      self.status  = "stopped"
      self.nb_messages = nb_messages
   
    def run(self):
    
        print("[Producer %s] Start running " %(self.name))
        self.status = "running"
    
        i = 0    
        while self.nb_messages != 0:
            if self.status == "running":
                
                if i % 2 == 0:
                    cpt = 1
                else:
                    cpt = 2
                
                item = NMSQueueItem(cpt,"data %s" % (i))
                print("[Producer %s] produce %s" % (self.name, item))
                self.queue.put(item)
                self.nb_messages -= 1
                i += 1
            else:
                print("[Producer %s] Status is not running exit. Job maybe unfinished" % (self.name) )
                return
                
            
        print("[Producer %s] job finished. Bye" % (self.name) )
    
    def change_status(self, value):
        
        print("[Producer %s] Set status to %s" %(self.name, value))
        
        self.status = value
        
        
      
def start_workers(nb_of_threads, queue):
    """ start consumers """
    for i in range(nb_of_threads):
        w = Worker("%s" % (i), queue)
        
        w.setDaemon(True)
        
        workers.append(w)
        
        w.start()
    
    print("End of Start Workers")
    
def start_producers(nb_producers, nb_messages, queue):
    """ start producer """
    
    for i in range(nb_producers):
        p = Producer("%s" % (i), queue, nb_messages)
        
        p.setDaemon(True)
        
        producers.append(p)
        
        p.start()
    
    print("End of Start Producers")

def stop_workers():
    
    for worker in workers:
        worker.change_status("stopped")
        

class NMSQueueTest(TestCase):
    
    def setUp(self):
        
        #os.environ['CONF_FILE'] = 'resources/test/nms_production_engine.conf'
        os.environ['CONF_FILE'] = '/home/aubert/workspace/NMSProject/nms_common/resources/test/nms_production_engine.conf'
        
        pass
            
    def test_consprod(self):
        """ test consumer, producer """
        
        queue = NMSQueue()
        
        start_producers(1,10,queue)
         
        time.sleep(1)    
                  
        start_workers(1,queue)  
        
        #wait for queue to be empty
        queue.join()
        
        print("After join \n")
        
        stop_workers()
        
        print("No more elements in the queue\n")
    
    def ztest_get_from_uuid(self):
        """ test get from uuid """
        
        queue = NMSQueue()
        
        item = NMSQueueItem(5,"data %s" % (1))
        
        item.set_uuid()
        
        print("item = %s\n" %(item))
        
        queue.put(item)
        
        newitem = queue.get_item(item.uuid)
        
        print("new item = %s\n" % (newitem) )
        
    def ztest_delete_from_uuid(self):
        """ test get from uuid """
        
        queue = NMSQueue()
        
        item = NMSQueueItem(5,"data %s" % (1))
        
        item.set_uuid()
        
        print("item = %s\n" %(item))
        
        queue.put(item)
        
        newitem = queue.get_item(item.uuid)
        
        print("new item = %s\n" % (newitem) )
        
        queue.delete_item(item.uuid)
        
        newitem = queue.get_item(item.uuid)
        
        print("new item = %s\n" % (newitem) )
    
        
    def ztest_get_range_of_nms_queue_items(self):
        """ get range of nms queue items """
        queue = NMSQueue()
        
        result_set = queue.get_items_with_priority(1,1,0,1)
        
        for item in result_set:
            print("\nItem = %s\n" % (item) )
    
    def ztest_change_status(self):
        """ change status """
        queue = NMSQueue()
        
        result_set = queue.get_items_with_priority(1,1,0,1)
        
        the_item = None
        
        for item in result_set:
            print("\nItem = %s\n" % (item) )
            the_item = item
        
        queue.change_item_status(the_item.uuid, "BURIED")
        
        result_set = queue.get_items_with_priority(1,1,0,10)
        
        for item in result_set:
            print("\nItem = %s\n" % (item) )
        
    
    def ztest_get_item(self):
        """ get an item using its uuid """
        
        queue = NMSQueue()
        
        result_set = queue.get_items_with_priority(1,1,0,1)
        
        for item in result_set:
            print("\nItem = %s\n" % (item) )
            newitem = queue.get_item(item.uuid)
            print("\nRetrieve the same from queue Item = %s\n" % (newitem) )
    
    def ztest_delete_item(self):
        """ delete item """
        
        queue = NMSQueue()
        
        result_set = queue.get_items_with_priority(1,1,0,1)
        the_item = None
        for item in result_set:
            print("\nItem = %s\n" % (item) )
            the_item = item
            print("\nItem with uuid %s deleted" % (item.uuid) )
        
        queue.delete_item(the_item.uuid)
    
    def ztest_sql_queue(self):
        """ test for the internal sqlqueue """
        
        sql_queue = SQLQueue()
               
        #insertion
        for i in range(10):
            item = NMSQueueItem(5,"data %s" % (i))
            item.set_uuid()
            sql_queue.put(item.dictify())
        
        size = sql_queue.size()
            
        while size != 0:
            the_dict = sql_queue.pop()
            item = NMSQueueItem.create_from_dict(the_dict)
            print("size = %d, item = %s\n" % (size, item))
            size = sql_queue.size()
        
        print("size = %s" % size )
        
    def ztest_tokyo_queue(self):
        """ test for the internal tokyo cabinet queue """
        
        sql_queue = TokyoCabinetQueue()
        
        print("Queue size = %d\n" %(sql_queue.size()) )
                     
        #insertion
        for i in range(10):
            if i % 2 == 0:
                p = 0
            else:
                p = 1
            item = NMSQueueItem(p,"data %s" % (i))
            item.set_uuid()
            sql_queue.put(item.dictify())
            #time.sleep(0.5)
        
        size = sql_queue.size()
            
        while size != 0:
            the_dict = sql_queue.pop()
            item = NMSQueueItem.create_from_dict(the_dict)
            print("size = %d, item = %s\n" % (size, item))
            size = sql_queue.size()
        
        print("size = %s" % size )
        
        
        
        
        
            
            