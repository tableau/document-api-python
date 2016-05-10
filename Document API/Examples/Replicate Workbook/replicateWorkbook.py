import csv              # so we can work with our database list (in a CSV file)
import copy             # to make copies

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
    next(csvfile)               # Skip the first line which is our CSV header row
    databases = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in databases:
        newWB = copy.copy(sourceWB)
        
        # Set our unique values for this database
        newWB.datasources[0].connection.server = row[1]         # Server
        newWB.datasources[0].connection.dbname = row[2]         # Database
        newWB.datasources[0].connection.username = row[3]       # User
        newWB.save_as(row[0] + ' - Superstore' + '.twb')        # Save our newly created .twb with the new file name
