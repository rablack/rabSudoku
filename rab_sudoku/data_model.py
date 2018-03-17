from rab_sudoku import game_model

class PlayingData:
    """
    Stores content information for the playing grid.
    
    This class is used to model both the problem and the solution.
    """

    def __init__(self, boardType):
        self.__boardType = boardType
        self.__cellCount = (self.__boardType.getBoardXSize() *
                            self.__boardType.getBoardYSize())
        self.__cells = [0] * self.__cellCount
        #for i in range(self.__cellCount):
        #   self.__cells[i] = 0
            
            
    def getCell(self, x, y):
        """
        Get the contents of the cell at coordinates x, y
        
        x is 0-based offset from the left of the grid
        y is 0-based offset from the top of the grid
        A return value of 0 means the cell is empty
        """
        
        # Validate the parameters
        
        x = int(x)
        y = int(y)
        if x < 0 or x >= self.__boardType.getBoardXSize():
            raise IndexError("Index x = {0:d} is outside grid".format(x))
        if y < 0 or y >= self.__boardType.getBoardYSize():
            raise IndexError("Index y = {0:d} is outside grid".format(y))
        
        # Return the cell contents
        
        return self.__cells[x + y * self.__boardType.getBoardXSize()]
        
        
    def setCell(self, x, y, value):
        """
        Set the contents of the cell at coordinates x, y to value
        
        x is 0-based offset from the left of the grid
        y is 0-based offset from the top of the grid
        value is the numeric representation of the contents of the cell
        where 0 indicates an empty cell
        """
        
        #Validate the parameters
        
        x = int(x)
        y = int(y)
        value = int(value)
        if x < 0 or x >= self.__boardType.getBoardXSize():
            raise IndexError("Index x = {0:d} is outside grid".format(x))
        if y < 0 or y >= self.__boardType.getBoardYSize():
            raise IndexError("Index y = {0:d} is outside grid".format(y))
        # Range of value is one greater than x because it includes empty
        if value < 0 or value > self.__boardType.getBoardXSize():
            raise ValueError("Value {0:d} is out of range".format(value))
        
        # Set the cell contents
        
        self.__cells[x + y * self.__boardType.getBoardXSize()] = value
        
    def getBoard(self):
        return self.__boardType
        
        
        
class GameModel:
    """
    Stores and manages all of the model elements for a game
    """
    
    def __init__(self, board):
        self.__board = board
        if self.__board == None:
            raise ValueError("Board is not valid")
        self.__problem = PlayingData(board)
        self.__solution = PlayingData(board)
        
    def getBoard(self):
        return self.__board
                    
    def getProblem(self):
        return self.__problem
            
    def getSolution(self):
        return self.__solution
        
        
        
class GameModelController:
    """
    The main class for running the game model
    
    This maintains state for the game
    """
    def __init__(self):
        self.__model = None
    
    def loadGame(self, file):
        reader = CsvModelReader()
        
        with open(file, 'r') as fd:
            newModel = reader.read(fd)
            
        self.__model = newModel
        
        return newModel

    def getModel(self):
        return self.__model 
    
    
