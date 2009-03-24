

class CTBTOError(Exception):
    """Base class for All exceptions"""

    cErrs = {
                -1: "Generic Error",
            }

    def __init__(self,aErrno, aMsg):
        
        super(CTBTOError,self).__init__(aMsg)
        self.args   = (aErrno, aMsg)
        self.errno  = aErrno


