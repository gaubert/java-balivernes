''' 
    Use this method to hide the module name (the file name) and import the Classes in the package 
    Use this to export Classes public to the package (used outside of the package)
'''
__all__ = []
for subpackage in ['conf_helper','exceptions','resource','scanf']:
    try:
        exec 'import ' + subpackage     #IGNORE:W0122
        exec 'from ' + subpackage + ' import *' #IGNORE:W0122
        __all__.append( subpackage )
    except ImportError:      #IGNORE:W0704
        pass