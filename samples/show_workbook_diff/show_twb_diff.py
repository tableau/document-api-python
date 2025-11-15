#################################################################
# SAMPLE: Demonstrate how to generate and visualize a workbook diff
#################################################################
import subprocess
import os
#################################################################
# Step 1)  Generate the diff CSV using the new CLI
#################################################################
subprocess.run([
    "twb-diff",
    "--wb1", "samples/show_workbook_diff/Workbook_v1.twbx",
    "--wb2", "samples/show_workbook_diff/Workbook_v2.twbx",
    "--out", "samples/show_workbook_diff/Data/df_diff.csv"
], check=True)
print("✅ Diff file generated at samples/show_workbook_diff/Data/df_diff.csv")
#################################################################
# Step 2)  Visualize in Tableau
#################################################################
print("""
Open 'samples/show_workbook_diff/diff_dashboard.twb' in Tableau Desktop,
then refresh the data source to visualize the differences captured in df_diff.csv.
""")
