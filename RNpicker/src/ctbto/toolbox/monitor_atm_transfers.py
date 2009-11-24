'''
Created on Nov 24, 2009

Script for automatically monitoring the ATM file transfers with ECAccess

@author: guillaume.aubert@ctbto.org
'''

import subprocess

import smtplib
import mimetypes
import base64
from email.mime.audio       import MIMEAudio
from email.mime.image       import MIMEImage
from email.mime.multipart   import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text        import MIMEText

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
        command = "/home/aubert/ecaccess-v3.3.0/client/tools/ectls %s"
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
                    raise  Exception("Error when execution ectls %s to get more information on this job: %s" %(transfer_id, lines))
                else:
                    lines = ''.join(proc.stdout.readlines())
                    return "==== Transfer %s Info ====\n%s\n" % (transfer_id, lines)
        
    
    def check_transfers_status(self):
        """ 
            Use subprocess to call the ecaccess ectls command and check if there are any job in STOP mode
        """
        
        command = "/home/aubert/ecaccess-v3.3.0/client/tools/ectls"
        
        
        try:
            
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
                raise  Exception("Error when calling %s:\n %s" %( command, lines))
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
                    self._emailer.send_text_message('guillaume.aubert@ctbto.org', 'ATM ECMWF Transfers errors', lines)
                    print("email sent\n")
                else:
                    print("No transfer errors\n")
            
        except Exception, exc:
            print(exc)

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
        self._server_port = a_server_port if (a_server_port != None) else 25
        
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
        self._smtp_server.sendmail(self._sender, [a_receivers], msg.as_string())


if __name__ == '__main__':
    
    host     = 'malta14.office.ctbto.org'
    port     = 25
    login    = 'aubert'
    password = 'ZXJuZXN0MjU='
    sender   = 'guillaume.aubert@ctbto.org'
    
    emailer = DataEmailer(host, port, sender, login, password)
    
    emailer.connect()
    
    checker = ATMFileTransferChecker(emailer)
    
    checker.check_transfers_status()