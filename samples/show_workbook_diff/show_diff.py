#################################################################
# Step 1)  Use Workbook object from the Document API
#################################################################
from tableaudocumentapi.query import Query
#################################################################
# Step 2)  Create diff of 2 versions of a tableau workboook (.twb or .twbx) we want compare
############################################################
df_diff = Query.compare_diffs(wb1_filename="samples/show_workbook_diff/AESO.twbx", wb2_filename="samples/show_workbook_diff/AESO2.twbx")
#################################################################
# Step 3)  Output the diff to csv
#################################################################
df_diff.to_csv("samples/show_workbook_diff/Data/df_diff.csv", index=False)
#################################################################
# Step 4)  Open the diff_dashboard.twb and refresh the datasource
#################################################################