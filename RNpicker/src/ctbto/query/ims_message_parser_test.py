'''
Created on May 18, 2009

@author: guillaume.aubert@ctbto.org
'''

from unittest import TestCase,TestLoader,TextTestRunner

from ims_message_parser import IMSParser

class IMSMessageParserTest(TestCase):
    
    def setUp(self):
        pass
    
    def test_simple_request_message(self):
        """ simple message taken from AutoDRM Help response message """
        
        message = "begin ims1.0\r\nmsg_type request\nmsg_id ex009 any_ndc \ne-mail foo.bar.ssi@domain.name.de \ntime 1999/06/13 to 1999/06/14 \nbull_type idc_reb \nbulletin ims1.0\nstop"
        
        parser = IMSParser()
        
        result = parser.parse(message)
        
        #print("\nresult = %s\n" %(result))
        
        # check mandatory fields
        self.assertEqual(result['MSGFORMAT'],'ims1.0')
        self.assertEqual(result['MSGTYPE'],'request')
        self.assertEqual(result['MSGID'],'ex009')
        self.assertEqual(result['EMAIL'],'foo.bar.ssi@domain.name.de')
        
        # optional for this request
        self.assertEqual(result['SOURCE'],'any_ndc')
        
        # product_1
        self.assertTrue(result.has_key('PRODUCT_1'))
         
        self.assertEqual(result['PRODUCT_1'],{'FORMAT': 'ims1.0', 'STARTDATE': '1999/06/13', 'BULLTYPE': 'idc_reb', 'ENDDATE': '1999/06/14', 'TYPE': 'BULLETIN'})
     
    def test_simple_request_message_without_source(self): 
        """ simple message taken from AutoDRM Help response message without the optional source field """
        
        message = "begin ims1.0\r\nmsg_type request\nmsg_id ex009  \ne-mail foo.bar.ssi@domain.name.de \ntime 1999/06/13 to 1999/06/14 \nbull_type idc_reb \nbulletin ims1.0\nstop"
        
        parser = IMSParser()
        
        result = parser.parse(message)
        
        #print("\nresult = %s\n" %(result))
        
        # check mandatory fields
        self.assertEqual(result['MSGFORMAT'],'ims1.0')
        self.assertEqual(result['MSGTYPE'],'request')
        self.assertEqual(result['MSGID'],'ex009')
        self.assertEqual(result['EMAIL'],'foo.bar.ssi@domain.name.de')
        
        # optional for this request
        self.assertFalse(result.has_key('SOURCE'))
        
        # product_1
        self.assertTrue(result.has_key('PRODUCT_1'))
         
        self.assertEqual(result['PRODUCT_1'],{'FORMAT': 'ims1.0', 'STARTDATE': '1999/06/13', 'BULLTYPE': 'idc_reb', 'ENDDATE': '1999/06/14', 'TYPE': 'BULLETIN'})
     
    def test_multiple_products_request(self):
        """ multiple products request message taken from AutoDRM Help response message """
        
        
        message = "begin ims1.0\nmsg_type request    \nmsg_id ex042 myndc    \ne-mail foo.bar@pluto.com    \ntime 1999/06/01 to 1999/07/01    \nbull_type idc_reb\nmag 3.5 to 5.0\ndepth to 30\nlat -30 to -20\nlon -180 to -140\nbulletin ims1.0\nlat 75 to 79\nlon 110 to 140\nbulletin ims2.0:cm6\nstop"

        parser = IMSParser()
        
        result = parser.parse(message)
        
        #print("\nresult = %s\n" %(result))
        
        # check mandatory fields
        self.assertEqual(result['MSGFORMAT'],'ims1.0')
        self.assertEqual(result['MSGTYPE'],'request')
        self.assertEqual(result['MSGID'],'ex042')
        self.assertEqual(result['EMAIL'],'foo.bar@pluto.com')
        
        # optional for this request
        self.assertEqual(result['SOURCE'],'myndc')
        
        # product_1
        self.assertTrue(result.has_key('PRODUCT_1'))
        
        self.assertEqual(result['PRODUCT_1'],{'ENDLON': '-140', 'STARTDATE': '1999/06/01', 'ENDDATE': '1999/07/01', 'ENDDEPTH': '30', 'FORMAT': 'ims1.0', 'ENDLAT': '-20', 'STARTLAT': '-30', 'STARTDEPTH': 'MIN', 'BULLTYPE': 'idc_reb', 'STARTMAG': '3.5', 'ENDMAG': '5.0', 'STARTLON': '-180', 'TYPE': 'BULLETIN'})
     
        # product_2
        self.assertTrue(result.has_key('PRODUCT_2'))
     
        self.assertEqual(result['PRODUCT_2'],{'STARTDATE': '1999/06/01', 'ENDDATE': '1999/07/01', 'ENDDEPTH': '30', 'FORMAT': 'ims2.0', 'ENDLAT': '79', 'STARTLAT': '75', 'STARTDEPTH': 'MIN', 'SUBFORMAT': 'cm6', 'BULLTYPE': 'idc_reb', 'STARTMAG': '3.5', 'ENDLON': '140', 'ENDMAG': '5.0', 'STARTLON': '110', 'TYPE': 'BULLETIN'})
      
    def test_multiple_lat_lon_request(self): 
        """ multiple products request message with different lat/lon taken from AutoDRM Help response message """ 
        
        message = "begin ims1.0\nmsg_type request    \nmsg_id ex042   \ne-mail foo_bar.a.vb.bar@venus.com    \ntime 1999/07/12 to 1999/07/13    \nbull_type idc_sel3\nbulletin ims1.0\nstop"

        parser = IMSParser()
        
        result = parser.parse(message)
        
        print("\nresult = %s\n" %(result))
        
        # check mandatory fields
        self.assertEqual(result['MSGFORMAT'],'ims1.0')
        self.assertEqual(result['MSGTYPE'],'request')
        self.assertEqual(result['MSGID'],'ex042')
        self.assertEqual(result['EMAIL'],'foo_bar.a.vb.bar@venus.com')
        
        # optional for this request
        self.assertFalse(result.has_key('SOURCE'))
      
        # product_1
        self.assertTrue(result.has_key('PRODUCT_1'))
        
        self.assertEqual(result['PRODUCT_1'],{'FORMAT': 'ims1.0', 'STARTDATE': '1999/07/12', 'BULLTYPE': 'idc_sel3', 'ENDDATE': '1999/07/13', 'TYPE': 'BULLETIN'})
    
    def test_parse_several_request_with_the_same_parser(self): 
        """ parse multiple request message with the same parser (check if internal state stays consistent) """ 
        
        message = "begin ims1.0\nmsg_type request    \nmsg_id ex042   \ne-mail foo_bar.a.vb.bar@venus.com    \ntime 1999/07/12 to 1999/07/13    \nbull_type idc_sel3\nbulletin ims1.0\nstop"

        parser = IMSParser()
        
        result = parser.parse(message)
        
        print("\nresult = %s\n" %(result))
        
        # check mandatory fields
        self.assertEqual(result['MSGFORMAT'],'ims1.0')
        self.assertEqual(result['MSGTYPE'],'request')
        self.assertEqual(result['MSGID'],'ex042')
        self.assertEqual(result['EMAIL'],'foo_bar.a.vb.bar@venus.com')
        
        # optional for this request
        self.assertFalse(result.has_key('SOURCE'))
      
        # product_1
        self.assertTrue(result.has_key('PRODUCT_1'))
        
        self.assertEqual(result['PRODUCT_1'],{'FORMAT': 'ims1.0', 'STARTDATE': '1999/07/12', 'BULLTYPE': 'idc_sel3', 'ENDDATE': '1999/07/13', 'TYPE': 'BULLETIN'})
    
        # first message ok, get the second one
        
        message_1 = "begin ims1.0\nmsg_type request    \nmsg_id ex042 myndc    \ne-mail foo.bar@pluto.com    \ntime 2005/06/01 to 2006/07/01    \nbull_type idc_reb\nmag 3.5 to 5.0\ndepth to 30\nlat -30 to -20\nlon -180 to -140\nbulletin ims1.0\nlat 75 to 79\nlon 110 to 140\nbulletin ims2.0:cm6\nstop"
       
        result1 = parser.parse(message_1)
         
        # check mandatory fields
        self.assertEqual(result1['MSGFORMAT'],'ims1.0')
        self.assertEqual(result1['MSGTYPE'],'request')
        self.assertEqual(result1['MSGID'],'ex042')
        self.assertEqual(result1['EMAIL'],'foo.bar@pluto.com')
        
        # optional for this request
        self.assertEqual(result1['SOURCE'],'myndc')
        
        # product_1
        self.assertTrue(result1.has_key('PRODUCT_1'))
        
        self.assertEqual(result1['PRODUCT_1'],{'ENDLON': '-140', 'STARTDATE': '2005/06/01', 'ENDDATE': '2006/07/01', 'ENDDEPTH': '30', 'FORMAT': 'ims1.0', 'ENDLAT': '-20', 'STARTLAT': '-30', 'STARTDEPTH': 'MIN', 'BULLTYPE': 'idc_reb', 'STARTMAG': '3.5', 'ENDMAG': '5.0', 'STARTLON': '-180', 'TYPE': 'BULLETIN'})
     
        # product_2
        self.assertTrue(result1.has_key('PRODUCT_2'))
     
        self.assertEqual(result1['PRODUCT_2'],{'STARTDATE': '2005/06/01', 'ENDDATE': '2006/07/01', 'ENDDEPTH': '30', 'FORMAT': 'ims2.0', 'ENDLAT': '79', 'STARTLAT': '75', 'STARTDEPTH': 'MIN', 'SUBFORMAT': 'cm6', 'BULLTYPE': 'idc_reb', 'STARTMAG': '3.5', 'ENDLON': '140', 'ENDMAG': '5.0', 'STARTLON': '110', 'TYPE': 'BULLETIN'})
      
        
    
    def test_slsd_request(self): 
        """ test with station list and slsd taken from AutoDRM Help response message """ 
        
        message = "begin ims1.0\nmsg_type request    \nmsg_id ex006 any_ndc \ne-mail foo_bar.a.vb.bar@venus.com    \ntime 1999/08/01 to 1999/09/01   \nsta_list HIA,MJARbull_type idc_sel1\nslsd:automatic ims1.0\nstop"
        
        parser = IMSParser()
        
        result = parser.parse(message)
        
        print("\nresult = %s\n" %(result))
        
        # check mandatory fields
        self.assertEqual(result['MSGFORMAT'],'ims1.0')
        self.assertEqual(result['MSGTYPE'],'request')
        self.assertEqual(result['MSGID'],'ex042')
        self.assertEqual(result['EMAIL'],'foo_bar.a.vb.bar@venus.com')
        
        # optional for this request
        self.assertTrue(result.has_key('SOURCE'))
        
    """    Add Errors (bad email address, missing essential elements,)    
    """
        
        
        