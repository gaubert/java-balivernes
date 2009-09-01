#!/home/smd/aubert/public/infrasound/infrasound_profile_runtime/bin/python

import sys
import string
from ctypes import *

from netCDF4 import Dataset, date2num
import datetime
import time
import numpy 

def call_g2s():

   libg2s = cdll.LoadLibrary("/home/smd/aubert/public/infrasound/g2s_profile_generator/lib/libg2sclient.so")

   print("libg2s = %s\n" % (libg2s) )

   # call the g2sclient
   g2sclient_pt = libg2s.g2sclient_pt

   err       = -1
   pt_err    = byref(c_int(err))

   nb_points    = 2
   pt_nb_points = byref(c_int(nb_points))

   # Prepare type double * nb of lat points
   lat_arr = c_double * nb_points
   lon_arr = c_double * nb_points

   # allocate and add values (lat=10 and lon=10)
   lat_points = lat_arr(10,45)
   lon_points = lon_arr(10,-45)

   nz = 401 
   pt_nz = byref(c_int(401))
   dz = 0.5
   pt_dz = byref(c_double(0.5))
   #command     = 'extract'
   # need to pad with space chars the command string
   command     = string.ljust('extract',128)
   pt_command  = c_char_p(command)

   #filename    = '/home/smd/aubert/public/infrasound/G2SGCSx2009071518_HWM07.bin'
   filename    = string.ljust('./G2SGCSx2009071518_HWM07.bin',128)
   pt_filename = c_char_p(filename)
   
   # add datetime
   the_date = '2009071518'
   dt = datetime.datetime.strptime(the_date, '%Y%m%d%H')

   # create the 3 array types
   cz_t = c_double * nz * nb_points
   uz_t = c_double * nz * nb_points
   vz_t = c_double * nz * nb_points

   cz = cz_t()
   uz = uz_t()
   vz = vz_t()

   print("Calling g2sclient_pt")
   g2sclient_pt(pt_err,lat_points, lon_points, pt_nb_points, pt_filename, pt_command, pt_nz, pt_dz, cz, uz, vz)
   print("After to call g2sclient_pt")
   print("cz = %s" %(cz) )
   print("len(cz) = %s" %(len(cz)) )

   #if pt_err:
   #   return pt_err

   #for pt in range(nb_points):
   #   for lev in range(nz):
   #      print("pt_ind=%s,lev_ind=%s,celerity=%s,uwind=%s,vwind=%s\n" %(pt, lev, cz[pt][lev], uz[pt][lev], vz[pt][lev]))

   err = create_netcdf(lat_points, lon_points, nz, cz, uz, vz, dt, 'dummy_loc')

   return err

def create_netcdf(a_lat_points,a_lon_points, a_nb_levels, a_celerity_arr, a_u_arr, a_v_arr, a_time,a_loc_name):
   """
    dimensions:
      altitude = 401;
      profile  = 1 ;

    variables:
       float altitude(altitude) ;
         altitude:long_name = "height above mean sea level" ;
         altitude:units = "km" ;
         altitude:positive = "up" ; 

       double time(profile);
         time:long_name = "time" ;
         time:units = "days since 1970-01-01 00:00:00" ;
       
       float lon(profile);
         lon:long_name = "longitude" ;
         lon:units = "degrees_east" ;

       float lat(profile);
         lat:long_name = "latitude" ;
         lat:units = "degrees_north" ;

       float celerity(profile, altitude) ;
         celerity:long_name = "celerity" ;
         celerity:units = "m s**-1" ;
         celerity:coordinates = "time lon lat altitude" ;

       float u(profile, altitude) ;
         u:long_name = "U velocity" ;
         celerity:units = "m s**-1" ;
         celerity:coordinates = "time lon lat altitude" ;

       float v(profile, altitude) ;
         u:long_name = "V velocity" ;
         celerity:units = "m s**-1" ;
         celerity:coordinates = "time lon lat altitude" ;
   
       attributes:
          :CF\:featureType = "profile";
 

   """
   print("In create_netcdf")

   #create file
   #dataset = rootgrp = Dataset('./test.nc', 'w', format='NETCDF3_CLASSIC')
   dataset = rootgrp = Dataset('./test.nc', 'w', format='NETCDF4')
   #dataset = rootgrp = Dataset('./test.nc', 'w', format='NETCDF4_CLASSIC')

   #create dimension
   dataset.createDimension('altitude', a_nb_levels)
   dataset.createDimension('profile', len(a_lat_points))

   #create basic variables
   the_time  = dataset.createVariable('time',      'f8', ('profile'))
   lat       = dataset.createVariable('latitude',  'f4', ('profile'))
   lon       = dataset.createVariable('longitude', 'f4', ('profile'))
   altitudes = dataset.createVariable('altitude',  'f4', ('altitude'))

   # create loc_name
   #loc_name  = dataset.createVariable('loc_name', str,('profile'))


   # create param variables
   # u and v wind components
   u         = dataset.createVariable('u',   'f4',('profile', 'altitude'))
   v         = dataset.createVariable('v',   'f4',('profile', 'altitude'))
   # celerity 
   c         = dataset.createVariable('c',    'f4',('profile','altitude'))

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
   #loc_name.units      = '-'
   #loc_name.long_name  = 'Location name'
   the_time.units      = 'hours since 0001-01-01 00:00:00.0'
   the_time.calendar   = 'gregorian'
   the_time.long_name  = 'Time'
   # param attributes
   u.units             = 'm s**-1'
   u.long_name         = 'U velocity'
   v.units             = 'm s**-1'
   v.long_name         = 'V velocity'
   c.units             = 'm s**-1'
   c.long_name         = 'Celerity'

   # create altitude
   alts = numpy.arange(0,500*a_nb_levels,500)

   altitudes[:] = alts
   print 'altitudes =\n',altitudes[:]

   # add lat,lon
   lat[:]    = a_lat_points
   lon[:]    = a_lon_points
   #not used for the moment
   loc_name  = a_loc_name

   #add time
   dt  = date2num(a_time, "days since 1970-01-01 00:00:00", calendar='gregorian') 

   the_time[:] = [ dt, dt ]
   dataset.sync()

   c[:]=a_celerity_arr[:]
   u[:]=a_u_arr[:]
   v[:]=a_v_arr[:]

   dataset.sync()

   dataset.close()

   return 0


if __name__ == "__main__":

   #the_time = [1,2]
   #alts = numpy.arange(0,500*5,500)
   #alts_list = alts.tolist()
   #print(alts_list)
   #list = [0, 500]

   #num_cel = numpy.array( [ the_time, [3,4], list ] )
   #print(num_cel)
   #sys.exit(1)

   nb_points    = 3
   # Prepare type double * nb of lat points
   lat_arr = c_double * nb_points
   lon_arr = c_double * nb_points

   lat_points = lat_arr(10,11)
   lon_points = lon_arr(20,21)

   nz = 3

   cz_t = c_double * nz * nb_points
   uz_t = c_double * nz * nb_points
   vz_t = c_double * nz * nb_points

   cz=cz_t((100.0,120.0,140.0),(200.0,220.0,240.0),(300.0,320.0,340.0))
   uz=uz_t((100.0,120.0,140.0),(200.0,220.0,240.0),(300.0,320.0,340.0))
   vz=vz_t((100.0,120.0,140.0),(200.0,220.0,240.0),(300.0,320.0,340.0))

   c_arr = numpy.array(cz)
   print "c.shape = ", c_arr.shape

   err = call_g2s()

   sys.exit(1)

