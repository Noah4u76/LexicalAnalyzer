class Token:
    def __init__(self, token_type, lexeme):
        self.token_type = token_type
        self.lexeme = lexeme
    
    def __str__(self):
        return f"Token({self.token_type:<20} {self.lexeme})"
    
    def __repr__(self):
        return f"Token({self.token_type}, {self.lexeme})"