from ward import test

from tableaudocumentapi import Workbook

@test("only show visible worksheets")
def _():
    wb = Workbook("test/assets/sr-backlog.twb")
    assert wb.worksheet_names() == ['Sum SR State']
