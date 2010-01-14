'''
Created on Apr 3, 2009

@module: data_calculations

Module containing different kind of operations that can be performed on the data itself.

@author: Guillaume Aubert
         
'''

import logging

import ctbto.common.scanf_util
import ctbto.common.time_utils as time_utils

from decimal import Decimal
import math


class NobleGasDecayCorrector(object):
    """ Apply decay correction on the noble gas activity concentration  """
    
    XE131M = 'XE-131M'
    XE133M = 'XE-133M'
    XE135  = 'XE-135'
    XE133  = 'XE-133'
    
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

    def __init__(self,a_coll_start=0,a_coll_stop=0,a_acq_start=0,a_acq_stop=0,a_real = None):
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
        
        
    def set_time_information(self,a_coll_start,a_coll_stop,a_acq_start,a_acq_stop,a_real = None):
        """
           add the necessary time info
        """
        self._coll_stop  = a_coll_stop
        self._coll_start = a_coll_start
        self._acq_stop   = a_acq_stop
        self._acq_start  = a_acq_start
        
        self._calculate_time_coeffs(a_real)
        
        
    def _calculate_time_coeffs(self,a_real = None):
        """"""
        
        self._t_count = str(time_utils.getDifferenceInTime(self._coll_start,self._coll_stop))
        self._t_prep  = str(time_utils.getDifferenceInTime(self._coll_stop,self._acq_start))
        self._t_real  = str(time_utils.getDifferenceInTime(self._acq_start,self._acq_stop)) if a_real is None else a_real
        
    
    def _calculate_fi(self,a_half_life_string):
        """ calculate f(i) = (lambda*lambda*tcount*treal)/f(1)*f(2)*f(3)
            with 
            lambda = ln(2)/half-life) iso in sec.
            f(1)   = (1-exp(-tcount*lambda))
            f(2)   = (exp(-tprep*lambda)
            f(3)   = (1-exp(-treal*lambda)
            
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
        
        lambda_coeff     = Decimal(2).ln() / half_life
        
        t_count     = Decimal(self._t_count)
        
        first_exp   =  Decimal(str((1-math.exp(-t_count*lambda_coeff))))
        sec_exp     =  Decimal(str(math.exp(-(Decimal(self._t_prep))*lambda_coeff)))
        third_exp   =  Decimal(str((1-math.exp(-Decimal(self._t_real)*lambda_coeff))))
        
        fi_result = (lambda_coeff *lambda_coeff * t_count * Decimal(self._t_real)) / (first_exp*sec_exp*third_exp)
        
        #print("factor %s\n" %(fi_result))
                                         
        return fi_result
    
    def undecay_correct(self,  a_iso_type, *args):
        """ undecay correct for one unique nuclide.
            Except a_iso_type which defines the type of isotope and one or two concentrations.
            One in the case of XE131M, XE133M and XE135 two for XE133
        """
        
        if len(args) <= 0 and len(args) > 2:
            Exception("This method can accept only 1 or two variable arguments using the *args method")
        
        cls = self.__class__
        
        if a_iso_type in (cls.XE131M, cls.XE133M, cls.XE135):
            
            if len(args) != 1:
                Exception("Should only have one variable arg in the case of XE-131, XE-133M, XE-135")
            
            return self.undecay_correct_method1(a_iso_type, args[0])
        elif a_iso_type == cls.XE133:
            
            if len(args) != 2:
                Exception("Should have two variable args in the case of XE-133")
            
            return self.undecay_correct_method2(args[0], args[1])
        else:
            raise Exception("unknown type %s\n" % (a_iso_type))
    
    def undecay_correct_all(self, a_XE131M_act, a_XE133_act, a_XE133M_act, a_XE135_act):
        """ get all activities of all XE isotopes for a particular sample and undecay correct them 
        """
        
        xe131_res  = self.undecay_correct_method1('XE-131M', a_XE131M_act)
        
        xe133M_res = self.undecay_correct_method1('XE-133M', a_XE133M_act)
        
        xe133_res  = self.undecay_correct_method2(a_XE133_act, a_XE133M_act)
        
        xe135_res  = self.undecay_correct_method1('XE-135' , a_XE135_act)
        
        return (xe131_res, xe133_res , xe133M_res, xe135_res)
        
        
    def undecay_correct_method1(self,a_isotope_name, a_activity_concentration):
        """ decay correction method one used for XE135, XE133, XE131M 
        """
         
        half_life_string = NobleGasDecayCorrector.c_default_half_life.get(a_isotope_name,None)
        
        if half_life_string == None:
            raise Exception("No defined half_life for %s"%(a_isotope_name))
        
        #print("fi for %s\n" % (a_isotope_name) )
        fi = self._calculate_fi(half_life_string)
        
        return Decimal(str(a_activity_concentration)) / fi 
    
    def undecay_correct_method2(self, a_XE133_activity_concentration, a_XE133M_activity_concentration):
        """ undecay correction for XE133 is special due to the metastable isotopes """
        
        XE133_half_life_string  = NobleGasDecayCorrector.c_default_half_life.get('XE-133', None)
        XE133M_half_life_string = NobleGasDecayCorrector.c_default_half_life.get('XE-133M', None)
        
       
        fi_XE133  = self._calculate_fi(XE133_half_life_string)
        
        fi_XE133M = self._calculate_fi(XE133M_half_life_string)
        
        lambda3_coeff   = Decimal(2).ln() / convert_half_life_in_sec(XE133_half_life_string)
        lambda6_coeff   = Decimal(2).ln() / convert_half_life_in_sec(XE133M_half_life_string)
        
        lbdas = lambda3_coeff / (lambda6_coeff - lambda3_coeff)
        
        return (1/fi_XE133) * Decimal(str(a_XE133_activity_concentration)) \
               + (lbdas*((1/fi_XE133) - (1/fi_XE133M))*Decimal(str(a_XE133M_activity_concentration)))

TIME_UNIT_TO_SEC = { 
               'S' : 1 ,
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
    
    number, time_unit = scan_result
    
    # if this is zero then there is a problem
    result = Decimal(TIME_UNIT_TO_SEC.get(time_unit, 0)) * Decimal(number)
    
    if result == 0:
        raise Exception("The value %s in %s cannot be used as a time_unit" % (time_unit, a_half_life_string))
    
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
        
    
    def testCalculate(self):
        """ Caclulate uncorrected values for one sample"""
        
        coll_start = time_utils.getDateTimeFromISO8601('2009-01-01T12:00:00')
        coll_stop  = time_utils.getDateTimeFromISO8601('2009-01-02T11:30:00')
        
        acq_start = time_utils.getDateTimeFromISO8601('2009-01-02T12:30:00')
        acq_stop  = time_utils.getDateTimeFromISO8601('2009-01-03T12:31:00')
        
        #activity concentrations
        XE_131M_conc = 1.061635915
        XE_133_conc  = 112.7781
        XE_133M_conc = 13.74831626
        XE_135_conc  = 5.053032873
                        
        nbCorrector = NobleGasDecayCorrector(coll_start, coll_stop,acq_start, acq_stop)
        
        nbCorrector.undecay_correct(NobleGasDecayCorrector.XE131M, XE_131M_conc)
        
        (X_131M_uncorr , X_133_uncorr, X_133M_uncorr, X_135_uncorr) = nbCorrector.undecay_correct_all(XE_131M_conc, XE_133_conc, XE_133M_conc, XE_135_conc)
        
        print("131M  (corr, uncorr) = (%f, %f) \n, 133  (corr, uncorr) = (%f, %f) \n, 133M  (corr, uncorr) = (%f, %f) \n, 135  (corr, uncorr) = (%f, %f) \n" % \
              (XE_131M_conc, X_131M_uncorr, \
               XE_133_conc, X_133_uncorr, \
               XE_133M_conc, X_133M_uncorr, \
               XE_135_conc, X_135_uncorr) )

if __name__ == '__main__':
    tests()     