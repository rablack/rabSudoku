"""Classes for defining sudoku game model"""

class BoardType:
	"""Class for defining sudoku board"""
	def __init__(self, xSize = 3, ySize = 3):
		self.__xSize = int(xSize)
		self.__ySize = int(ySize)
		
	def getXSize(self):
		return self.__xSize
		
	def getYSize(self):
		return self.__ySize
		
	def getBoardXSize(self):
		return self.__xSize * self.__ySize
		
	def getBoardYSize(self):
		return self.__ySize * self.__xSize
		
		
