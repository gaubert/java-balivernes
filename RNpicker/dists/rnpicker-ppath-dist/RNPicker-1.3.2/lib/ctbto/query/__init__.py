''' 
    Use this method to hide the module name (the file name) and import the Classes in the package 
    Use this to export Classes public to the package (used outside of the package)
'''
__all__ = []
for subpackage in ['parser']:
    try:
       exec 'import ' + subpackage
       exec 'from ' + subpackage + ' import *'
       __all__.append( subpackage )
    except ImportError:
       pass