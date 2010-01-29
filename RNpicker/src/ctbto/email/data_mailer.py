""" 
    Copyright 2008 CTBTO Organisation
    
    module: data_mailer
"""
#general packages
import logging
import os

# email stuff
import smtplib
import mimetypes
from email.mime.audio       import MIMEAudio
from email.mime.image       import MIMEImage
from email.mime.multipart   import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text        import MIMEText


from ctbto.common.logging_utils import LoggerFactory
import ctbto.common.utils  
 

class DataEmailer(object):
    """ Class used to send emails containing attached data """

    def __init__(self,a_server_host,a_server_port=25,a_login=None,a_password=None,a_debugging_level=0):
        
        super(DataEmailer,self).__init__()
        
        self._server_host = a_server_host
        
        # set to SMTP default if no ports are given
        self._server_port = a_server_port if (a_server_port != None) else 25
        
        self._login       = a_login
        self._password    = a_password
        self._debug_level = a_debugging_level
        
        self._smtp_server = None
        
        self._log    = LoggerFactory.get_logger(self)
          
    
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
            self._smtp_server.login(self._login,self._password)
    
    def send_email_attached_files(self,a_sender,a_receivers,a_list_of_attached_files,a_subject='(no subject)',a_text_content=None):
        """
            Send email with the passed data to the receiver
        
            Args:
                a_subject                : the message subject
                a_sender                 : the sender
                a_receivers              : the comma separated string of receivers (ex:'foo@ctbto.org,bar@ctbto.org')
                a_list_of_attached_files : a list of files to attach to the email
                a_text_content           : If you fancy a text content in the email
               
            Returns:
        
            Raises:
               exception if cannot connect to the server
        """
        
        # check arguments
        if a_sender == None:
            raise Exception('Need a sender prior to sending any emails')
        
        if a_receivers == None:
            raise Exception('Cannot send any emails as not receivers have been given')
        else:
            # split list of receivers
            receivers = a_receivers.split(',')
            if len(receivers) == 0:
                raise Exception('a_receivers [%s] should be a string with comma separated values.'%(a_receivers))
            
        # check if files exists otherwise raise an exception
        for f in a_list_of_attached_files:
            ctbto.common.utils.file_exits(f)
            
        
        # Create the container (outer) email message.
        outer = MIMEMultipart()
        outer['Subject'] = a_subject
    
        # prepare the message
    
        outer['From']  = a_sender
        #outer.preamble = ''
        
        # if there is a text content add it
        if a_text_content != None:
            outer.attach(MIMEText(a_text_content))
        
        # Assume we know that the image files are all in PNG format
        for file in a_list_of_attached_files:
            ctype, encoding = mimetypes.guess_type(file)
            if ctype is None or encoding is not None:
                # No guess could be made, or the file is encoded (compressed), so
                # use a generic bag-of-bits type.
                ctype = 'application/octet-stream'
        
            maintype, subtype = ctype.split('/', 1)
            if maintype == 'text':
                fp = open(file)
                # Note: we should handle calculating the charset
                msg = MIMEText(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == 'image':
                fp = open(file, 'rb')
                msg = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == 'audio':
                fp = open(file, 'rb')
                msg = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
            else:
                fp = open(file)
                #deal with xml and other application data
                msg = MIMEApplication(fp.read(), _subtype=subtype)
            
            # Set the filename parameter
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            outer.attach(msg)
            
        # send to all receivers
        for receiver in receivers:
            outer['To'] = receiver 
            self._log.info('send message to %s with the following attachments %s.'%(receiver,a_list_of_attached_files))
            self._smtp_server.sendmail(a_sender, [receiver], outer.as_string())
        
        return

# unit tests part
import unittest
import ctbto.email.data_mailer
import ctbto.tests

def tests():
    suite = unittest.TestLoader().loadTestsFromModule(ctbto.email.data_mailer)
    unittest.TextTestRunner(verbosity=2).run(suite)

class TestDataEmailer(unittest.TestCase):
    
    def _setBasicLoggingConfig(self):
        if len(logging.root.handlers) == 0:
            console = logging.StreamHandler()
            fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            console.setFormatter(fmt)
            logging.root.addHandler(console)
        
            log = logging.getLogger("ROOT")
            log.setLevel(logging.INFO)
            log.info("Start")
    
    def _get_tests_dir_path(self):
        """ get the ctbto.tests path depending on where it is defined """
        
        fmod_path = ctbto.tests.__path__
        
        test_dir = "%s/conf_tests"%fmod_path[0]
        
        return test_dir
    
    def setUp(self):
        self._setBasicLoggingConfig()
        
    def testSendEmailWithAttachedFiles(self):
        
        s = DataEmailer('malta14.office.ctbto.org')
        s.connect('aubert','ernest25')
        
        s.send_email_attached_files('guillaume.aubert@ctbto.org','guillaume.aubert@gmail.com',['%s/samples/sampml-full-967273.xml.master'%(self._get_tests_dir_path())], 'a test')
    
    def testSendtoMultipleClients(self):
        
        s = DataEmailer('malta14.office.ctbto.org')
        s.connect('aubert','ernest25')
        
        s.send_email_attached_files('guillaume.aubert@ctbto.org','guillaume.aubert@gmail.com,guillaume.aubert@ctbto.org',['%s/samples/sampml-full-967273.xml.master'%(self._get_tests_dir_path())], 'a test')
    

if __name__ == '__main__':
    tests()
       
        