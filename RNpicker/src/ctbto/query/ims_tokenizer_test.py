'''
Created on May 16, 2009

@author: guillaume.aubert@ctbto.org
'''
import StringIO

from unittest import TestCase

from ims_tokenizer import IMSTokenizer, Token, IllegalCharacterError, BadTokenError, NonExistingTokenError, TokensNotFoundError, TokenCreator

class LexerTest(TestCase):
    """ LexerTest """
    
    def setUp(self):
        """ setUp method """
        pass
        
    def test_list_tokens_lower_case(self):
        """ test_list_tokens_lower_case """
        tokenizer = IMSTokenizer()
        
        io_prog = StringIO.StringIO("     begin IMS2.0     \nmsg_type data \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \ntime 2000/11/22 to 2001/01/01\nsta_list ARP01\nalert_temp\n    stop")
         
        tokenizer.set_io_prog(io_prog)
    
        cpt = 0
        for token in tokenizer:
            #print("\nToken = %s"%(token))
            
            if cpt == 0:
                # retrieve token
                self.assertEqual(token.type,'BEGIN')
                self.assertEqual(token.value,'begin')
            elif cpt == 1:
                self.assertEqual(token.type,'MSGFORMAT')
                self.assertEqual(token.value,'IMS2.0')
            elif cpt == 2:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value, '\n')
            elif cpt == 3:
                self.assertEqual(token.type,'MSGTYPE')
                self.assertEqual(token.value, 'msg_type')
            elif cpt == 4:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'data')
            elif cpt == 5:
                self.assertEqual(token.type, Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 6:
                self.assertEqual(token.type,'MSGID')
                self.assertEqual(token.value, 'msg_id')
            elif cpt == 7:
                self.assertEqual(token.type,'NUMBER')
                self.assertEqual(token.value,'54695')
            elif cpt == 8:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'ctbto_idc')
            elif cpt == 9:
                self.assertEqual(token.type, Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 10:
                self.assertEqual(token.type,'EMAIL')
                self.assertEqual(token.value,'e-mail')
            elif cpt == 11:
                self.assertEqual(token.type,'EMAILADDR')
                self.assertEqual(token.value,'guillaume.aubert@ctbto.org')
            elif cpt == 12:
                self.assertEqual(token.type, Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 13:
                self.assertEqual(token.type,'TIME')
                self.assertEqual(token.value,'time')
            elif cpt == 14:
                self.assertEqual(token.type,'DATETIME')
                self.assertEqual(token.value,'2000/11/22')
            elif cpt == 15:
                self.assertEqual(token.type,'TO')
                self.assertEqual(token.value,'to')
            elif cpt == 16:
                self.assertEqual(token.type,'DATETIME')
                self.assertEqual(token.value,'2001/01/01')
            elif cpt == 17:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 18:
                self.assertEqual(token.type,'STALIST')
                self.assertEqual(token.value,'sta_list')
            elif cpt == 19:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'ARP01')
            elif cpt == 20:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 21:
                self.assertEqual(token.type,'ALERTTEMP')
                self.assertEqual(token.value,'alert_temp')
            elif cpt == 22:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 23:
                self.assertEqual(token.type,'STOP')
                self.assertEqual(token.value,'stop')
            elif cpt == 24:
                self.assertEqual(token.type,Token.ENDMARKER)
                self.assertEqual(token.value,None)
    
            cpt+=1
    
    def test_generate_exception(self):
        
        tokenizer = IMSTokenizer()
        
        io_prog = StringIO.StringIO("     begin IMS2;###$0   llllll  \nmsg_type data \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \ntime 2000/11/22 to 2001/01/01\nsta_list ARP01\nalert_temp\n    stop")
         
        tokenizer.set_io_prog(io_prog)
    
        try:
            cpt = 0
            for token in tokenizer:
                #print("\nToken = %s"%(token))
            
                if cpt == 0:
                    # retrieve token
                    self.assertEqual(token.type,'BEGIN')
                    self.assertEqual(token.value,'begin')
                elif cpt == 1:
                    self.assertEqual(token.type,'ID')
                    self.assertEqual(token.value,'IMS2')
                cpt +=1
            
            fail("No LexerError Exception raised")
        except IllegalCharacterError, le:
            self.assertEqual(le.line,"     begin IMS2;###$0   llllll  \n")
            self.assertEqual(le.pos,15)
            self.assertEqual(le.line_num,1)
            
   
    def test_help_message(self):
        
        tokenizer = IMSTokenizer()
        
        io_prog = StringIO.StringIO("begin IMS2.0     \nmsg_type request \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \nhelp\nstop")
         
        tokenizer.set_io_prog(io_prog)
    
        cpt = 0
        for token in tokenizer:
            #print("\nToken = %s"%(token))
            
            if cpt == 0:
                # retrieve token
                self.assertEqual(token.type,'BEGIN')
                self.assertEqual(token.value,'begin')
            elif cpt == 1:
                self.assertEqual(token.type,'MSGFORMAT')
                self.assertEqual(token.value,'IMS2.0')
            elif cpt == 2:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 3:
                self.assertEqual(token.type,'MSGTYPE')
                self.assertEqual(token.value,'msg_type')
            elif cpt == 4:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'request')
            elif cpt == 5:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 6:
                self.assertEqual(token.type,'MSGID')
                self.assertEqual(token.value,'msg_id')
            elif cpt == 7:
                self.assertEqual(token.type,'NUMBER')
                self.assertEqual(token.value,'54695')
            elif cpt == 8:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'ctbto_idc')
            elif cpt == 9:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 10:
                self.assertEqual(token.type,'EMAIL')
                self.assertEqual(token.value,'e-mail')
            elif cpt == 11:
                self.assertEqual(token.type,'EMAILADDR')
                self.assertEqual(token.value,'guillaume.aubert@ctbto.org')
            elif cpt == 12:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 13:
                self.assertEqual(token.type,'HELP')
                self.assertEqual(token.value,'help')
            elif cpt == 14:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 15:
                self.assertEqual(token.type,'STOP')
                self.assertEqual(token.value,'stop')
            elif cpt == 16:
                self.assertEqual(token.type,Token.ENDMARKER)
                self.assertEqual(token.value,None)
            
            cpt+=1
    
    def test_time_1(self):
        ''' test with an advance time part '''

        tokenizer = IMSTokenizer()
        
        io_prog = StringIO.StringIO("     begin IMS2.0     \nmsg_type data \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \ntime 1999/02/01 23:14:19.7 to 1999/02/01 23:29:19.76\nsta_list ABC,DEF, FGH  \nalert_temp\n    stop")
         
        tokenizer.set_io_prog(io_prog)
    
        cpt = 0
        for token in tokenizer:
            #print("\nToken = %s"%(token))
            
            if cpt == 0:
                # retrieve token
                self.assertEqual(token.type,'BEGIN')
                self.assertEqual(token.value,'begin')
            elif cpt == 1:
                self.assertEqual(token.type,'MSGFORMAT')
                self.assertEqual(token.value,'IMS2.0')
            elif cpt == 2:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 3:
                self.assertEqual(token.type,'MSGTYPE')
                self.assertEqual(token.value,'msg_type')
            elif cpt == 4:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'data')
            elif cpt == 5:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 6:
                self.assertEqual(token.type,'MSGID')
                self.assertEqual(token.value,'msg_id')
            elif cpt == 7:
                self.assertEqual(token.type,'NUMBER')
                self.assertEqual(token.value,'54695')
            elif cpt == 8:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'ctbto_idc')
            elif cpt == 9:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 10:
                self.assertEqual(token.type,'EMAIL')
                self.assertEqual(token.value,'e-mail')
            elif cpt == 11:
                self.assertEqual(token.type,'EMAILADDR')
                self.assertEqual(token.value,'guillaume.aubert@ctbto.org')
            elif cpt == 12:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 13:
                self.assertEqual(token.type,'TIME')
                self.assertEqual(token.value,'time')
            elif cpt == 14:
                self.assertEqual(token.type,'DATETIME')
                self.assertEqual(token.value,'1999/02/01 23:14:19.7')
            elif cpt == 15:
                self.assertEqual(token.type,'TO')
                self.assertEqual(token.value,'to')
            elif cpt == 16:
                self.assertEqual(token.type,'DATETIME')
                self.assertEqual(token.value,'1999/02/01 23:29:19.76')
            elif cpt == 17:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 18:
                self.assertEqual(token.type,'STALIST')
                self.assertEqual(token.value,'sta_list')
            elif cpt == 19:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'ABC')
            elif cpt == 20:
                self.assertEqual(token.type,'COMMA')
                self.assertEqual(token.value,',')
            elif cpt == 21:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'DEF')
            elif cpt == 22:
                self.assertEqual(token.type,'COMMA')
                self.assertEqual(token.value,',')
            elif cpt == 23:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'FGH')
            elif cpt == 24:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 25:
                self.assertEqual(token.type,'ALERTTEMP')
                self.assertEqual(token.value,'alert_temp')
            elif cpt == 26:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 27:
                self.assertEqual(token.type,'STOP')
                self.assertEqual(token.value,'stop')
            elif cpt == 28:
                self.assertEqual(token.type,Token.ENDMARKER)
                self.assertEqual(token.value,None)
            
            cpt += 1
    
    def test_time_2(self):
        ''' test time extreme cases '''
        tokenizer = IMSTokenizer()
        
        io_prog = StringIO.StringIO("     begin IMS2.0     \nmsg_type data \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \ntime 1999/02/01 23:1:1.7 to 1999/2/1 2:29:19.76\nsta_list ABC,DEF, FGH  \nalert_temp\n    stop")
         
        tokenizer.set_io_prog(io_prog)
    
        cpt = 0
        for token in tokenizer:
            #print("\nToken = %s"%(token))
            
            if cpt == 0:
                # retrieve token
                self.assertEqual(token.type,'BEGIN')
                self.assertEqual(token.value,'begin')
            elif cpt == 1:
                self.assertEqual(token.type,'MSGFORMAT')
                self.assertEqual(token.value,'IMS2.0')
            elif cpt == 2:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 3:
                self.assertEqual(token.type,'MSGTYPE')
                self.assertEqual(token.value,'msg_type')
            elif cpt == 4:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'data')
            elif cpt == 5:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 6:
                self.assertEqual(token.type,'MSGID')
                self.assertEqual(token.value,'msg_id')
            elif cpt == 7:
                self.assertEqual(token.type,'NUMBER')
                self.assertEqual(token.value,'54695')
            elif cpt == 8:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'ctbto_idc')
            elif cpt == 9:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 10:
                self.assertEqual(token.type,'EMAIL')
                self.assertEqual(token.value,'e-mail')
            elif cpt == 11:
                self.assertEqual(token.type,'EMAILADDR')
                self.assertEqual(token.value,'guillaume.aubert@ctbto.org')
            elif cpt == 12:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 13:
                self.assertEqual(token.type,'TIME')
                self.assertEqual(token.value,'time')
            elif cpt == 14:
                self.assertEqual(token.type,'DATETIME')
                self.assertEqual(token.value,'1999/02/01 23:1:1.7')
            elif cpt == 15:
                self.assertEqual(token.type,'TO')
                self.assertEqual(token.value,'to')
            elif cpt == 16:
                self.assertEqual(token.type,'DATETIME')
                self.assertEqual(token.value,'1999/2/1 2:29:19.76')
            elif cpt == 17:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 18:
                self.assertEqual(token.type,'STALIST')
                self.assertEqual(token.value,'sta_list')
            elif cpt == 19:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'ABC')
            elif cpt == 20:
                self.assertEqual(token.type,'COMMA')
                self.assertEqual(token.value,',')
            elif cpt == 21:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'DEF')
            elif cpt == 22:
                self.assertEqual(token.type,'COMMA')
                self.assertEqual(token.value,',')
            elif cpt == 23:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'FGH')
            elif cpt == 24:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 25:
                self.assertEqual(token.type,'ALERTTEMP')
                self.assertEqual(token.value,'alert_temp')
            elif cpt == 26:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 27:
                self.assertEqual(token.type,'STOP')
                self.assertEqual(token.value,'stop')
            elif cpt == 28:
                self.assertEqual(token.type,Token.ENDMARKER)
                self.assertEqual(token.value,None)
            
            cpt += 1
    
    def test_time_3(self):
        ''' test time with 0 '''
        tokenizer = IMSTokenizer()
        
        io_prog = StringIO.StringIO("     begin IMS2.0     \nmsg_type data \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \ntime 1999/02/01 0:0:1.7 to 1999/2/1 2:0:19.76\nsta_list ABC,DEF, FGH  \nalert_temp\n    stop")
         
        tokenizer.set_io_prog(io_prog)
    
        cpt = 0
        for token in tokenizer:
            #print("\nToken = %s"%(token))
            
            if cpt == 0:
                # retrieve token
                self.assertEqual(token.type,'BEGIN')
                self.assertEqual(token.value,'begin')
            elif cpt == 1:
                self.assertEqual(token.type,'MSGFORMAT')
                self.assertEqual(token.value,'IMS2.0')
            elif cpt == 2:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 3:
                self.assertEqual(token.type,'MSGTYPE')
                self.assertEqual(token.value,'msg_type')
            elif cpt == 4:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'data')
            elif cpt == 5:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 6:
                self.assertEqual(token.type,'MSGID')
                self.assertEqual(token.value,'msg_id')
            elif cpt == 7:
                self.assertEqual(token.type,'NUMBER')
                self.assertEqual(token.value,'54695')
            elif cpt == 8:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'ctbto_idc')
            elif cpt == 9:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 10:
                self.assertEqual(token.type,'EMAIL')
                self.assertEqual(token.value,'e-mail')
            elif cpt == 11:
                self.assertEqual(token.type,'EMAILADDR')
                self.assertEqual(token.value,'guillaume.aubert@ctbto.org')
            elif cpt == 12:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 13:
                self.assertEqual(token.type,'TIME')
                self.assertEqual(token.value,'time')
            elif cpt == 14:
                self.assertEqual(token.type,'DATETIME')
                self.assertEqual(token.value,'1999/02/01 0:0:1.7')
            elif cpt == 15:
                self.assertEqual(token.type,'TO')
                self.assertEqual(token.value,'to')
            elif cpt == 16:
                self.assertEqual(token.type,'DATETIME')
                self.assertEqual(token.value,'1999/2/1 2:0:19.76')
            elif cpt == 17:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 18:
                self.assertEqual(token.type,'STALIST')
                self.assertEqual(token.value,'sta_list')
            elif cpt == 19:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'ABC')
            elif cpt == 20:
                self.assertEqual(token.type,'COMMA')
                self.assertEqual(token.value,',')
            elif cpt == 21:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'DEF')
            elif cpt == 22:
                self.assertEqual(token.type,'COMMA')
                self.assertEqual(token.value,',')
            elif cpt == 23:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'FGH')
            elif cpt == 24:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 25:
                self.assertEqual(token.type,'ALERTTEMP')
                self.assertEqual(token.value,'alert_temp')
            elif cpt == 26:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 27:
                self.assertEqual(token.type,'STOP')
                self.assertEqual(token.value,'stop')
            elif cpt == 28:
                self.assertEqual(token.type,Token.ENDMARKER)
                self.assertEqual(token.value,None)
            
            cpt += 1
    
    def test_station_list(self):
        ''' test with a station list'''
        tokenizer = IMSTokenizer()
        
        io_prog = StringIO.StringIO("     begin IMS2.0     \nmsg_type data \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \ntime 2000/11/22 to 2001/01/01\nsta_list ABC,DEF, FGH  \nalert_temp\n    stop")
         
        tokenizer.set_io_prog(io_prog)
    
        cpt = 0
        for token in tokenizer:
            #print("\nToken = %s"%(token))
            
            if cpt == 0:
                # retrieve token
                self.assertEqual(token.type,'BEGIN')
                self.assertEqual(token.value,'begin')
            elif cpt == 1:
                self.assertEqual(token.type,'MSGFORMAT')
                self.assertEqual(token.value,'IMS2.0')
            elif cpt == 2:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 3:
                self.assertEqual(token.type,'MSGTYPE')
                self.assertEqual(token.value,'msg_type')
            elif cpt == 4:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'data')
            elif cpt == 5:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 6:
                self.assertEqual(token.type,'MSGID')
                self.assertEqual(token.value,'msg_id')
            elif cpt == 7:
                self.assertEqual(token.type,'NUMBER')
                self.assertEqual(token.value,'54695')
            elif cpt == 8:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'ctbto_idc')
            elif cpt == 9:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 10:
                self.assertEqual(token.type,'EMAIL')
                self.assertEqual(token.value,'e-mail')
            elif cpt == 11:
                self.assertEqual(token.type,'EMAILADDR')
                self.assertEqual(token.value,'guillaume.aubert@ctbto.org')
            elif cpt == 12:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 13:
                self.assertEqual(token.type,'TIME')
                self.assertEqual(token.value,'time')
            elif cpt == 14:
                self.assertEqual(token.type,'DATETIME')
                self.assertEqual(token.value,'2000/11/22')
            elif cpt == 15:
                self.assertEqual(token.type,'TO')
                self.assertEqual(token.value,'to')
            elif cpt == 16:
                self.assertEqual(token.type,'DATETIME')
                self.assertEqual(token.value,'2001/01/01')
            elif cpt == 17:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 18:
                self.assertEqual(token.type,'STALIST')
                self.assertEqual(token.value,'sta_list')
            elif cpt == 19:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'ABC')
            elif cpt == 20:
                self.assertEqual(token.type,'COMMA')
                self.assertEqual(token.value,',')
            elif cpt == 21:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'DEF')
            elif cpt == 22:
                self.assertEqual(token.type,'COMMA')
                self.assertEqual(token.value,',')
            elif cpt == 23:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'FGH')
            elif cpt == 24:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 25:
                self.assertEqual(token.type,'ALERTTEMP')
                self.assertEqual(token.value,'alert_temp')
            elif cpt == 26:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 27:
                self.assertEqual(token.type,'STOP')
                self.assertEqual(token.value,'stop')
            elif cpt == 28:
                self.assertEqual(token.type,Token.ENDMARKER)
                self.assertEqual(token.value,None)
    
            cpt+=1

    def test_lat_lon(self):
        ''' lat-lon test '''
        
        tokenizer = IMSTokenizer()
        
        io_prog = StringIO.StringIO("     begin IMS2.0     \nmsg_type data \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \ntime 2000/11/22 to 2001/01/01\nlat -12 to 17\nlon 44 to 66\nalert_temp\n    stop")
         
        tokenizer.set_io_prog(io_prog)
    
        cpt = 0
        for token in tokenizer:
            #print("\nToken = %s"%(token))
            
            if cpt == 0:
                # retrieve token
                self.assertEqual(token.type,'BEGIN')
                self.assertEqual(token.value,'begin')
            elif cpt == 1:
                self.assertEqual(token.type,'MSGFORMAT')
                self.assertEqual(token.value,'IMS2.0')
            elif cpt == 2:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 3:
                self.assertEqual(token.type,'MSGTYPE')
                self.assertEqual(token.value,'msg_type')
            elif cpt == 4:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'data')
            elif cpt == 5:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 6:
                self.assertEqual(token.type,'MSGID')
                self.assertEqual(token.value,'msg_id')
            elif cpt == 7:
                self.assertEqual(token.type,'NUMBER')
                self.assertEqual(token.value,'54695')
            elif cpt == 8:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'ctbto_idc')
            elif cpt == 9:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 10:
                self.assertEqual(token.type,'EMAIL')
                self.assertEqual(token.value,'e-mail')
            elif cpt == 11:
                self.assertEqual(token.type,'EMAILADDR')
                self.assertEqual(token.value,'guillaume.aubert@ctbto.org')
            elif cpt == 12:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 13:
                self.assertEqual(token.type,'TIME')
                self.assertEqual(token.value,'time')
            elif cpt == 14:
                self.assertEqual(token.type,'DATETIME')
                self.assertEqual(token.value,'2000/11/22')
            elif cpt == 15:
                self.assertEqual(token.type,'TO')
                self.assertEqual(token.value,'to')
            elif cpt == 16:
                self.assertEqual(token.type,'DATETIME')
                self.assertEqual(token.value,'2001/01/01')
            elif cpt == 17:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 18:
                self.assertEqual(token.type,'LAT')
                self.assertEqual(token.value,'lat')
            elif cpt == 19:
                self.assertEqual(token.type,'MINUS')
                self.assertEqual(token.value,'-')
            elif cpt == 20:
                self.assertEqual(token.type,'NUMBER')
                self.assertEqual(token.value,'12')
            elif cpt == 21:
                self.assertEqual(token.type,'TO')
                self.assertEqual(token.value,'to')
            elif cpt == 22:
                self.assertEqual(token.type,'NUMBER')
                self.assertEqual(token.value,'17')
            elif cpt == 23:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 24:
                self.assertEqual(token.type,'LON')
                self.assertEqual(token.value,'lon')
            elif cpt == 25:
                self.assertEqual(token.type,'NUMBER')
                self.assertEqual(token.value,'44')
            elif cpt == 26:
                self.assertEqual(token.type,'TO')
                self.assertEqual(token.value,'to')
            elif cpt == 27:
                self.assertEqual(token.type,'NUMBER')
                self.assertEqual(token.value,'66')
            elif cpt == 28:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 29:
                self.assertEqual(token.type,'ALERTTEMP')
                self.assertEqual(token.value,'alert_temp')
            elif cpt == 30:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 31:
                self.assertEqual(token.type,'STOP')
                self.assertEqual(token.value,'stop')

    
            cpt+=1
    
    def test_star_expansion(self):
        ''' test with expansion star'''                                                                                                           
        tokenizer = IMSTokenizer()
        
        io_prog = StringIO.StringIO("     begin IMS2.0     \nmsg_type data \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \ntime 2000/11/22 to 2000/11/23\nsta_list *BC,A*T,AD*  \nalert_temp\n    stop")
         
        tokenizer.set_io_prog(io_prog)
    
        cpt = 0
        for token in tokenizer:
            #print("\nToken = %s"%(token))
            
            if cpt == 0:
                # retrieve token
                self.assertEqual(token.type,'BEGIN')
                self.assertEqual(token.value,'begin')
            elif cpt == 1:
                self.assertEqual(token.type,'MSGFORMAT')
                self.assertEqual(token.value,'IMS2.0')
            elif cpt == 2:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 3:
                self.assertEqual(token.type,'MSGTYPE')
                self.assertEqual(token.value,'msg_type')
            elif cpt == 4:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'data')
            elif cpt == 5:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 6:
                self.assertEqual(token.type,'MSGID')
                self.assertEqual(token.value,'msg_id')
            elif cpt == 7:
                self.assertEqual(token.type,'NUMBER')
                self.assertEqual(token.value,'54695')
            elif cpt == 8:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'ctbto_idc')
            elif cpt == 9:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 10:
                self.assertEqual(token.type,'EMAIL')
                self.assertEqual(token.value,'e-mail')
            elif cpt == 11:
                self.assertEqual(token.type,'EMAILADDR')
                self.assertEqual(token.value,'guillaume.aubert@ctbto.org')
            elif cpt == 12:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 13:
                self.assertEqual(token.type,'TIME')
                self.assertEqual(token.value,'time')
            elif cpt == 14:
                self.assertEqual(token.type,'DATETIME')
                self.assertEqual(token.value,'2000/11/22')
            elif cpt == 15:
                self.assertEqual(token.type,'TO')
                self.assertEqual(token.value,'to')
            elif cpt == 16:
                self.assertEqual(token.type,'DATETIME')
                self.assertEqual(token.value,'2000/11/23')
            elif cpt == 17:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 18:
                self.assertEqual(token.type,'STALIST')
                self.assertEqual(token.value,'sta_list')
            elif cpt == 19:
                self.assertEqual(token.type,'WCID')
                self.assertEqual(token.value,'*BC')
            elif cpt == 20:
                self.assertEqual(token.type,'COMMA')
                self.assertEqual(token.value,',')
            elif cpt == 21:
                self.assertEqual(token.type,'WCID')
                self.assertEqual(token.value,'A*T')
            elif cpt == 22:
                self.assertEqual(token.type,'COMMA')
                self.assertEqual(token.value,',')
            elif cpt == 23:
                self.assertEqual(token.type,'WCID')
                self.assertEqual(token.value,'AD*')
            elif cpt == 24:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 25:
                self.assertEqual(token.type,'ALERTTEMP')
                self.assertEqual(token.value,'alert_temp')
            elif cpt == 26:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 27:
                self.assertEqual(token.type,'STOP')
                self.assertEqual(token.value,'stop')
            elif cpt == 28:
                self.assertEqual(token.type,Token.ENDMARKER)
                self.assertEqual(token.value,None)
    
            cpt+=1
            
    def test_data_token(self):
        ''' test if data token is properly matched'''                                                                                                           
        tokenizer = IMSTokenizer()
        
        io_prog = StringIO.StringIO("     begin IMS2.0     \nmsg_type data \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \ntime 2000/11/22 to 2000/11/23\nsta_list *BC,A*T,AD*  \nDATA_TYPE WAVEFORM IMS1.0:cm6\nktNf8WlSrl-ujDUvl3Yc5px0ypClUV9Vmq5UtiRlnZ1yV6Zt7Vdy8hw7mWoR\neeBVUhJasEZmJmUVFlgLWst4sYHmVk8wnGVgp8VUZ3ldXPws5axBUlyAklU9\n    stop")
         
        tokenizer.set_io_prog(io_prog)
    
        cpt = 0
        for token in tokenizer:
            #print("\nToken = %s"%(token))
            
            if cpt == 0:
                # retrieve token
                self.assertEqual(token.type,'BEGIN')
                self.assertEqual(token.value,'begin')
            elif cpt == 1:
                self.assertEqual(token.type,'MSGFORMAT')
                self.assertEqual(token.value,'IMS2.0')
            elif cpt == 2:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 3:
                self.assertEqual(token.type,'MSGTYPE')
                self.assertEqual(token.value,'msg_type')
            elif cpt == 4:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'data')
            elif cpt == 5:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 6:
                self.assertEqual(token.type,'MSGID')
                self.assertEqual(token.value,'msg_id')
            elif cpt == 7:
                self.assertEqual(token.type,'NUMBER')
                self.assertEqual(token.value,'54695')
            elif cpt == 8:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'ctbto_idc')
            elif cpt == 9:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 10:
                self.assertEqual(token.type,'EMAIL')
                self.assertEqual(token.value,'e-mail')
            elif cpt == 11:
                self.assertEqual(token.type,'EMAILADDR')
                self.assertEqual(token.value,'guillaume.aubert@ctbto.org')
            elif cpt == 12:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 13:
                self.assertEqual(token.type,'TIME')
                self.assertEqual(token.value,'time')
            elif cpt == 14:
                self.assertEqual(token.type,'DATETIME')
                self.assertEqual(token.value,'2000/11/22')
            elif cpt == 15:
                self.assertEqual(token.type,'TO')
                self.assertEqual(token.value,'to')
            elif cpt == 16:
                self.assertEqual(token.type,'DATETIME')
                self.assertEqual(token.value,'2000/11/23')
            elif cpt == 17:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 18:
                self.assertEqual(token.type,'STALIST')
                self.assertEqual(token.value,'sta_list')
            elif cpt == 19:
                self.assertEqual(token.type,'WCID')
                self.assertEqual(token.value,'*BC')
            elif cpt == 20:
                self.assertEqual(token.type,'COMMA')
                self.assertEqual(token.value,',')
            elif cpt == 21:
                self.assertEqual(token.type,'WCID')
                self.assertEqual(token.value,'A*T')
            elif cpt == 22:
                self.assertEqual(token.type,'COMMA')
                self.assertEqual(token.value,',')
            elif cpt == 23:
                self.assertEqual(token.type,'WCID')
                self.assertEqual(token.value,'AD*')
            elif cpt == 24:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 25:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'DATA_TYPE')
            elif cpt == 26:
                self.assertEqual(token.type,'WAVEFORM')
                self.assertEqual(token.value,'WAVEFORM')
            elif cpt == 27:
                self.assertEqual(token.type,'MSGFORMAT')
                self.assertEqual(token.value,'IMS1.0')
            elif cpt == 28:
                self.assertEqual(token.type,'COLON')
                self.assertEqual(token.value,':')
            elif cpt == 29:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'cm6')
            elif cpt == 30:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 31:
                self.assertEqual(token.type,'DATA')
                self.assertEqual(token.value,'ktNf8WlSrl-ujDUvl3Yc5px0ypClUV9Vmq5UtiRlnZ1yV6Zt7Vdy8hw7mWoR')
            elif cpt == 32:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 33:
                self.assertEqual(token.type,'DATA')
                self.assertEqual(token.value,'eeBVUhJasEZmJmUVFlgLWst4sYHmVk8wnGVgp8VUZ3ldXPws5axBUlyAklU9')
            elif cpt == 34:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 35:
                self.assertEqual(token.type,'STOP')
                self.assertEqual(token.value,'stop')
            elif cpt == 36:
                self.assertEqual(token.type,Token.ENDMARKER)
                self.assertEqual(token.value,None)
    
            cpt+=1
            
    def test_advance_in_message(self):
        ''' test if data token is properly matched'''  
        
        tokenizer = IMSTokenizer()
        
        str = "     begin IMS2.0     \nmsg_type data \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \ntime 2000/11/22 to 2000/11/23\nsta_list ABC,DEF,FGH  \n    alert_temp\n    stop"
        
        io_prog = StringIO.StringIO(str)
         
        tokenizer.set_io_prog(io_prog)
    
        cpt = 0
        for token in tokenizer:
            #print("\nToken = %s"%(token))
            
            if cpt == 0:
                # retrieve token
                self.assertEqual(token.type,'BEGIN')
                self.assertEqual(token.value,'begin')
            elif cpt == 1:
                self.assertEqual(token.type,'MSGFORMAT')
                self.assertEqual(token.value,'IMS2.0')
            elif cpt == 2:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 3:
                self.assertEqual(token.type,'MSGTYPE')
                self.assertEqual(token.value,'msg_type')
            elif cpt == 4:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'data')
            elif cpt == 5:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
                # break loop now
                break  
            cpt+=1
        
        #advance until the next found token 
        tokenizer.advance_until([Token.STALIST])
        
        cpt = 0
        for token in tokenizer:
            if cpt == 0:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'ABC')
            elif cpt == 1:
                self.assertEqual(token.type,'COMMA')
                self.assertEqual(token.value,',')
            elif cpt == 2:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'DEF')
            elif cpt == 3:
                self.assertEqual(token.type,'COMMA')
                self.assertEqual(token.value,',')
            elif cpt == 4:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'FGH')
            elif cpt == 5:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 6:
                self.assertEqual(token.type,'ALERTTEMP')
                self.assertEqual(token.value,'alert_temp')
            elif cpt == 7:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 8:
                self.assertEqual(token.type,'STOP')
                self.assertEqual(token.value,'stop')
            elif cpt == 9:
                self.assertEqual(token.type,Token.ENDMARKER)
                self.assertEqual(token.value,None)
    
            cpt+=1
        
        # continue to read token one by one from there
        
    def test_advance_in_message_and_error(self):
        ''' use advance_until but do not find the token and exit in exception '''
        
        try:
            
            tokenizer = IMSTokenizer()
        
            str = "     begin IMS2.0     \nmsg_type data \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \ntime 2000/11/22 to 2000/11/23\nchan_list ABC,DEF,FGH  \n    alert_temp\n    stop"
        
            io_prog = StringIO.StringIO(str)
         
            tokenizer.set_io_prog(io_prog)
            
            tok = tokenizer.advance_until(['STALIST'])
            print("tok = %s\n"%(tok))
        
        except  TokensNotFoundError, e:
            self.assertEqual(e.message,'Could not find any of the following tokens [\'STALIST\']')
    
    def test_advance_in_message_non_existing_token_error(self):
        ''' use of advance_until. raise NonExistingTokenError  '''
        
        try:
            
            tokenizer = IMSTokenizer()
        
            str = "     begin IMS2.0     \nmsg_type data \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \ntime 2000/11/22 to 2000/11/23\nchan_list ABC,DEF,FGH  \n    alert_temp\n    stop"
        
            io_prog = StringIO.StringIO(str)
         
            tokenizer.set_io_prog(io_prog)
            
            #look for a wrong token name
            tok = tokenizer.advance_until(['STALISTA'])
            print("tok = %s\n"%(tok))
        
        except  NonExistingTokenError, e:
            self.assertEqual(e.message,'The token named STALISTA doesn\'t exist')
    
    def test_get_current_token(self):
        
        tokenizer = IMSTokenizer()
        
        io_prog = StringIO.StringIO("begin IMS2.0     \nmsg_type request \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \nhelp\nstop")
         
        tokenizer.set_io_prog(io_prog)
    
        cpt = 0
        for token in tokenizer:
            #print("\nToken = %s"%(token))
            
            if cpt == 0:
                # retrieve token
                self.assertEqual(token.type,'BEGIN')
                self.assertEqual(token.value,'begin')                
            elif cpt == 1:
                self.assertEqual(token.type,'MSGFORMAT')
                self.assertEqual(token.value,'IMS2.0')
            elif cpt == 2:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 3:
                self.assertEqual(token.type,'MSGTYPE')
                self.assertEqual(token.value,'msg_type')
            elif cpt == 4:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'request')
            elif cpt == 5:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 6:
                self.assertEqual(token.type,'MSGID')
                self.assertEqual(token.value,'msg_id')
            elif cpt == 7:
                self.assertEqual(token.type,'NUMBER')
                self.assertEqual(token.value,'54695')
            elif cpt == 8:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'ctbto_idc')
            elif cpt == 9:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 10:
                self.assertEqual(token.type,'EMAIL')
                self.assertEqual(token.value,'e-mail')
            elif cpt == 11:
                self.assertEqual(token.type,'EMAILADDR')
                self.assertEqual(token.value,'guillaume.aubert@ctbto.org')
            elif cpt == 12:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 13:
                self.assertEqual(token.type,'HELP')
                self.assertEqual(token.value,'help')
            elif cpt == 14:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 15:
                self.assertEqual(token.type,'STOP')
                self.assertEqual(token.value,'stop')
            elif cpt == 16:
                self.assertEqual(token.type,Token.ENDMARKER)
                self.assertEqual(token.value,None)
            
            #check current token
            curr_tok = tokenizer.current_token()
                
            self.assertEqual(curr_tok.type,token.type)
            self.assertEqual(curr_tok.value,token.value)
            
            cpt+=1
            
    def test_next_method(self):
        ''' test next functionality '''
        
        tokenizer = IMSTokenizer()
        
        str = "     begin IMS2.0     \nmsg_type data \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \ntime 2000/11/22 to 2001/01/01\nsta_list ABC,DEF, FGH  \nalert_temp\n    stop"
        
        io_prog = StringIO.StringIO(str)
         
        tokenizer.set_io_prog(io_prog)
        
        cpt = 0
        
        token = tokenizer.next()
        
        while token.type != Token.ENDMARKER:
            if cpt == 0:
                # retrieve token
                self.assertEqual(token.type,'BEGIN')
                self.assertEqual(token.value,'begin')
            elif cpt == 1:
                self.assertEqual(token.type,'MSGFORMAT')
                self.assertEqual(token.value,'IMS2.0')
            elif cpt == 2:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 3:
                self.assertEqual(token.type,'MSGTYPE')
                self.assertEqual(token.value,'msg_type')
            elif cpt == 4:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'data')
            elif cpt == 5:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 6:
                self.assertEqual(token.type,'MSGID')
                self.assertEqual(token.value,'msg_id')
            elif cpt == 7:
                self.assertEqual(token.type,'NUMBER')
                self.assertEqual(token.value,'54695')
            elif cpt == 8:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'ctbto_idc')
            elif cpt == 9:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 10:
                self.assertEqual(token.type,'EMAIL')
                self.assertEqual(token.value,'e-mail')
            elif cpt == 11:
                self.assertEqual(token.type,'EMAILADDR')
                self.assertEqual(token.value,'guillaume.aubert@ctbto.org')
            elif cpt == 12:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 13:
                self.assertEqual(token.type,'TIME')
                self.assertEqual(token.value,'time')
            elif cpt == 14:
                self.assertEqual(token.type,'DATETIME')
                self.assertEqual(token.value,'2000/11/22')
            elif cpt == 15:
                self.assertEqual(token.type,'TO')
                self.assertEqual(token.value,'to')
            elif cpt == 16:
                self.assertEqual(token.type,'DATETIME')
                self.assertEqual(token.value,'2001/01/01')
            elif cpt == 17:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 18:
                self.assertEqual(token.type,'STALIST')
                self.assertEqual(token.value,'sta_list')
            elif cpt == 19:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'ABC')
            elif cpt == 20:
                self.assertEqual(token.type,'COMMA')
                self.assertEqual(token.value,',')
            elif cpt == 21:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'DEF')
            elif cpt == 22:
                self.assertEqual(token.type,'COMMA')
                self.assertEqual(token.value,',')
            elif cpt == 23:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'FGH')
            elif cpt == 24:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 25:
                self.assertEqual(token.type,'ALERTTEMP')
                self.assertEqual(token.value,'alert_temp')
            elif cpt == 26:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 27:
                self.assertEqual(token.type,'STOP')
                self.assertEqual(token.value,'stop')
            elif cpt == 28:
                self.assertEqual(token.type,Token.ENDMARKER)
                self.assertEqual(token.value,None)
            
            # inc cpt and go to next token
            cpt+=1
            token = tokenizer.next()
        
   
    def test_consume_next_token_method(self):
        ''' test consume next token functionality '''
        
        tokenizer = IMSTokenizer()
        
        str = "     begin IMS2.0     \nmsg_type data \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \ntime 2000/11/22 to 2001/01/01\nsta_list ABC,DEF, FGH  \nalert_temp\n    stop"
        
        io_prog = StringIO.StringIO(str)
         
        tokenizer.set_io_prog(io_prog)
        
        cpt = 0
        
        token = tokenizer.next()
        
        while token.type != Token.ENDMARKER:
            
            if cpt == 0:
                # retrieve token
                self.assertEqual(token.type,'BEGIN')
                self.assertEqual(token.value,'begin')
            elif cpt == 1:
                self.assertEqual(token.type,'MSGFORMAT')
                self.assertEqual(token.value,'IMS2.0')
            elif cpt == 2:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 3:
                self.assertEqual(token.type,'MSGTYPE')
                self.assertEqual(token.value,'msg_type')
            elif cpt == 4:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'data')
                break
            
            token = tokenizer.next()
            
            cpt +=1
            
        
        token = tokenizer.consume_next_token(Token.NEWLINE)
        
        self.assertEqual(token.type,Token.NEWLINE)
        self.assertEqual(token.value,'\n')
        
        token = tokenizer.next()
        
        self.assertEqual(token.type,Token.MSGID)
        self.assertEqual(token.value,'msg_id')
    
    def test_consume_next_tokens_method(self):
        ''' test consume next tokens list functionality '''
        
        tokenizer = IMSTokenizer()
        
        str = "     begin IMS2.0     \nmsg_type data \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \ntime 2000/11/22 to 2001/01/01\nsta_list ABC,DEF, FGH  \nalert_temp\n    stop"
        
        io_prog = StringIO.StringIO(str)
         
        tokenizer.set_io_prog(io_prog)
        
        cpt = 0
        
        token = tokenizer.next()
        
        while token.type != Token.ENDMARKER:
            
            if cpt == 0:
                # retrieve token
                self.assertEqual(token.type,'BEGIN')
                self.assertEqual(token.value,'begin')
            elif cpt == 1:
                self.assertEqual(token.type,'MSGFORMAT')
                self.assertEqual(token.value,'IMS2.0')
            elif cpt == 2:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 3:
                self.assertEqual(token.type,'MSGTYPE')
                self.assertEqual(token.value,'msg_type')
            elif cpt == 4:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'data')
                break
            
            token = tokenizer.next()
            
            cpt +=1
            
        token = tokenizer.consume_next_tokens([Token.NEWLINE])
        
        self.assertEqual(token.type,Token.NEWLINE)
        self.assertEqual(token.value,'\n')
        
        token = tokenizer.next()
        
        self.assertEqual(token.type,Token.MSGID)
        self.assertEqual(token.value,'msg_id')
        
    
    def test_consume_next_token_method_error(self):
        ''' test consume next token functionality and raise exception '''
        
        tokenizer = IMSTokenizer()
        
        str = "     begin IMS2.0     \nmsg_type data \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \ntime 2000/11/22 to 2001/01/01\nsta_list ABC,DEF, FGH  \nalert_temp\n    stop"
        
        io_prog = StringIO.StringIO(str)
         
        tokenizer.set_io_prog(io_prog)
        
        cpt = 0
        
        token = tokenizer.next()
        
        while token.type != Token.ENDMARKER:
            
            if cpt == 0:
                # retrieve token
                self.assertEqual(token.type,'BEGIN')
                self.assertEqual(token.value,'begin')
            elif cpt == 1:
                self.assertEqual(token.type,'MSGFORMAT')
                self.assertEqual(token.value,'IMS2.0')
            elif cpt == 2:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 3:
                self.assertEqual(token.type,'MSGTYPE')
                self.assertEqual(token.value,'msg_type')
            elif cpt == 4:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'data')
                break
            
            token = tokenizer.next()
            
            cpt +=1
            
        try:
            token = tokenizer.consume_next_token(Token.MSGID)
        except  BadTokenError, e:
            self.assertEqual(e.message,'Found Token with type NEWLINE and value [\n] in Line 2, position 14. Was expecting MSGID.')
    
    def test_consume_next_tokens_method_error(self):
        ''' test consume next tokens list functionality and raise exception '''
        
        tokenizer = IMSTokenizer()
        
        str = "     begin IMS2.0     \nmsg_type data \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \ntime 2000/11/22 to 2001/01/01\nsta_list ABC,DEF, FGH  \nalert_temp\n    stop"
        
        io_prog = StringIO.StringIO(str)
         
        tokenizer.set_io_prog(io_prog)
        
        cpt = 0
        
        token = tokenizer.next()
        
        while token.type != Token.ENDMARKER:
            
            if cpt == 0:
                # retrieve token
                self.assertEqual(token.type,'BEGIN')
                self.assertEqual(token.value,'begin')
            elif cpt == 1:
                self.assertEqual(token.type,'MSGFORMAT')
                self.assertEqual(token.value,'IMS2.0')
            elif cpt == 2:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 3:
                self.assertEqual(token.type,'MSGTYPE')
                self.assertEqual(token.value,'msg_type')
            elif cpt == 4:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'data')
                break
            
            token = tokenizer.next()
            
            cpt +=1
            
        try:
            
            token = tokenizer.consume_next_tokens([Token.MSGID])
        except  BadTokenError, e:
            self.assertEqual(e.message,"Found Token with type NEWLINE and value [\n] in Line 2, position 14. Was expecting ['MSGID'].")
    
    def ztest_consume_while_next_token_is_in(self):
        ''' test consume while next token is in functionality '''
        
        tokenizer = IMSTokenizer()
        
        str = "     begin IMS2.0     \n\n\n\n\n\n\nmsg_type data \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \ntime 2000/11/22 to 2001/01/01\nsta_list ABC,DEF, FGH  \nalert_temp\n    stop"
        
        io_prog = StringIO.StringIO(str)
         
        tokenizer.set_io_prog(io_prog)
        
        cpt = 0
        
        token = tokenizer.next()
        
        while token.type != Token.ENDMARKER:
            
            if cpt == 0:
                # retrieve token
                self.assertEqual(token.type,'BEGIN')
                self.assertEqual(token.value,'begin')
            elif cpt == 1:
                self.assertEqual(token.type,'MSGFORMAT')
                self.assertEqual(token.value,'IMS2.0')
                break
            
            token = tokenizer.next()
            cpt +=1
        
        # test the method now
        tokenizer.consume_while_next_token_is_in([Token.NEWLINE])
        
        token = tokenizer.current_token()
    
        self.assertEqual(token.type,'MSGTYPE')
        self.assertEqual(token.value,'msg_type')
        
        token = tokenizer.next()
        
        self.assertEqual(token.type,'ID')
        self.assertEqual(token.value,'data')
        
    
    def test_sphdf_sphdp(self):
        """ """
        
        tokenizer = IMSTokenizer()
        
        str = "begin ims1.0\nmsg_type request\nmsg_id ex026\ne-mail foo.bar@google.com\ntime 1999/07/01 to 2000/08/01\nsta_list AU*\nsphdf rms2.0\nsphdp rms2.0\nstop\n"
        
        io_prog = StringIO.StringIO(str)
         
        tokenizer.set_io_prog(io_prog)
        
        cpt = 0
        
        token = tokenizer.next()
        
        while token.type != Token.ENDMARKER:
            #print("\nToken = %s"%(token))
    
            if cpt == 0:
                # retrieve token
                self.assertEqual(token.type,'BEGIN')
                self.assertEqual(token.value,'begin')
            elif cpt == 1:
                self.assertEqual(token.type,'MSGFORMAT')
                self.assertEqual(token.value,'ims1.0')
            elif cpt == 2:
                self.assertEqual(token.type, Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 3:
                self.assertEqual(token.type,'MSGTYPE')
                self.assertEqual(token.value,'msg_type')
            elif cpt == 4:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'request')
            elif cpt == 5:
                self.assertEqual(token.type, Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 6:
                self.assertEqual(token.type,'MSGID')
                self.assertEqual(token.value,'msg_id')
            elif cpt == 7:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'ex026')
            elif cpt == 8:
                self.assertEqual(token.type, Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 9:
                self.assertEqual(token.type,'EMAIL')
                self.assertEqual(token.value,'e-mail')
            elif cpt == 10:
                self.assertEqual(token.type,'EMAILADDR')
                self.assertEqual(token.value,'foo.bar@google.com')
            elif cpt == 11:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 12:
                self.assertEqual(token.type,Token.TIME)
                self.assertEqual(token.value,'time')
            elif cpt == 13:
                self.assertEqual(token.type,Token.DATETIME)
                self.assertEqual(token.value,'1999/07/01')
            elif cpt == 14:
                self.assertEqual(token.type,Token.TO)
                self.assertEqual(token.value,'to')
            elif cpt == 15:
                self.assertEqual(token.type,Token.DATETIME)
                self.assertEqual(token.value,'2000/08/01')
            elif cpt == 16:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 17:
                self.assertEqual(token.type,Token.STALIST)
                self.assertEqual(token.value,'sta_list')
            elif cpt == 18:
                self.assertEqual(token.type,Token.WCID)
                self.assertEqual(token.value,'AU*')
            elif cpt == 19:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 20:
                self.assertEqual(token.type,Token.SPHDF)
                self.assertEqual(token.value,'sphdf')
            elif cpt == 21:
                self.assertEqual(token.type,Token.MSGFORMAT)
                self.assertEqual(token.value,'rms2.0')
            elif cpt == 22:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 23:
                self.assertEqual(token.type,Token.SPHDP)
                self.assertEqual(token.value,'sphdp')
            elif cpt == 24:
                self.assertEqual(token.type,Token.MSGFORMAT)
                self.assertEqual(token.value,'rms2.0')
            elif cpt == 25:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 26:
                self.assertEqual(token.type,'STOP')
                self.assertEqual(token.value,'stop')
            elif cpt == 27:
                self.assertEqual(token.type,Token.NEWLINE)
                self.assertEqual(token.value,'\n')
            elif cpt == 28:
                self.assertEqual(token.type,Token.ENDMARKER)
                self.assertEqual(token.value,None)
            
            
            token = tokenizer.next()
            cpt += 1
    
    def test_token_creator(self):
        """ create tokens """
        
        import re
        
        tokC = TokenCreator()
        
        tokC.register_token("ID",re.compile(r'[/\*A-Za-z_\+=\(\)\<\>]([\w]|[/=\<\>\(\)\.@\*\+-])*'),'HEAD')
        
        tokC.ID     
                 
    def ztest_read_from_email(self):
        ''' test read from an email message and lex '''
        
        import email
    
    
        #dir = '/home/aubert/req_messages'
        dir='/tmp/req_messages'
        fd  = open('%s/%s'%(dir,'34379477.msg'))
        msg = email.message_from_file(fd)
    
        #print("msg = %s\n"%(msg))
    
        if not msg.is_multipart():
            to_parse = msg.get_payload()
            #print("to_parse %s\n"%(to_parse))
                
            index = to_parse.lower().find('begin')
                
            if index >= 0:
                
                tokenizer = IMSTokenizer()
        
                io_prog = StringIO.StringIO(to_parse[index:])
         
                tokenizer.set_io_prog(io_prog)
                
                cpt = 0
                for token in tokenizer:
                    #print("\nToken = %s"%(token))
                    cpt +=1
            else:
                print("Cannot find begin")
        else:
            print("multipart")
        
            for part in msg.walk():
                #print(part.get_content_type())
                # if we have a text/plain this a IMS2.0 message so we try to parse it
                if part.get_content_type() == 'text/plain':
                    to_parse = part.get_payload()
                    index = to_parse.lower().find('begin')
                
                    if index >= 0:
                        tokenizer = IMSTokenizer()
        
                        io_prog = StringIO.StringIO(to_parse)
         
                        tokenizer.set_io_prog(io_prog)
                
                        cpt = 0
                        for token in tokenizer:
                            #print("\nToken = %s"%(token))
                            cpt +=1  
                    else:
                        print("Cannot find begin in %s"%(to_parse))
    
    def ztest_loop_read_from_dir(self):
        ''' This is not a unit test as it reads a full dir and then launch the lexer on each file '''
        
        import email
        import os
        
        #dir = '/home/aubert/req_messages'
        dir = '/tmp/req_messages'
        for f in os.listdir(dir):
            
            print("********************* Try to Parse %s/%s **************************"%(dir,f))
            
            fd = open('%s/%s'%(dir,f))
            
            msg = email.message_from_file(fd)
    
            print("it is not multipart")
            
            if not msg.is_multipart():
                to_parse = msg.get_payload()
                #print("to_parse %s\n"%(to_parse))
                
                index = to_parse.lower().find('begin')
                
                if index >= 0:
                
                    tokenizer = IMSTokenizer()
        
                    io_prog = StringIO.StringIO(to_parse[index:])
         
                    tokenizer.set_io_prog(io_prog)
                
                    cpt = 0
                    for token in tokenizer:
                        #print("\nToken = %s"%(token))
                        cpt +=1
                else:
                   print("Cannot find begin")
                
            else:
                print("it is multipart")
        
                for part in msg.walk():
                    #print(part.get_content_type())
                    # if we have a text/plain this a IMS2.0 message so we try to parse it
                    if part.get_content_type() == 'text/plain':
                        to_parse = part.get_payload()
                        index = to_parse.lower().find('begin')
                
                        if index >= 0:
                           tokenizer = IMSTokenizer()
        
                           io_prog = StringIO.StringIO(to_parse)
         
                           tokenizer.set_io_prog(io_prog)
                
                           cpt = 0
                           for token in tokenizer:
                               #print("\nToken = %s"%(token))
                               cpt +=1  
                        else:
                            print("Cannot find begin in %s\n"%(to_parse))     
        
        
