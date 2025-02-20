from tableaudocumentapi import Workbook

# Load the workbook
# twb = Workbook('/data/jenkins/workspace/internal/platform/devops-internal/tableau-test/workbook/test.twb')

twb = Workbook("/Users/gdowding/git/github.com/tableau/SR Backlog.twb")
# Keep only desired sheets

print("before deleting dashboard from workbook")
for dashboard in twb.dashboards:
    print(dashboard)

db0_name = twb.dashboards[0]
print(f"removing dashboard {db0_name}\n")

# twb.remove_dashboard_by_name(db0_name)

print("\nafter deleting dashboard from workbook\n")
for dashboard in twb.dashboards:
    print(dashboard)


# Save the filtered workbook
print("saving file with new name: test_new.twb\n")
twb.save_as("/Users/gdowding/git/github.com/tableau/test_new.twb")


print("loading new file and checking\n")
# Load the workbook
# twb = Workbook('/data/jenkins/workspace/internal/platform/devops-internal/tableau-test/workbook/test_new.twb')

twb_new = Workbook("/Users/gdowding/git/github.com/tableau/test_new.twb")
# Keep only desired sheets

for dashboard in twb_new.dashboards:
    print(dashboard)
