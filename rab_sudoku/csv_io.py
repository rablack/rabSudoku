"""
CSV I/O Classes
"""
from rab_sudoku import game_model, data_model 

class VersionError(Exception):
    """
    Unsupported file version
    """

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
        - Sequence containing the parsed fields. The precise nature of
          the sequence may vary.
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
        field_builder_list = []
        
        if quoted_field:
            parse_pos += 1
            
            while parse_pos < len(line):
                end_pos = line.find(self.__quote_char, parse_pos)
                if end_pos == -1:
                    raise SyntaxError("Missing '" '"' "' in CSV file")
                
                field_builder_list += line[parse_pos:end_pos]
                
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
                    field_builder_list += self.__quote_char
                    parse_pos += 1
                else:
                    raise SyntaxError("Invalid field syntax")
        else:
            # Not quoted field
            end_pos = line.find(self.__separator, parse_pos)
            if end_pos == -1:
                # Last field of line
                field_builder_list += line[parse_pos:]
                parse_pos = -1
            else:
                # Field ending in separator
                field_builder_list += line[parse_pos:end_pos]
                parse_pos = end_pos + 1;
            
        return parse_pos, "".join(field_builder_list)
        
        
        
        
class CsvModelReader:
    """
    A reader for solution and problem models
    """
    
    def __init__(self):
        self.__parser = CsvLineParser()
        self.__newModel = None
        
        
        
        
    def read(self, fobj):
        """
        Read a GameModel from a CSV io.TextIOBase
        
        Attributes:
        - fobj - io.TextIOBase
        Returns
        - GameModel
        """
        self.__newModel = None
        
        # The first line is the file format version
        version = self._readVersion(fobj)
        if version['major'] == 1:
            self._readFormat1(fobj)
        else:
            raise VersionError('Unsupported sudoku file version')
            
        return self.__newModel
        
        
        
        
    def _readLast(self):
        """
        Return the last model returned by read(fobj)
        
        Will be incomplete if read(fobj) generated an error.
        This is intended to be used for unit testing internal
        details. It is not intended to be stable.
        """
        return self.__newModel
        
        
        
        
    def _readVersion(self, fobj):
        """
        Read the version number from the start of a sudoku file
        """
        line = fobj.readline()
        fields = self.__parser.parseLine(line)
        
        # Sanitize the fields
        version_dict = {'cmd': fields[0].strip()}
        
        # Find the start and end of the integer fields
        start_int = 1
        end_int = len(fields)
        try:
            test_int = int(fields[-1].strip())
        except ValueError:
            version_dict['rel-type'] = fields[-1].strip()
            end_int = len(fields) - 1

        if end_int <= start_int:
            raise SyntaxError("Version number invalid. Correct syntax is: "
                        "version:,<major int>[,<minor>[,patch]][,<type str>]")
        
        int_fields_dict = dict(zip(['major','minor','patch'],
                                fields[start_int:end_int]))
                                
        for key, value in int_fields_dict.items():
            try:
                version_dict[key] = int(value.strip())
            except ValueError:
                msg = "Invalid version number component {0:s}: {1:s}"
                raise SyntaxError(msg.format(key, value))
                
        # Check for a correct 'version:' string
                                
        if version_dict['cmd'] != 'version:':
            raise SyntaxError("File must start with a 'version:' field")
            
        return version_dict
        
        
        
        
    def _readFormat1(self, fobj):
        """
        Read a file a format 1.0
        """
        commands = {    'problem:': 'ProblemModel',
                        'solution:': 'SolutionModel',
                        'dimensions:': 'Dimensions' }
        cmd = None
        cmd_line_no = 0
        
        for line in fobj:
            fields = self.__parser.parseLine(line)
            cmd_field = fields[0].strip()
            if cmd == None and cmd_field in commands:
                cmd = getattr(self, "_cmd1{0:s}".format(commands[cmd_field]))
                cmd_line_no = 0

            if cmd != None:
                cmd = cmd(cmd, cmd_line_no, fields)
                cmd_line_no += 1
            elif len(fields) != 1 or len(cmd_field) != 0:
                raise SyntaxError("Bad command '{0:s}'", cmd_field)
          
          
          
                
    def _cmd1ProblemModel(self, cmd, cmd_line_no, fields):
        if self.__newModel == None:
            raise SyntaxError("problem: should come after dimensions:")
            
        return self._cmd1CommonModel("problem:",
                                    self.__newModel.getProblem(),
                                    cmd,
                                    cmd_line_no,
                                    fields)
        
        
        
        
    def _cmd1SolutionModel(self, cmd, cmd_line_no, fields):
        if self.__newModel == None:
            raise SyntaxError("solution: should come after dimensions:")
            
        return self._cmd1CommonModel("solution:",
                                    self.__newModel.getSolution(),
                                    cmd,
                                    cmd_line_no,
                                    fields)
        
        
        
        
    def _cmd1CommonModel(self, modelName, model, cmd, cmd_line_no, fields):
        if cmd_line_no == 0:
            if len(fields) != 1:
                msg = "{0:s} should be defined on subsequent lines"
                raise SyntaxError(msg.format(modelName))
        else:
            board = model.getBoard()
            if len(fields) != board.getBoardXSize():
                msg = "{0:s}[{1:d}] invalid number of fields"
                raise SyntaxError(msg.format(modelName, cmd_line_no))
                
            for i, field in enumerate(fields):
                try:
                    field = field.strip()
                except AttributeError:
                    # field might already be an int which will
                    # generate an AttributeError in response to strip()
                    pass
                    
                if field == '':
                    field = 0
                try:
                    field_int = int(field)
                    model.setCell(i, cmd_line_no - 1, field_int)
                except ValueError:
                    msg = "Invalid integer '{0:s}' in cell ({1:d}, {2:d})"
                    raise SyntaxError(msg.format(field, i + 1, cmd_line_no))
         
            # If we have run out of lines cancel the command       
            if cmd_line_no >= board.getBoardYSize():
                cmd = None
        
        return cmd
        
        
        
        
    def _cmd1Dimensions(self, cmd, cmd_line_no, fields):
        if len(fields) != 3:
            raise SyntaxError("dimensions: should have exactly 2 arguments")
        x = int(fields[1])
        y = int(fields[2])
        
        if self.__newModel != None:
            raise SyntaxError("dimensions: defined multiple times")
            
        self.__newModel = data_model.GameModel(game_model.BoardType(x, y))
        
        return None
        