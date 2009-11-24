'''
Created on Nov 24, 2009

Script for automatically monitoring the ATM file transfers with ECAccess

@author: guillaume.aubert@ctbto.org
'''


import subprocess
import os

import datetime
import smtplib
import mimetypes
import base64
from email.mime.text        import MIMEText

# GLOBAL VARIABLES: SETTINGS
# To be set

HOST      = 'malta14.office.ctbto.org'
PORT      = 25
LOGIN     = 'aubert'
PASSWORD  = 'ZXJuZXN0MjU='
SENDER    = 'guillaume.aubert@office.ctbto.org'

# multiples can be entered with comma separated values
ATM_MON_RECEIVERS = 'guillaume.aubert@office.ctbto.org,guillaume.aubert@gmail.com'
    
ECACCESS_HOME = '/home/aubert/ecaccess-v3.3.0'


class ATMFileTransferChecker(object):
    """ Class used to send emails containing attached data """
    
    
    def __init__(self, emailer):
        """ constructor """
        
        self._emailer = emailer
        

    def look_for_transfer_problems(self, a_stdoutline):
        """
           Parse a ectls line.
           It should be something like that: 
           20170823   STOP       cbba                 ctbto4.ctbto.org     Nov 24 09:44
           
           args:
               a_stdoutline: the line to parse
        """
        command = "%s/client/tools/ectls" % (os.environ['ECACCESS_HOME'])
        command += " %s"
        
        if len(a_stdoutline) > 0:
            vals = a_stdoutline.split()
            
            # get transfer_id and use again ectls with the transfer id
            
            #check if state is in STOP mode (it means error somewhere)
            if vals[1] == 'STOP':
                transfer_id = vals[0]
                
                proc = subprocess.Popen(command % (transfer_id),
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                )
                
                proc.wait()
                
                returncode = proc.returncode
                
                if returncode != 0:
                    lines = ''.join(proc.stdout.readlines())
                    raise  Exception("Problem when execution ectls %s to get more information on this job: %s" %(transfer_id, lines))
                else:
                    lines = ''.join(proc.stdout.readlines())
                    return "==== Transfer %s Info ====\n%s\n" % (transfer_id, lines)
        
    def check_transfers_status(self):
        """ 
            Use subprocess to call the ecaccess ectls command and check if there are any job in STOP mode
        """
        command = "%s/client/tools/ectls 2>&1" % (os.environ['ECACCESS_HOME'])
        
        print("INFO: Calling command [%s]\n" % (command) )
        
        proc = subprocess.Popen(command,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                               )
        
        proc.wait()
        
        returncode = proc.returncode
        
        if returncode != 0:
            lines = ''.join(proc.stdout.readlines())
            raise  Exception("Problem when calling %s:\n %s" %( command, lines))
        else:
            orig_lines = ""
            lines = "Some ATM ECMWF Transfers failed. Please check below for the error(s).\n\n"
            has_error = False
            for line in proc.stdout:
                has_error = True
                # keep original lines for debugging
                orig_lines += line
                
                message = self.look_for_transfer_problems(line)
                
                lines += message
            
            if has_error:
                print(lines)
                
                # send it my email
                receivers = os.environ['ATM_MON_RECEIVERS']
                d_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._emailer.send_text_message(receivers, '%s = ATM ECMWF Transfers errors' %(d_now), lines)
                
                print("INFO: Sent error notification email sent to %s\n" %(receivers) )
            else:
                print("INFO: No transfer errors\n")

def encrypt(a_string):
    """ weak encryption for hiding password from being understandable by humans """
    return base64.b64encode(a_string)

def decrypt(a_string):
    """ weak decryption for hiding password from being understandable by humans """
    return base64.decodestring(a_string)

