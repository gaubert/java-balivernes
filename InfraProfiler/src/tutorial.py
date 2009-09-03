'''
Created on Sep 2, 2009

@author: aubert
'''

import netCDF4 

def read_netcdf(filename):
    file = netCDF4.Dataset(filename)
    
    profile  = file.dimensions['profile']
    altitude = file.dimensions['altitude']
    
    print("nb of points = %d, nb of altitudes = %d" %(len(profile), len(altitude)))
    
    for pt in xrange(0,len(profile)):
        print("====================================\n")
        print("point ind=%s, lat=%s, lon=%s\n" %(pt, file.variables['latitude'][pt], file.variables['longitude'][pt]) )
        print("------------------------------------\n")
        for alt in xrange(0,len(altitude)):
             print("alt ind=%s, alt val=%s, celerity=%s\n" %(alt, file.variables['altitude'][pt], file.variables['c'][pt][alt]) )
    
    
    file.close()


if __name__ == "__main__":
    
    read_netcdf("/tmp/G2SGCSx2009083103_HWM07.bin.nc")
    
    