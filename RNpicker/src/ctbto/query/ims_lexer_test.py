'''
Created on May 13, 2009

@author: guillaume.aubert@ctbto.org
'''
from unittest import TestCase,TestLoader,TextTestRunner

from ims_lexer import IMSLexer, LexerError

class LexerTest(TestCase):
    
    def setUp(self):
        pass
        
    def test_list_tokens_lower_case(self):
        
        lexer  = IMSLexer()
        lexer.input("     begin IMS2.0     \nmsg_type data \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \ntime 2000/11/22 to 2001/01/01\nsta_list ARP01\nalert_temp\n    stop")
    
        cpt = 0
        for token in lexer:
            #print("\nToken = %s"%(token))
            
            if cpt == 0:
                # retrieve token
                self.assertEqual(token.type,'BEGIN')
                self.assertEqual(token.value,'begin')
            elif cpt == 1:
                self.assertEqual(token.type,'MSGFORMAT')
                self.assertEqual(token.value,'IMS2.0')
            elif cpt == 2:
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 3:
                self.assertEqual(token.type,'MSG_TYPE')
                self.assertEqual(token.value,'msg_type')
            elif cpt == 4:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'data')
            elif cpt == 5:
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 6:
                self.assertEqual(token.type,'MSG_ID')
                self.assertEqual(token.value,'msg_id')
            elif cpt == 7:
                self.assertEqual(token.type,'NUMBER')
                self.assertEqual(token.value,(54695, '54695'))
            elif cpt == 8:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'ctbto_idc')
            elif cpt == 9:
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 10:
                self.assertEqual(token.type,'EMAIL')
                self.assertEqual(token.value,'e-mail')
            elif cpt == 11:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'guillaume.aubert@ctbto.org')
            elif cpt == 12:
                self.assertEqual(token.type,'NEWLINE')
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
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 18:
                self.assertEqual(token.type,'STA_LIST')
                self.assertEqual(token.value,'sta_list')
            elif cpt == 19:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'ARP01')
            elif cpt == 20:
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 21:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'alert_temp')
            elif cpt == 22:
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 23:
                self.assertEqual(token.type,'STOP')
                self.assertEqual(token.value,'stop')
            elif cpt == 24:
                self.assertEqual(token.type,'ENDMARKER')
                self.assertEqual(token.value,None)
    
            cpt+=1
            
   
    def test_help_message(self):
        
        lexer  = IMSLexer()
        lexer.input("begin IMS2.0     \nmsg_type request \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \nhelp\nstop")
    
        cpt = 0
        for token in lexer:
            #print("\nToken = %s"%(token))
            
            if cpt == 0:
                # retrieve token
                self.assertEqual(token.type,'BEGIN')
                self.assertEqual(token.value,'begin')
            elif cpt == 1:
                self.assertEqual(token.type,'MSGFORMAT')
                self.assertEqual(token.value,'IMS2.0')
            elif cpt == 2:
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 3:
                self.assertEqual(token.type,'MSG_TYPE')
                self.assertEqual(token.value,'msg_type')
            elif cpt == 4:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'request')
            elif cpt == 5:
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 6:
                self.assertEqual(token.type,'MSG_ID')
                self.assertEqual(token.value,'msg_id')
            elif cpt == 7:
                self.assertEqual(token.type,'NUMBER')
                self.assertEqual(token.value,(54695, '54695'))
            elif cpt == 8:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'ctbto_idc')
            elif cpt == 9:
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 10:
                self.assertEqual(token.type,'EMAIL')
                self.assertEqual(token.value,'e-mail')
            elif cpt == 11:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'guillaume.aubert@ctbto.org')
            elif cpt == 12:
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 13:
                self.assertEqual(token.type,'HELP')
                self.assertEqual(token.value,'help')
            elif cpt == 14:
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 15:
                self.assertEqual(token.type,'STOP')
                self.assertEqual(token.value,'stop')
            elif cpt == 16:
                self.assertEqual(token.type,'ENDMARKER')
                self.assertEqual(token.value,None)
            
            cpt+=1
    
    def test_time_1(self):
        ''' test with an advance time part '''
        lexer  = IMSLexer()
        lexer.input("     begin IMS2.0     \nmsg_type data \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \ntime 1999/02/01 23:14:19.7 to 1999/02/01 23:29:19.76\nsta_list ABC,DEF, FGH  \nalert_temp\n    stop")
    
        cpt = 0
        for token in lexer:
            #print("\nToken = %s"%(token))
            
            if cpt == 0:
                # retrieve token
                self.assertEqual(token.type,'BEGIN')
                self.assertEqual(token.value,'begin')
            elif cpt == 1:
                self.assertEqual(token.type,'MSGFORMAT')
                self.assertEqual(token.value,'IMS2.0')
            elif cpt == 2:
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 3:
                self.assertEqual(token.type,'MSG_TYPE')
                self.assertEqual(token.value,'msg_type')
            elif cpt == 4:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'data')
            elif cpt == 5:
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 6:
                self.assertEqual(token.type,'MSG_ID')
                self.assertEqual(token.value,'msg_id')
            elif cpt == 7:
                self.assertEqual(token.type,'NUMBER')
                self.assertEqual(token.value,(54695, '54695'))
            elif cpt == 8:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'ctbto_idc')
            elif cpt == 9:
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 10:
                self.assertEqual(token.type,'EMAIL')
                self.assertEqual(token.value,'e-mail')
            elif cpt == 11:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'guillaume.aubert@ctbto.org')
            elif cpt == 12:
                self.assertEqual(token.type,'NEWLINE')
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
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 18:
                self.assertEqual(token.type,'STA_LIST')
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
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 25:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'alert_temp')
            elif cpt == 26:
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 27:
                self.assertEqual(token.type,'STOP')
                self.assertEqual(token.value,'stop')
            elif cpt == 28:
                self.assertEqual(token.type,'ENDMARKER')
                self.assertEqual(token.value,None)
            
            cpt += 1
    
    def test_star_expansion(self):
        pass

    def test_station_list(self):
        ''' test with a station list'''
        
        lexer  = IMSLexer()
        lexer.input("     begin IMS2.0     \nmsg_type data \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \ntime 2000/11/22 to 2001/01/01\nsta_list ABC,DEF, FGH  \nalert_temp\n    stop")
    
        cpt = 0
        for token in lexer:
            #print("\nToken = %s"%(token))
            
            if cpt == 0:
                # retrieve token
                self.assertEqual(token.type,'BEGIN')
                self.assertEqual(token.value,'begin')
            elif cpt == 1:
                self.assertEqual(token.type,'MSGFORMAT')
                self.assertEqual(token.value,'IMS2.0')
            elif cpt == 2:
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 3:
                self.assertEqual(token.type,'MSG_TYPE')
                self.assertEqual(token.value,'msg_type')
            elif cpt == 4:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'data')
            elif cpt == 5:
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 6:
                self.assertEqual(token.type,'MSG_ID')
                self.assertEqual(token.value,'msg_id')
            elif cpt == 7:
                self.assertEqual(token.type,'NUMBER')
                self.assertEqual(token.value,(54695, '54695'))
            elif cpt == 8:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'ctbto_idc')
            elif cpt == 9:
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 10:
                self.assertEqual(token.type,'EMAIL')
                self.assertEqual(token.value,'e-mail')
            elif cpt == 11:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'guillaume.aubert@ctbto.org')
            elif cpt == 12:
                self.assertEqual(token.type,'NEWLINE')
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
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 18:
                self.assertEqual(token.type,'STA_LIST')
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
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 25:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'alert_temp')
            elif cpt == 26:
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 27:
                self.assertEqual(token.type,'STOP')
                self.assertEqual(token.value,'stop')
            elif cpt == 28:
                self.assertEqual(token.type,'ENDMARKER')
                self.assertEqual(token.value,None)
    
            cpt+=1
        
        pass

    def test_lat_lon(self):
        ''' lat-lon test '''
        
        lexer  = IMSLexer()
        lexer.input("     begin IMS2.0     \nmsg_type data \nmsg_id 54695 ctbto_idc\ne-mail guillaume.aubert@ctbto.org     \ntime 2000/11/22 to 2001/01/01\nlat -12 to 17\nlon 44 to 66\nalert_temp\n    stop")
    
        cpt = 0
        for token in lexer:
            #print("\nToken = %s"%(token))
            
            if cpt == 0:
                # retrieve token
                self.assertEqual(token.type,'BEGIN')
                self.assertEqual(token.value,'begin')
            elif cpt == 1:
                self.assertEqual(token.type,'MSGFORMAT')
                self.assertEqual(token.value,'IMS2.0')
            elif cpt == 2:
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 3:
                self.assertEqual(token.type,'MSG_TYPE')
                self.assertEqual(token.value,'msg_type')
            elif cpt == 4:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'data')
            elif cpt == 5:
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 6:
                self.assertEqual(token.type,'MSG_ID')
                self.assertEqual(token.value,'msg_id')
            elif cpt == 7:
                self.assertEqual(token.type,'NUMBER')
                self.assertEqual(token.value,(54695, '54695'))
            elif cpt == 8:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'ctbto_idc')
            elif cpt == 9:
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 10:
                self.assertEqual(token.type,'EMAIL')
                self.assertEqual(token.value,'e-mail')
            elif cpt == 11:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'guillaume.aubert@ctbto.org')
            elif cpt == 12:
                self.assertEqual(token.type,'NEWLINE')
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
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 18:
                self.assertEqual(token.type,'LAT')
                self.assertEqual(token.value,'lat')
            elif cpt == 19:
                self.assertEqual(token.type,'MINUS')
                self.assertEqual(token.value,'-')
            elif cpt == 20:
                self.assertEqual(token.type,'NUMBER')
                self.assertEqual(token.value,(12,'12'))
            elif cpt == 21:
                self.assertEqual(token.type,'TO')
                self.assertEqual(token.value,'to')
            elif cpt == 22:
                self.assertEqual(token.type,'NUMBER')
                self.assertEqual(token.value,(17,'17'))
            elif cpt == 23:
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 24:
                self.assertEqual(token.type,'LON')
                self.assertEqual(token.value,'lon')
            elif cpt == 25:
                self.assertEqual(token.type,'NUMBER')
                self.assertEqual(token.value,(44,'44'))
            elif cpt == 26:
                self.assertEqual(token.type,'TO')
                self.assertEqual(token.value,'to')
            elif cpt == 27:
                self.assertEqual(token.type,'NUMBER')
                self.assertEqual(token.value,(66,'66'))
            elif cpt == 28:
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 29:
                self.assertEqual(token.type,'ID')
                self.assertEqual(token.value,'alert_temp')
            elif cpt == 30:
                self.assertEqual(token.type,'NEWLINE')
                self.assertEqual(token.value,'\n')
            elif cpt == 31:
                self.assertEqual(token.type,'STOP')
                self.assertEqual(token.value,'stop')
            elif cpt == 32:
                self.assertEqual(token.type,'ENDMARKER')
                self.assertEqual(token.value,None)
    
            cpt+=1
