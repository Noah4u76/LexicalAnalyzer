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