class DataEmailer(object):
    """ Class used to send emails containing attached data """

    def __init__(self, a_server_host, a_server_port=25, a_sender=None, a_login=None, a_password=None, a_debugging_level=0):
        
        super(DataEmailer,self).__init__()
        
        self._server_host = a_server_host
        
        # set to SMTP default if no ports are given
        if a_server_port:
            self._server_port = a_server_port 
        else:
            25
        
        self._login       = a_login
        self._password    = a_password
        self._debug_level = a_debugging_level
        self._sender      = a_sender
        
        self._smtp_server = None
          
    
    def connect(self,a_login=None,a_password=None,a_server_host=None,a_server_port=None):
        """
            Connect to the SMTP Server. All the passed information (host,port,login,password) are keeped
            in the related object's attributes.
        
            Args:
                a_server_host: the server hostname (default=None)
                a_server_port: the server port. If None are passed set it to SMTP default 25
                a_login: login for the SMTP server if login/pass is required
                a_password:  password for the SMTP server if login/pass is required
               
            Returns:
        
            Raises:
               exception if cannot connect to the server
        """
        # setup attributes for keeping the info
        if a_server_host != None:
            self._server_host = a_server_host
        
        if a_server_port != None:
            self._server_port = a_server_port
        
        if a_login != None:
            self._login = a_login
        
        if a_password != None:
            self._password = a_password
            
        # check preconditions
        if self._server_host == None:
            raise Exception("Need a SMTP host")
            
        # connect to the server
        self._smtp_server = smtplib.SMTP()
        self._smtp_server.set_debuglevel(self._debug_level)
        
        self._smtp_server.connect(self._server_host,self._server_port)
        
        #login if there is a login passed
        if self._login != None: 
            self._smtp_server.login(self._login,decrypt(self._password))
            
    
    def send_text_message(self,a_receivers, a_subject='(no subject)',a_text_content=''):
        
        if a_receivers == None:
            raise Exception('Cannot send any emails as not receivers have been given')
        else:
            # split list of receivers
            receivers = a_receivers.split(',')
            if len(receivers) == 0:
                raise Exception('a_receivers [%s] should be a string with comma separated values.'%(a_receivers))
            
        # Create a text/plain message
        msg = MIMEText(a_text_content)
        
        # me == the sender's email address
        # you == the recipient's email address
        msg['Subject'] = a_subject
        msg['From']    = self._sender
        msg['To']      = a_receivers
        
        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        self._smtp_server.sendmail(self._sender, receivers, msg.as_string())

def check_env():
    """ check the necessary env variables """
    
    ecaccess_home = os.environ['ECACCESS_HOME']
    
    if not ecaccess_home:
        raise Exception("Please set ECACCESS_HOME env variable")
    elif not os.path.exists('%s/client/tools/ectls' % (ecaccess_home)):
        raise Exception("The Env variable ECACCESS_HOME=[%s] doesn't seem to point to a valid ECACCESS client distribution. Please check" % (ecaccess_home))


if __name__ == '__main__':
    
    # put DEFAULT if no env variables
    if not os.environ.get('ATM_MON_RECEIVERS', None):
        print("INFO: ATM_MON_RECEIVERS variable set to default value %s.\n" %(ATM_MON_RECEIVERS) )
        os.environ['ATM_MON_RECEIVERS'] = ATM_MON_RECEIVERS
    
    if not os.environ.get('ECACCESS_HOME', None):
        print("INFO: ECACCESS_HOME ENV variable set to default value %s.\n" %(ECACCESS_HOME) )
        os.environ['ECACCESS_HOME'] = ECACCESS_HOME
    
    try:
        # preconditions checking
        check_env()
        
        emailer = DataEmailer(HOST, PORT, SENDER, LOGIN, PASSWORD)
        
        emailer.connect()
        
        checker = ATMFileTransferChecker(emailer)
        
        checker.check_transfers_status()
        
        print('INFO: Successfully ran script.\n')
        
        exit(0)
    except Exception, excep:
        print('ERROR: %s' %(excep))
        print('Exit in error.\n')
        exit(1)