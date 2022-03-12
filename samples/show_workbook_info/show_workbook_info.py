############################################################
# Step 1)  Use Datasource object from the Document API
############################################################
from tableaudocumentapi import Workbook
import xml.etree.ElementTree as ET

############################################################
# Step 2)  Open the .tds we want to explore
############################################################
sourceTWBX = Workbook('geocoding.twbx')

############################################################
# Step 3)  List out info from the TWBX
############################################################
print('----------------------------------------------------------')
print('-- Info for our .twbx:')
print('--   name:\t{0}'.format(sourceTWBX.filename))
print('--   CONTENTS')
print('--   dashboards:\t{0}'.format(len(sourceTWBX.dashboards)))
for dash in sourceTWBX.dashboards:
    print("--      {}".format(dash))

print('--   datasources:\t{0}'.format(len(sourceTWBX.datasources)))
for data in sourceTWBX.datasources:
    print("--      {}".format(data.name))

print('--   worksheets:\t{0}'.format(len(sourceTWBX.worksheets)))
for data in sourceTWBX.worksheets:
    print("--      {}".format(data))

print('--   shapes:\t{0}'.format(len(sourceTWBX.shapes)))
for shape in sourceTWBX.shapes:
    print("--      {}".format(shape))
print('----------------------------------------------------------')

worksheets = sourceTWBX.worksheets
for worksheet in worksheets:
    print("worksheet: {}".format(worksheet))
    for datasource in sourceTWBX.datasources:
        print("-- datasource: {}".format(datasource.name))
        for count, field in enumerate(datasource.fields.values()):
            if worksheet in field.worksheets:
                print(field)
