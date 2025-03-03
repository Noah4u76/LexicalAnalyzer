from token import Token
from finite_state_machines import FiniteStateMachines
from constants import TOKEN_KEYWORD, TOKEN_IDENTIFIER, TOKEN_INTEGER, TOKEN_REAL, TOKEN_OPERATOR, TOKEN_SEPARATOR
from constants import KEYWORDS, OPERATORS, SEPARATORS

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
    

    def get_next_token(self):
        self.skip_whitespace()
        if self.current_char is None:
            return None
        
        #Checking order of the FSM's
        fsm = FiniteStateMachines(self)
        for method in [fsm.identifier, fsm.integer, fsm.real, fsm.operator, fsm.seperator]:
             token = method()
             if token:
                 return token
        print(f"Debug: Unrecognized character '{self.current_char}' at line {self.line}, column {self.column}")
        
        if self.current_char in SEPARATORS:
            print(f"Debug: Recognized separator '{self.current_char}'")
            token = Token(TOKEN_SEPARATOR, self.current_char)
            self.advance()
            return token
        
        if self.current_char == '.' and self.pos > 0 and self.text[self.pos - 1].isdigit():
            result = '.'
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            print(f"Debug: Recognized real number '{result}'")
            return Token(TOKEN_REAL, result)
        
        raise SyntaxError(f"Invalid Character '{self.current_char}' at line {self.line}, column {self.column}")

    
    def tokenize(self):
        tokens = []
        while (token := self.get_next_token()) is not None:
            tokens.append(token)
        return tokens