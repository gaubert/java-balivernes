#!/home/smd/aubert/public/infrasound/infrasound_profile_runtime/bin/python

from netCDF4 import Dataset
import time
import numpy 

#create file
dataset = rootgrp = Dataset('test.nc', 'w', format='NETCDF4')

#create dimension
dataset.createDimension('longitude', 1)
dataset.createDimension('latitude', 1)
dataset.createDimension('time', 1)
dataset.createDimension('altitude', 361)
dataset.createDimension('loc_name', 1)

#create basic variables
the_time  = dataset.createVariable('time', 'f8', ('time'))
lat       = dataset.createVariable('latitude', 'f4', ('latitude'))
lon       = dataset.createVariable('longitude', 'f4', ('longitude'))
altitudes = dataset.createVariable('altitude', 'f4', ('altitude'))

# create loc_name
loc_name  = dataset.createVariable('loc_name', str,('loc_name'))

# create param variables
# temperature
t         = dataset.createVariable('t','f4',('time', 'altitude', 'latitude', 'longitude', 'loc_name'))
# u and v wind components
u         = dataset.createVariable('u','f4',('time', 'altitude', 'latitude', 'longitude', 'loc_name'))
v         = dataset.createVariable('v','f4',('time', 'altitude', 'latitude', 'longitude', 'loc_name'))
# log surface pressure
lnsp      = dataset.createVariable('lnsp','f4',('time', 'altitude', 'latitude', 'longitude', 'loc_name'))
# Q (humidity)
q         = dataset.createVariable('q','f4',('time', 'altitude', 'latitude', 'longitude', 'loc_name'))
# geopotential (no altitude)
z         = dataset.createVariable('z','f4',('time', 'latitude', 'longitude', 'loc_name'))

#dataset.sync()

# add attributes
dataset.description = 'CTBTO Infrasound wind profiles'
dataset.history     = 'Created ' + time.ctime(time.time()) + ' by infra-profile-generator-v1.2.2'
dataset.source      = 'infra-profile-generator-v1.2.2'
dataset.version     = 'infrasound profile v1.0-20090801'
#dataset.station     = 'IS42'
lat.units           = 'degrees north'
lat.long_name       = 'Latitude'
lon.units           = 'degrees east'
lon.long_name       = 'Longitude'
altitudes.units     = 'm'
altitudes.long_name = 'Altitude'
loc_name.units      = '-'
loc_name.long_name  = 'Location name'
the_time.units      = 'hours since 0001-01-01 00:00:00.0'
the_time.calendar   = 'gregorian'
the_time.long_name  = 'Time'
# param attributes
t.units             = 'K'
t.long_name         = 'Temperature'
u.units             = 'm s**-1'
u.long_name         = 'U velocity'
v.units             = 'm s**-1'
v.long_name         = 'V velocity'
lnsp.units          = '-'
lnsp.long_name      = 'Logarithm of surface pressure'
q.units             = 'kg kg**-1'
q.long_name         = 'Specific Humidity'
z.units             = 'm**2 s**-2'
z.long_name         = 'Geopotential'

# add altitude levels
#0, 500, 1000, 1500, 2000, 2500, 3000, .....
alts = numpy.arange(0,180500,500)
print 'len(alts) =\n',len(alts)
print 'alts =\n',alts

altitudes[:] = alts
print 'altitudes =\n',altitudes[:]



# close netcdf file
dataset.close()



