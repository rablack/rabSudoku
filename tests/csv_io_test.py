"""
Test cases for classes in csv_io.py

These cover the handling of reading and writing CSV files
"""

import unittest
import sys

# If this test is being executed standalone, add '..' to the path
# to start searching for packages from the top level of the app.
if __name__ == "__main__":
    sys.path.insert(0, '..')

from rab_sudoku import data_model
from rab_sudoku import game_model
from rab_sudoku import csv_io

class TestCsvLineParser(unittest.TestCase):
    """
    Test case for rab_sudoku.csv_io.CsvLineParser
    
    Verify that fields and lines are parsed correctly
    """
    
    def setUp(self):
        self.parser = csv_io.CsvLineParser()
        
    def tearDown(self):
        self.parser = None
    
    def testParseField(self):
        """
        Test the parsing of correctly formed fields
        
        Fields include all spaces.
        Commas may be included in fields enclosed in double quotes.
        Double quotes may be included in quoted fields by repeating them.
        A pair of double quotes in the CSV becomes one double quote.
        """
        basic = '2, 3 ,4'
        
        basic_pos_1st, basic_field_1st = self.parser.parseField(basic, 0)
        
        self.assertEqual("2", basic_field_1st)
        self.assertEqual(2, basic_pos_1st)
        
        basic_2nd = self.parser.parseField(basic, basic_pos_1st)
        
        self.assertEqual(" 3 ", basic_2nd[1])
        self.assertEqual(6, basic_2nd[0])
        
        basic_3rd = self.parser.parseField(basic, basic_2nd[0])
        
        self.assertEqual("4", basic_3rd[1])
        self.assertEqual(7, basic_3rd[0])
        
        quoted = '"Hello ""World""","Contains ,",""'
        
        quoted_1st = self.parser.parseField(quoted, 0)
        
        self.assertEqual('Hello "World"', quoted_1st[1])
        self.assertEqual(18, quoted_1st[0])
        
        quoted_2nd = self.parser.parseField(quoted, quoted_1st[0])
        
        self.assertEqual('Contains ,', quoted_2nd[1])
        self.assertEqual(31, quoted_2nd[0])
        
        quoted_3rd = self.parser.parseField(quoted, quoted_2nd[0])
        
        self.assertEqual('', quoted_3rd[1])
        self.assertEqual(33, quoted_3rd[0])

if __name__ == "__main__":
    unittest.main()
        
        