############################################################
# Step 1)  Use Datasource object from the Document API
############################################################
from tableaudocumentapi import Datasource

############################################################
# Step 2)  Open the .tds we want to replicate
############################################################
sourceTDS = Datasource.from_file('world.tds')

############################################################
# Step 3)  List out info from the TDS
############################################################
print('----------------------------------------------------------')
print('-- Info for our .tds:')
print('--   name:\t{0}'.format(sourceTDS.name))
print('--   version:\t{0}'.format(sourceTDS.version))
print('----------------------------------------------------------')
