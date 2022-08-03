
############################################################
# Step 1)  Use Workbook object from the Document API
############################################################
from tableaudocumentapi import Workbook


def assertContainsUserNamespace(filename):
    print('asserting on ' + filename)
    with open(filename, 'r') as in_file:
        # the namespace is in the first five lines for all the docs I've checked
        lineCount = 0
        doc_beginning_excerpt = ""
        while lineCount < 5:
            doc_beginning_excerpt += (in_file.readline().strip())  # first line should be xml tag
            lineCount += 1
    found = doc_beginning_excerpt.rfind("xmlns:user=")
    print(doc_beginning_excerpt[found:found+10])
    assert (found >= 0)


############################################################
# Step 2)  Open the .twb we want to replicate
############################################################
assertContainsUserNamespace('filtering.twb')
sourceWB = Workbook('filtering.twb')
sourceWB.save_as('saved-as-filtering.twb')
assertContainsUserNamespace('saved-as-filtering.twb')
sourceWb2 = Workbook('TABLEAU_10_TWB.twb')
sourceWb2.save_as('saved-as-tableau-10' + '.twb')
# there was no namespace in the original
# so there isn't one in the saved doc either assertContainsUserNamespace('saved-as-tableau-10.twb')
