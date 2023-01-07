import unittest

from .. import reference as ref
from ..constants import book_regex

class BookNormalization(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_test(self):
        """Override me
        """
        self.assertEqual(0,0)

    def test_match_full_name(self):
        """Can match full book name
        """
        for [_,name,_] in book_regex:
            self.assertEqual(ref._get_normalized_book_name(name),name)

    def test_match_partial_name(self):
        """Can match partial book name
        """
        self.assertEqual(ref._get_normalized_book_name("Gen"),"Genesis")
        self.assertEqual(ref._get_normalized_book_name("1K"),"1 Kings")
        self.assertEqual(ref._get_normalized_book_name("1_K"),"1 Kings")
        self.assertEqual(ref._get_normalized_book_name("1 K"),"1 Kings")
        self.assertEqual(ref._get_normalized_book_name("So"),"Song of Solomon")
        self.assertEqual(ref._get_normalized_book_name("Song of"),"Song of Solomon")

    def test_match_abbreviated_name(self):
        """Can match abbreviated book name
        """
        self.assertEqual(ref._get_normalized_book_name("Gen."),"Genesis")
        self.assertEqual(ref._get_normalized_book_name("Son. of S."),"Song of Solomon")
        self.assertEqual(ref._get_normalized_book_name("SoS"),"Song of Solomon")



class ReferenceFromString(unittest.TestCase):

    def match(self, string, previous, expected):
        if previous is None:
            prev = None
        else:
            prev = ref.Reference(*previous)
        exp = ref.Reference(*expected)
        r = ref.Reference.from_string(string,prev)
        self.assertEqual(r.book,exp.book)
        self.assertEqual(r.chapter,exp.chapter)
        self.assertEqual(r.verse,exp.verse)

    def match_range(self, string, previous_start, previous_end, expected):
        prev = ref.Range(ref.Reference(*previous_start),ref.Reference(*previous_end))
        exp = ref.Reference(*expected)
        r = ref.Reference.from_string(string,prev)
        self.assertEqual(r.book,exp.book)
        self.assertEqual(r.chapter,exp.chapter)
        self.assertEqual(r.verse,exp.verse)

    def test_match_full_reference(self):
        """Matches full reference
        """
        self.match("Genesis 1:1", None, ["Genesis", 1, 1])
        self.match("Genesis.1:1", None, ["Genesis", 1, 1])
        self.match("Genesis_1:1", None, ["Genesis", 1, 1])
        self.match("Genesis1:1", None, ["Genesis", 1, 1])
        self.match("Genesis 1_1", None, ["Genesis", 1, 1])
        self.match("Genesis.1_1", None, ["Genesis", 1, 1])
        self.match("Genesis_1_1", None, ["Genesis", 1, 1])
        self.match("Genesis1_1", None, ["Genesis", 1, 1])
        self.match("Genesis 1.1", None, ["Genesis", 1, 1])
        self.match("Genesis.1.1", None, ["Genesis", 1, 1])
        self.match("Genesis_1.1", None, ["Genesis", 1, 1])
        self.match("Genesis 1.1", None, ["Genesis", 1, 1])
        self.match("Genesis 1 1", None, ["Genesis", 1, 1])
        self.match("Genesis.1 1", None, ["Genesis", 1, 1])
        self.match("Genesis_1 1", None, ["Genesis", 1, 1])
        self.match("Genesis1 1", None, ["Genesis", 1, 1])
        self.match("1 John 3:15", None, ["1 John", 3, 15])
        self.match("1_John 3:15", None, ["1 John", 3, 15])
        self.match("1John 3:15", None, ["1 John", 3, 15])
        self.match("1 John 3 15", None, ["1 John", 3, 15])
        self.match("1_John 3 15", None, ["1 John", 3, 15])
        self.match("1John 3 15", None, ["1 John", 3, 15])
        self.match("1 John3:15", None, ["1 John", 3, 15])
        self.match("1_John3:15", None, ["1 John", 3, 15])
        self.match("1John3:15", None, ["1 John", 3, 15])

    def test_match_partial_reference(self):
        """Matches partial references
        """
        self.match("Gen. 1:1", None, ["Genesis", 1, 1])
        self.match("Gen.1:1", None, ["Genesis", 1, 1])
        self.match("Gen1:1", None, ["Genesis", 1, 1])

    def test_match_chapter(self):
        """Matches references to only chapters
        """
        self.match("Genesis 1", None, ["Genesis", 1, None])
        self.match("Gen. 1", None, ["Genesis", 1, None])
        self.match("Gen 1", None, ["Genesis", 1, None])
        self.match("Gen.1", None, ["Genesis", 1, None])
        self.match("1 John 2", None, ["1 John", 2, None])
        self.match("1John 2", None, ["1 John", 2, None])
        self.match("1 John_2", None, ["1 John", 2, None])
        self.match("1_John_2", None, ["1 John", 2, None])
        self.match("1John_2", None, ["1 John", 2, None])
        self.match("1 John2", None, ["1 John", 2, None])
        self.match("1_John2", None, ["1 John", 2, None])
        self.match("1John2", None, ["1 John", 2, None])


    def test_ignore_previous(self):
        """Ignore previous reference
        """
        pre = ["Genesis", 1, 2]
        self.match("Genesis 1:3", pre, ["Genesis", 1, 3])
        self.match("Genesis 1", pre, ["Genesis", 1, None])
        self.match("1Jo3.4", pre, ["1 John", 3, 4])

        self.match_range("Genesis 1:3", pre, pre, ["Genesis", 1, 3])
        self.match_range("Genesis 1", pre, pre, ["Genesis", 1, None])
        self.match_range("1Jo3.4", pre, pre, ["1 John", 3, 4])

        pre2 = ["Genesis", 1, 5]
        self.match_range("Genesis 1:3", pre, pre2, ["Genesis", 1, 3])
        self.match_range("Genesis 1", pre, pre2, ["Genesis", 1, None])
        self.match_range("1Jo3.4", pre, pre2, ["1 John", 3, 4])

    def test_infer_book(self):
        """Infer the book of a reference
        """
        pre = ["Genesis", 1, 2]
        self.match("1:3", pre, ["Genesis", 1, 3])
        self.match("1:3", ["Genesis", 2, None], ["Genesis", 1, 3])
        self.match("3", ["Genesis", 2, None], ["Genesis", 3, None])

        self.match_range("1:3", pre, pre, ["Genesis", 1, 3])
        self.match_range("1:3", pre, ["Genesis", 1, 10], ["Genesis", 1, 3])
        self.match_range("1:3", pre, ["Genesis", 2, 10], ["Genesis", 1, 3])
        self.match_range("1:3", pre, ["Genesis", 2, None], ["Genesis", 1, 3])
        self.match_range("3", pre, ["Genesis", 2, None], ["Genesis", 3, None])

    def test_infer_verse(self):
        """Infer the verse of a reference
        """
        pre = ["Genesis", 1, 2]
        self.match("3", pre, ["Genesis", 1, 3])

        self.match_range("3", pre, pre, ["Genesis", 1, 3])
        self.match_range("3", pre, ["Genesis", 1, 10], ["Genesis", 1, 3])
        self.match_range("3", pre, ["Genesis", 2, 10], ["Genesis", 2, 3])


class VRegex(unittest.TestCase):

    def match(self, string, expect):
        m = ref.Reference.V_regex.match(string)
        if m is None:
            self.assertEqual(expect,None)
            return
        for v1,v2 in zip(expect, m.groups()):
            self.assertEqual(v1,v2)

    def test_full_reference(self):
        """Doesn't Match full references
        """
        self.match("Genesis 1:1", None)
        self.match("Genesis_1:1", None)
        self.match("Genesis.1:1", None)
        self.match("Genesis1:1", None)
        self.match("Genesis 1.1", None)
        self.match("Genesis_1.1", None)
        self.match("Genesis.1.1", None)
        self.match("Genesis1.1", None)
        self.match("Genesis 1_1", None)
        self.match("Genesis_1_1", None)
        self.match("Genesis.1_1", None)
        self.match("Genesis1_1", None)
        self.match("Genesis 1 1", None)
        self.match("Genesis_1 1", None)
        self.match("Genesis.1 1", None)
        self.match("Genesis1 1", None)
        self.match("1 John 4:15", None)
        self.match("1_John 4:15", None)
        self.match("1.John 4:15", None)
        self.match("1 John4:15", None)
        self.match("1_John4:15", None)
        self.match("1.John4:15", None)

    def test_partial_reference(self):
        """Doesn't Match partial references
        """
        self.match("Gen. 1:1", None)
        self.match("Gen 1:1", None)
        self.match("Gen.1:1", None)
        self.match("Gen1:1", None)

    def test_incomplete_reference(self):
        """Doesn't Match incomplete references
        """
        self.match("1:1", None)
        self.match("1 1", None)
        self.match("1.1", None)
        self.match("1", ["1"])
        self.match("15", ["15"])



class CVRegex(unittest.TestCase):

    def match(self, string, expect):
        m = ref.Reference.CV_regex.match(string)
        if m is None:
            self.assertEqual(expect,None)
            return
        for v1,v2 in zip(expect, m.groups()):
            self.assertEqual(v1,v2)

    def test_full_reference(self):
        """Doesn't Match full references
        """
        self.match("Genesis 1:1", None)
        self.match("Genesis_1:1", None)
        self.match("Genesis.1:1", None)
        self.match("Genesis1:1", None)
        self.match("Genesis 1.1", None)
        self.match("Genesis_1.1", None)
        self.match("Genesis.1.1", None)
        self.match("Genesis1.1", None)
        self.match("Genesis 1_1", None)
        self.match("Genesis_1_1", None)
        self.match("Genesis.1_1", None)
        self.match("Genesis1_1", None)
        self.match("Genesis 1 1", None)
        self.match("Genesis_1 1", None)
        self.match("Genesis.1 1", None)
        self.match("Genesis1 1", None)
        self.match("1 John 4:15", None)
        self.match("1_John 4:15", None)
        self.match("1.John 4:15", None)
        self.match("1 John4:15", None)
        self.match("1_John4:15", None)
        self.match("1.John4:15", None)

    def test_partial_reference(self):
        """Doesn't Match partial references
        """
        self.match("Gen. 1:1", None)
        self.match("Gen 1:1", None)
        self.match("Gen.1:1", None)
        self.match("Gen1:1", None)

    def test_incomplete_reference(self):
        """Doesn't Match incomplete references
        """
        self.match("1:1", ["1","1"])
        self.match("1 1", ["1","1"])
        self.match("1.1", ["1","1"])
        self.match("1", None)
        self.match("15", None)


class BCVRegex(unittest.TestCase):

    def match(self, string, expect):
        m = ref.Reference.BCV_regex.match(string)
        if m is None:
            self.assertEqual(expect,None)
            return
        for v1,v2 in zip(expect, m.groups()):
            self.assertEqual(v1,v2)

    def test_full_reference(self):
        """Matches full references
        """
        self.match("Genesis 1:1", ["Genesis", "1", "1"])
        self.match("Genesis_1:1", ["Genesis", "1", "1"])
        self.match("Genesis.1:1", ["Genesis", "1", "1"])
        self.match("Genesis1:1", ["Genesis", "1", "1"])
        self.match("Genesis 1.1", ["Genesis", "1", "1"])
        self.match("Genesis_1.1", ["Genesis", "1", "1"])
        self.match("Genesis.1.1", ["Genesis", "1", "1"])
        self.match("Genesis1.1", ["Genesis", "1", "1"])
        self.match("Genesis 1_1", ["Genesis", "1", "1"])
        self.match("Genesis_1_1", ["Genesis", "1", "1"])
        self.match("Genesis.1_1", ["Genesis", "1", "1"])
        self.match("Genesis1_1", ["Genesis", "1", "1"])
        self.match("Genesis 1 1", ["Genesis", "1", "1"])
        self.match("Genesis_1 1", ["Genesis", "1", "1"])
        self.match("Genesis.1 1", ["Genesis", "1", "1"])
        self.match("Genesis1 1", ["Genesis", "1", "1"])
        self.match("1 John 4:15", ["1 John", "4", "15"])
        self.match("1_John 4:15", ["1_John", "4", "15"])
        self.match("1.John 4:15", ["1.John", "4", "15"])
        self.match("1 John4:15", ["1 John", "4", "15"])
        self.match("1_John4:15", ["1_John", "4", "15"])
        self.match("1.John4:15", ["1.John", "4", "15"])

        # matches Multi-words
        self.match("So1.1", ["So", "1", "1"])
        self.match("Song of Solomon 1:1", ["Song of Solomon", "1", "1"])
        self.match("Song of Sol 1:1", ["Song of Sol", "1", "1"])
        self.match("Song o 1:1", ["Song o", "1", "1"])

    def test_partial_reference(self):
        """Matches partial references
        """
        self.match("Gen. 1:1", ["Gen", "1", "1"])
        self.match("Gen 1:1", ["Gen", "1", "1"])
        self.match("Gen.1:1", ["Gen", "1", "1"])
        self.match("Gen1:1", ["Gen", "1", "1"])





    def test_incomplete_reference(self):
        """Doesn't Match incomplete references
        """
        self.match("1:1", None)
        self.match("1 1", None)
        self.match("1.1", None)
        self.match("1", None)
        self.match("15", None)

class ToString(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_range_to_string(self):
        """Can convert ranges to strings
        """
        for instring, outstring in [
            ["Gen1:2", "Genesis 1:2"],
            ["Gen1:2-3", "Genesis 1:2-3"],
            ["Gen1-2", "Genesis 1-2"],
            ["Gen1-2:2", "Genesis 1-2:2"],
            ["Gen11:12-11:13", "Genesis 11:12-13"],
            ["Gen10:12-13:2", "Genesis 10:12-13:2"]
        ]:
            self.assertEqual(ref.Range.from_string(instring).to_string(), outstring)

    def test_range_to_string_short(self):
        """Can convert range lists to short strings
        """
        for instring, outstring in [
            # Single references
            ["Gen1:2", "Genesis 1:2"],
            ["Gen1:2-3", "Genesis 1:2-3"],
            ["Gen1-2", "Genesis 1-2"],
            ["Gen1-2:2", "Genesis 1-2:2"],
            ["Gen11:12-11:13", "Genesis 11:12-13"],
            ["Gen10:12-13:2", "Genesis 10:12-13:2"],
            ["Gen1, Ex2", "Genesis 1, Exodus 2"],
            ["Gen1:1, Ex1:1", "Genesis 1:1, Exodus 1:1"],
            ["Gen1:1-3:4, Ex2:3", "Genesis 1:1-3:4, Exodus 2:3"],
            ["Gen1:1, Gen2:3", "Genesis 1:1, 2:3"],
            ["Gen1:1, Gen1:2", "Genesis 1:1, 2"],
            ["Gen1:3-5,1:6", "Genesis 1:3-5, 6"], # FIXME
            ["Gen1-2, 4", "Genesis 1-2, 4"],
            ["Gen1:2-4:6, 5:6-6:1", "Genesis 1:2-4:6, 5:6-6:1"]
        ]:
            self.assertEqual(ref.shorten_reference_string(instring),outstring)



if __name__ == "__main__":
    unittest.main()
