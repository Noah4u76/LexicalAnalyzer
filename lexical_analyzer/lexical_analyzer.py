from token import Token
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
            