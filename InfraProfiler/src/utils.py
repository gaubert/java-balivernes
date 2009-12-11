'''
Created on Sep 2, 2009

@author: guillaume.aubert@ctbto.org
'''
import os
import time
import itertools
import gc
import fnmatch

import error_commons


class FindError(error_commons.CLIError):
    """ find error """

    def __init__(self, a_error_msg):
        super(FindError,self).__init__()
        self._error_message = a_error_msg
    
    def get_message_error(self):
        return self._error_message


def ftimer(func, args, kwargs, result = [], number=1, timer=time.time): #IGNORE:W0102
    """ time a func or object method """
    it = itertools.repeat(None, number)
    gc_saved = gc.isenabled()
    
    try:
        gc.disable()
        t0 = timer()
        for i in it:                  #IGNORE:W0612
            r = func(*args, **kwargs) #IGNORE:W0142
            if r is not None:
                result.append(r)
            t1 = timer()
    finally:
        if gc_saved:
            gc.enable()
        
    return t1 - t0

def makedirs(a_path):
    """ my own version of makedir """
    
    if os.path.isdir(a_path):
        # it already exists so return
        return
    elif os.path.isfile(a_path):
        raise Exception("a file with the same name as the desired dir, '%s', already exists."%(a_path))

    os.makedirs(a_path)


def ffind(path, shellglobs=None, namefs=None, relative=True):
    """
    Finds files in the directory tree starting at 'path' (filtered by
    Unix shell-style wildcards ('shellglobs') and/or the functions in
    the 'namefs' sequence).

    The parameters are as follows:

    - path: starting path of the directory tree to be searched
    - shellglobs: an optional sequence of Unix shell-style wildcards
      that are to be applied to the file *names* found
    - namefs: an optional sequence of functions to be applied to the
      file *paths* found
    - relative: a boolean flag that determines whether absolute or
      relative paths should be returned

    Please not that the shell wildcards work in a cumulative fashion
    i.e. each of them is applied to the full set of file *names* found.

    Conversely, all the functions in 'namefs'
        * only get to see the output of their respective predecessor
          function in the sequence (with the obvious exception of the
          first function)
        * are applied to the full file *path* (whereas the shell-style
          wildcards are only applied to the file *names*)

    Returns a sequence of paths for files found.
    """
    if not os.access(path, os.R_OK):
        raise FindError("cannot access path: '%s'" % path)

    fileList = [] # result list
    try:
        for dir, _, files in os.walk(path):
            if shellglobs:
                matched = []
                for pattern in shellglobs:
                    filterf = lambda s: fnmatch.fnmatchcase(s, pattern)
                    matched.extend(filter(filterf, files))
                fileList.extend(['%s%s%s' % (dir, os.sep, f) for f in matched])
            else:
                fileList.extend(['%s%s%s' % (dir, os.sep, f) for f in files])
        if not relative: fileList = map(os.path.abspath, fileList)
        if namefs: 
            for ff in namefs: fileList = filter(ff, fileList)
    except Exception, exc: 
        raise FindError(str(exc))
    return(fileList)