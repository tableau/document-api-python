from fastmcp import FastMCP
from tableaudocumentapi.query import Query

mcp = FastMCP("TWB-Diff")

@mcp.tool
def compare_twb_workbooks(
    wb1_filepath: str = None, 
    wb2_filepath: str = None,
    wb1_xml_string: str = None, 
    wb2_xml_string: str = None
):
    """
    Compare 2 versions of a tableau workbook file (twb) and identify the differences.
    
    Provide either file paths OR XML strings (not both):
    - For file comparison: wb1_filepath and wb2_filepath
    - For XML string comparison: wb1_xml_string and wb2_xml_string
    """
    
    # Validate inputs
    has_filepaths = wb1_filepath is not None and wb2_filepath is not None
    has_xmlstrings = wb1_xml_string is not None and wb2_xml_string is not None
    
    if has_filepaths and has_xmlstrings:
        raise ValueError("Provide either file paths OR XML strings, not both")
    
    if not has_filepaths and not has_xmlstrings:
        raise ValueError("Must provide either both file paths or both XML strings")
    
    # Check for partial inputs
    if (wb1_filepath is not None) != (wb2_filepath is not None):
        raise ValueError("Both wb1_filepath and wb2_filepath must be provided together")
    
    if (wb1_xml_string is not None) != (wb2_xml_string is not None):
        raise ValueError("Both wb1_xml_string and wb2_xml_string must be provided together")
    
    # Call compare_workbooks with appropriate parameters
    if has_filepaths:
        df = Query.compare_workbooks(
            wb1_filepath, 
            wb2_filepath, 
            wb1_twb_string=None, 
            wb2_twb_string=None
        )
    else:
        df = Query.compare_workbooks(
            None, 
            None, 
            wb1_twb_string=wb1_xml_string, 
            wb2_twb_string=wb2_xml_string
        )
    
    # Return only the differences
    return df[df['Workbook_Source'] != 'both'].to_json(orient='records')

if __name__ == "__main__":
    mcp.run()