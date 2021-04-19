

class BadQueryError(Exception):
    """The API query returned not bible verses
    """
    pass

class ReferenceError(Exception):
    """Errors associated with references
    """
    pass
