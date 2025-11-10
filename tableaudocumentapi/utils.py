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
    if not isinstance(text, str) or not text:
        return (None, None)

    cleaned_fields = []

    # Remove wrapping parentheses, if any
    if text.startswith("(") and text.endswith(")"):
        text = text[1:-1]

    two_part_tokens = re.findall(r'\[[^\]]+\]\.\[[^\]]+\]', text)

    text_without_two_part = text
    for token in two_part_tokens:
        text_without_two_part = text_without_two_part.replace(token, '', 1)

    single_part_tokens = re.findall(r'\[[^\]]+\]', text_without_two_part)

    raw_fields = two_part_tokens + single_part_tokens

    for field in raw_fields:
        if '].[' in field:
            parts = field.split('].[', 1)
            first_part = parts[0] + ']'
            second_part = '[' + parts[1]

            inner = second_part[1:-1]
            if ':' in inner:
                colon_parts = inner.split(':', 1)
                if len(colon_parts) > 1 and colon_parts[0] in ['none', 'sum', 'attr', 'avg', 'min', 'max', 'count', 'usr']:
                    inner = colon_parts[1]
            if ':' in inner:
                inner = inner.rsplit(':', 1)[0]

            cleaned_field = first_part + '.[' + inner + ']'
            cleaned_fields.append(cleaned_field)
        else:
            inner = field[1:-1]
            if ':' in inner:
                colon_parts = inner.split(':', 1)
                if len(colon_parts) > 1 and colon_parts[0] in ['none', 'sum', 'attr', 'avg', 'min', 'max', 'count', 'usr']:
                    inner = colon_parts[1]
            if ':' in inner:
                inner = inner.rsplit(':', 1)[0]
            cleaned_fields.append(f'[{inner}]')

    # NEW: guard no matches
    if not cleaned_fields:
        return (None, None)

    result = re.split(r'(?<=\])\.(?=\[)', cleaned_fields[0])
    datasource_name = result[0][1:-1] if len(result) > 1 else None
    field_name = result[1] if len(result) > 1 else cleaned_fields[0]
    return datasource_name, field_name

