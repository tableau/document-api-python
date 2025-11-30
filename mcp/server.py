from fastmcp import FastMCP
from tableaudocumentapi.query import Query

# mcp = FastMCP("TWB-Diff2")

# @mcp.tool
# def compare_twb_workbooks(wb1_twb_xml_string: str, wb2_twb_xml_string:str):
#     """Compare 2 versions of a tableau workbook file (twb) and identify the differences"""
#     df = Query.compare_workbooks(None, None, wb1_twb_xml_string, wb2_twb_xml_string)
#     return df[df['Workbook_Source']!='both'].to_json(orient='records')

# if __name__ == "__main__":
#     mcp.run(transport="http", port=8000)
    

from fastmcp import FastMCP
from tableaudocumentapi.query import Query

mcp = FastMCP("TWB-Diff")

@mcp.tool
def compare_twb_workbooks(wb1_filepath: str, wb2_filepath: str):
    """
    Compare 2 versions of a tableau workbook file (twb) located at the given paths
    and identify the differences.
    """
    # Call compare_workbooks, passing the paths and setting strings to None
    df = Query.compare_workbooks(
        wb1_filepath, 
        wb2_filepath, 
        wb1_twb_string=None, 
        wb2_twb_string=None
    )
    # Return only the differences
    return df[df['Workbook_Source']!='both'].to_json(orient='records')

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)

