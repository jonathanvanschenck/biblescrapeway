unicode_mapping = [
    # ("\u201c", "\""),
    # ("\u201d", "\""),
    # ("\u2018", "'"),
    # ("\u2019", "'")
]


def clean_string(string):
    _string = str(string)
    for uchar,schar in unicode_mapping:
        _string = _string.replace(uchar,schar)
    return _string
