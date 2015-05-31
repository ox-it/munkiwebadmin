#
# Utility routines to access other parts of the application
#
# N.B Caching probably needs implementing for some/all of
# these routines
#

from manifests.models import Manifest
from catalogs.models import Catalog

def get_cataloglist():
    return Catalog.list()

def get_manifestlist():
    return Manifest.list()

def get_packagenamelist():
    catalogs = Catalog()
    package_details = []
    for cat in catalogs.list():
       package_details = package_details + catalogs.detail(cat)
  
    package_list = list( set( [ pkg['name'] for pkg in package_details] ) ) 

    return package_list

def make_selectlist(item_list, nullvalue='--------'):
    return_list =  map(lambda x: (x,x), sorted( item_list ) )
    return [ (None, nullvalue) ] + return_list

def get_manifest_selectlist( ):
    return make_selectlist(get_manifestlist(), '(no manifest selected)' )

def get_catalog_selectlist( ):
    return make_selectlist(get_cataloglist(), '(no catalog selected)' )

def get_packagename_selectlist( ):
    return make_selectlist(get_packagenamelist(), '(no package selected)' )


