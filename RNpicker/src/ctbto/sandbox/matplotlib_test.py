'''
Created on Aug 7, 2009

@author: aubert
'''


import matplotlib.pyplot as plt


def test_figure0():
    XE133= [0.03, 0.01, -0.05, 0.05, 0.05, 0.01, 0.01, 0.07, 0.04, 0.04, 0.01, 0.01]
    
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



if __name__ == '__main__':
    test_figure1()