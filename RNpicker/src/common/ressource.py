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
    
    def __init__(self,CliArgument=None,EnvVariable=None): 
      """ 
          Default Constructor.
          It is important to understand that there is precedence between the different ways to set the ressource:
          - get from the command line if defined otherwise get from the Env variable if defined otherwise get from the conf file otherwise error
       
           Args:
              CliArgument : The command line argument name
              EnvVariable : The env variable name used for this ressource
       """
      
      self._cliArg   = CliArgument.lower() if CliArgument is not None else None
      self._envVar   = EnvVariable.upper() if EnvVariable is not None else None
      #TODO be implemented  
      self._confVal  = None   
      
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
     
      if os.environ[self._envVar]:
         return os.environ[self._envVar]
      else:
         return None
      
    def _getFromConf(self):
        """
           Get from conf. To be done.
        """
        return None
        
    def getValue(self):
       """
           Return the value of the Resource as a string.
           - get from the command line if defined otherwise get from the Env variable if defined otherwise get from the conf file otherwise error
              
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
               if val is None:
                   raise ResourceError("Cannot find any ressource having the commandline argument %s, nor the Env Variable %s, nor the Conf value %s\n"%(self._cliArg,self._envVar,self._confVal))
    
       # we do have a val
       return val
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
  
  
if __name__ == '__main__':
    # call little tests
    tests()     
 
       