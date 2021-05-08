import json

from .scraper import Verse

class JSONFile:
    """Abstraction layer for JSON file IO

    This class creates a (real or virtual) json file containing
    a single `{...}` objects, then allows the user to add things
    into, or read things out of the file, saving after each 
    write operation

    Parameters
    ----------
    fp : string or None
        A file path to where the JSON file exsits, or where it should
        be immediately created. If set to `None` the class will create
        and empty "virtual" file, which will be destroyed with the 
        class instance. Default is `None`.
    """
    def __init__(self, fp = None):
        self.fp = fp
        self.json = dict()
        self.pull()

    @property
    def file_path(self):
        if self.fp is None:
            return "Virtual"
        return self.fp

    def __repr__(self):
        return "<JSONFile @ {}>".format(self.file_path)

    def pull(self):
        """Load contents of the JSON file into memory

        Note, this will destroy any unsaved changes currently
        in the class instance memory. (Use `.push` to save)
        """
        # Virtual files don't get saved to the hard disk
        if self.fp == None:
            return self

        # Attempt to open file
        try:
            f = open(self.fp)
        except FileNotFoundError:
            # The files doesn't exist yet, so nuke any local
            #  json configuration
            self.json = dict()
            return self

        # Load json, might throw an error if your file is
        #  corrupted
        self.json = json.load(f)
        f.close()

        return self

    def push(self):
        """Save local json object to the hard disk

        Note, this creates a file at `self.fp` if one
        does not already exist there.
        """
        # Virtual files don't get saved anywhere
        if self.fp == None:
            return self

        # Save, might throw an error if you did something
        #  weird to `self.json`
        with open(self.fp, "w+") as f:
            json.dump(self.json, f)

        return self

class BibleCacher:
    """Abstraction layer for bible verse/range IO to files

    This class allows bible verse (previously queried) to
    be cached locally in a file, so that repeated queries
    can just look up the result.

    The file structure is as follows:
    ```json
    {
        "queries" : {
            "Normalized range string" : "List of verse strings in range",
            "John 3:16-17 (ESV)" : [
                "John 3:16 (ESV)",
                "John 3:17 (ESV)"
            ],
            ...
        },
        "items" : {
            "Normalized verse string" : "serialized `bsw.scraper.Verse` object",
            "John 3:16 (ESV)" : { VerseObject },
            ...
        }
    }
    ```

    Parameters
    ----------
    fp : string or None
        A file path to where to cache bible verse, if the
        path doesn't exist, this will attempt to create it.
        If `None` then a virtual file will be used, and 
        also destroyed with this class instance. Default
        is `None`.
    """
    def __init__(self, fp = None):
        self.file = JSONFile(fp)
        
        # Setup structure
        changed = False
        try:
            self.json['queries']
        except KeyError:
            self.json['queries'] = dict()
            changed = True

        try:
            self.json['items']
        except KeyError:
            self.json['items'] = dict()
            changed = True

        if changed:
            self.file.push()

    @property
    def json(self):
        return self.file.json

    @property
    def file_path(self):
        return self.file.file_path

    def __repr__(self):
        return "<BibleCacher @ {}>".format(self.file_path)

    def generate_query_key(self, range_or_range_string, version):
        """Generate key for a `query` (list of normalized verse strings)
        """
        if type(range_or_range_string) is str:
            query_key = range_or_range_string + " ({})".format(version.upper())
        else:
            # Treat `range_string` as a range object and stringify it
            query_key = range_or_range_string.to_string() + " ({})".format(version.upper())

        return query_key

    def generate_item_key(self, verse):
        """Generate the key for an `item` (serialized verse object)
        """
        return "{} {}:{} ({})".format(verse.book, verse.chapter, verse.verse, verse.version)

    def look_up(self, range_or_range_string, version="ESV"):
        """Check the cache file for the result of a bible range
        """

        query_key = self.generate_query_key( range_or_range_string, version )
        try:
            item_key_list = self.json['queries'][query_key]
        except KeyError:
            return None

        return [ Verse.from_dict(self.json['items'][item_key]) for item_key in item_key_list ]

    def cache(self, range_or_range_string, verse_list):
        """Save the results of a query to the cache
        """

        query_key = self.generate_query_key( range_or_range_string, verse_list[0].version )
        self.json['queries'][query_key] = []
        for verse in verse_list:
            item_key = self.generate_item_key(verse)
            self.json['queries'][query_key].append(item_key)
            self.json['items'][item_key] = verse.to_dict()

        self.file.push().pull()

        return self

