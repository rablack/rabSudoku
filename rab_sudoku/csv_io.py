"""
CSV I/O Classes
"""
from rab_sudoku import game_model, data_model 

class CsvLineParser:
    """
    Parse a CSV line into fields.
    """
    
    def __init__(self):
        self.__quote_char = '"'
        self.__separator = ','
        
        
    def parseLine(self, line):
        """
        Parse a CSV line into fields
        - line - String containing the CSV to parse
        Returns
        - Sequence containing the parsed fields
        """
        parse_pos = 0
        fields = []
        while parse_pos != -1:
            parse_pos, field = self.parseField(line, parse_pos)
            fields.append(field)
        return fields
        
        
    def parseField(self, line, field_pos):
        """
        Parse a field from a CSV line
        - line - String containing the field to be parsed
        - field_pos - int start position of the field
        Returns
        - parse_pos - int start of the next field or -1 if there are no more
        - field - String containing the parsed field
        """
        parse_pos = field_pos
        quoted_field = line.startswith(self.__quote_char, field_pos)
        fieldBuilderList = []
        
        if quoted_field:
            parse_pos += 1
            
            while parse_pos < len(line):
                end_pos = line.find(self.__quote_char, parse_pos)
                if end_pos == -1:
                    raise SyntaxError("Missing '" '"' "' in CSV file")
                
                fieldBuilderList += line[parse_pos:end_pos]
                
                parse_pos = end_pos + 1
                
                if parse_pos == len(line):
                    # End of line
                    parse_pos = -1
                    break
                elif line[parse_pos] == self.__separator:
                    # End of field. Consume the separator
                    parse_pos += 1;
                    break;
                elif line[parse_pos] == self.__quote_char:
                    # Quoted quote. Turn into a single instance of a quote.
                    fieldBuilderList += self.__quote_char
                    parse_pos += 1
                else:
                    raise SyntaxError("Invalid field syntax")
        else:
            # Not quoted field
            end_pos = line.find(self.__separator, parse_pos)
            if end_pos == -1:
                # Last field of line
                fieldBuilderList += line[parse_pos:]
                parse_pos = -1
            else:
                # Field ending in separator
                fieldBuilderList += line[parse_pos:end_pos]
                parse_pos = end_pos + 1;
            
        return parse_pos, "".join(fieldBuilderList)
        
        
        
        
class CsvModelReader:
    """
    A reader for solution and problem models
    """
    
    def __init__(self, board):
        self.__board_type = BoardType(board)
        self.__parser = CsvLineParser
        
    def read(self, fobj):
        pass