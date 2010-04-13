'''
Created on Jan 28, 2010

@author: guillaume.aubert@ctbto.org
'''

import logging.config
import traceback
import sys
from org.ctbto.conf.conf_helper import Conf

class LoggerFactory:
    """ Factory for handling Loggers """
    __INITIALIZED__ = False
    __DEBUG__ = False
    DISABLED = 1000
    
    def __init__(self):
        """ default cons  """
        
        self._additional_handlers = []
    
    @classmethod
    def _get_logger(cls, logger_name):
        """ Return the logger for the given class name """
        if not cls.__INITIALIZED__ :
            conf_file = None
            debug = False
            try:
                conf_file = Conf.get_instance().get('Logging', 'conf_file', None)
                logging.addLevelName(LoggerFactory.DISABLED, "DISABLED")
                debug = Conf.get_instance().getboolean('Logging', 'debug', False)
                if debug is True:
                    print 'debug ' + str(debug) + ',initializing logging, using ' + conf_file
                
                logging.config.fileConfig(conf_file)
                
                #add console handler: specific for RNPicker Apps
                cls._add_console_handler()
                
                
            except Exception, ex: #pylint: disable-msg=W0703
                err_msg = str(ex)
                if conf_file and not cls.__check_conf_file_exist__(conf_file):
                    err_msg = ('file ' + conf_file + ' not found')
                if debug is True:
                    print 'logging configuration error, ' + err_msg
                    print traceback.print_exc(10, sys.stderr)
            cls.__INITIALIZED__ = True
        return logging.getLogger(logger_name)
    
    @classmethod
    def _add_console_handler(cls):
        """ add the specific console handler for RNPicker programs """
        
        #create console handler
        console = logging.StreamHandler()
        console_formatter = logging.Formatter("%(levelname)s - %(message)s")
        console_filter    = logging.Filter(Conf.get_instance().get('Logging', 'consoleFilter', 'Runner'))
        console.setFormatter(console_formatter)
        console.addFilter(console_filter)

        logging.root.addHandler(console)
    
    @classmethod
    def get_logger(cls, logged_object):
        """Return a logger with a logger name based on logger_object class name"""
        if not isinstance(logged_object, str):
            logger_name = logged_object.__class__.__name__
        else:
            logger_name = str(logged_object)
        return LoggerFactory._get_logger(logger_name)
    
    
    @classmethod
    def __check_conf_file_exist__(cls, conf_file_name):
        """ check if the conf file exists"""
        conf_file_exists = True
        try:
            open(conf_file_name)
        except IOError:
            conf_file_exists = False
        return conf_file_exists
