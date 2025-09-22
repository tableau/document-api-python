import re

def _clean_aggregated_column_names(text):
    """
    Clean Tableau field references inside brackets:
      - Strip derivation prefixes like 'none:', 'sum:', 'attr:' (before first ':')
      - Strip suffix flags like ':ok', ':nk', ':qk' (after last ':')
    Works for both:
      [federated.xxx].[none:Date:ok]  -> [federated.xxx].[Date]
      [Calculation_123:qk]            -> [Calculation_123]
    """
    cleaned_fields = []
    if not isinstance(text, str) or not text:
        return cleaned_fields

    # Remove wrapping parentheses, if any
    if text.startswith("(") and text.endswith(")"):
        text = text[1:-1]

    # First, find and remove all two-part tokens from text, collecting them
    two_part_tokens = re.findall(r'\[[^\]]+\]\.\[[^\]]+\]', text)
    
    # Remove two-part tokens from text to avoid overlap with single-part detection
    text_without_two_part = text
    for token in two_part_tokens:
        text_without_two_part = text_without_two_part.replace(token, '', 1)
    
    # Now find single-part tokens in the remaining text
    single_part_tokens = re.findall(r'\[[^\]]+\]', text_without_two_part)
    
    # Combine in order found
    raw_fields = two_part_tokens + single_part_tokens

    for field in raw_fields:
        if '].[' in field:
            # Two-part token: [first].[second:suffix] -> [first].[second]
            # Only clean the second bracket
            parts = field.split('].[', 1)
            first_part = parts[0] + ']'  # Keep first part as-is
            second_part = '[' + parts[1]  # Add back the opening bracket
            
            # Clean the second part
            inner = second_part[1:-1]  # Remove brackets
            # Remove prefix before first colon (if any)
            if ':' in inner:
                colon_parts = inner.split(':', 1)
                if len(colon_parts) > 1 and colon_parts[0] in ['none', 'sum', 'attr', 'avg', 'min', 'max', 'count', 'usr']:
                    inner = colon_parts[1]  # Remove known prefix
            # Remove suffix after last colon (if any)  
            if ':' in inner:
                inner = inner.rsplit(':', 1)[0]  # Remove last suffix
            
            cleaned_field = first_part + '.[' + inner + ']'
            cleaned_fields.append(cleaned_field)
        else:
            # Single-part token: [something:suffix] -> [something]
            inner = field[1:-1]  # Remove brackets
            # Remove prefix before first colon (if any)
            if ':' in inner:
                colon_parts = inner.split(':', 1)
                if len(colon_parts) > 1 and colon_parts[0] in ['none', 'sum', 'attr', 'avg', 'min', 'max', 'count', 'usr']:
                    inner = colon_parts[1]  # Remove known prefix
            # Remove suffix after last colon (if any)
            if ':' in inner:
                inner = inner.rsplit(':', 1)[0]  # Remove last suffix
            
            cleaned_fields.append(f'[{inner}]')
    
    result = re.split(r'(?<=\])\.(?=\[)', cleaned_fields[0])
    datasource_name = result[0][1:-1]
    field_name = result[1]
    return datasource_name, field_name
