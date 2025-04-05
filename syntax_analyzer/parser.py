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
        
    def rat25s(self):
        """
        R1. <Rat25S> ::= $$ <Opt Function Definitions> $$ <Opt Declaration List> $$ <Statement List> $$
        """
        self.print_production("<Rat25S> -> $$ <Opt Function Definitions> $$ <Opt Declaration List> $$ <Statement List> $$")
        
        # Match the first $$
        if self.current_token and self.current_token.lexeme == "$$":
            self.match(lexeme="$$")
        else:
            self.error("Expected '$$' at the beginning of the program")
        
        # Parse optional function definitions
        self.opt_function_definitions()
        
        # Match the second $$
        if self.current_token and self.current_token.lexeme == "$$":
            self.match(lexeme="$$")
        else:
            self.error("Expected '$$' after function definitions")
        
        # Parse optional declarations
        self.opt_declaration_list()
        
        # Match the third $$
        if self.current_token and self.current_token.lexeme == "$$":
            self.match(lexeme="$$")
        else:
            self.error("Expected '$$' after declarations")
        
        # Parse statement list
        self.statement_list()
        
        # Match the fourth $$
        if self.current_token and self.current_token.lexeme == "$$":
            self.match(lexeme="$$")
        else:
            self.error("Expected '$$' at the end of the program")
    
    def opt_function_definitions(self):
        """
        R2. <Opt Function Definitions> ::= <Function Definitions> | <Empty>
        """
        self.print_production("<Opt Function Definitions> -> <Function Definitions> | <Empty>")
        
        # Check if we have a function definition
        if self.current_token and self.current_token.lexeme == "function":
            self.function_definitions()
        # else: Empty production, do nothing
    
    def function_definitions(self):
        """
        R3. <Function Definitions> ::= <Function> | <Function> <Function Definitions>
        """
        self.print_production("<Function Definitions> -> <Function> | <Function> <Function Definitions>")
        
        # Parse a function
        self.function()
        
        # Check if there are more functions
        if self.current_token and self.current_token.lexeme == "function":
            self.function_definitions()
    
    def function(self):
        """
        R4. <Function> ::= function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>
        """
        self.print_production("<Function> -> function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")
        
        # Match 'function' keyword
        self.match(TOKEN_KEYWORD, "function")
        
        # Match identifier
        if self.current_token and self.current_token.token_type == TOKEN_IDENTIFIER:
            self.match(TOKEN_IDENTIFIER)
        else:
            self.error("Expected identifier after 'function'")
        
        # Match opening parenthesis
        if self.current_token and self.current_token.lexeme == "(":
            self.match(TOKEN_SEPARATOR, "(")
        else:
            self.error("Expected '(' after function identifier")
        
        # Parse optional parameter list
        self.opt_parameter_list()
        
        # Match closing parenthesis
        if self.current_token and self.current_token.lexeme == ")":
            self.match(TOKEN_SEPARATOR, ")")
        else:
            self.error("Expected ')' after parameter list")
        
        # Parse optional declaration list
        self.opt_declaration_list()
        
        # Parse function body
        self.body()
    
    def opt_parameter_list(self):
        """
        R5. <Opt Parameter List> ::= <Parameter List> | <Empty>
        """
        self.print_production("<Opt Parameter List> -> <Parameter List> | <Empty>")
        
        # Check if there's a parameter (by checking for an identifier)
        if self.current_token and self.current_token.token_type == TOKEN_IDENTIFIER:
            self.parameter_list()
        # else: Empty production, do nothing
    
    def parameter_list(self):
        """
        R6. <Parameter List> ::= <Parameter> | <Parameter> , <Parameter List>
        """
        self.print_production("<Parameter List> -> <Parameter> | <Parameter> , <Parameter List>")
        
        # Parse a parameter
        self.parameter()
        
        # Check if there are more parameters
        if self.current_token and self.current_token.lexeme == ",":
            self.match(TOKEN_SEPARATOR, ",")
            self.parameter_list()
    
    def parameter(self):
        """
        R7. <Parameter> ::= <IDs> <Qualifier>
        """
        self.print_production("<Parameter> -> <IDs> <Qualifier>")
        
        # Parse IDs
        self.ids()
        
        # Parse qualifier
        self.qualifier()
    
    def qualifier(self):
        """
        R8. <Qualifier> ::= integer | boolean | real
        """
        self.print_production("<Qualifier> -> integer | boolean | real")
        
        # Match one of the type qualifiers
        if self.current_token and self.current_token.lexeme in ["integer", "boolean", "real"]:
            self.match(TOKEN_KEYWORD)
        else:
            self.error("Expected type qualifier (integer, boolean, or real)")
    
    def body(self):
        """
        R9. <Body> ::= { <Statement List> }
        """
        self.print_production("<Body> -> { <Statement List> }")
        
        # Match opening brace
        if self.current_token and self.current_token.lexeme == "{":
            self.match(TOKEN_SEPARATOR, "{")
        else:
            self.error("Expected '{' at the beginning of function body")
        
        # Parse statement list
        self.statement_list()
        
        # Match closing brace
        if self.current_token and self.current_token.lexeme == "}":
            self.match(TOKEN_SEPARATOR, "}")
        else:
            self.error("Expected '}' at the end of function body")
    
    def opt_declaration_list(self):
        """
        R10. <Opt Declaration List> ::= <Declaration List> | <Empty>
        """
        self.print_production("<Opt Declaration List> -> <Declaration List> | <Empty>")
        
        # Check if there's a declaration (by checking for a qualifier)
        if self.current_token and self.current_token.lexeme in ["integer", "boolean", "real"]:
            self.declaration_list()
        # else: Empty production, do nothing
        
    