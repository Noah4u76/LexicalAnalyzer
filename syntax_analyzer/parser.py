from lexical_analyzer.lexical_analyzer import Lexer
from lexical_analyzer.token import Token
from lexical_analyzer.constants import (
    TOKEN_KEYWORD, TOKEN_IDENTIFIER, TOKEN_INTEGER, 
    TOKEN_REAL, TOKEN_OPERATOR, TOKEN_SEPARATOR
)

class Parser:
    """
    Initializes the parser with a lexer and an optional output file.
    """
    def __init__(self, lexer, output_file=None, debug=None):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.output_file = output_file
        self.debug = debug
        
        if output_file:
            self.output_file = open(output_file, 'w')
        else:
            self.output_file = None
    
    def __del__(self):
        if self.output_file:
            self.output_file.close()
            
    def error(self, message="Syntax error"):
        """
        Raises an error with a message and the current line and column of the lexer.
        """
        error_msg = f"{message} at line {self.lexer.line}, column {self.lexer.column}"
        error_msg += f"\nUnexpected token: {self.current_token}"
        
        if self.output:
            self.output_file.write(f"Error: {error_msg}\n")
        
        raise Exception(error_msg)
    
    def print_production(self, production):
        """
        Prints production rule that is being used.
        """
        
        if self.debug:
            output_str = (f"Production: {production}")
        
            if self.output:
                self.output.write(f"{output_str}\n")
                
            print(output_str)
            
    def print_token(self):
        """
        Prints the current token and lexemme
        """
        
        if self.current_token:
            output_str = f"Token: {self.current_token.type}, Lexeme: {self.current_token.lexeme}"
            
            if self.output:
                self.output.write(f"{output_str}\n")
            
            print(output_str)
    
    def match(self, token_type=None, lexeme=None):
        """
        Matches the current token with the expected token type and lexeme.
        """
        
        if self.current_token is None:
            self.error("Unexpected end of input")
            
        self.print_token()
        
        if token_type and self.current_token.type != token_type:
            self.error(f"Expected token type {token_type}, but got {self.current_token.type}")
            
        if lexeme and self.current_token.lexeme != lexeme:
            self.error(f"Expected lexeme {lexeme}, but got {self.current_token.lexeme}")
            
        self.current_token = self.lexer.get_next_token()
        
    def parse(self):
        """
        Starts the parsing process from the top-level rule <Rat25S>.
        """
        
        try:
            self.rat25s()
            print("Parsing completed successfully!")
            if self.output:
                self.output.write("Parsing completed successfully!\n")
        except SyntaxError as e:
            print(f"Parsing failed: {e}")
            if self.output:
                self.output.write(f"Parsing failed: {e}\n")
        
            
        
    