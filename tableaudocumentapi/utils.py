import re

def _clean_aggregated_column_name(text):
    """Function that clean an aggregated column name, removing 'none:' ,':nk" etc.."""
    
    # 1. Remove wrapping parentheses, if any
    if text.startswith("(") and text.endswith(")"):
        text = text[1:-1]

    # 2. Regex to find all bracketed expressions like [foo].[bar:ok]
    raw_fields = re.findall(r'\[[^\]]+\]\.\[[^\]]+\]', text)

    cleaned_fields = []
    for field in raw_fields:
        # Remove the prefix inside the second bracket up to the first colon
        # Example: [federated.xxx].[none:Date:ok] → [federated.xxx].[Date:ok]
        field = re.sub(r'(\.\[)[^:\]]*:(.*?)\]', r'\1\2]', field)

        # Remove everything after the last colon before the closing bracket
        # Example: [federated.xxx].[Date:ok] → [federated.xxx].[Date]
        field = re.sub(r':[^:\]]*(?=\])', '', field)

        cleaned_fields.append(field)

    return cleaned_fields