import re
from bs4 import BeautifulSoup
import requests as r

from .errors import BadQueryError

# TODO : clean up the strings to be asciii safe? i.e. \u2014 -> '--'
# TODO : modify to allow verse or chapter scraping

def scrap(B="John", C=1, V="ESV"):
    URL = "https://www.biblegateway.com/passage/?search={}+{}&version={}".format(B.replace(" ","+"),C,V)
    page = r.get(URL)
    
    sc = BeautifulSoup(page.content, "html.parser")

    if "No results found" in sc.text:
        raise BadQueryError("Cannot get {} {} ({})".format(B,C,V))
    
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

    # Generate a list of verse json objects
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

        # Prep the json verse object
        verses.append(dict(
            text = "",
            verse = v,
            chapter = C,
            footnotes = []
        ))

        # Loop through all the found verse html tags, and extract the text
        for obj in children:
            # If no 'attrs', then this is probably just a string
            #  so append it
            try:
                obj.attrs
            except:
                verses[i]["text"] = verses[i]["text"] + str(obj)
                continue

            # Ignore html tags that don't have a class
            try:
                obj.attrs['class']
            except:
                continue

            # Get the tetragrammoton
            if "small-caps" in obj.attrs['class']:
                verses[i]["text"] = verses[i]["text"] + str(obj.text).upper()

            # Get all the footnotes
            if "footnote" in obj.attrs['class']:
                fn_id = obj.attrs['data-fn']
                fn = sc.find(id=fn_id[1:]).find(class_="footnote-text")
                fn.attrs['class'] = "bible-footnote"
                verses[i]['footnotes'].append(dict(
                    str_index = len(verses[i]['text']),
                    html = str(fn)
                ))
                continue

    return verses

