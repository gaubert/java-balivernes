#!/usr/bin/env python

import os
import sys
import math

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, '..'))

from pygooglechart import ScatterChart

import settings
import helper

def scatter_circle():
    chart = ScatterChart(settings.width, settings.height, 
                         x_range=(0, 100), y_range=(0, 100))
    steps = 40
    xradius = 25
    yradius = 45
    xmid = 50
    ymid = 50
    xlist = []
    ylist = []
    for angle in xrange(0, steps + 1):
        angle = float(angle) / steps * math.pi * 2
        xlist.append(math.cos(angle) * xradius + xmid)
        ylist.append(math.sin(angle) * yradius + ymid)
    chart.add_data(xlist)
    chart.add_data(ylist)
    chart.add_data(range(len(ylist)))
    chart.add_marker(0, 1.0, 'o', '00ff00', 10)
    chart.download('scatter-circle.png')

def scatter_bg():
   
    chart = ScatterChart(width=100, height=100 ,x_range=(0, 10), y_range=(0, 10))

    xlist = []

    data_line1 = "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0"
    data_line2 = "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0"
    data_line3 = "0 0 0 0 0 0 1 0 0 0 0 0 0 1 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0"
    data_line4 = "0 2 1 1 6 9 7 5 4 3 2 2 1 3 2 2 2 5 1 0 1 4 3 1 4 2 2 2 4 6 1 0 3 2 0 2 0 1 1 5 1 2 2 2 0 8 1 3 1 2 2 1 1 3 3 1 2 1 2 0 0 0 2 3 1 2 1 1 4 0 1 3 0 0 1 1 0 1 0 2 1 1 1 2 0 2 1 0 1 1 1 0 0 1 1 2 2 2 0 4 0 1 1 1 0 0 1 1 0 0 0 3 0 1 1 0 0 0 1 0 1 1 2 2 3 0 0 0 3 0 0 2 1 0 0 0 0 0 1 1 1 1 0 0 0 0 1 1 1 0 1 1 2 1 0 1 1 1 1 2 1 0 1 1 0 0 0 0 0 2 0 0 1 1 1 0 0 0 0 0 0 1 1 0 0 0 0 1 2 0 0 0 0 1 0 0 1 0 0 0 0 0 0 0 0 2 2 1 0 1 1 0 0 1 0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 1 0 0 2 0 0 0 0 0 0 0 0 0 0 2 0 0 1 0 1 0 0 1 0 0 0"
    
    xlist1 = data_line1.split()
    xlist2 = data_line2.split()
    xlist3 = data_line3.split()
    xlist4 = data_line4.split()
    
    xlist = [5,0,0,0,0,0,0,0,0,0]
    ylist = [5,0,0,0,5,0,0,0,0,10]
    zlist = [30]
    #chart.add_marker(1, 4, 'o', '00ff00', 1)

    #data = helper.random_data(4, 2)
    #print "RandomData ",data

    #print "list1",map(int,xlist1)

    #chart.add_data(map(int,xlist1))
    #chart.add_data(map(int,xlist2))
    #chart.add_data(map(int,xlist3))
    #chart.add_data(map(int,xlist4))
    
    chart.add_data(map(int,xlist))
    chart.add_data(map(int,ylist))
    #chart.add_data(map(int,zlist))
    
    chart.set_title("a Title")
    
    
    chart.download('/tmp/myscatter.png')
    
    print "Bye %s"%(chart.get_url())
    
    #chart.add_data(data)




def main():
    scatter_bg()

if __name__ == '__main__':
    main()

