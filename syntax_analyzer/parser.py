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
    def __init__(self, lexer, output_file=None, symbol_table=None, assembly_gen=None, debug=None):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.output_file = None
        self.debug = True
        self.symbol_table = symbol_table
        self.assembly_gen = assembly_gen
        
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
            self.output_file.write(f"{output_str}\n")
                
        print(output_str)
            
    def print_token(self):
        """
        Prints the current token and lexemme
        """
        
        if self.current_token:
            output_str = f"Token: {self.current_token.token_type}, Lexeme: {self.current_token.lexeme}"
            
            if self.output_file:
                self.output_file.write(f"{output_str}\n")
            
            print(output_str)
    
    def match(self, token_type=None, lexeme=None):
        """
        Matches the current token with the expected token type and lexeme.
        """
        
        if self.current_token is None:
            self.error("Unexpected end of input")
            
        if self.debug:
            self.print_token()
        
        if token_type and self.current_token.token_type != token_type:
            self.error(f"Expected token type {token_type}, but got {self.current_token.token_type}")
            
        if lexeme and self.current_token.lexeme != lexeme:
            self.error(f"Expected lexeme {lexeme}, but got {self.current_token.lexeme}")
            
        current_token = self.current_token
        self.current_token = self.lexer.get_next_token()
        return current_token
        
    def parse(self):
        """
        Starts the parsing process from the top-level rule <Rat25S>.
        """
        
        try:
            self.rat25s()
            print("Parsing completed successfully!")
            if self.output_file:
                self.output_file.write("Parsing completed successfully!\n")
        except Exception as e:
            print(f"Parsing failed: {e}")
            if self.output_file:
                self.output_file.write(f"Parsing failed: {e}\n")
        
    def rat25s(self):
        """
        R1. <Rat25S> ::= $$ <Opt Function Definitions> $$ <Opt Declaration List> $$ <Statement List> $$
        For simplified Rat25S, we'll ignore function definitions.
        Modified to: <Rat25S> ::= $$ $$ <Opt Declaration List> $$ <Statement List> $$
        """
        # Match the first $$
        if self.current_token and self.current_token.lexeme == "$$":
            self.match(lexeme="$$")
        else:
            self.error("Expected '$$' at the beginning of the program")
        
        # For simplified Rat25S, we skip function definitions
        # Just match the second $$
        if self.current_token and self.current_token.lexeme == "$$":
            self.match(lexeme="$$")
        else:
            self.error("Expected '$$' after beginning of program")
        
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

        self.print_production("<Rat25S> -> $$ $$ <Opt Declaration List> $$ <Statement List> $$")
        
    def opt_declaration_list(self):
        """
        R5. <Opt Declaration List> ::= <Declaration List> | <Empty>
        """
        if self.current_token and self.current_token.lexeme in ["integer", "boolean"]:
            self.declaration_list()
        # else: Empty production, do nothing
        
        self.print_production("<Opt Declaration List> -> <Declaration List> | <Empty>")
        
    def declaration_list(self):
        """
        R6. <Declaration List> ::= <Declaration> ; | <Declaration> ; <Declaration List>
        """
        self.declaration()
        
        if self.current_token and self.current_token.lexeme == ";":
            self.match(lexeme=";")
        else:
            self.error("Expected ';' after declaration")
        
        if self.current_token and self.current_token.lexeme in ["integer", "boolean"]:
            self.declaration_list()
            
        self.print_production("<Declaration List> -> <Declaration> ; | <Declaration> ; <Declaration List>")
        
    def declaration(self):
        """
        R7. <Declaration> ::= <Qualifier> <IDs>
        Modified for simplified Rat25S: Only allow integer and boolean, no real
        """
        # Get the type from qualifier
        type_name = self.qualifier()
        
        # Parse IDs and add them to symbol table
        self.ids(type_name)
        
        self.print_production("<Declaration> -> <Qualifier> <IDs>")
        
    def qualifier(self):
        """
        R8. <Qualifier> ::= integer | boolean
        Modified for simplified Rat25S: No real type
        """
        if self.current_token and self.current_token.lexeme == "integer":
            self.match(lexeme="integer")
            qualifier_type = "integer"
        elif self.current_token and self.current_token.lexeme == "boolean":
            self.match(lexeme="boolean")
            qualifier_type = "boolean"
        else:
            self.error("Expected 'integer' or 'boolean'")
        
        self.print_production("<Qualifier> -> integer | boolean")
        return qualifier_type
        
    def ids(self, type_name):
        """
        R10. <IDs> ::= <Identifier> | <Identifier>, <IDs>
        Now also adds identifiers to the symbol table.
        """
        if self.current_token and self.current_token.token_type == TOKEN_IDENTIFIER:
            # Get the identifier lexeme
            id_token = self.match(TOKEN_IDENTIFIER)
            
            # Add to symbol table
            if self.symbol_table:
                try:
                    self.symbol_table.insert(id_token.lexeme, type_name)
                except Exception as e:
                    self.error(str(e))
        else:
            self.error("Expected identifier")
        
        if self.current_token and self.current_token.lexeme == ",":
            self.match(lexeme=",")
            self.ids(type_name)
            
        self.print_production("<IDs> -> <Identifier> | <Identifier>, <IDs>")
    
    def statement_list(self):
        """
        R11. <Statement List> ::= <Statement> | <Statement> <Statement List>
        """
        self.statement()
        
        if self.current_token and self.current_token.lexeme != "$$" and self.current_token.lexeme != "}":
            self.statement_list()
        
        self.print_production("<Statement List> -> <Statement> | <Statement> <Statement List>")
    
    def statement(self):
        """
        R12. <Statement> ::= <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>
        """
        if not self.current_token:
            self.error("Unexpected end of input in statement")
            
        if self.current_token.lexeme == "{":
            self.compound()
        elif self.current_token.token_type == TOKEN_IDENTIFIER:
            self.assign()
        elif self.current_token.lexeme == "if":
            self.if_statement()
        elif self.current_token.lexeme == "print":
            self.print_statement()
        elif self.current_token.lexeme == "scan":
            self.scan_statement()
        elif self.current_token.lexeme == "while":
            self.while_statement()
        else:
            self.error(f"Invalid statement starting with '{self.current_token.lexeme}'")
            
        self.print_production("<Statement> -> <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>")
    
    def compound(self):
        """
        R13. <Compound> ::= { <Statement List> }
        """
        if self.current_token and self.current_token.lexeme == "{":
            self.match(lexeme="{")
        else:
            self.error("Expected '{' to start compound statement")
            
        if self.current_token and self.current_token.lexeme != "}":
            self.statement_list()
            
        if self.current_token and self.current_token.lexeme == "}":
            self.match(lexeme="}")
        else:
            self.error("Expected '}' to end compound statement")
            
        self.print_production("<Compound> -> { <Statement List> }")
    
    def assign(self):
        """
        R14. <Assign> ::= <Identifier> = <Expression> ;
        Now also generates assembly code for the assignment.
        """
        if self.current_token and self.current_token.token_type == TOKEN_IDENTIFIER:
            # Get the identifier
            id_token = self.match(TOKEN_IDENTIFIER)
            identifier = id_token.lexeme
            
            # Check if identifier is in symbol table
            if self.symbol_table:
                try:
                    identifier_type = self.symbol_table.get_type(identifier)
                except Exception as e:
                    self.error(str(e))
        else:
            self.error("Expected identifier for assignment")
            
        if self.current_token and self.current_token.lexeme == "=":
            self.match(lexeme="=")
        else:
            self.error("Expected '=' in assignment")
            
        # Parse the expression, which will put the result on the stack
        expr_type = self.expression()
        
        # Type checking for assignment
        if self.symbol_table and not self.symbol_table.check_type_compatibility(identifier_type, expr_type):
            self.error(f"Type mismatch in assignment: Cannot assign {expr_type} to {identifier_type}")
        
        # Generate assembly code for the assignment
        if self.assembly_gen:
            self.assembly_gen.gen_assignment(identifier)
            
        if self.current_token and self.current_token.lexeme == ";":
            self.match(lexeme=";")
        else:
            self.error("Expected ';' after assignment")
            
        self.print_production("<Assign> -> <Identifier> = <Expression> ;")
    
    def if_statement(self):
        """
        R15. <If> ::= if ( <Condition> ) <Statement> endif | 
                   if ( <Condition> ) <Statement> else <Statement> endif
        Now also generates assembly code for the if statement.
        """
        if self.current_token and self.current_token.lexeme == "if":
            self.match(lexeme="if")
        else:
            self.error("Expected 'if'")
            
        if self.current_token and self.current_token.lexeme == "(":
            self.match(lexeme="(")
        else:
            self.error("Expected '(' after 'if'")
            
        # Parse the condition, which will put the result on the stack
        self.condition()
        
        # Generate assembly code for the if statement
        if_jmp_addr = None
        if self.assembly_gen:
            if_jmp_addr = self.assembly_gen.start_if_statement()
            
        if self.current_token and self.current_token.lexeme == ")":
            self.match(lexeme=")")
        else:
            self.error("Expected ')' after condition")
            
        # Parse the statement
        self.statement()
        
        # Check if there's an else part
        else_jmp_addr = if_jmp_addr
        if self.current_token and self.current_token.lexeme == "else":
            self.match(lexeme="else")
            
            # Generate assembly code for the else part
            if self.assembly_gen:
                else_jmp_addr = self.assembly_gen.else_statement(if_jmp_addr)
                
            # Parse the else statement
            self.statement()
        
        # Match the endif
        if self.current_token and self.current_token.lexeme == "endif":
            self.match(lexeme="endif")
        else:
            self.error("Expected 'endif'")
            
        # Generate assembly code for the end of the if statement
        if self.assembly_gen:
            self.assembly_gen.end_if_statement(else_jmp_addr)
            
        self.print_production("<If> -> if ( <Condition> ) <Statement> endif | if ( <Condition> ) <Statement> else <Statement> endif")

    def print_statement(self):
        """
        R17. <Print> ::= print ( <Expression> ) ;
        Now also generates assembly code for the print statement.
        """
        if self.current_token and self.current_token.lexeme == "print":
            self.match(lexeme="print")
        else:
            self.error("Expected 'print'")
            
        if self.current_token and self.current_token.lexeme == "(":
            self.match(lexeme="(")
        else:
            self.error("Expected '(' after 'print'")
            
        # Parse the expression, which will put the result on the stack
        self.expression()
        
        if self.current_token and self.current_token.lexeme == ")":
            self.match(lexeme=")")
        else:
            self.error("Expected ')' after expression")
            
        # Generate assembly code for the print statement
        if self.assembly_gen:
            self.assembly_gen.gen_stdout()
            
        if self.current_token and self.current_token.lexeme == ";":
            self.match(lexeme=";")
        else:
            self.error("Expected ';' after print statement")
            
        self.print_production("<Print> -> print ( <Expression> ) ;")
    
    def scan_statement(self):
        """
        R18. <Scan> ::= scan ( <IDs> ) ;
        Now also generates assembly code for the scan statement.
        """
        if self.current_token and self.current_token.lexeme == "scan":
            self.match(lexeme="scan")
        else:
            self.error("Expected 'scan'")
            
        if self.current_token and self.current_token.lexeme == "(":
            self.match(lexeme="(")
        else:
            self.error("Expected '(' after 'scan'")
            
        # Parse the IDs and generate scan instructions for each one
        self.scan_ids()
            
        if self.current_token and self.current_token.lexeme == ")":
            self.match(lexeme=")")
        else:
            self.error("Expected ')' after IDs")
            
        if self.current_token and self.current_token.lexeme == ";":
            self.match(lexeme=";")
        else:
            self.error("Expected ';' after scan statement")
            
        self.print_production("<Scan> -> scan ( <IDs> ) ;")
    
    def scan_ids(self):
        """
        Helper method for scan statement to handle multiple IDs.
        Similar to <IDs> rule but generates scan instructions for each ID.
        """
        if self.current_token and self.current_token.token_type == TOKEN_IDENTIFIER:
            # Get the identifier
            id_token = self.match(TOKEN_IDENTIFIER)
            identifier = id_token.lexeme
            
            # Check if identifier is in symbol table
            if self.symbol_table:
                try:
                    self.symbol_table.get_type(identifier)  # This will raise an error if not found
                    
                    # Generate assembly code for the scan
                    if self.assembly_gen:
                        self.assembly_gen.gen_scan(identifier)
                except Exception as e:
                    self.error(str(e))
        else:
            self.error("Expected identifier for scan")
        
        if self.current_token and self.current_token.lexeme == ",":
            self.match(lexeme=",")
            self.scan_ids()
    
    def while_statement(self):
        """
        R19. <While> ::= while ( <Condition> ) <Statement> endwhile
        Now also generates assembly code for the while loop.
        """
        if self.current_token and self.current_token.lexeme == "while":
            self.match(lexeme="while")
        else:
            self.error("Expected 'while'")
            
        # Generate label for the start of the while loop
        loop_start = None
        if self.assembly_gen:
            loop_start = self.assembly_gen.start_while_loop()
            
        if self.current_token and self.current_token.lexeme == "(":
            self.match(lexeme="(")
        else:
            self.error("Expected '(' after 'while'")
            
        # Parse the condition, which will put the result on the stack
        self.condition()
        
        # Generate conditional jump for the while condition
        condition_jmp = None
        if self.assembly_gen:
            condition_jmp = self.assembly_gen.while_condition()
            
        if self.current_token and self.current_token.lexeme == ")":
            self.match(lexeme=")")
        else:
            self.error("Expected ')' after condition")
            
        # Parse the statement
        self.statement()
        
        # Generate code to jump back to the condition
        if self.assembly_gen:
            self.assembly_gen.end_while_loop(loop_start, condition_jmp)
            
        if self.current_token and self.current_token.lexeme == "endwhile":
            self.match(lexeme="endwhile")
        else:
            self.error("Expected 'endwhile'")
            
        self.print_production("<While> -> while ( <Condition> ) <Statement> endwhile")
    
    def condition(self):
        """
        R20. <Condition> ::= <Expression> <Relop> <Expression>
        Now also generates assembly code for the condition.
        """
        # Parse the first expression
        expr1_type = self.expression()
        
        # Get the relational operator
        relop = self.relop()
        
        # Parse the second expression
        expr2_type = self.expression()
        
        # Type checking for the condition
        if self.symbol_table and not self.symbol_table.check_type_compatibility(expr1_type, expr2_type):
            self.error(f"Type mismatch in condition: Cannot compare {expr1_type} with {expr2_type}")
        
        # Generate assembly code for the condition
        if self.assembly_gen:
            self.assembly_gen.gen_relational(relop)
            
        self.print_production("<Condition> -> <Expression> <Relop> <Expression>")
    
    def relop(self):
        """
        R21. <Relop> ::= == | != | > | < | <= | >=
        Now returns the relational operator for code generation.
        """
        relop = None
        
        if self.current_token and self.current_token.lexeme == "==":
            self.match(lexeme="==")
            relop = "=="
        elif self.current_token and self.current_token.lexeme == "!=":
            self.match(lexeme="!=")
            relop = "!="
        elif self.current_token and self.current_token.lexeme == ">":
            self.match(lexeme=">")
            relop = ">"
        elif self.current_token and self.current_token.lexeme == "<":
            self.match(lexeme="<")
            relop = "<"
        elif self.current_token and self.current_token.lexeme == "<=":
            self.match(lexeme="<=")
            relop = "<="
        elif self.current_token and self.current_token.lexeme == ">=":
            self.match(lexeme=">=")
            relop = ">="
        else:
            self.error("Expected relational operator")
            
        self.print_production("<Relop> -> == | != | > | < | <= | >=")
        return relop
    
    def expression(self):
        """
        R22. <Expression> ::= <Term> | <Term> + <Expression> | <Term> - <Expression>
        Now also generates assembly code for the expression and returns the type.
        """
        # Parse the first term
        term_type = self.term()
        
        # Check if there's an operator
        if self.current_token and self.current_token.lexeme in ["+", "-"]:
            operator = self.current_token.lexeme
            self.match(lexeme=operator)
            
            # Parse the rest of the expression
            expr_type = self.expression()
            
            # Type checking for the expression
            if self.symbol_table:
                # Check if both operands are same type and not boolean for arithmetic operations
                if not self.symbol_table.check_type_compatibility(term_type, expr_type, operator):
                    self.error(f"Type mismatch in expression: Cannot perform {operator} on {term_type} and {expr_type}")
            
            # Generate assembly code for the expression
            if self.assembly_gen:
                self.assembly_gen.gen_arithmetic(operator)
                
            return term_type  # Return the type of the expression
            
        return term_type  # Return the type of the term if no operator
    
    def term(self):
        """
        R23. <Term> ::= <Factor> | <Factor> * <Term> | <Factor> / <Term>
        Now also generates assembly code for the term and returns the type.
        """
        # Parse the first factor
        factor_type = self.factor()
        
        # Check if there's an operator
        if self.current_token and self.current_token.lexeme in ["*", "/"]:
            operator = self.current_token.lexeme
            self.match(lexeme=operator)
            
            # Parse the rest of the term
            term_type = self.term()
            
            # Type checking for the term
            if self.symbol_table:
                # Check if both operands are same type and not boolean for arithmetic operations
                if not self.symbol_table.check_type_compatibility(factor_type, term_type, operator):
                    self.error(f"Type mismatch in term: Cannot perform {operator} on {factor_type} and {term_type}")
            
            # Generate assembly code for the term
            if self.assembly_gen:
                self.assembly_gen.gen_arithmetic(operator)
                
            return factor_type  # Return the type of the term
            
        return factor_type  # Return the type of the factor if no operator
    
    def factor(self):
        """
        R24. <Factor> ::= - <Primary> | <Primary>
        Now also generates assembly code for the factor and returns the type.
        """
        # Check if there's a unary minus
        if self.current_token and self.current_token.lexeme == "-":
            self.match(lexeme="-")
            
            # Parse the primary
            primary_type = self.primary()
            
            # Type checking for the unary minus
            if self.symbol_table and primary_type == "boolean":
                self.error("Cannot apply unary minus to boolean value")
            
            # Generate assembly code for the unary minus (negate by multiplying by -1)
            if self.assembly_gen:
                self.assembly_gen.gen_pushi(-1)
                self.assembly_gen.gen_mul()
                
            return primary_type
            
        # Parse the primary
        return self.primary()
    
    def primary(self):
        """
        R25. <Primary> ::= <Identifier> | <Integer> | <Identifier> ( <IDs> ) | ( <Expression> ) | <Real> | true | false
        Modified for simplified Rat25S: No function calls
        Now also generates assembly code for the primary and returns the type.
        """
        if not self.current_token:
            self.error("Unexpected end of input in primary")
            
        # Identifier
        if self.current_token.token_type == TOKEN_IDENTIFIER:
            # Get the identifier
            id_token = self.match(TOKEN_IDENTIFIER)
            identifier = id_token.lexeme
            
            # Check if identifier is in symbol table
            if self.symbol_table:
                try:
                    identifier_type = self.symbol_table.get_type(identifier)
                    
                    # Generate assembly code for the identifier
                    if self.assembly_gen:
                        address = self.symbol_table.get_address(identifier)
                        self.assembly_gen.gen_pushm(address)
                        
                    return identifier_type
                except Exception as e:
                    self.error(str(e))
            
            return "unknown"  # Default type if no symbol table
            
        # Integer
        elif self.current_token.token_type == TOKEN_INTEGER:
            value = self.current_token.lexeme
            self.match(TOKEN_INTEGER)
            
            # Generate assembly code for the integer
            if self.assembly_gen:
                self.assembly_gen.gen_pushi(value)
                
            return "integer"
            
        # Expression in parentheses
        elif self.current_token.lexeme == "(":
            self.match(lexeme="(")
            expr_type = self.expression()
            
            if self.current_token and self.current_token.lexeme == ")":
                self.match(lexeme=")")
            else:
                self.error("Expected ')' after expression")
                
            return expr_type
            
        # Boolean literals
        elif self.current_token.lexeme == "true":
            self.match(lexeme="true")
            
            # Generate assembly code for true (1)
            if self.assembly_gen:
                self.assembly_gen.gen_pushi(1)
                
            return "boolean"
            
        elif self.current_token.lexeme == "false":
            self.match(lexeme="false")
            
            # Generate assembly code for false (0)
            if self.assembly_gen:
                self.assembly_gen.gen_pushi(0)
                
            return "boolean"
            
        else:
            self.error(f"Invalid primary: {self.current_token.lexeme}")
            
        self.print_production("<Primary> -> <Identifier> | <Integer> | ( <Expression> ) | true | false")
    
    def empty(self):
        """
        R26. <Empty> ::= ε
        """
        self.print_production("<Empty> -> ε")
