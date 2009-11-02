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

from nms_queue import NMSQueue

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
        for i in range(1,20):
            items.append( (i,"data") )
    
        for item in items:
            queue.put(item)
        
        
        
        
            
            