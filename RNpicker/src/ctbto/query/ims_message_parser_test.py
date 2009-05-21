'''
Created on May 18, 2009

@author: guillaume.aubert@ctbto.org
'''

from unittest import TestCase

from ims_message_parser import IMSParser, ParsingError

class IMSMessageParserTest(TestCase):
    
    def setUp(self):
        pass
    
    def ztest_simple_request_message(self):
        """ test simple message taken from AutoDRM Help response message """
        
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
         
        self.assertEqual(result['PRODUCT_1'], {'FORMAT': 'ims1.0', 'STARTDATE': '1999/06/13', 'BULLTYPE': 'idc_reb', 'ENDDATE': '1999/06/14', 'TYPE': 'BULLETIN'})
     
    def ztest_simple_request_message_without_source(self): 
        """ test simple message taken from AutoDRM Help response message without the optional source field """
        
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
         
        self.assertEqual(result['PRODUCT_1'], {'FORMAT': 'ims1.0', 'STARTDATE': '1999/06/13', 'BULLTYPE': 'idc_reb', 'ENDDATE': '1999/06/14', 'TYPE': 'BULLETIN'})
     
    def ztest_multiple_products_request(self):
        """ test multiple products request message taken from AutoDRM Help response message """
        
        
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
        
        self.assertEqual(result['PRODUCT_1'], {'ENDLON': '-140', 'STARTDATE': '1999/06/01', 'ENDDATE': '1999/07/01', 'ENDDEPTH': '30', 'FORMAT': 'ims1.0', 'ENDLAT': '-20', 'STARTLAT': '-30', 'STARTDEPTH': 'MIN', 'BULLTYPE': 'idc_reb', 'STARTMAG': '3.5', 'ENDMAG': '5.0', 'STARTLON': '-180', 'TYPE': 'BULLETIN'})
     
        # product_2
        self.assertTrue(result.has_key('PRODUCT_2'))
     
        self.assertEqual(result['PRODUCT_2'], {'STARTDATE': '1999/06/01', 'ENDDATE': '1999/07/01', 'ENDDEPTH': '30', 'FORMAT': 'ims2.0', 'ENDLAT': '79', 'STARTLAT': '75', 'STARTDEPTH': 'MIN', 'SUBFORMAT': 'cm6', 'BULLTYPE': 'idc_reb', 'STARTMAG': '3.5', 'ENDLON': '140', 'ENDMAG': '5.0', 'STARTLON': '110', 'TYPE': 'BULLETIN'})
      
    def ztest_multiple_lat_lon_request(self): 
        """ test multiple products request message with different lat/lon taken from AutoDRM Help response message """ 
        
        message = "begin ims1.0\nmsg_type request    \nmsg_id ex042   \ne-mail foo_bar.a.vb.bar@venus.com    \ntime 1999/07/12 to 1999/07/13    \nbull_type idc_sel3\nbulletin ims1.0\nstop"

        parser = IMSParser()
        
        result = parser.parse(message)
        
        #print("\nresult = %s\n" %(result))
        
        # check mandatory fields
        self.assertEqual(result['MSGFORMAT'],'ims1.0')
        self.assertEqual(result['MSGTYPE'],'request')
        self.assertEqual(result['MSGID'],'ex042')
        self.assertEqual(result['EMAIL'],'foo_bar.a.vb.bar@venus.com')
        
        # optional for this request
        self.assertFalse(result.has_key('SOURCE'))
      
        # product_1
        self.assertTrue(result.has_key('PRODUCT_1'))
        
        self.assertEqual(result['PRODUCT_1'], {'FORMAT': 'ims1.0', 'STARTDATE': '1999/07/12', 'BULLTYPE': 'idc_sel3', 'ENDDATE': '1999/07/13', 'TYPE': 'BULLETIN'})
    
    def ztest_parse_several_request_with_the_same_parser(self): 
        """ test parse multiple request message with the same parser (check if internal state stays consistent) """ 
        
        message = "begin ims1.0\nmsg_type request    \nmsg_id ex042   \ne-mail foo_bar.a.vb.bar@venus.com    \ntime 1999/07/12 to 1999/07/13    \nbull_type idc_sel3\nbulletin ims1.0\nstop"

        parser = IMSParser()
        
        result = parser.parse(message)
        
        #print("\nresult = %s\n" %(result))
        
        # check mandatory fields
        self.assertEqual(result['MSGFORMAT'],'ims1.0')
        self.assertEqual(result['MSGTYPE'],'request')
        self.assertEqual(result['MSGID'],'ex042')
        self.assertEqual(result['EMAIL'],'foo_bar.a.vb.bar@venus.com')
        
        # optional for this request
        self.assertFalse(result.has_key('SOURCE'))
      
        # product_1
        self.assertTrue(result.has_key('PRODUCT_1'))
        
        self.assertEqual(result['PRODUCT_1'], {'FORMAT': 'ims1.0', 'STARTDATE': '1999/07/12', 'BULLTYPE': 'idc_sel3', 'ENDDATE': '1999/07/13', 'TYPE': 'BULLETIN'})
    
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
        
        self.assertEqual(result1['PRODUCT_1'], {'ENDLON': '-140', 'STARTDATE': '2005/06/01', 'ENDDATE': '2006/07/01', 'ENDDEPTH': '30', 'FORMAT': 'ims1.0', 'ENDLAT': '-20', 'STARTLAT': '-30', 'STARTDEPTH': 'MIN', 'BULLTYPE': 'idc_reb', 'STARTMAG': '3.5', 'ENDMAG': '5.0', 'STARTLON': '-180', 'TYPE': 'BULLETIN'})
     
        # product_2
        self.assertTrue(result1.has_key('PRODUCT_2'))
     
        self.assertEqual(result1['PRODUCT_2'], {'STARTDATE': '2005/06/01', 'ENDDATE': '2006/07/01', 'ENDDEPTH': '30', 'FORMAT': 'ims2.0', 'ENDLAT': '79', 'STARTLAT': '75', 'STARTDEPTH': 'MIN', 'SUBFORMAT': 'cm6', 'BULLTYPE': 'idc_reb', 'STARTMAG': '3.5', 'ENDLON': '140', 'ENDMAG': '5.0', 'STARTLON': '110', 'TYPE': 'BULLETIN'})
      
        
    
    def ztest_slsd_automatic_request(self): 
        """ test with station list and slsd taken from AutoDRM Help response message """ 
        
        message = "begin ims1.0\nmsg_type request    \nmsg_id ex134 any_ndc \ne-mail foo_bar.a.vb.bar@venus.com    \ntime 1999/08/01 to 1999/09/01   \nsta_list HIA,MJAR\nbull_type idc_sel1\nslsd:automatic ims1.0\nstop"
        
        parser = IMSParser()
        
        result = parser.parse(message)
        
        #print("\nresult = %s\n" %(result))
        
        # check mandatory fields
        self.assertEqual(result['MSGFORMAT'],'ims1.0')
        self.assertEqual(result['MSGTYPE'],'request')
        self.assertEqual(result['MSGID'],'ex134')
        self.assertEqual(result['EMAIL'],'foo_bar.a.vb.bar@venus.com')
        
        # optional for this request
        self.assertTrue(result.has_key('SOURCE'))
       
        # product_1
        self.assertTrue(result.has_key('PRODUCT_1'))
        
        # validate that there is a sta_list and a subtype
        self.assertEqual(result['PRODUCT_1'], {'BULLTYPE': 'idc_sel1', 'STARTDATE': '1999/08/01', 'ENDDATE': '1999/09/01', 'SUBTYPE': 'automatic', 'FORMAT': 'ims1.0', 'TYPE': 'SLSD', 'STALIST': ['HIA', 'MJAR']})
    
    def ztest_slsd_automatic_with_many_newlines_request(self): 
        """ test with station list and slsd taken from AutoDRM Help response message.
            added many new lines in order to check if the parser allow that
        """ 
        
        message = "begin ims1.0\nmsg_type request    \n\n\nmsg_id ex134 any_ndc \r\n\r\n\n\n\n\n\ne-mail foo_bar.a.vb.bar@venus.com    \n\n\n\n\n\ntime 1999/08/01 to 1999/09/01   \nsta_list HIA,MJAR\n\nbull_type idc_sel1\nslsd:automatic ims1.0\n\r\n\nstop"
        
        parser = IMSParser()
        
        result = parser.parse(message)
        
        #print("\nresult = %s\n" %(result))
        
        # check mandatory fields
        self.assertEqual(result['MSGFORMAT'],'ims1.0')
        self.assertEqual(result['MSGTYPE'],'request')
        self.assertEqual(result['MSGID'],'ex134')
        self.assertEqual(result['EMAIL'],'foo_bar.a.vb.bar@venus.com')
        
        # optional for this request
        self.assertTrue(result.has_key('SOURCE'))
       
        # product_1
        self.assertTrue(result.has_key('PRODUCT_1'))
        
        # validate that there is a sta_list and a subtype
        self.assertEqual(result['PRODUCT_1'], {'BULLTYPE': 'idc_sel1', 'STARTDATE': '1999/08/01', 'ENDDATE': '1999/09/01', 'SUBTYPE': 'automatic', 'FORMAT': 'ims1.0', 'TYPE': 'SLSD', 'STALIST': ['HIA', 'MJAR']})
     
     
    def ztest_slsd_associated_request(self):
        """ test with slsd:associated taken from AutoDRM help response message """
        
        message = "begin ims1.0\nmsg_type request\nmsg_id ex007 any_ndc\ne-mail guillaume.aubert@gmail.com\ntime 1999/06/01 to 1999/07/01\nsta_list ZAL\nbull_type idc_reb\narrival:associated ims2.0\nstop"
        
        parser = IMSParser()
        
        result = parser.parse(message)
        
        #print("\nresult = %s\n" %(result))
        
        # check mandatory fields
        self.assertEqual(result['MSGFORMAT'],'ims1.0')
        self.assertEqual(result['MSGTYPE'],'request')
        self.assertEqual(result['MSGID'],'ex007')
        self.assertEqual(result['EMAIL'],'guillaume.aubert@gmail.com')
        
        # optional for this request
        self.assertTrue(result.has_key('SOURCE'))
       
        # product_1
        self.assertTrue(result.has_key('PRODUCT_1'))
        
        # validate that there is a sta_list and a subtype
        self.assertEqual(result['PRODUCT_1'], {'STARTDATE': '1999/06/01', 'BULLTYPE': 'idc_reb', 'ENDDATE': '1999/07/01', 'SUBTYPE': 'associated', 'FORMAT': 'ims2.0', 'TYPE': 'ARRIVAL', 'STALIST': ['ZAL']})  
   
    def ztest_waveform_segment_and_bulletin_request(self):
        """ test with waveform_segment and bulletin taken from AutoDRM help response message """
        
        message = " begin ims1.0\nmsg_type request\nmsg_id ex002 any_ndc\ne-mail john.doo@ndc.gov.tr\ntime 1999/7/6 1:45 to 1999/7/6 2:00\nbull_type idc_reb\nbulletin ims1.0\nrelative_to bulletin\nwaveform ims2.0:cm6\nstop"
        
        parser = IMSParser()
        
        result = parser.parse(message)
        
        #print("\nresult = %s\n" %(result))
        
        # check mandatory fields
        self.assertEqual(result['MSGFORMAT'],'ims1.0')
        self.assertEqual(result['MSGTYPE'],'request')
        self.assertEqual(result['MSGID'],'ex002')
        self.assertEqual(result['EMAIL'],'john.doo@ndc.gov.tr')
        
        # optional for this request
        self.assertTrue(result.has_key('SOURCE'))
       
        # product_1
        self.assertTrue(result.has_key('PRODUCT_1'))
        
        # validate that there is a sta_list and a subtype
        self.assertEqual(result['PRODUCT_1'], {'STARTDATE': '1999/7/6 1:45', 'ENDDATE': '1999/7/6 2:00', 'FORMAT': 'ims1.0', 'RELATIVETO': 'bulletin', 'BULLTYPE': 'idc_reb', 'TYPE': 'BULLETIN'})
   
        # product_2
        self.assertTrue(result.has_key('PRODUCT_2'))
        
        # validate that there is a sta_list and a subtype
        self.assertEqual(result['PRODUCT_2'], {'STARTDATE': '1999/7/6 1:45', 'ENDDATE': '1999/7/6 2:00', 'FORMAT': 'ims2.0', 'RELATIVETO': 'bulletin', 'SUBFORMAT': 'cm6', 'BULLTYPE': 'idc_reb', 'TYPE': 'WAVEFORM'})
    
    def ztest_waveform_segment_request_1(self):
        """ test with waveform_segment taken from AutoDRM help response message """
        
        message = " begin ims1.0\nmsg_type request\nmsg_id ex002 any_ndc\ne-mail john.doo@ndc.gov.tr\ntime 1999/7/6 1:45 to 1999/7/6 2:00\nbull_type idc_reb\nrelative_to bulletin\nwaveform ims2.0:cm6\nstop"
        
        parser = IMSParser()
        
        result = parser.parse(message)
        
        #print("\nresult = %s\n" %(result))
        
        # check mandatory fields
        self.assertEqual(result['MSGFORMAT'],'ims1.0')
        self.assertEqual(result['MSGTYPE'],'request')
        self.assertEqual(result['MSGID'],'ex002')
        self.assertEqual(result['EMAIL'],'john.doo@ndc.gov.tr')
        
        # optional for this request
        self.assertTrue(result.has_key('SOURCE'))
       
        # product_1
        self.assertTrue(result.has_key('PRODUCT_1'))
        
        # validate that there is a sta_list and a subtype
        self.assertEqual(result['PRODUCT_1'], {'STARTDATE': '1999/7/6 1:45', 'ENDDATE': '1999/7/6 2:00', 'FORMAT': 'ims2.0', 'RELATIVETO': 'bulletin', 'SUBFORMAT': 'cm6', 'BULLTYPE': 'idc_reb', 'TYPE': 'WAVEFORM'})
     
    def ztest_waveform_segment_request_2(self):
        """ test with waveform_segment taken from AutoDRM help response message """
        
        message = "begin ims1.0\nmsg_type request\nmsg_id ex002 any_ndc\ne-mail john.doo@ndc.gov.tr\ntime 2000/1/9 1:00 to 2000/1/9 1:15\nsta_list CMAR,   PDAR\nwaveform ims1.0:int\nstop"
        
        parser = IMSParser()
        
        result = parser.parse(message)
        
        #print("\nresult = %s\n" %(result))
        
        # check mandatory fields
        self.assertEqual(result['MSGFORMAT'],'ims1.0')
        self.assertEqual(result['MSGTYPE'],'request')
        self.assertEqual(result['MSGID'],'ex002')
        self.assertEqual(result['EMAIL'],'john.doo@ndc.gov.tr')
        
        # optional for this request
        self.assertTrue(result.has_key('SOURCE'))
       
        # product_1
        self.assertTrue(result.has_key('PRODUCT_1'))
        
        # validate that there is a sta_list and a subtype
        self.assertEqual(result['PRODUCT_1'], {'STARTDATE': '2000/1/9 1:00', 'SUBFORMAT': 'int', 'ENDDATE': '2000/1/9 1:15', 'FORMAT': 'ims1.0', 'TYPE': 'WAVEFORM', 'STALIST': ['CMAR', 'PDAR']})
    
    def ztest_sta_status(self):
        """ test a sta_status request taken from the AutoDRM help response message """
        
        message = "begin ims1.0\nmsg_type request\nmsg_id ex029 any_ndc\ne-mail foo@bar.com\ntime 1999/07/01 0:01 to 1999/07/31 23:59\nsta_list ARCES\nsta_status gse2.0\nstop\n"
        
        parser = IMSParser()
        
        result = parser.parse(message)
        
        #print("\nresult = %s\n" %(result))
        
        # check mandatory fields
        self.assertEqual(result['MSGFORMAT'],'ims1.0')
        self.assertEqual(result['MSGTYPE'],'request')
        self.assertEqual(result['MSGID'],'ex029')
        self.assertEqual(result['EMAIL'],'foo@bar.com')
   
        # optional for this request
        self.assertTrue(result.has_key('SOURCE'))
        self.assertEqual(result['SOURCE'],'any_ndc')
   
        # product_1
        self.assertTrue(result.has_key('PRODUCT_1'))
        
        # validate that there is a sta_list and a subtype
        self.assertEqual(result['PRODUCT_1'], {'STARTDATE': '1999/07/01 0:01', 'FORMAT': 'gse2.0', 'ENDDATE': '1999/07/31 23:59', 'STALIST': ['ARCES'], 'TYPE': 'STASTATUS'})
    
    
    def ztest_chan_status(self):
        """ test a chan_status request taken from the AutoDRM help response message """
        
        message = "begin ims1.0\nmsg_type request\nmsg_id ex015 any_ndc\ne-mail guillaume.aubert@ctbto.org\ntime 1999/07/11 0:01 to 1999/07/11 23:59\nchan_status gse2.0\nstop"
        
        parser = IMSParser()
        
        result = parser.parse(message)
        
        #print("\nresult = %s\n" %(result))
        
        # check mandatory fields
        self.assertEqual(result['MSGFORMAT'],'ims1.0')
        self.assertEqual(result['MSGTYPE'],'request')
        self.assertEqual(result['MSGID'],'ex015')
        self.assertEqual(result['EMAIL'],'guillaume.aubert@ctbto.org')
   
        # optional for this request
        self.assertTrue(result.has_key('SOURCE'))
        self.assertEqual(result['SOURCE'],'any_ndc')
   
        # product_1
        self.assertTrue(result.has_key('PRODUCT_1'))
        
        # validate that there is a sta_list and a subtype
        self.assertEqual(result['PRODUCT_1'], {'STARTDATE': '1999/07/11 0:01', 'FORMAT': 'gse2.0', 'ENDDATE': '1999/07/11 23:59', 'TYPE': 'CHANSTATUS'})
    
    def ztest_calibphd(self):
        """ test a calibphd request taken from the AUTODRM Help response message """
        
        message = "begin ims1.0\nmsg_type request\nmsg_id ex013\ne-mail foo.bar@google.com\ntime 1999/01/01 to 2000/01/01\ncalibphd rms2.0\nstop"
        
        parser = IMSParser()
        
        result = parser.parse(message)
        
        # check mandatory fields
        self.assertEqual(result['MSGFORMAT'],'ims1.0')
        self.assertEqual(result['MSGTYPE'],'request')
        self.assertEqual(result['MSGID'],'ex013')
        self.assertEqual(result['EMAIL'],'foo.bar@google.com')
   
        # optional for this request
        self.assertFalse(result.has_key('SOURCE'))

        # product_1
        self.assertTrue(result.has_key('PRODUCT_1'))
        
        # validate that there is a sta_list and a subtype
        self.assertEqual(result['PRODUCT_1'], {'STARTDATE': '1999/01/01', 'FORMAT': 'rms2.0', 'ENDDATE': '2000/01/01', 'TYPE': 'CALIBPHD'})
    
    def ztest_calibphd_def_format(self):
        """ test a calibphd request without a message format taken from the AUTODRM Help response message """
        
        message = "begin ims1.0\nmsg_type request\nmsg_id ex013\ne-mail foo.bar@google.com\ntime 1999/01/01 to 2000/01/01\ncalibphd   \nstop"
        
        parser = IMSParser()
        
        result = parser.parse(message)
        
        # check mandatory fields
        self.assertEqual(result['MSGFORMAT'],'ims1.0')
        self.assertEqual(result['MSGTYPE'],'request')
        self.assertEqual(result['MSGID'],'ex013')
        self.assertEqual(result['EMAIL'],'foo.bar@google.com')
   
        # optional for this request
        self.assertFalse(result.has_key('SOURCE'))

        # product_1
        self.assertTrue(result.has_key('PRODUCT_1'))
        
        # validate that there is a sta_list and a subtype
        self.assertEqual(result['PRODUCT_1'], {'STARTDATE': '1999/01/01', 'ENDDATE': '2000/01/01', 'TYPE': 'CALIBPHD'})
        
    def ztest_2_sphd(self):
        """ test a sphd request without a message format taken from the AUTODRM Help response message """
        
        message = "begin ims1.0\nmsg_type request\nmsg_id ex026\ne-mail foo.bar@google.com\ntime 1999/07/01 to 2000/08/01\nsta_list AU*\nsphdf rms2.0\nsphdp rms2.0\nstop\n"
        
        parser = IMSParser()
        
        result = parser.parse(message)
        
        # check mandatory fields
        self.assertEqual(result['MSGFORMAT'],'ims1.0')
        self.assertEqual(result['MSGTYPE'],'request')
        self.assertEqual(result['MSGID'],'ex026')
        self.assertEqual(result['EMAIL'],'foo.bar@google.com')
   
        # optional for this request
        self.assertFalse(result.has_key('SOURCE'))

        # product_1
        self.assertTrue(result.has_key('PRODUCT_1'))
        
        # validate that there is a sta_list and a subtype
        self.assertEqual(result['PRODUCT_1'], {'STARTDATE': '1999/07/01', 'ENDDATE': '2000/08/01', 'FORMAT': 'rms2.0', 'TYPE': 'SPHDF', 'STALIST': ['AU*']})
        
        # product_1
        self.assertTrue(result.has_key('PRODUCT_2'))
        
        # validate that there is a sta_list and a subtype
        self.assertEqual(result['PRODUCT_2'], {'STARTDATE': '1999/07/01', 'ENDDATE': '2000/08/01', 'FORMAT': 'rms2.0', 'TYPE': 'SPHDP', 'STALIST': ['AU*']})
    
    def ztest_arr(self):
        """ test a arr request without a message format taken from the AUTODRM Help response message """
        
        message = "begin ims1.0\nmsg_type request\nmsg_id ex005\ne-mail foo.bar@bar.fr\ntime 1999/04/01 to 1999/05/01\nsta_list FI001,UK001\narr rms2.0\nstop"
        
        parser = IMSParser()
        
        result = parser.parse(message)
        
        # check mandatory fields
        self.assertEqual(result['MSGFORMAT'],'ims1.0')
        self.assertEqual(result['MSGTYPE'],'request')
        self.assertEqual(result['MSGID'],'ex005')
        self.assertEqual(result['EMAIL'],'foo.bar@bar.fr')
        
        # product_1
        self.assertTrue(result.has_key('PRODUCT_1'))
        
        # validate that there is a sta_list and a subtype
        self.assertEqual(result['PRODUCT_1'], {'STARTDATE': '1999/04/01', 'FORMAT': 'rms2.0', 'ENDDATE': '1999/05/01', 'STALIST': ['FI001', 'UK001'], 'TYPE': 'ARR'})
        
    def ztest_error_email_address(self):
        """ error with bad email address """
        
        message = "begin ims1.0\nmsg_type request\nmsg_id ex005\ne-mail foo.bar@to_to\ntime 1999/04/01 to 1999/05/01\nsta_list FI001,UK001\narr rms2.0\nstop"
        
        parser = IMSParser()
        
        try:
            parser.parse(message)
            self.fail("should launch an exception")
        except ParsingError, p_err:
            self.assertEqual(p_err.message,"Error[line=4,pos=7]: Next keyword should be an email address but instead was 'foo.bar@to_to' (keyword type ID).")
            self.assertEqual(p_err.suggestion,'The email address might be missing or is malformated')
        
    def ztest_error_bad_msg_type_keyword(self):
        """ error with bad msg_type keyword """
        
        message = "begin ims1.0\nmsg_tyype request\nmsg_id ex005\ne-mail foo.bar@to_to\ntime 1999/04/01 to 1999/05/01\nsta_list FI001,UK001\narr rms2.0\nstop"
        
        parser = IMSParser()
        
        try:
            parser.parse(message)
            self.fail("should launch an exception")
        except ParsingError, p_err:
            self.assertEqual(p_err.message,"Error[line=2,pos=0]: Next keyword should be a msg_type but instead was 'msg_tyype' (keyword type ID).")
        
        
    
    def ztest_error_no_stop(self):
        """ error missing stop """
        message = "begin ims1.0\nmsg_type request\nmsg_id ex005\ne-mail foo.bar@to.fr\ntime 1999/04/01 to 1999/05/01\nsta_list FI001,UK001\narr rms2.0\n"
        
        parser = IMSParser()
        
        try:
            parser.parse(message)
            self.fail("should launch an exception")
        except ParsingError, p_err:
            self.assertEqual(p_err.message,'Error[line=7,pos=EOF]: End of request reached without encountering a stop keyword.')
        
    def ztest_error_bad_datetime(self):
        """ error with bad datetime """
        message = "begin ims1.0\nmsg_type request\nmsg_id ex005\ne-mail foo.bar@to.com\ntime 1999/04/01/04 to 1999/05/01\nsta_list FI001,UK001\narr rms2.0\nstop"
        
        parser = IMSParser()
        
        try:
            parser.parse(message)
            self.fail("should launch an exception")
        except ParsingError, p_err:
            self.assertEqual(p_err.message,"Error[line=5,pos=15]: Next keyword should be a to but instead was '/04' (keyword type DATA).")
        
    def ztest_error_incomplete_format(self):
        """ error incomplete format """
        message = "begin ims1.0\nmsg_type request\nmsg_id ex005\ne-mail foo.bar@to.com\ntime 1999/04/01 to 1999/05/01\nsta_list FI001,UK001\narr rms2A\nstop"
        
        parser = IMSParser()
        
        try:
            parser.parse(message)
            self.fail("should launch an exception")
        except ParsingError, p_err:
            self.assertEqual(p_err.message,"Error[line=7,pos=4]: Next keyword should be a newline or a msg format (ex:ims2.0) but instead was 'rms2A' (keyword type ID).")
     
    def ztest_error_incomplete_subformat(self):
        """ error incomplete subformat """
        message = "begin ims1.0\nmsg_type request\nmsg_id ex005\ne-mail foo.bar@to.com\ntime 1999/04/01 to 1999/05/01\nsta_list FI001,UK001\narr rms2.00::kkkk\nstop"
        
        parser = IMSParser()
        
        try:
            parser.parse(message)
            self.fail("should launch an exception")
        except ParsingError, p_err:
            self.assertEqual(p_err.message,"Error[line=7,pos=12]: Next keyword should be a subformat value but instead was ':' (keyword type COLON).")
    
    def ztest_error_sta_list(self):
        """ error incomplete sta_list """
        message = "begin ims1.0\nmsg_type request\nmsg_id ex005\ne-mail foo.bar@to.com\ntime 1999/04/01 to 1999/05/01\nsta_list FI001+UK001\narr rms2.00\nstop"
        
        parser = IMSParser()
        
        try:
            parser.parse(message)
            self.fail("should launch an exception")
        except ParsingError, p_err:
            self.assertEqual(p_err.message,"Error[line=6,pos=9]: Next keyword should be a sta_list id but instead was 'FI001+UK001' (keyword type DATA).")
      
      
    def ztest_help(self):
        """ test a help """
        
        message = "BEGIN IMS1.0\nMSG_TYPE REQUEST\nMSG_ID xxx ga\ne-mail guillaume.aubert@ctbto.org\nHELP\nSTOP"
        
        parser = IMSParser()
        
        result = parser.parse(message)
        
        # check mandatory fields
        self.assertEqual(result['MSGFORMAT'],'ims1.0')
        self.assertEqual(result['MSGTYPE'],'request')
        self.assertEqual(result['MSGID'],'xxx')
        self.assertEqual(result['SOURCE'],'ga')
        
        self.assertEqual(result['EMAIL'],'guillaume.aubert@ctbto.org')
        
        # product_1
        self.assertTrue(result.has_key('PRODUCT_1'))
        
        # validate that there is a sta_list and a subtype
        self.assertEqual(result['PRODUCT_1'],{'TYPE': 'HELP'})
        
    
    def ztest_channel_list(self):
        """ test chan_list """
        
        message = "  BEGIN IMS1.0\nMSG_TYPE REQUEST\nMSG_ID 34372481 CTBT_IDC\nE-MAIL messages@dc.ctbto.org\nTIME 2009/05/11 05:20:16 TO 2009/05/11 05:27:00\nSTA_LIST GUMO\nCHAN_LIST BH*\nWAVEFORM IMS1.0:CM6\nSTOP"
        
        parser = IMSParser()
        
        result = parser.parse(message)
      
        # check mandatory fields
        self.assertEqual(result['MSGFORMAT'],'ims1.0')
        self.assertEqual(result['MSGTYPE'],'request')
        self.assertEqual(result['MSGID'],'34372481')
        self.assertEqual(result['SOURCE'],'CTBT_IDC')
        
        self.assertEqual(result['EMAIL'],'messages@dc.ctbto.org')
        
        # product_1
        self.assertTrue(result.has_key('PRODUCT_1'))
        
        # validate that there is a sta_list and a subtype
        self.assertEqual(result['PRODUCT_1'], {'STARTDATE': '2009/05/11 05:20:16', 'SUBFORMAT': 'CM6', 'ENDDATE': '2009/05/11 05:27:00', 'FORMAT': 'IMS1.0', 'CHANLIST': ['BH*'], 'TYPE': 'WAVEFORM', 'STALIST': ['GUMO']})
        
    def test_ref_part_1(self):
        """ test with ref_id part 1 """
        
        message = "  BEGIN IMS1.0\nMSG_TYPE REQUEST\nMSG_ID WS01-KURK186874 \nref_id 34370664 CTBT_IDC part 1\nE-MAIL messages@dc.ctbto.org\nTIME 2009/05/11 05:20:16 TO 2009/05/11 05:27:00\nSTA_LIST GUMO\nCHAN_LIST BH*\nWAVEFORM IMS1.0:CM6\nSTOP"
        
        parser = IMSParser()
        
        result = parser.parse(message)
        
        # check mandatory fields
        self.assertEqual(result['MSGFORMAT'],'ims1.0')
        self.assertEqual(result['MSGTYPE'],'request')
        self.assertEqual(result['MSGID'],'WS01-KURK186874')
        self.assertEqual(result['EMAIL'],'messages@dc.ctbto.org')
        
        self.assertEqual(result['REFID'],{'SEQNUM': '1', 'REFSRC': 'CTBT_IDC', 'REFSTR': '34370664'})
        
        # product_1
        self.assertTrue(result.has_key('PRODUCT_1'))
        
        # validate that there is a sta_list and a subtype
        self.assertEqual(result['PRODUCT_1'], {'STARTDATE': '2009/05/11 05:20:16', 'SUBFORMAT': 'CM6', 'ENDDATE': '2009/05/11 05:27:00', 'FORMAT': 'IMS1.0', 'CHANLIST': ['BH*'], 'TYPE': 'WAVEFORM', 'STALIST': ['GUMO']})
    
    def test_ref_part_2(self):
        """ test with ref_id part 2 of x """
        
        message = "  BEGIN IMS1.0\nMSG_TYPE REQUEST\nMSG_ID WS01-KURK186874 \nref_id 34370664 CTBT_IDC part 1 of 2\nE-MAIL messages@dc.ctbto.org\nTIME 2009/05/11 05:20:16 TO 2009/05/11 05:27:00\nSTA_LIST GUMO\nCHAN_LIST BH*\nWAVEFORM IMS1.0:CM6\nSTOP"
        
        parser = IMSParser()
        
        result = parser.parse(message)
        
        # check mandatory fields
        self.assertEqual(result['MSGFORMAT'],'ims1.0')
        self.assertEqual(result['MSGTYPE'],'request')
        self.assertEqual(result['MSGID'],'WS01-KURK186874')
        self.assertEqual(result['EMAIL'],'messages@dc.ctbto.org')
        
        self.assertEqual(result['REFID'],{'SEQNUM': '1', 'TOTNUM':'2', 'REFSRC': 'CTBT_IDC', 'REFSTR': '34370664'})
        
        # product_1
        self.assertTrue(result.has_key('PRODUCT_1'))
        
        # validate that there is a sta_list and a subtype
        self.assertEqual(result['PRODUCT_1'], {'STARTDATE': '2009/05/11 05:20:16', 'SUBFORMAT': 'CM6', 'ENDDATE': '2009/05/11 05:27:00', 'FORMAT': 'IMS1.0', 'CHANLIST': ['BH*'], 'TYPE': 'WAVEFORM', 'STALIST': ['GUMO']})
     
    def test_ref_part_3(self):
        """ test with ref_id without part """
        
        message = "  BEGIN IMS1.0\nMSG_TYPE REQUEST\nMSG_ID WS01-KURK186874 \nref_id 34370664\nE-MAIL messages@dc.ctbto.org\nTIME 2009/05/11 05:20:16 TO 2009/05/11 05:27:00\nSTA_LIST GUMO\nCHAN_LIST BH*\nWAVEFORM IMS1.0:CM6\nSTOP"
        
        parser = IMSParser()
        
        result = parser.parse(message)
        
        # check mandatory fields
        self.assertEqual(result['MSGFORMAT'],'ims1.0')
        self.assertEqual(result['MSGTYPE'],'request')
        self.assertEqual(result['MSGID'],'WS01-KURK186874')
        self.assertEqual(result['EMAIL'],'messages@dc.ctbto.org')
        
        self.assertEqual(result['REFID'],{'REFSTR': '34370664'})
        
        # product_1
        self.assertTrue(result.has_key('PRODUCT_1'))
        
        # validate that there is a sta_list and a subtype
        self.assertEqual(result['PRODUCT_1'], {'STARTDATE': '2009/05/11 05:20:16', 'SUBFORMAT': 'CM6', 'ENDDATE': '2009/05/11 05:27:00', 'FORMAT': 'IMS1.0', 'CHANLIST': ['BH*'], 'TYPE': 'WAVEFORM', 'STALIST': ['GUMO']})
               
        
    """ Add Errors:
        - (DONE) bad email address, 
        - (DONE) no stop,
        - (DONE) bad datetime values,
        - (DONE) multiple lines separator (shall we eat them)
        - (Done) incomplete format:subformat req, 
        - (Done) incomplete type:subtype format),
        - bad station list (ZA,),
        - missing essential elements,
        
    """
        
        
        