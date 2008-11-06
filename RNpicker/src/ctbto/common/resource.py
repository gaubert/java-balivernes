"""
   Manage external Resources. A cli resource (command line ressource) is an information passed in the command line or with an ENV variable (to be implemented => or as part of a configuration file if the file)
   For example the Conf object is defining a ressource called conf-path as 
"""


import sys
import os

class ResourceError(Exception):
    """Base class for ressource exceptions"""

    cErrs = {
                -1: "Ressource Error",
            }

    def __init__(self,aMsg):
        self.args   = (-1, aMsg)
        self.errno  = -1
        self.errmsg = aMsg


class Resource(object):
    """
        Class read a ressource.
        It can be read first from the Command Line, then from the ENV as an env variable and finally from a conf file 
    """
    
    def __init__(self,CliArgument=None,EnvVariable=None,ConfProperty=None): 
      """ 
          Default Constructor.
          It is important to understand that there is precedence between the different ways to set the ressource:
          - get from the command line if defined otherwise get from the Env variable if defined otherwise get from the conf file otherwise error
       
           Args:
              CliArgument : The command line argument name
              EnvVariable : The env variable name used for this ressource
              ConfProperty: It should be a tupr containing two elements (group,property)
       """
      
      self._cliArg   = CliArgument.lower() if CliArgument is not None else None
      self._envVar   = EnvVariable.upper() if EnvVariable is not None else None
      
      if ConfProperty is not None:
         (self._confGroup,self._confProperty) = ConfProperty
      else:
         self._confGroup    = None
         self._confProperty = None
      
    def setCliArgument(self,CliArgument):
        self._cliArg = CliArgument.lower()
        
    def setEnvVariable(self,EnvVariable):
        self._envVar = EnvVariable
    
    def _getValueFromTheCommandLine(self):
      """
          internal method for extracting the value from the command line.
          All command line agruments must be lower case (unix style).
          To Do support short and long cli args.
           
           Returns:
             the Value if defined otherwise None
      """
          
      # check precondition
      if self._cliArg == None:
        return None
    
      # look for cliArg in sys argv
      for arg in sys.argv:
         if arg.lower() == self._cliArg:
           i = sys.argv.index(arg)
           print "i = %d, val = %s\n"%(i,sys.argv[i])
           if len(sys.argv) <= i:
             # No more thing to read in the command line so quit
             print "Ressource: Commandline argument %s has no value\n"%(self._cliArg)
             return None 
           else:
            print "i+1 = %d, val = %s\n"%(i+1,sys.argv[i+1])
            return sys.argv[i+1]
            

    def _getValueFromEnv(self):
      """
          internal method for extracting the value from the env.
          All support ENV Variables should be in uppercase.
           
           Returns:
             the Value if defined otherwise None
      """
      
      # precondition
      if self._envVar == None:
          return None
     
      return os.environ.get(self._envVar,None)
      
    def _getFromConf(self):
        """
           Try to read the info from the Configuration if possible
        """
        if (self._confGroup is not None) and (self._confProperty is not None):
            # TODO: do something with the conf 
            if Conf.can_be_instanciated():
                return Conf.get_instance().get(self._confGroup,self._confProperty)
        
        return None
          
        
    def getValue(self,aRaiseException=True):
       """
           Return the value of the Resource as a string.
           - get from the command line if defined otherwise get from the Env variable if defined otherwise get from the conf file otherwise error
              
           Arguments:
              aRaiseException: flag indicating if an exception should be raise if value not found
           Returns:
              value of the Resource as a String
       
           Raises:
              exception CTBTOError if the aRaiseExceptionOnError flag is activated
       """
       
       # get a value using precedence rule 1) command-line, 2) ENV, 3) Conf
       val = self._getValueFromTheCommandLine()
       if val is None:
           val = self._getValueFromEnv()
           if val is None:
               val = self._getFromConf()
               if (val is None) and aRaiseException:
                  raise ResourceError("Cannot find any ressource having the commandline argument %s, nor the Env Variable %s, nor the Conf Group:[%s] and Property=%s\n"%(self._cliArg,self._envVar,self._confGroup,self._confProperty))
    
       # we do have a val
       return val
   
    def _get(self,conv):
      """
           Private _get method used to convert to the right expected type (int,float or boolean).
           Strongly inspired by ConfigParser.py
              
           Returns:
              value converted into the asked type
       
           Raises:
              exception ValueError if conversion issue
      """
      return conv(self.getValue())

    def getValueAsInt(self):
      """
           Return the value as an int
              
           Returns:
              value converted into the asked type
       
           Raises:
              exception ValueError if conversion issue
      """
      return self._get(int)

    def getValueAsFloat(self):
      """
           Return the value as a float
              
           Returns:
              value converted into the asked type
       
           Raises:
              exception ValueError if conversion issue
      """
      return self._get(float)

    _boolean_states = {'1': True, 'yes': True, 'true': True, 'on': True,
                       '0': False, 'no': False, 'false': False, 'off': False}

    def getValueAsBoolean(self):
        """
           Return the value as a boolean
              
           Returns:
              value converted into the asked type
       
           Raises:
              exception ValueError if conversion issue
        """
        v = self.getValue()
        if v.lower() not in self._boolean_states:
            raise ValueError, 'Not a boolean: %s' % v
        return self._boolean_states[v.lower()]
   
   
def tests():
  # set command line
  sys.argv.append("--LongName")
  sys.argv.append("My Cli Value")
   
  r = Resource(CliArgument="--LongName",EnvVariable=None) 
  
  print "Val from commandLine [%s]\n"%(r.getValue())
  
  os.environ["MYENVVAR"]="My ENV Value"
  
  r = Resource(CliArgument=None,EnvVariable="MYENVVAR")
  
  print "Val from ENV [%s]\n"%(r.getValue())
  
  r = Resource(CliArgument="--LongName",EnvVariable="MYENVVAR")
  
  print "Check precedence Rule. Should get the Cli Val first [%s]=[My Cli Value]\n"%(r.getValue())
  
  os.environ["MYENVVAR"]="yes"
  
  r = Resource(CliArgument=None,EnvVariable="MYENVVAR")
  
  print "Get Boolean Value =%s. return res of (r.getValueAsBoolean) == True : %s \n"%(r.getValueAsBoolean(),(r.getValueAsBoolean() == True))
  
  os.environ["MYENVVAR"]="4"
  
  r = Resource(CliArgument=None,EnvVariable="MYENVVAR")
  
  print "Get Int Value =%s. return res of (r.getValueAsInt()+1) = %s \n"%(r.getValueAsInt(),(r.getValueAsInt()+1))
  
  os.environ["MYENVVAR"]="4.345"
  
  r = Resource(CliArgument=None,EnvVariable="MYENVVAR")
  
  print "Get Float Value =%s. return res of (r.getValueAsFloat()+1) = %s \n"%(r.getValueAsFloat(),(r.getValueAsFloat()+1))
  
  
  
  
if __name__ == '__main__':
    # call little tests
    tests()     
 
       