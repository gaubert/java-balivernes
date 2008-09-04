import datetime
import time

def getDateTimeFromISO8601(aISOStr):
    """ transform a datetime object in ISO 8601 string """
    
    return datetime.datetime.strptime(aISOStr,'%Y-%m-%dT%H:%M:%S')
    

def getDifferenceInTime(aStart,aStop):
    """ return in seconds the difference between the two passed dates doing (aStop - aStart)"""
    
    # check if the two object are start and stop dates
    sec_start = time.mktime(aStart.timetuple())
    
    sec_stop  = time.mktime(aStop.timetuple())
    
    return sec_stop - sec_start
