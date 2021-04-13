import re
from bs4 import BeautifulSoup
import requests as r

from .errors import BadQueryError
from .reference import Reference

# TODO : clean up the strings to be asciii safe? i.e. \u2014 -> '--'
# TODO : error check the r.get 

class Verse(Reference):
    def __init__(self, book, chapter, verse, version, text="", footnotes=[]):
        super().__init__(book, chapter, verse)
        self.text = text
        self.version = version
        self.footnotes = footnotes

    def __repr__(self):
        return "<Verse: {}>".format(super().to_string())

    def to_string(self):
        return "{} `{}` ({})".format(super().to_string(),self.text,self.version)

    def to_dict(self):
        return dict(
            book = self.book,
            chapter = self.chapter,
            verse = self.verse,
            version = self.version,
            text = self.text,
            footnotes = self.footnotes
        )

    @classmethod
    def from_dict(cls,obj):
        return cls(**obj)

    def add_footnote(self, footnote):
        self.footnotes.append(footnote)

def scrap(ref_string_or_obj, version="ESV"):
    """Scrap a verse or chapter from the web
    Params
    ------
    ref_string_or_obj : str or Reference
        The string of a chapter/verse to query

    version (optional) : str
        The bible version to query from, default is "ESV"
        
    Returns
    -------
    Verse_or_list : Verse,list of Verses
        Either a list of, or just the single verse object in formatted json
    """
    
    # Ensure that we have a reference object
    if type(ref_string_or_obj) is str:
        ref = Reference.from_string(ref_string_or_obj)
    else:
        ref = ref_string_or_obj

    # Just in case `ref` is actually a `Verse` instance, infer version
    try:
        _version = ref.version
    except AttributeError:
        _version = version

    # Generate URL
    if ref.verse is None:
        URL = "https://www.biblegateway.com/passage/?search={}+{}&version={}".format(ref.book, ref.chapter, _version)
    else:
        URL = "https://www.biblegateway.com/passage/?search={}+{}:{}&version={}".format(ref.book, ref.chapter, ref.verse, _version)

    page = r.get(URL)
    
    sc = BeautifulSoup(page.content, "html.parser")

    if "No results found" in sc.text:
        raise BadQueryError("Cannot get {} ({})".format(ref.to_string(), _version))
    
    # Get all the p tags underneath the passage content
    #  which are all the verse, and no headings
    par = sc.find(class_="passage-content").find_all("p")

    # Infer all the available verses from the html class
    #  attribute of the `text` objects
    verse_ids = dict()
    for node in sc.find_all(class_="text"):
        for clsstr in node.attrs['class']:
            if re.match("[A-Za-z0-9]+[-]\d+[-]\d+",clsstr):
                vv = int(clsstr.split("-")[-1])
                verse_ids[vv] = clsstr

    # Generate a list of Verse instances
    verses = []
    for i,v in enumerate(verse_ids.keys()):
        
        # Get all the nodes matching the verse id
        elem_list = []
        for p in par:
            elem_list += p.find_all(class_=verse_ids[v])
        
        # Skip this round if no verses were found
        if len(elem_list) < 1:
            continue
        
        # Concatentate all the found verses (space delimited)
        #  since verses over carraige returns have mulitple
        #  html tags associated with them 
        children = []
        for node in elem_list:
            children += list(node.children)
            children += [" "]
        children.pop()

        # Prep verse object
        verse = Verse(ref.book, ref.chapter, v, _version)

        # Loop through all the found verse html tags, and extract the text
        for obj in children:
            # If no 'attrs', then this is probably just a string
            #  so append it
            try:
                obj.attrs
            except:
                verse.text = verse.text + str(obj)
                continue

            # Ignore html tags that don't have a class
            try:
                obj.attrs['class']
            except:
                continue

            # Get the tetragrammoton
            if "small-caps" in obj.attrs['class']:
                verse.text = verse.text + str(obj.text).upper()

            # Get all the footnotes
            if "footnote" in obj.attrs['class']:
                fn_id = obj.attrs['data-fn']
                fn = sc.find(id=fn_id[1:]).find(class_="footnote-text")
                fn.attrs['class'] = "bible-footnote"
                verse.add_footnote(dict(
                    str_index = len(verse.text),
                    html = str(fn)
                ))
                continue

        # append the completed verse
        verses.append(verse)

    if ref.verse is None:
        return verses
    return verses[0]

