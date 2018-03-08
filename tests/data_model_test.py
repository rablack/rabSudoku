"""
Test cases for classes in data_model.py

These cover the handling of data for games in progress
"""

import unittest
import sys

# If this test is being executed standalone, add '..' to the path
# to start searching for packages from the top level of the app.
if __name__ == "__main__":
    sys.path.insert(0, '..')

from rab_sudoku import data_model
from rab_sudoku import game_model

class TestEntryData(unittest.TestCase):
    """
    Test case for rab_sudoku.data_model.EntryData
    
    Verify that the PlayingData class for manipulating
    the numbers entered into the playing grid works as intended
    """
    
    def setUp(self):
        self.board33 = game_model.BoardType(3, 3)
        self.board24 = game_model.BoardType(2, 4)
        
    def tearDown(self):
        self.board33 = None
        self.board24 = None
    
    def testCells(self):
        """
        Test that the reading and writing of cells works
        """
        solution = data_model.PlayingData(self.board33)
        
        # All cells start as 0 (empty)
        self.assertEqual(0, solution.getCell(1, 1))
        
        # Set the value of a cell to 4
        solution.setCell(1, 1, 4)
        self.assertEqual(4, solution.getCell(1,1))
        self.assertEqual(0, solution.getCell(2,1))
        
        # Clear the cell again
        solution.setCell(1, 1, 0)
        self.assertEqual(0, solution.getCell(1, 1))
        
        # Check the corners
        solution.setCell(0, 0, 1)
        solution.setCell(8, 0, 2)
        solution.setCell(0, 8, 3)
        solution.setCell(8, 8, 4)
        self.assertEqual(1, solution.getCell(0, 0))
        self.assertEqual(2, solution.getCell(8, 0))
        self.assertEqual(3, solution.getCell(0, 8))
        self.assertEqual(4, solution.getCell(8, 8))
        
    def testCellInvalidIndex(self):
        """
        Test that x and y index parameters outside the play area
        trigger an IndexError exception
        """
        solution = data_model.PlayingData(self.board33)
        solution24 = data_model.PlayingData(self.board24)
        
        INVALID_CELLS = ((-1, 2), (0, -1), (9, 1), (2, 9))
        
        for cell in INVALID_CELLS:
            for do_set in (True, False):
                exception_thrown = False
                try:
                    if do_set:
                        solution.setCell(*cell, 1)
                    else:
                        solution.getCell(*cell)
                except IndexError:
                    exception_thrown = True
                msg = "Exception thrown for invalid cell ({0:d}, {1:d})"
                self.assertTrue(exception_thrown, msg.format(*cell))
        
    def testCellInvalidValue(self):
        """
        Test that invalid values generate ValueError exceptions
        """
        solutions = ((data_model.PlayingData(self.board33), "3x3"),
                    (data_model.PlayingData(self.board24), "2x4"))
                    
        # Value tests are:
        # (test_value, (board33_valid, board24_valid))
        VALUE_TESTS = ((0, (True, True)),
                        (-1, (False, False)),
                        (9, (True, False)),
                        (10, (False, False)))
        for value_test in VALUE_TESTS:
            value = value_test[0]
            for solution_id in range(len(solutions)):
                solution = solutions[solution_id][0]
                solution_name = solutions[solution_id][1]
                is_valid = value_test[1][solution_id]
                
                exception_thrown = False    
                try:
                    solution.setCell(1, 1, value)
                except ValueError:
                    exception_thrown = True
                
                if (is_valid):  
                    msg = "No exception for valid value {0:d} in {1:s}"
                    self.assertFalse(exception_thrown,
                                    msg.format(value, solution_name))
                else:
                    msg = "Exception for invalid value {0:d} in {1:s}"
                    self.assertTrue(exception_thrown,
                                    msg.format(value, solution_name))       
        
if __name__ == "__main__":
    unittest.main()
        
        