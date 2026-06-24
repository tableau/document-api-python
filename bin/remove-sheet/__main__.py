from tableaudocumentapi import Workbook

# Load the workbook
# twb = Workbook('/data/jenkins/workspace/internal/platform/devops-internal/tableau-test/workbook/test.twb')

twb = Workbook("/Users/gdowding/git/github.com/tableau/SR Backlog.twb")
# Keep only desired sheets

print("before deleting worksheet from workbook")
for worksheet in twb.worksheets:
    print(worksheet)

del twb.worksheets[3]

wb3_name = twb.worksheets[3]
print(f"removing worksheet {wb3_name}\n")

twb.remove_worksheet_by_name(wb3_name)

print("\nafter deleting worksheet from workbook\n")
for worksheet in twb.worksheets:
    print(worksheet)


# Save the filtered workbook
print("saving file with new name: test_new.twb\n")
twb.save_as("/Users/gdowding/git/github.com/tableau/test_new.twb")


print("loading new file and checking\n")
# Load the workbook
# twb = Workbook('/data/jenkins/workspace/internal/platform/devops-internal/tableau-test/workbook/test_new.twb')

twb_new = Workbook("/Users/gdowding/git/github.com/tableau/test_new.twb")
# Keep only desired sheets

for worksheet in twb_new.worksheets:
    print(worksheet)
