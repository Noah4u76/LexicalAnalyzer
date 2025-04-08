from .token import Token
from .finite_state_machines import FiniteStateMachines
from .constants import TOKEN_KEYWORD, TOKEN_IDENTIFIER, TOKEN_INTEGER, TOKEN_REAL, TOKEN_OPERATOR, TOKEN_SEPARATOR
from .constants import KEYWORDS, OPERATORS, SEPARATORS

class Lexer:
    def __init__(self,text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        if self.current_char is not None:
            if self.current_char == '\n':
                self.line += 1
                self.column = 0
            self.pos += 1
            self.column += 1
            self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
            
    def skip_comment(self):
        if self.text[self.pos:self.pos+2] == "[*":
            while self.current_char is not None:
                self.advance()
                if self.text[self.pos-1:self.pos+1] == "*]":
                    self.advance()  # Move past the closing "]*"
                    return

    def get_next_token(self):
        self.skip_whitespace()
        
        if self.text[self.pos:self.pos+2] == "[*":
            self.skip_comment()
            return self.get_next_token()
    
        if self.current_char is None:
            return None
            
        # Handle $$
        if self.current_char == '$' and self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '$':
            result = '$$'
            self.advance()
            self.advance()
            return Token(TOKEN_SEPARATOR, result)
    
        # Handle numbers properly (including real numbers with decimals)
        if self.current_char.isdigit():
            result = ''
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
        
        # If a decimal point follows, check for a valid real number
            if self.current_char == '.':
                result += '.'
                self.advance()
            
            # Ensure at least one digit follows the decimal
                if self.current_char is not None and self.current_char.isdigit():
                    while self.current_char is not None and self.current_char.isdigit():
                        result += self.current_char
                        self.advance()
                    print(f"Debug: Recognized real number '{result}'")
                    return Token(TOKEN_REAL, result)
                else:
                    raise SyntaxError(f"Invalid real number format at line {self.line}, column {self.column}")
        
            print(f"Debug: Recognized integer '{result}'")
            return Token(TOKEN_INTEGER, result)

        fsm = FiniteStateMachines(self)
        for method in [fsm.identifier, fsm.integer, fsm.real, fsm.operator, fsm.separator]:
            token = method()
            if token:
                return token

        print(f"Debug: Unrecognized character '{self.current_char}' at line {self.line}, column {self.column}")

    # Handle standalone '.'
        if self.current_char == '.':
            raise SyntaxError(f"Invalid use of '.' at line {self.line}, column {self.column}")

        raise SyntaxError(f"Invalid Character '{self.current_char}' at line {self.line}, column {self.column}")

    
    def tokenize(self):
        tokens = []
        while (token := self.get_next_token()) is not None:
            tokens.append(token)
        return tokens
