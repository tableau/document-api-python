import argparse
from tableaudocumentapi import Datasource
import pandas as pd
from tabulate import tabulate


def main():
    """

    :return:
    """
    parser = argparse.ArgumentParser(description='View information in .twb files')
    parser.add_argument('--datasource', required=True, help='The path to a  Tableau .tds file')
    # parser.add_argument('--v', '--view_fields', help='View the field information in a dataframe.')
    # parser.add_argument('--c', '--csv', help='Export the field information to a csv.')
    args = parser.parse_args()


    if args.datasource is not None:
        sourceTDS = Datasource.from_file(args.datasource)


        all_fields = []

        for count, field in enumerate(sourceTDS.fields.values()):
            field_info = {}

            field_info['name'] = field.name
            field_info['type'] = field.datatype
            field_info['caption'] = field.caption
            field_info['description'] = field.description

            # if field.calculation:
            field_info['calculation'] = field.calculation
            field_info['default_aggregation'] = field.default_aggregation


            print(field_info)

            # print('-----')
            # print(field.name)
            # print('-----')
            #
            # print('{:>4}: {} is a {}'.format(count + 1, field.name, field.datatype))
            # blank_line = False
            # if field.calculation:
            #     print('      the formula is {}'.format(field.calculation))
            #     blank_line = True
            # if field.default_aggregation:
            #     print('      the default aggregation is {}'.format(field.default_aggregation))
            #     blank_line = True
            # if field.description:
            #     print('      the description is {}'.format(field.description))

        #     if blank_line:
        #         print('')
        # print('----------------------------------------------------------')


        # print(sourceTDS)
        #
        # # fields = []
        # for field in enumerate(sourceTDS.fields.values()):
        #     print('{:>4}: {} is a {}'.format(field.name, field.datatype))

            # field_info['name'] = field.name
            # field_info['type'] = field.datatype

            # print(field.name)
            # print(field.datatype)


        #
        #     fields.append(field_info)
        #
        # print(field_info)
        # df = pd.DataFrame.from_dict(fields)
        #
        # print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))





if __name__ == "__main__":
    main()



