import unittest

from main import extract_title


class TestMain(unittest.TestCase):
    def test_extract_title(self):
        markdown1 = "# This file has a heading"
        markdown2 = "This file is missing a heading"

        self.assertEqual(extract_title(markdown1), "This file has a heading")
        
        with self.assertRaises(Exception) as exc:
            extract_title(markdown2)
        self.assertEqual(f'{exc.exception}', 'file is missing a "# heading"')

   
if __name__ == "__main__":
    unittest.main()