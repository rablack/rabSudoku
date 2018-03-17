"""
Test cases for classes in csv_io.py

These cover the handling of reading and writing CSV files
"""

import unittest
import sys
import io

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
        self.assertEqual(-1, basic_3rd[0])
        
        quoted = '"Hello ""World""","Contains ,",""'
        
        quoted_1st = self.parser.parseField(quoted, 0)
        
        self.assertEqual('Hello "World"', quoted_1st[1])
        self.assertEqual(18, quoted_1st[0])
        
        quoted_2nd = self.parser.parseField(quoted, quoted_1st[0])
        
        self.assertEqual('Contains ,', quoted_2nd[1])
        self.assertEqual(31, quoted_2nd[0])
        
        quoted_3rd = self.parser.parseField(quoted, quoted_2nd[0])
        
        self.assertEqual('', quoted_3rd[1])
        self.assertEqual(-1, quoted_3rd[0])
        
        
        
        
    def testParseFieldInvalid(self):
        """
        Test for known invalid input:
        
        - Fields only part quoted
        - Unterminated quotes
        """
        pass
        
        
        
        
    def testParseLine(self):
        """
        Test the parsing of CSV lines
        """
        basic_line = '1,,3  ,4'
        basic_fields = self.parser.parseLine(basic_line)
        
        self.assertEqual('1', basic_fields[0])
        self.assertEqual('', basic_fields[1])
        self.assertEqual('3  ', basic_fields[2])
        self.assertEqual('4', basic_fields[3])
        self.assertEqual(4, len(basic_fields))
        
        
        quoted_line = '"Hello","""World""",",",""'
        quoted_fields = self.parser.parseLine(quoted_line)
        
        self.assertEqual('Hello', quoted_fields[0])
        self.assertEqual('"World"', quoted_fields[1])
        self.assertEqual(',', quoted_fields[2])
        self.assertEqual('', quoted_fields[3])
        self.assertEqual(4, len(quoted_fields))
        
        
        
        
    def testEmptyFinalField(self):
        """
        Test for issue #1
        
        CsvLineParser should handle the case where the final field is empty.
        This should result in an empty field in the output.
        """
        empty_final = '1,2,'
        empty_final_fields = self.parser.parseLine(empty_final)
        self.assertEqual(3, len(empty_final_fields))
        self.assertEqual('', empty_final_fields[2])
        
        empty_line = ''
        empty_fields = self.parser.parseLine(empty_line)
        
        self.assertEqual(1, len(empty_fields))
        self.assertEqual('', empty_fields[0])
        
        
        
        
