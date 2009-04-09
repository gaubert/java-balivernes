'''
Created on Apr 3, 2009

@module: data_calculations

Module containing different kind of operations that can be performed on the data itself.

@author: Guillaume Aubert
         
'''

import logging

import ctbto.common.scanf_util
import ctbto.common.time_utils as time_utils

from decimal import *
import math


class NobleGasDecayCorrector(object):
    """ Apply decay correction on the noble gas activity concentration  """
    
    # Class members
    c_log = logging.getLogger("NobleGasDecayCorrector")
    c_log.setLevel(logging.INFO)
    
    c_default_half_life = {
            'XE-131M' : '11.900 D',
            'XE-133M' : '2.190 D',
            'XE-133'  : '5.243 D',
            'XE-135'  : '9.140 H'
        }      
   
    c_computation_method  =  {
            'XE-135' :'m1'  ,
            'XE-131M':'m1'  ,
            'XE-133M':'m1'  ,
            'XE-133' :'m2'  ,
        }

    def __init__(self,a_coll_start=0,a_coll_stop=0,a_acq_start=0,a_acq_stop=0,a_real=0):
        """ Constructor. 
            
            Args:
            a_coll_start,a_coll_stop,a_acq_start,a_acq_stop as ISO String Dates
            a_live as ISO Period
               
            Returns:
                a Decimal to avoid carrying numerical arithemic inprecision errors
                To get a float do float(Decimal) and To get an int int(Decimal)
         
            Raises:
            exception if cannot connect to the server
        """
        
        super(NobleGasDecayCorrector,self).__init__()
        
        self._coll_stop  = -1
        self._coll_start = -1
        self._acq_stop   = -1
        self._acq_start  = -1
        self._a_real     = -1
        
        self._t_count    = -1
        self._t_real     = -1
        self._t_live     = -1
        self._t_prep     = -1
        
        self.set_time_information(a_coll_start, a_coll_stop, a_acq_start, a_acq_stop, a_real)
        
        
    def set_time_information(self,a_coll_start,a_coll_stop,a_acq_start,a_acq_stop,a_real):
        """
           add the necessary time info
        """
        self._coll_stop  = a_coll_stop
        self._coll_start = a_coll_start
        self._acq_stop   = a_acq_stop
        self._acq_start  = a_acq_start
        self._a_real     = a_real
        
        self._calculate_time_coeffs()
        
        
    def _calculate_time_coeffs(self):
        """"""
        
        self._t_count = str(time_utils.getDifferenceInTime(self._coll_start,self._coll_stop))
        self._t_prep  = str(time_utils.getDifferenceInTime(self._coll_stop,self._acq_start))
        self._t_real  = str(time_utils.getDifferenceInTime(self._acq_start,self._acq_stop))
        self._t_real  = str(self._a_real)
        
    def _calculate_fi(self,a_half_life_string):
        """ calculate f(i) = A^2/(1-exp(-A*tcount)*exp(-A*tprep)*(1-exp(-A*treal) 
            with A = ln(2)/half-life iso in sec.
            
            Args:
            a_half_life_string  : the half life value as a string
               
            Returns:
                a Decimal to avoid carrying numerical arithemic inprecision errors
                To get a float do float(Decimal) and To get an int int(Decimal)
         
            Raises:
            exception if cannot connect to the server
        """
        
        # get a Decimal object 
        half_life   = convert_half_life_in_sec(a_half_life_string)
        
        A_coeff     = Decimal(2).ln() / half_life
        
        A_tcount    = A_coeff * Decimal(self._t_count)
        A_tprep     = A_coeff * Decimal(self._t_prep)
        A_treal     = A_coeff * Decimal(self._t_real)
        
        first_exp = (1-math.exp(-A_tcount))
        sec_exp   = math.exp(-A_tprep)
        third_exp = (1-math.exp(-A_treal))
        
        f_divider   = (first_exp*sec_exp*third_exp)
        str_divider = str(f_divider)
        
        fi_result   = (pow(A_coeff,2) / Decimal(str_divider) )
                                         
        return fi_result
        
    def undecay_correct(self,a_isotope_name,a_activity_concentration):
        """ decay correct the values passed """
         
        half_life_string = NobleGasDecayCorrector.c_default_half_life.get(a_isotope_name,None)
        
        if half_life_string == None:
            raise Exception("No defined half_life for %s"%(a_isotope_name))
       
        fi = self._calculate_fi(half_life_string)
        
        return Decimal(str(a_activity_concentration)) / fi 
    
    def undecay_correct_XE133(self,a_XE133_activity_concentration,a_XE133M_activity_concentration):
        """ undecay correction for XE133 is special due to the metastable isotopes """
        
        XE133_half_life_string  = NobleGasDecayCorrector.c_default_half_life.get('XE-133',None)
        XE133M_half_life_string = NobleGasDecayCorrector.c_default_half_life.get('XE-133M',None)
        
        fi_XE133  = self._calculate_fi(XE133_half_life_string)
        fi_XE133M = self._calculate_fi(XE133M_half_life_string)
        
        lambda3_coeff   = Decimal(2).ln() / convert_half_life_in_sec(XE133_half_life_string)
        lambda6_coeff   = Decimal(2).ln() / convert_half_life_in_sec(XE133M_half_life_string)
        
        lbdas = lambda3_coeff / (lambda6_coeff - lambda3_coeff)
        
        return (1/fi_XE133) * Decimal(str(a_XE133_activity_concentration)) + (lbdas*((1/fi_XE133) - (1/fi_XE133M))*Decimal(str(a_XE133M_activity_concentration)))

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
                a Decimal to avoid carrying numerical arithemic inprecision errors
                To get a float do float(Decimal) and To get an int int(Decimal)
        
        Raises:
            None
    """
    #use scanf to parse the string
    scan_result = ctbto.common.scanf_util.scanf("%s %c", a_half_life_string)
    
    if len(scan_result) != 2:
        raise Exception("Did not recognise the following string as a valid half-life")
    
    number,time_unit = scan_result
    
    # if this is zero then there is a problem
    result = Decimal(time_unit_to_sec.get(time_unit,0)) * Decimal(number)
    
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
       
        self.assertEqual(452995.2,float(r))
       
        r = convert_half_life_in_sec("22.300 Y")
       
        self.assertEqual(703719449.800,float(r))
    
    def testCalculateFi(self):
        
        coll_start = time_utils.getDateTimeFromISO8601('2009-04-06T08:48:00')
        coll_stop  = time_utils.getDateTimeFromISO8601('2009-04-06T20:48:00')
        
        acq_start = time_utils.getDateTimeFromISO8601('2009-04-07T03:48:58')
        acq_stop  = time_utils.getDateTimeFromISO8601('2009-04-07T14:58:58')
        
        live = 40201
        
        #activity concentration
        #XE_135_conc = 0.23472596729190701
        XE_135_conc = 0.23472596729190701
                                            #(a_coll_start=0,         a_coll_stop=0,        a_acq_start=0         a_acq_stop=0,       a_live=0)
        nbCorrector = NobleGasDecayCorrector(coll_start,coll_stop,acq_start,acq_stop,live)
        
        v = nbCorrector.undecay_correct('XE-135', XE_135_conc)
        
        print "V = %f"%(float(v)) 
   

if __name__ == '__main__':
    tests()     