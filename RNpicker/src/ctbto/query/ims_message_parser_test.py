'''
Created on May 18, 2009

@author: guillaume.aubert@ctbto.org
'''

import StringIO

from unittest import TestCase,TestLoader,TextTestRunner

from ims_message_parser import IMSParser

class IMSMessageParserTest(TestCase):
    
    def setUp(self):
        pass
        
    def test_list_tokens_lower_case(self):
        pass