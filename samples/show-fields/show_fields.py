############################################################
# Step 1)  Use Datasource object from the Document API
############################################################
from tableaudocumentapi import Datasource

############################################################
# Step 2)  Open the .tds we want to inspect
############################################################
datasources = [Datasource.from_file('world.tds'), Datasource.from_file('nested.tds')]
for sourceTDS in datasources:

    ############################################################
    # Step 3)  Print out all of the fields and what type they are
    ############################################################
    print('----------------------------------------------------------')
    print('-- Info for our .tds:')
    print('--   name:\t{0}'.format(sourceTDS.name))
    print('--   version:\t{0}'.format(sourceTDS.version))
    print('----------------------------------------------------------')
    print('--- {} total fields in this datasource'.format(len(sourceTDS.fields)))
    print('----------------------------------------------------------')
    for count, field in enumerate(sourceTDS.fields.values()):
        blank_line = False
        if field.calculation:
            print('{:>4}: field named `{}` is a `{}`'.format(count+1, field.name, field.datatype))
            print('      field id, caption, calculation: `{}`, `{}`, `{}`'.format(field.id, field.caption,
                                                                                  field.calculation))
            blank_line = True
        if field.default_aggregation:
            print('{:>4}: `{}` is a `{}`, default aggregation is `{}`'.format(count+1, field.name, field.datatype,
                                                                              field.default_aggregation))

        if field.description:
            print('{:>4}: `{}` is a `{}`, description is `{}`'.format(count+1, field.name, field.datatype,
                                                                      field.description))

        if blank_line:
            print('')
    print('----------------------------------------------------------')
