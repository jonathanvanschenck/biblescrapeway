import json
import re
from bs4 import BeautifulSoup
import requests as r

def scrap(B="John", C=1, V="ESV"):
    URL = "https://www.biblegateway.com/passage/?search={}+{}&version={}".format(B,C,V)
    page = r.get(URL)

    sc = BeautifulSoup(page.content, "html.parser")
    par = sc.find(class_="passage-content").find_all("p")

    raw_list = dict()
    for node in sc.find_all(class_="text"):
        for clsstr in node.attrs['class']:
            if re.match("[A-Za-z0-9]+[-]\d+[-]\d+",clsstr):
                vv = int(clsstr.split("-")[-1])
                raw_list[vv] = clsstr


    verses = []
    for i,v in enumerate(raw_list.keys()):#enumerate(apparent_verses):#range(vnum_max):
        
        # Get all the nodes matching the verse
        elem_list = []
        for p in par:
            elem_list += p.find_all(class_=raw_list[v])#"{}-{}-{}".format(B,C,v))
        
        # Skip this round if no verses were found
        if len(elem_list) < 1:
            continue
        else:
            # Concatentate all the found verses (space delimited)
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

        # Loop through all the found verse htmls, and extract the text
        for obj in children:
            # If no 'attrs', then this is probably just a string
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

