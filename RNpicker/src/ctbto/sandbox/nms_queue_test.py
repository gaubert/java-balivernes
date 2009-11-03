'''
Created on Nov 02, 2009

Unit tests for NMSQueue

@author: guillaume.aubert@ctbto.org
'''

from unittest import TestCase,TestLoader,TextTestRunner
import pickle
import os
import datetime
import pprint

from nms_queue import NMSQueue, NMSQueueItem

from threading import Thread

workers = []

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
        
      
def start_workers(nb_of_threads, queue):
    
    for i in range(nb_of_threads):
        w = Worker("%s" % (i), queue)
        
        w.setDaemon(True)
        
        workers.append(w)
        
        w.start()
    
    print("End of Start Workers")

def stop_workers():
    
    for worker in workers:
        worker.change_status("stopped")
        

class NMSQueueTest(TestCase):
    
    def setUp(self):
        
        #os.environ['CONF_FILE'] = 'resources/test/nms_production_engine.conf'
        os.environ['CONF_FILE'] = '/home/aubert/workspace/NMSProject/nms_common/resources/test/nms_production_engine.conf'
        
        pass
            
    def test_simple_test(self):
        """ test NMSQueue """
        
        queue = NMSQueue()
        
        items = []
        # create items
        for i in range(50):
            items.append( NMSQueueItem(i,"data %s" % (i)) )
    
        #add items in queue
        for item in items:
            queue.put(item)
          
        start_workers(3,queue)  
        
        #wait for queue to be empty
        queue.join()
        
        print("After join \n")
        
        stop_workers()
        
        print("No more elements in the queue\n")
        
        
        
        
            
            