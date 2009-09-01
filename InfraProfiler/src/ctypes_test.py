#!/home/smd/aubert/public/infrasound/infrasound_profile_runtime/bin/python

import string
from ctypes import *

libg2s = cdll.LoadLibrary("/home/smd/aubert/public/infrasound/g2s_profile_generator/lib/libg2sclient.so")

print("libg2s = %s\n" % (libg2s) )

#
# call test_python
#
#method = libg2s.test_python
#x = c_double(0)
#print("x before calling method %s\n" % (x))
#method(byref(x))
#print("x after calling method %s\n" % (x))

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
lat_points = lat_arr(10,20)
lon_points = lon_arr(10,20)

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

# create the 3 array types
cz_t = c_double * nz * nb_points
uz_t = c_double * nz * nb_points
vz_t = c_double * nz * nb_points

cz = cz_t()
uz = uz_t()
vz = vz_t()

print("len(cz) = %s" %(len(cz)) )

print("Before to call g2sclient_pt")
g2sclient_pt(pt_err,lat_points, lon_points, pt_nb_points, pt_filename, pt_command, pt_nz, pt_dz, cz, uz, vz)

print("After to call g2sclient_pt")
print("cz = %s" %(cz) )
print("len(cz) = %s" %(len(cz)) )

for pt in range(nb_points):
   for lev in range(nz):
      print("pt_ind=%s,lev_ind=%s,celerity=%s,uwind=%s,vwind=%s\n" %(pt, lev, cz[pt][lev], uz[pt][lev], vz[pt][lev]))

