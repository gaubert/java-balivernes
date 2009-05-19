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
        
        
        print("Start\n")
        message = "begin ims1.0\nmsg_type request    \nmsg_id ex042 any_ndc    \ne-mail foo.bar@mars.com    \ntime 1999/06/01 to 1999/07/01    \nbull_type idc_reb\nmag 3.5 to 5.0\ndepth to 30\nlat -30 to -20\nlon -180 to -140\nbulletin ims1.0\nlat 75 to 79\nlon 110 to 140\nbulletin ims1.0\nstop"

        parser = IMSParser()
        
        result = parser.parse(message)
        
        print("Result = %s\n"%(result))