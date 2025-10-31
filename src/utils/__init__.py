from typing import List

def stringify(value: any, qualifier: str = '"') -> str:
    """ Convert a value to string """

    if value is None or value == '':
        return ''
    elif isinstance(value, str) and value.isnumeric():
        return value
    elif isinstance(value, int) or isinstance(value, float):
        return str(value)
    else:
        return qualifier + str(value) + qualifier

def dict2csv(rows: List[dict], columns: List[dict], separator: str = ';', qualifier: str = '"', lineseparator: str = '\n') -> str:
    """ Converts a dict into a CSV file """

    lines = []
    colnames = list(map(lambda x: x['header'], columns))
    lines.append(qualifier + (f"{qualifier}{separator}{qualifier}".join(colnames)) + qualifier)

    for row in rows:
        line = []
        for column in columns:
            line.append(stringify(column['selector'](row), qualifier))

        lines.append(separator.join(line))

    return lineseparator.join(lines) + lineseparator