class TestCsvModelReader(unittest.TestCase):
    def setUp(self):
        self.reader = csv_io.CsvModelReader()
        
        
        
        
    def tearDown(self):
        self.reader = None
        
        
        
        
    def test_Cmd1CommonModel(self):
        """
        Test for the common code for importing models
        """
        testData = data_model.PlayingData(game_model.BoardType(2, 2))
        newCmd = self.reader._cmd1CommonModel("test:", testData,
                                            "cmd", 1,
                                            ('1',2,'',4))
        self.assertEqual(1, testData.getCell(0, 0))
        self.assertEqual(2, testData.getCell(1, 0))
        self.assertEqual(0, testData.getCell(2, 0))
        self.assertEqual(4, testData.getCell(3, 0))
        self.assertEqual("cmd", newCmd)
        
        lastCmd = self.reader._cmd1CommonModel("test:", testData,
                                            "cmd", 4,
                                            ('4',3,2,' '))
        self.assertEqual(4, testData.getCell(0, 3))
        self.assertEqual(3, testData.getCell(1, 3))
        self.assertEqual(2, testData.getCell(2, 3))
        self.assertEqual(0, testData.getCell(3, 3))
        self.assertEqual(None, lastCmd)
        
        
        
        
    def testCmd1Dimensions(self):
        """
        Test for creation of a model
        """
        newCmd = self.reader._cmd1Dimensions("cmd", 0, ("dim:", "2", "3"))
        self.assertEqual(None, newCmd)
        
        board = self.reader._readLast().getBoard()
        self.assertEqual(2, board.getXSize())
        self.assertEqual(3, board.getYSize())
        
        
        
        
    def testCmd1ProblemModel(self):
        """
        Test for loading a problem
        """
        self.reader._cmd1Dimensions("dimensions:", 0, ("dimensions:", "3", "2"))
        newCmd = self.reader._cmd1ProblemModel("cmd:", 0, ("problem:",))
        self.assertEqual("cmd:", newCmd)
        self.assertEqual(0, self.reader._readLast().getProblem().getCell(4, 0))
        
        firstProblem = ("1", "", "3", "", "5", "")
        firstCmd = self.reader._cmd1ProblemModel("cmd:", 1, firstProblem)
        self.assertEqual("cmd:", firstCmd)
        self.assertEqual(5, self.reader._readLast().getProblem().getCell(4, 0))
        
        fifthProblem = ("", "", "", "", "", "6")
        fifthCmd = self.reader._cmd1ProblemModel("cmd:", 5, fifthProblem)
        self.assertEqual("cmd:", fifthCmd)
        self.assertEqual(6, self.reader._readLast().getProblem().getCell(5, 4))
        
        sixthProblem = ("", "2", "", "", "", "6")
        sixthCmd = self.reader._cmd1ProblemModel("cmd:", 6, sixthProblem)
        self.assertEqual(None, sixthCmd)
        self.assertEqual(2, self.reader._readLast().getProblem().getCell(1, 5))
       
       
       
       
    def testCmd1SolutionModel(self):
        """
        Test for loading a solution
        """
        self.reader._cmd1Dimensions("dimensions:", 0, ("dimensions:", "3", "2"))
        newCmd = self.reader._cmd1SolutionModel("cmd:", 0, ("solution:",))
        self.assertEqual("cmd:", newCmd)
        self.assertEqual(0, self.reader._readLast().getProblem().getCell(4, 0))
        
        firstSolution = ("1", "", "3", "", "5", "")
        firstCmd = self.reader._cmd1SolutionModel("cmd:", 1, firstSolution)
        self.assertEqual("cmd:", firstCmd)
        self.assertEqual(5, self.reader._readLast().getSolution().getCell(4, 0))
        
        fifthSolution = ("", "", "", "", "", "6")
        fifthCmd = self.reader._cmd1SolutionModel("cmd:", 5, fifthSolution)
        self.assertEqual("cmd:", fifthCmd)
        self.assertEqual(6, self.reader._readLast().getSolution().getCell(5, 4))
        
        sixthSolution = ("", "2", "", "", "", "6")
        sixthCmd = self.reader._cmd1SolutionModel("cmd:", 6, sixthSolution)
        self.assertEqual(None, sixthCmd)
        self.assertEqual(2, self.reader._readLast().getSolution().getCell(1, 5))

        # Check that this did not affect the problem model
        self.assertEqual(0, self.reader._readLast().getProblem().getCell(1, 5))
        
        
        
        
    def _createTestCsvObjectFormat1(self, version=True, versionString=None,
            dimensions=True, problem=True, solution=True, junk=False):
        """
        Create a CSV I/O object to test format 1.x
        
        This object should be closed by calling its close() method
        to free resources
        """
        fobj = io.StringIO()
        
        if version:
            if versionString == None:
                print("version:, 1, 0, 9, dev", file=fobj)
            else:
                print("{0:s}".format(versionString), file=fobj)
                
        if dimensions:
            print("", file=fobj)
            print("dimensions:, 3, 3", file=fobj)
            
        if problem:
            print("", file=fobj)
            print("problem:", file=fobj)
            print(" ,1,2,5,3, ,7, , ", file=fobj)
            print("7, , , , ,6,4, ,3", file=fobj)
            print("4,3, , , , ,5,2, ", file=fobj)
            print(" ,4,3,9,1, ,8,7,6", file=fobj)
            print("8, , , , , ,2, , ", file=fobj)
            print("5,6,1,8, ,2,9,3, ", file=fobj)
            print(" ,8,7,6, ,9,1,4,2", file=fobj)
            print("1, ,5, , ,8, ,9, ", file=fobj)
            print("6,9,4,1,2,7,3, ,5", file=fobj)
            
        if solution:
            print("", file=fobj)
            print("solution:", file=fobj)
            print("9, , , , ,4, ,6,8", file=fobj)
            print(" ,5,8,2,9, , ,1, ", file=fobj)
            print(" , ,6,7,8,1, , ,9", file=fobj)
            print("2, , , , ,5, , , ", file=fobj)
            print(" ,7,9,4,6,3, ,5,1", file=fobj)
            print(" , , , ,7, , , ,4", file=fobj)
            print("3, , , ,5, , , , ", file=fobj)
            print(" ,2, ,3,4, ,6, ,7", file=fobj)
            print(" , , , , , , ,8, ", file=fobj)
            
        if junk:
            print("junk", file=fobj)
        
        fobj.seek(0)
        
        return fobj
        
        
        
        
    def testVersion(self):
        """
        Test the version handling
        """
        fobj = self._createTestCsvObjectFormat1()
        try:
            version = self.reader._readVersion(fobj)
            self.assertEqual("version:", version['cmd'])
            self.assertEqual(1, version['major'])
            self.assertEqual(0, version['minor'])
            self.assertEqual(9, version['patch'])
            self.assertEqual("dev", version['rel-type'])
        finally:
            fobj.close()
        
        
        
        
    def testFormat1(self):
        """
        Test the handling of Format1
        """
        fobj = self._createTestCsvObjectFormat1(version=False)
        try:
            self.reader._readFormat1(fobj)
            result = self.reader._readLast()
            
            self.assertEqual(3, result.getBoard().getXSize())
            self.assertEqual(1, result.getProblem().getCell(1, 0))
            self.assertEqual(0, result.getProblem().getCell(7, 8))
            self.assertEqual(9, result.getSolution().getCell(0, 0))
            self.assertEqual(8, result.getSolution().getCell(7, 8))
            
        finally:
            fobj.close()
            
            
            
            
    def testRead(self):
        """
        Test the full read method
        """
        fobj = self._createTestCsvObjectFormat1()
        try:
            result = self.reader.read(fobj)
            
            self.assertEqual(3, result.getBoard().getYSize())
            self.assertEqual(3, result.getSolution().getCell(0,6))
            self.assertEqual(6, result.getProblem().getCell(8,3))
        finally:
            fobj.close()
            
            
            
            
    def testReadNoVersion(self):
        fobj = self._createTestCsvObjectFormat1(version=False)
        try:
            self.assertRaises(SyntaxError, self.reader.read, fobj)
        finally:
            fobj.close()
            
            
            
            
    def testReadJunk(self):
        fobj = self._createTestCsvObjectFormat1(junk=True)
        try:
            self.assertRaises(SyntaxError, self.reader.read, fobj)
        finally:
            fobj.close()
            
            
            
                    
if __name__ == "__main__":
    unittest.main()
        
        