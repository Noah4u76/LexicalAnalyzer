from token import Token
from constants import TOKEN_KEYWORD, TOKEN_IDENTIFIER, TOKEN_INTEGER, TOKEN_REAL, TOKEN_OPERATOR, TOKEN_SEPARATOR
from constants import KEYWORDS, OPERATORS, SEPARATORS

class FiniteStateMachines:
    def __init__(self, lexer):
        self.lexer = lexer
        
    def identifier(self):
        """
        Regular Expression: [a-zA-Z][a-zA-Z0-9]*
        """
        # This is our initial state
        if not (self.lexer.current_char is not None and self.lexer.current_char.isalpha()):
            return None
        
        result = ''
        
        # Checking to make sure the first character is a letter our 1st state
        result += self.lexer.current_char
        self.lexer.advance()
        
        # Checking to make sure the rest of the characters are letters or numbers our 2nd state
        while self.lexer.current_char is not None and (self.lexer.current_char.isalnum()):
            result += self.lexer.current_char
            self.lexer.advance()
        
        # Checking if the result is a keyword or an identifier as a precaution for errors
        if result in KEYWORDS:
            return Token(TOKEN_KEYWORD, result)
        
        return Token(TOKEN_IDENTIFIER, result)
    
    def integer(self):
        """
        Regular Expression: [0-9]+
        """
        if not (self.lexer.current_char is not None and self.lexer.current_char.isdigit()):
            return None
        
        result = ''
        
        # Checking to make sure the first character is a digit our 1st state
        while self.lexer.current_char is not None and self.lexer.current_char.isdigit():
            result += self.lexer.current_char
            self.lexer.advance()
        
        # Checking for a real number with decimal point, saves current position for backtracking if needed
        if self.lexer.current_char == '.':
            temp_pos = self.lexer.pos
            temp_char = self.lexer.current_char
            temp_line = self.lexer.line
            temp_column = self.lexer.column
            
            result += self.lexer.current_char
            self.lexer.advance()

            #Checking if digits go beyond the decimal point, if real number revert back to previous position and let real number handle it
            if self.lexer.current_char is not None and self.lexer.current_char.isdigit():
                self.lexer.position = temp_pos
                self.lexer.current_char = temp_char
                self.lexer.line = temp_line
                self.lexer.column = temp_column
                return None
        
        return Token(TOKEN_INTEGER, result)
    
    def real(self):
        """
        Regular Expression: [0-9]+\.[0-9]+
        """
        if not (self.lexer.current_char is not None and self.lexer.current_char.isdigit()):
            return None
        
        result = ''
        
        # Checking to make sure the first character is a digit our 1st state
        while self.lexer.current_char is not None and self.lexer.current_char.isdigit():
            result += self.lexer.current_char
            self.lexer.advance()
        
        # Checking for a decimal point our 2nd state
        if self.lexer.current_char == '.':
            result += self.lexer.current_char
            self.lexer.advance()
        
            # Checking to make sure there is digits after decimal point our 3rd state
            if not (self.lexer.current_char is not None and self.lexer.current_char.isdigit()):
                raise SyntaxError(f"Invalid real number format at line {self.lexer.line}, column {self.lexer.column}")
        
            while self.lexer.current_char is not None and self.lexer.current_char.isdigit():
                result += self.lexer.current_char
                self.lexer.advance()
        
            return Token(TOKEN_REAL, result)
    
        return None
    
    def operator(self):
        """
        Simple Finite State Machine for Operators
        """
        if not (self.lexer.current_char is not None and self.lexer.current_char in OPERATORS):
            return None
        
        result = self.lexer.current_char
        self.lexer.advance()
        
        if result in ["=", "<", ">","!"] and self.lexer.current_char == "=":
            result += self.lexer.current_char
            self.lexer.advance()
        
        if result in OPERATORS:
            return Token(TOKEN_OPERATOR, result)
        else:
            raise SyntaxError(f"Invalid operator '{result}' at line {self.lexer.line}, column {self.lexer.column}")
            
        return Token(TOKEN_OPERATOR, result)
    
    def seperator(self):
        """
        Simple Finite State Machine for Separators
        """
        if not self.lexer.current_char is not None and self.lexer.current_char in SEPARATORS:
            result = self.lexer.current_char
            self.lexer.advance()
            return Token(TOKEN_SEPARATOR, result)
    
        return None