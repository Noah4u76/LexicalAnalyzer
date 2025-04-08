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
        self.output_file = None
        self.debug = True
        
        if output_file:
            self.output_file = open(output_file, 'w')
        else:
            self.output_file = None
    
    def __del__(self):
        if hasattr(self, 'output_file') and self.output_file:
            self.output_file.close()
            
    def error(self, message="Syntax error"):
        """
        Raises an error with a message and the current line and column of the lexer.
        """
        error_msg = f"{message} at line {self.lexer.line}, column {self.lexer.column}"
        error_msg += f"\nUnexpected token: {self.current_token}"
        
        if self.output_file:
            self.output_file.write(f"Error: {error_msg}\n")
        
        raise Exception(error_msg)
    
    def print_production(self, production):
        """
        Prints production rule that is being used.
        """
        output_str = (f"\tProduction: {production}")
        
        if self.output_file:
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
            if self.output_file:
                self.output_file.write("Parsing completed successfully!\n")
        except SyntaxError as e:
            print(f"Parsing failed: {e}")
            if self.output_file:
                self.output_file.write(f"Parsing failed: {e}\n")
        
    def rat25s(self):
        """
        R1. <Rat25S> ::= $$ <Opt Function Definitions> $$ <Opt Declaration List> $$ <Statement List> $$
        """
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

        self.print_production("<Rat25S> -> $$ <Opt Function Definitions> $$ <Opt Declaration List> $$ <Statement List> $$")
        
    def opt_function_definitions(self):
        """
        R2. <Opt Function Definitions> ::= <Function Definitions> | <Empty>
        """
        # Check if we have a function definition
        if self.current_token and self.current_token.lexeme == "function":
            self.function_definitions()
        # else: Empty production, do nothing
        
        self.print_production("<Opt Function Definitions> -> <Function Definitions> | <Empty>")
        
    def function_definitions(self):
        """
        R3. <Function Definitions> ::= <Function> | <Function> <Function Definitions>
        """
        # Parse a function
        self.function()
        
        # Check if there are more functions
        if self.current_token and self.current_token.lexeme == "function":
            self.function_definitions()

        self.print_production("<Function Definitions> -> <Function> | <Function> <Function Definitions>")
        
    def function(self):
        """
        R4. <Function> ::= function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>
        """
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

        self.print_production("<Function> -> function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")
        
    def opt_parameter_list(self):
        """
        R5. <Opt Parameter List> ::= <Parameter List> | <Empty>
        """
        # Check if there's a parameter (by checking for an identifier)
        if self.current_token and self.current_token.token_type == TOKEN_IDENTIFIER:
            self.parameter_list()
        # else: Empty production, do nothing

        self.print_production("<Opt Parameter List> -> <Parameter List> | <Empty>")
        
    def parameter_list(self):
        """
        R6. <Parameter List> ::= <Parameter> | <Parameter> , <Parameter List>
        """
        # Parse a parameter
        self.parameter()
        
        # Check if there are more parameters
        if self.current_token and self.current_token.lexeme == ",":
            self.match(TOKEN_SEPARATOR, ",")
            self.parameter_list()

        self.print_production("<Parameter List> -> <Parameter> | <Parameter> , <Parameter List>")
        
    def parameter(self):
        """
        R7. <Parameter> ::= <IDs> <Qualifier>
        """
        # Parse IDs
        self.ids()
        
        # Parse qualifier
        self.qualifier()
        
        self.print_production("<Parameter> -> <IDs> <Qualifier>")
        
    def qualifier(self):
        """
        R8. <Qualifier> ::= integer | boolean | real
        """
        # Match one of the type qualifiers
        if self.current_token and self.current_token.lexeme in ["integer", "boolean", "real"]:
            self.match(TOKEN_KEYWORD)
        else:
            self.error("Expected type qualifier (integer, boolean, or real)")
        
        self.print_production("<Qualifier> -> integer | boolean | real")
        
    def body(self):
        """
        R9. <Body> ::= { <Statement List> }
        """
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
        
        self.print_production("<Body> -> { <Statement List> }")
        
    def opt_declaration_list(self):
        """
        R10. <Opt Declaration List> ::= <Declaration List> | <Empty>
        """
        # Check if there's a declaration (by checking for a qualifier)
        if self.current_token and self.current_token.lexeme in ["integer", "boolean", "real"]:
            self.declaration_list()
        # else: Empty production, do nothing
        
        self.print_production("<Opt Declaration List> -> <Declaration List> | <Empty>")
        
    def declaration_list(self):
        """
        R11. <Declaration List> ::= <Declaration> | <Declaration> <Declaration List>
        """
        self.declaration()
        if self.current_token and self.current_token.lexeme in ["integer", "boolean", "real"]:
            self.declaration_list()

        self.print_production("<Declaration List> -> <Declaration> | <Declaration> <Declaration List>")
        
    def declaration(self):
        """
        R12. <Declaration ::= <Qualifier> <IDs>
        """
        self.qualifier()
        self.ids()

        # Match semicolon after IDs
        if self.current_token and self.current_token.lexeme == ";":
            self.match(TOKEN_SEPARATOR, ";")
        else:
            self.error("Expected ';' after declaration")
        
        self.print_production("<Declaration> -> <Qualifier> <IDs>")
    
    def ids(self):
        """
        R13. <IDs> ::= <Identifier> | <Identifier>, <IDs>
        """
        self.match(TOKEN_IDENTIFIER)
        if self.current_token and self.current_token.lexeme == ",":
            self.match(TOKEN_SEPARATOR, ",")
            self.ids()
        
        self.print_production("<IDs> -> <Identifier> | <Identifier>, <IDs>")
        
    def statement_list(self):
        """
        R14. <Statement List> ::= <Statement> | <Statement> <Statement List>
        """
        # Check if end of statement list
        if not self.current_token and self.current_token.lexeme == "$$" or self.current_token.lexeme == "}":
            return
                
        self.statement()
        # Parse for more statements if available
        if self.current_token and self.current_token.lexeme in ["identifier", "if", "while", "{"]:
            self.statement_list()

        self.print_production("<Statement List> -> <Statement> <Statement List>")
        
    def statement(self):
        """
        R15. <Statement> ::= <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>
        """
        if not self.current_token:
            return
            
        if self.current_token.lexeme == "{":
            self.compound()
        elif self.current_token.lexeme == "if":
            self.if_statement()
        elif self.current_token.lexeme == "return":
            self.return_statement()
        elif self.current_token.lexeme == "print":
            self.print_statement()
        elif self.current_token.lexeme == "scan":
            self.scan_statement()
        elif self.current_token.lexeme == "while":
            self.while_statement()
        elif self.current_token.lexeme = "$$" or self.current_token.lexeme == "}":
            self.empty()
        elif self.current_token.token_type == TOKEN_IDENTIFIER:
            self.assign()
        else:
            self.error("Invalid Statement, unexpected token: {self.current_token.lexeme}")

        self.print_production("<Statment> -> <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>")
        
    def compound(self): 
        """
        R16. <Compound> ::= { <Statement List> }
        """
        self.match(TOKEN_SEPARATOR, "{")
        self.statement_list()

        # Check for closing brace
        if self.current_token and self.current_token.lexeme == "}":
            self.match(TOKEN_SEPARATOR, "}")
        else:
            self.error("Expected '}}' at the end of compound statement")
            
        self.print_production("<Compound> -> { <Statement List> }")
        
    def assign(self):
        """
        R17. <Assign> ::= <Identifier> = <Expression>
        """
        self.match(TOKEN_IDENTIFIER)
        self.match(TOKEN_OPERATOR, "=")
        self.expression()

        # Match semicolon
        if self.current_token and self.current_token.lexeme == ";":
            self.match(TOKEN_SEPARATOR, ";")
        else:
            self.error("Expected ';' after assignment")
        
        self.print_production(" <Assign> -> <Identifier> = <Expression>")
        
    def if_statement(self):
        """
        R18. <If> ::= if ( <Condition> ) <Statement> endif | if ( <Condition> ) <Statement> else <Statement> endif
        """
          
        # Match 'if'
        self.match(TOKEN_KEYWORD, "if")
        
        # Match opening parenthesis
        if self.current_token and self.current_token.lexeme == "(":
            self.match(TOKEN_SEPARATOR, "(")
        else:
            self.error("Expected '(' after 'if'")
            
        # Parse condition
        self.condition()
        
        # Match closing parenthesis
        if self.current_token and self.current_token.lexeme == ")":
            self.match(TOKEN_SEPARATOR, ")")
        else:
            self.error("Expected ')' after condition")
        
        # Parse statement
        self.statement()
        
        # Check for 'else'
        if self.current_token and self.current_token.lexeme == "else":
            self.match(TOKEN_KEYWORD, "else")
            self.statement()
        
        # Match 'endif'
        if self.current_token and self.current_token.lexeme == "endif":
            self.match(TOKEN_KEYWORD, "endif")
        else:
            self.error("Expected 'endif' at end of if statement")
            
        self.print_production("<If> -> if ( <Condition> ) <Statement> endif | if ( <Condition> ) <Statement> else <Statement> endif")
        
    def return_statement(self):
        """
        R19. <Return> ::= return ; | return <Expression>
        """
        # Match 'return'
        self.match(TOKEN_KEYWORD, "return")
        
        # Parse expression
        self.expression()
        
        # Match semicolon
        if self.current_token and self.current_token.lexeme == ";":
            self.match(TOKEN_SEPARATOR, ";")
        else:
            self.error("Expected ';' after return expression")
                
        self.print_production("<Return> -> return ; | return <Expression>")
            
    def print_statement(self):
        """
        R20. <Print> ::= print ( <Expression>)
        """
        # Match 'print'
        self.match(TOKEN_KEYWORD, "print")
        
        # Match opening parenthesis
        if self.current_token and self.current_token.lexeme == "(":
            self.match(TOKEN_SEPARATOR, "(")
        else:
            self.error("Expected '(' after 'print'")
            
        # Parse expression
        self.expression()
        
        # Match closing parenthesis
        if self.current_token and self.current_token.lexeme == ")":
            self.match(TOKEN_SEPARATOR, ")")
        else:
            self.error("Expected ')' after expression")
            
        # Match semicolon
        if self.current_token and self.current_token.lexeme == ";":
            self.match(TOKEN_SEPARATOR, ";")
        else:
            self.error("Expected ';' after print expression")
            
        self.print_production(" <Print> -> print ( <Expression>)")

    def scan_statement(self):
        """
        R21. <Scan Statement> ::= scan ( <IDs> )
        """
        # Match 'scan'
        self.match(TOKEN_KEYWORD, "scan")
        
        # Match opening parenthesis
        if self.current_token and self.current_token.lexeme == "(":
            self.match(TOKEN_SEPARATOR, "(")
        else:
            self.error("Expected '(' after 'scan'")
        
        # Parse IDs
        self.ids()
        
        # Match closing parenthesis
        if self.current_token and self.current_token.lexeme == ")":
            self.match(TOKEN_SEPARATOR, ")")
        else:
            self.error("Expected ')' after IDs in scan statement")

        # Match semicolon
        if self.current_token and self.current_token.lexeme == ";":
            self.match(TOKEN_SEPARATOR, ";")
        else:
            self.error("Expected ';' after scan statement")
        
        self.print_production("<Scan Statement> -> scan ( <IDs> )")
        
    def while_statement(self):
        """
        R22. <While Statement> ::= while ( <Expression> ) <Statement>
        """
        # Match 'while'
        self.match(TOKEN_KEYWORD, "while")
        
        # Match opening parenthesis
        if self.current_token and self.current_token.lexeme == "(":
            self.match(TOKEN_SEPARATOR, "(")
        else:
            self.error("Expected '(' after 'while'")
        
        # Parse condition
        self.condition()
        
        # Match closing parenthesis
        if self.current_token and self.current_token.lexeme == ")":
            self.match(TOKEN_SEPARATOR, ")")
        else:
            self.error("Expected ')' after expression in while statement")
        
        # Parse statement
        self.statement()

        # Match "endwhile"
        if self.current_token and self.current_token.lexeme == "endwhile":
            self.match(TOKEN_KEYWORD, "endwhile")
        else:
            self.error("Expected 'endwhile' after while statement")

        self.print_production("<While Statement> -> while ( <Expression> ) <Statement>")
        
    def condition(self):
        """
        R23. <Condition> ::= <Expression> <Relop> <Expression>
        """
        # Parse first expression
        self.expression()
        
        # Parse relational operator
        self.relop()
        
        # Parse second expression
        self.expression()

        self.print_production("<Condition> -> <Expression> <Relop> <Expression>")
        
    def relop(self):
        """
        R24. <Relop> ::= == | != | > | < | <= | >=
        """
        # Match one of the relational operators
        if self.current_token and self.current_token.lexeme in [ "==", "!=", ">", "<", "<=", ">="]:
            self.match(TOKEN_OPERATOR)
        else:
            self.error("Expected relational operator (==, !=, >, <, <=, >=)")

        self.print_production("<Relop> -> == | != | > | < | <= | >=")
        
    def expression(self):
        """
        R25. <Expression> ::= + <Term> <Expression> | - <Term> <Expression> | <Empty>
        """
        # Parse term
        self.term()
        
        # Check if there's an addition operator
        if self.current_token and self.current_token.lexeme == "+":
            self.match(TOKEN_OPERATOR, "+")
            self.expression()
        # Check if there's a subtraction operator
        elif self.current_token and self.current_token.lexeme == "-":
            self.match(TOKEN_OPERATOR, "-")
            self.expression()
        # else: Empty production, do nothing
        
        self.print_production("<Expression> -> + <Term> <Expression> | - <Term> <Expression> | <Empty>")

    def term(self):
        """
        R26. <Term> ::= <Factor> | <Factor> <Mulop> <Term>
        """
        # Parse factor
        self.factor()
        
        # Check if there's a multiplication/ division operator
        if self.current_token and self.current_token.lexeme == "*":
            self.match(TOKEN_OPERATOR, "*")
            self.term()
        elif self.current_token and self.current_token.lexeme == "/":
            self.match(TOKEN_OPERATOR, "/")
            self.term()
        # else: Empty production, do nothing
    
        self.print_production("<Term> -> <Factor> | <Factor> <Mulop> <Term>")
        
    def factor(self):
        """
        R27. <Factor> ::= <Primary> | <Primary>
        """
        # Parse primary
        self.primary()
        
        if self.current_token and self.current_token.lexeme == "-":
            self.match(TOKEN_OPERATOR, "-")
            self.primary()
        else:
            self.primary()
        
        self.print_production("<Factor> -> <Primary> | <Primary>")
    
    def primary(self):
        """
        R28. <Primary> ::= <Identifier> | <Integer> | <Identifier> ( <IDs>) | ( <Expression> ) | <Real> | true | false
        """
        # Empty production check
        if self.current_token is None:
            self.error("Unexpected end of input")

        # Check for IDs
        if self.current_token and self.current_token.token_type == TOKEN_IDENTIFIER:
            self.match(TOKEN_IDENTIFIER)

            # Check for function call
            if self.current_token and self.current_token.lexeme == "(":
                self.match(TOKEN_SEPARATOR, "(")
                self.ids()

                if self.current_token and self.current_token.lexeme ==")":
                    self.match(TOKEN_SEPARATOR, ")")
                else:
                    self.error("Expected ')' after function arguments
        
        # Check for integers
        elif self.current_token and self.current_token.token_type == TOKEN_INTEGER:
            self.match(TOKEN_INTEGER)
        
        # Check for reals
        elif self.current_token and self.current_token.token_type == TOKEN_REAL:
            self.match(TOKEN_REAL)
        
        # Check for parenthesized expressions
        elif self.current_token and self.current_token.lexeme == "(":
            self.match(TOKEN_SEPARATOR, "(")
            self.expression()
            
            if self.current_token and self.current_token.lexeme == ")":
                self.match(TOKEN_SEPARATOR, ")")
            else:
                self.error("Expected ')' after expression")

        # Check for boolean literals
        elif self.current_token and self.current_token.lexeme in ["true", "false"]:
            self.match(TOKEN_KEYWORD)

        # Syntax error if none of the above
        else:
            self.error("Expected identifier, integer, real, or boolean literal")

        self.print_production("<Primary> -> <Identifier> | <Integer> | <Identifier> ( <IDs>) | ( <Expression> ) | <Real> | true | false")

    # R29 is here for requirements, but not really used
    def empty(self):
            """
            R29. <Empty> ::= <Epsilon>
            """
            self.print_production("<Empty> -> <Epsilon>")
            # Empty production, do nothing
