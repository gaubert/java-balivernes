import datetime
import time

def getDateTimeFromISO8601(aISOStr):
    """ transform a datetime object in ISO 8601 string """
    
    return datetime.datetime.strptime(aISOStr,'%Y-%m-%dT%H:%M:%S')
    
def getOracleDateFromISO8601(aISOStr):
    """ transform an ISO8601 date into an Oracle compatible date.
        The transformation consist in removing the T and replacing it with space
    """
    return aISOStr.replace("T"," ")

def getISO8601fromDateTime(aDateTime):
    
    s = str(aDateTime).split('.')
    return s[0].replace(" ","T")

def getDifferenceInTime(aStart,aStop):
    """ return in seconds the difference between the two passed dates doing (aStop - aStart)"""
    
    # check if the two object are start and stop dates
    sec_start = time.mktime(aStart.timetuple())
    
    sec_stop  = time.mktime(aStop.timetuple())
    
    return sec_stop - sec_start

def getSecondsInHours(aSec):
    
    return float(aSec)/float(3600)
