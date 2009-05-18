'''
Created on May 18, 2009

@author: guillaume.aubert@ctbto.org
'''

from unittest import TestCase,TestLoader,TextTestRunner

from ims_message_parser import IMSParser

class IMSMessageParserTest(TestCase):
    
    def setUp(self):
        pass
        
    def test_list_tokens_lower_case(self):
        
        
        message = "     begin IMS2.0     \nmsg_type data \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \ntime 2000/11/22 to 2001/01/01\nsta_list ARP01\nalert_temp\n    stop"
        
        parser = IMSParser()
        
        result = parser.parse(message)
        
        print("Result = %s\n"%(result))