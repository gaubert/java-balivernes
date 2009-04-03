'''
Created on Apr 3, 2009

@module: data_calculations

Module containing different kind of operations that can be performed on the data itself.

@author: Guillaume Aubert
         
'''
import logging

import ctbto.common.scanf_util


class NobleGasDecayCorrector(object):
    """ Apply decay correction on the noble gas activity concentration  """
    
    # Class members
    c_log = logging.getLogger("NobleGasDecayCorrector")
    c_log.setLevel(logging.INFO)

    def __init__(self):
        
        super(NobleGasDecayCorrector,self).__init__(a_coll_start=0,a_coll_stop=0,a_acq_start=0,a_acq_stop=0,a_live=0)
        
        self._coll_stop  = a_coll_stop
        self._coll_start = a_coll_start
        self._acq_stop   = a_acq_stop
        self._acq_start  = a_acq_start
        self._a_live     = a_live
        
        self._t_count    = -1
        self._t_real     = -1
        self._t_live     = -1
        self._t_prep     = -1
        
        self._calculate_time_coeffs()
    
    def _calculate_time_coeffs(self):
        """"""
        
        self._t_count = self._coll_stop - self._coll_start
        self._t_prep  = self._acq_start - self._coll_stop
        self._t_real  = self._acq_stop  - self._acq_start
        self._t_live  = self._a_live
        
    def _calculate_fi(self,a_half_life):
        """ calculate f(i) = A^2/(1-exp(-A*tcount)*exp(-A*tprep)*(1-exp(-A*treal) 
            with A = ln(2)/half-life iso in sec
        """
        
    
    def decay_correct(self,a_isotope_name,a_values):
        """ decay correct the values passed """
        
        
   


time_unit_to_sec = { 'S' : 1 ,
               'M' : 60,
               'H' : 3600,
               'D' : 86400,
               'Y' : 31556926,            
             }
     

def convert_half_life_in_sec(a_half_life_string):
    """ convert the half_life in sec from the string.
        support the following strings [numeric value] [time unit].
        With time unit equal to S or M or H or D or Y.
        
        Args:
                a_half_life_string  : the half life value as a string
               
            Returns:
        
            Raises:
               exception if cannot connect to the server
    """
    
    #use scanf to parse the string
    scan_result = ctbto.common.scanf_util.scanf("%f %c", a_half_life_string)
    
    if len(scan_result) != 2:
        raise Exception("Did not recognise the following string as a valid half-life")
    
    number,time_unit = scan_result
    
    # if this is zero then there is a problem
    result = time_unit_to_sec.get(time_unit,0) * number
    
    if result == 0:
        raise Exception("The value %s in %s cannot be used as a time_unit"%(time_unit,a_half_life_string))
    
    return result
    
    
    













# unit tests part
import unittest
import ctbto.calculation.data_calculation
import ctbto.tests

def tests():
    suite = unittest.TestLoader().loadTestsFromModule(ctbto.calculation.data_calculation)
    unittest.TextTestRunner(verbosity=2).run(suite)

class TestDataModule(unittest.TestCase):
    
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
        
    def testHalfLifeConversion(self):
       
        r = convert_half_life_in_sec("5.243 D")
       
        self.assertEqual(452995.2,r)
       
        r = convert_half_life_in_sec("22.300 Y")
       
        self.assertEqual(703719449.80000007,r)
   

if __name__ == '__main__':
    tests()     