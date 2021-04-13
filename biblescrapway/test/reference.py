import unittest

from .. import reference as ref


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
        self.assertEqual(ref._get_normalized_book_name("Genesis"),"Genesis")

    def test_match_partial_name(self):
        """Can match partial book name
        """
        self.assertEqual(ref._get_normalized_book_name("Gen"),"Genesis")

    def test_match_abbreviated_name(self):
        """Can match abbreviated book name
        """
        self.assertEqual(ref._get_normalized_book_name("Gen."),"Genesis")
if __name__ == "__main__":
    unittest.main()
