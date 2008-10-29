__all__ = []
for subpackage in ['connections', 'datafetchers', 'sqlrequests']:
    try: 
       exec 'import ' + subpackage
       __all__.append( subpackage )
    except ImportError:
       pass

