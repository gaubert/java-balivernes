import datetime
import time

from ctbto.common import scanf

def getToday():
    """ return today in iso format """
    today = datetime.date.today()
    return today.strftime('%Y-%m-%dT%H:%M:%S')

def getYesterday():
    """ return yesterday in so format """
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(1)
    return yesterday.strftime('%Y-%m-%dT%H:%M:%S')

def getTomorrow():
    """ return tomorrow in so format """
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(1)
    return tomorrow.strftime('%Y-%m-%dT%H:%M:%S')

def getDateTimeFromISO8601(aISOStr):
    """ transform a datetime object in ISO 8601 string """

    # if there is a no T, there is no time component add it T00:00:00 to the date
    if not aISOStr.find('T'):
        the_str = '%sT00:00:00'
    else:
        the_str = aISOStr
    
    return datetime.datetime.strptime(the_str,'%Y-%m-%dT%H:%M:%S')
    
def getOracleDateFromISO8601(aISOStr):
    """ transform an ISO8601 date into an Oracle compatible date.
        The transformation consist in removing the T and replacing it with space
    """
    return aISOStr.replace("T"," ")

def getOracleDateFromDateTime(aDateTime):
    
    s = str(aDateTime).split('.')
    return s[0]

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

def transformISO8601PeriodInFormattedTime(aPeriod):
    """ get an ISO period seconds such as PT29405s and transform it into DD-HH-MM-SS"""
    
    # deal with negative values in that case it will start with - and it has to be stripped
    period = aPeriod.strip('-')
    
    # extract seconds value
    res = scanf("PT%dS",period)
    
    if res == None or len(res) == 0:
        # Error
        raise ValueError("Unvalid Period %s. The only acceptable format is PT3212S"%(period))
    else:
        return getSecondsInFormattedTime(res[0])
    

def getSecondsInFormattedTime(aSec):
    """ return time in DD-HH-MM-SS """
    
    nb_of_days  = 0
    nb_of_hours = 0
    nb_of_min   = 0
    nb_of_sec   = 0
    
    a_day   = 86400
    an_hr   = 3600
    a_min   = 60
    
    rest = aSec
    
    # divide by day
    div = rest/a_day 
    if div != 0:
        nb_of_days = div
        rest = rest % a_day
 
    if rest > 0:
        # divide by hours
        div = rest/an_hr
        if div != 0:
            nb_of_hours = div
            rest = rest % an_hr
         
    if rest > 0:
        nb_of_min = rest/a_min
        nb_of_sec = rest % a_min
    else:
        nb_of_sec = rest
       
    
    days_str  = "%s d"%(nb_of_days) if (nb_of_days > 0) else ""
    hours_str = "%s h"%(nb_of_hours) if (nb_of_hours > 0) else ""
    min_str   = "%s m"%(nb_of_min) if (nb_of_min > 0) else ""
    sec_str   = "%s s"%(nb_of_sec) if (nb_of_sec > 0) else ""
    
    return "%s %s %s %s"%(days_str,hours_str,min_str,sec_str)
            
            
        
    
