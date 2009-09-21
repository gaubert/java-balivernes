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

def another_time_example():
    """
    from datetime import date
    from matplotlib.pyplot import plot, show, title, \
         xlabel, ylabel, set, gca, bar, savefig

    d = {date(2003,11,1) : 12,
         date(2003,11,2) : 20,
         date(2003,11,5) : 20,
         date(2003,11,9) : 18,
         date(2003,11,12) : 2,
         }

    dates = [ (date, count) for date, count in d.items()]
    dates.sort()
    labels = [date.strftime('%b %d') for date, count in dates]

    dates, counts = zip(*dates)  # split to two lists
    days = [date.day for date in dates]  # get the day
    plot(days, counts)
    set(gca(), 'xticks', days)  # force the ticks to fall on the days
    set(gca(), 'xticklabels', labels)  # force the ticks to fall on the days
    ylabel('count')

    show()
    """
    pass

def time2():
    import datetime
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.dates as mpldates
    import matplotlib.ticker as ticker
    
    date1 = datetime.date( 1952, 1, 1 )
    date2 = datetime.date( 2004, 4, 12 )
    delta = datetime.timedelta(days=100)
    dates = mpldates.drange(date1, date2, delta)
    s1 = np.random.rand(len(dates))
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot_date(dates, s1,'r.')
    ax.hold(True)
    s2 = np.random.rand(len(dates))
    ax.plot_date(dates, s2,'bo')
    ax.legend(('s1','s2'), numpoints=1)
    
    # only write ticklabels on the decades
    def fmtticks(x, pos=None):
        dt = mpldates.num2date(x)
        if dt.year%10: return ''
        return dt.strftime('%Y')
    
    # this fizes yhe tick labels
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(fmtticks))
    
    # this fixes the toolbar x coord
    ax.fmt_xdata = mpldates.DateFormatter('%Y-%m-%d')
    
    # this rotates the ticklabels to help with overlapping
    fig.autofmt_xdate()
    plt.show()


def test_my_plot():
    
    import matplotlib.pyplot as plt
    import pylab
    import matplotlib.dates as mdates
    from matplotlib.dates import YearLocator, MonthLocator, DayLocator, DateFormatter


    #read csv file and get the data
    (XE131M_dict, XE133M_dict, XE133_dict) = test_read_csv()
    
    # sort the dates
    sorted_dates   = sorted(set(XE133_dict.keys()))
    XE133_sorted_values   = []
    XE131M_sorted_values  = []
    XE133M_sorted_values  = []
    
    for k in sorted_dates:
        XE133_sorted_values.append(XE133_dict[k])
        XE131M_sorted_values.append(XE131M_dict[k])
        XE133M_sorted_values.append(XE133M_dict[k])
        
    
    #print("sorted_dates=%s\n" % (sorted_dates) )
    
    # figure
    fig = plt.figure()
    # change the figure margins
    fig.subplots_adjust(left=0.025, bottom=None, right=None, wspace=None, hspace=None)
    
    #send the figure size
    fig.set_size_inches([17., 6.])
    
    plot1 = fig.add_subplot(212)
    
    # create plot for XE133
    plot1.plot_date(pylab.date2num(sorted_dates), XE133_sorted_values, marker='^', color='y', label='xe133') 
    
    #add legend
    plt.legend(shadow=True, fancybox=True, bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.)
    
    leg = plot1.get_legend() # all the text.Text instance in the legend
    for ltext in leg.get_texts():
        ltext.set_fontsize('small')

    xaxis1 = plot1.xaxis
    
    # format xaxis with dates
    xaxis1.set_major_locator(MonthLocator())
    xaxis1.set_major_formatter(mdates.DateFormatter('%b-%y'))
    
    xaxis1.get_label().set_text('Monthly Report')
    
    print("dir(Axis) = %s\n"%(dir(xaxis1)))
    
    # for day formatting
    #xaxis.set_major_locator(DayLocator())
    #xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))

    plot1.set_ylim( (0, 20) )
    plot1.set_xlim( (dateutil.parser.parse('01-01-2008'), dateutil.parser.parse('01-01-2009') ) )
    
    plot1.set_title("CNX22, XE-133 History")
   
    #create plot for metastables
    plot2 = fig.add_subplot(211)
    
    plot2.plot_date(pylab.date2num(sorted_dates), XE131M_sorted_values, marker='.', color='b',label='xe131m') 
    plot2.plot_date(pylab.date2num(sorted_dates), XE133M_sorted_values, marker='.', color='r', label='xe133m')
    
    xaxis2 = plot1.xaxis
    
    xaxis2.set_major_locator(MonthLocator())
    xaxis2.set_major_formatter(mdates.DateFormatter('%b-%y'))
    
    plot2.set_ylim( (-1, 1.5) )
    
    plt.legend(shadow=True, fancybox=True, bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.)
    
    leg = plot2.get_legend() # all the text.Text instance in the legend
    for ltext in leg.get_texts():
        ltext.set_fontsize('small')

    plot2.set_title("CNX22, Metastables History")
    
     # to have tick names in diagonals
    fig.autofmt_xdate()
    
    #save figure
    plt.savefig('/tmp/example.png',format='png')
    
    plt.show()

def test_legend():
    from matplotlib.pyplot import *

    subplot(211)
    plot([1,2,3], label="test1")
    plot([3,2,1], label="test2")
    #legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=2, mode="expand", borderaxespad=0.)

    subplot(223)
    plot([1,2,3], label="test1")
    plot([3,2,1], label="test2")
    legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


    show()

    
def test_read_csv():
    import csv
    csvReader = csv.reader(open('/home/aubert/cnx22-XE133-XE131M-XE133M.csv'), delimiter=',', quotechar='"')
    
    XE133_dict  = {}
    XE131M_dict = {}
    XE133M_dict = {}
    
    # create a dict date -> val
    cpt = 0
    for row in csvReader:
        cpt += 1
        if cpt == 1:
            continue
       
        XE131M_dict[dateutil.parser.parse(row[0])] = row[1]
        XE133M_dict[dateutil.parser.parse(row[0])] = row[2]
        XE133_dict[dateutil.parser.parse(row[0])]  = row[3]
    
    #print("dict = %s\n"%(res_dict))
    return  (XE131M_dict, XE133M_dict, XE133_dict)

if __name__ == '__main__':
    #test_legend()
    test_my_plot()