import csv              # so we can work with our database list (in a CSV file)

############################################################
# Step 1)  Use Workbook object from the Document API
############################################################
from tableaudocumentapi import Workbook

############################################################
# Step 2)  Open the .twb we want to replicate
############################################################
sourceWB = Workbook('Sample - Superstore.twb')

############################################################
# Step 3)  Use a database list (in CSV), loop thru and
#          create new .twb's with their settings
############################################################
with open('databases.csv') as csvfile:
    databases = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    for row in databases:
        # Set our unique values for this database
        sourceWB.datasources[0].connection.server = row['Server']
        sourceWB.datasources[0].connection.dbname = row['Database']
        sourceWB.datasources[0].connection.username = row['User']
        # Save our newly created .twb with the new file name
        sourceWB.save_as(row['DBFriendlyName'] + ' - Superstore' + '.twb')
