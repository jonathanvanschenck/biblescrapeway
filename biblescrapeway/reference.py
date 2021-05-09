import re

from .errors import ReferenceError
from .constants import book_regex

# TODO : document
# TODO : test
# TODO : create to_simple_string function?


def normalize_reference_string(reference_string):
    """Expand a reference string to full reference
    """
    return [
        ref.start.to_string() if ref.is_single_verse else ref.to_string()\
        for ref in parse_reference_string(reference_string)
    ]

def shorten_reference_string(reference_string):
    """Shorten a reference string

    Returns the minimum necessary string to unambigiously
    list references: E.g. `Genesis 1, Genesis 2` -> `Genesis 1, 2`
    """
    range_list = parse_reference_string(reference_string)
    if len(range_list) == 0:
        return ""

    string_list = [range_list[0].to_string()]
    if len(range_list) == 1:
        return string_list[0]

    for i in range(1,len(range_list)):
        string_list.append(range_list[i].to_string_short(range_list[i-1]))

    return ", ".join(string_list)


def parse_reference_string(reference_string):
    """Parse reference string to list of range objects
    """
    string_list = reference_string.strip().replace(";",",").split(",")
    res = [Range.from_string(string_list.pop(0))]
    for _string in string_list:
        res.append(Range.from_string(_string, res[-1]))
    return res

def _get_normalized_book_name(string):
    """Get the full book name from partial string
    """
    _string = string.strip()
    for regex in book_regex:
        if re.match(regex[0] + "[a-z\.]*", _string):
            return regex[1]
    raise ReferenceError("Cannot find book `{}`".format(_string))

class Reference:
    """A bible reference to either a chapter or verse
    """
    BCV_regex = re.compile("^([0-9]?[ _\.]?[A-Za-z]+)[\._ ]*([0-9]+)[\.: _]?([0-9]*)$")
    CV_regex = re.compile("^([0-9]+)[\.: ]([0-9]+)$")
    V_regex = re.compile("^([0-9]+)$")

    def __init__(self, book, chapter, verse = None):
        self.book = _get_normalized_book_name(book)
        self.chapter = int(chapter)
        try:
            self.verse = int(verse)
        except (TypeError, ValueError):
            # This reference is to the whole chapter
            self.verse = None

    def __repr__(self):
        return "<{}>".format(self.to_string())
    
    def to_string(self):
        if self.verse is None:
            return "{} {}".format(self.book,self.chapter)
        return "{} {}:{}".format(self.book,self.chapter,self.verse)
    
    def is_before(self,other):

        # Handle book comparision
        if self.book != other.book:
            raise ReferenceError("Cannot compare reference orders from different books")

        # Handle Chapter comparison
        if self.chapter < other.chapter:
            return True
        if other.chapter < self.chapter:
            return False
        
        # Handle verse comparisions
        if self.verse is None and other.verse is None:
            return True
        if other.verse is None or self.verse is None:
            raise ReferenceError("Cannot compare a chapter reference and a verse reference from same chapter")
        return self.verse < other.verse


    def equals(self,other):
        return self.book == other.book \
            and self.chapter == other.chapter \
            and self.verse == other.verse
    
    
    @classmethod
    def from_string(cls, string, previous = None):
        """Generate object from string (and previous obj if any)
        """
        _string = string.strip()
        match = cls.BCV_regex.match(_string)
        if not match is None:
            return cls(*match.groups())

        if previous is None:
            raise ReferenceError("Cannot infer book/chapter for reference")

        try:
            previous_book = previous.book
            previous_chapter = previous.chapter
            previous_verse = previous.verse
        except AttributeError:
            # previous is a Range object
            previous_book = previous.end.book
            previous_chapter = previous.end.chapter
            previous_verse = previous.end.verse

        match = cls.CV_regex.match(_string)
        if not match is None:
            # Infer book from previous
            return cls(previous_book, *match.groups())

        match = cls.V_regex.match(_string)
        if not match is None:
            if previous_verse is None:
                # previous is a chapter reference or range,
                #  so treat this like a chapter reference
                # TODO : single numbers after ranges spanning
                #  2+ chapters is ambigous: `John 3:10-4:12, 15`
                #  is that `John 15` or `John 4:15`? right now
                #  we treat that as the former.
                return cls(previous_book,*match.groups())
            # Infer both book and chapter from previous
            return cls(previous_book,previous_chapter,*match.groups())
        
        raise ReferenceError("Cannot parse string `{}` with previous `{}`".format(_string,previous.to_string()))

class Range:
    def __init__(self, start_reference, end_reference):
        try:
            if not (start_reference.is_before(end_reference) or start_reference.equals(end_reference)):
                raise ReferenceError("Cannot make range with end before beginning")
                # self.start = end_reference
                # self.end = start_reference
            else:
                self.start = start_reference
                self.end = end_reference
        except ReferenceError as e:
            raise ReferenceError("Cannot create range from provided references") from e
        # self.start = start_reference
        # self.end = end_reference

    def __repr__(self):
        return "<{}>".format(self.to_string())

    def to_string(self):
        return "{} - {}".format(self.start.to_string(), self.end.to_string())

    @property
    def book(self):
        return self.start.book

    @property
    def is_single_verse(self):
        return (not self.start.verse is None) and self.start.equals(self.end)

    @property
    def is_single_chapter(self):
        return (self.start.verse is None) and self.start.equals(self.end)

    def contains(self, ref):
        if self.start.book != ref.book:
            raise ReferenceError("Cannot compare references from different books")
        
        if self.start.verse is None and ref.chapter >= self.start.chapter:
            ge_start = True
        else:
            ge_start = not ref.is_before(self.start)
        
        if self.end.verse is None and ref.chapter <= self.end.chapter:
            le_end = True
        else:
            le_end = not self.end.is_before(ref)

        return ge_start and le_end

    def to_string(self):
        string = "{} {}".format(self.start.book, self.start.chapter)
        if not self.start.verse is None:
            string = string + ":{}".format(self.start.verse)
        if self.start.equals(self.end):
            return string

        string = string + "-"

        if self.end.chapter == self.start.chapter:
            return string + "{}".format(self.end.verse)

        if self.end.verse is None:
            return string + "{}".format(self.end.chapter)

        return string + "{}:{}".format(self.end.chapter, self.end.verse)

    def to_string_short(self, previous = None):
        """Generate the shortest reference string from this range
        """
        full = self.to_string()

        if previous is None or previous.start.book != self.start.book:
            return full

        # FIXME : assume Gen1:1-3:4,6 means also 3:6
        if (
            self.start.is_before(previous.end)\
            or previous.end.chapter != self.start.chapter\
            or self.start.chapter != self.end.chapter
        ):
            # Truncate only the book name
            return full.split(" ")[-1]

        return full.split(" ")[-1].split(":")[-1]


    @classmethod
    def from_string(cls, string, previous = None):

        strings = [_string.strip() for _string in string.split("-")]
        
        if len(strings) == 0 or len(strings) > 2:
            raise ReferenceError("Cannot create range from `{}`".format(string))

        ref = Reference.from_string(strings[0], previous)

        return cls(
            ref, 
            Reference.from_string(strings[len(strings) == 2], ref)
        )

