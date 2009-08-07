'''
Created on Aug 7, 2009

@author: aubert
'''


import matplotlib.pyplot as plt
import dateutil

XE133_Y = [0.03, 0.01, -0.05, 0.05, 0.05, 0.01, 0.01, 0.07, 0.04, 0.04, 0.01, 0.01]

XE133_LIGHT_Y = [0.03, 0.01, -0.05, 0.05, 0.05]
XE133_DATES   = ['2009-07-31 16:55', '2009-08-01 04:55', '2009-08-01 16:55', '2009-08-02 04:55', '2009-08-02 16:55']

dates = [dateutil.parser.parse(s) for s in XE133_DATES] 


def test_figure0():
    
    
    plt.plot([1,2,3])
    plt.ylabel('some numbers')
    plt.show()



def test_figure1():
    import numpy as np
    import matplotlib
    import matplotlib.pyplot as plt

    matplotlib.rcParams['axes.unicode_minus'] = False
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(10*np.random.randn(100), 10*np.random.randn(100), 'o')
    ax.set_title('My first Test')
    plt.show()
    
def test_multiple_figures():
    import matplotlib.pyplot as plt
    plt.figure(1)                # the first figure
    plt.subplot(211)             # the first subplot in the first figure
    plt.plot([1,2,3])
    plt.subplot(212)             # the second subplot in the first figure
    plt.plot([4,5,6])
    
    
    plt.figure(2)                # a second figure
    plt.plot([4,5,6])            # creates a subplot(111) by default
    
    plt.figure(1)                # figure 1 current; subplot(212) still current
    plt.subplot(211)             # make subplot(211) in figure1 current
    plt.title('Easy as 1,2,3')   # subplot 211 title

def test_time():
    import pylab, random
    from datetime import datetime, timedelta
    import matplotlib.dates as mdates
    
    today = datetime.now()
    
    dates = [today + timedelta(days=i) for i in range(3)]
    values = [random.randint(1, 20) for i in range(3)]
    
    print("DATES:%s\n" % (pylab.date2num(dates) ) )
    print("VALUES:%s\n" % (values) )
    
    pylab.plot_date(pylab.date2num(dates), values, linestyle='-') 
    
    ax = pylab.gca()
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b-%d %H:%M')) 
    plt.show()

def test_my_plot():
    
    import matplotlib.pyplot as plt
    import pylab
    import matplotlib.dates as mdates
    from matplotlib.dates import YearLocator, MonthLocator, DayLocator, DateFormatter

    
    print("dates = %s\n" %(dates) )
    
    # create plot
    plt.plot_date(pylab.date2num(dates), XE133_LIGHT_Y, linestyle='-') 
    # format 
    xaxis = plt.gca().xaxis
    xaxis.set_major_locator(DayLocator())
    #xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d-%H:%M')) 
    xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))
    #xaxis.autoscale_view()

    plt.savefig('/tmp/example.png',format='png')
    
    #plt.plot_date(dates, XE133_LIGHT_Y, fmt='bo', tz=None, xdate=True, ydate=False)

    #plt.plot([1,2,3,4], [1,4,9,16], 'ro')
    #plt.axis([0, 6], [0, 20])
    plt.show()


if __name__ == '__main__':
    test_my_plot()