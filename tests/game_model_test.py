"""Tests for game model classes in rab_sudoku.game_model"""
import unittest
import sys

sys.path.insert(0, '..')

from rab_sudoku import game_model

class TestBoardType(unittest.TestCase):
	"""Test case for rabSudoku.boardType"""
	
	def testBoardSize(self):
		"""Test various board size methods"""
		
		# Test sizes for a 2x4 Sudoku
		# 2x4 refers to the size of a block
		# The overall board size is 4 blocks by 2 blocks
		size = (2, 4)
		board = game_model.BoardType(size[0], size[1])
		self.assertEqual(size[0], board.getXSize())
		self.assertEqual(size[1], board.getYSize())
		boardSize = size[0] * size[1]
		self.assertEqual(boardSize, board.getBoardXSize())
		self.assertEqual(boardSize, board.getBoardYSize())
		
		# Test sizes for the default board
		defaultSize = (3, 3)
		defaultBoard = game_model.BoardType()
		self.assertEqual(defaultSize[0], defaultBoard.getXSize())
		self.assertEqual(defaultSize[1], defaultBoard.getYSize())
		defaultBoardSize = defaultSize[0] * defaultSize[1]
		self.assertEqual(defaultBoardSize, defaultBoard.getBoardXSize())
		self.assertEqual(defaultBoardSize, defaultBoard.getBoardYSize())

if __name__ == "__main__":
	unittest.main()