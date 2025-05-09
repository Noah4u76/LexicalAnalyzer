class SymbolTable:
    def __init__(self):
        self.table = {}
        self.memory_address = 10000  # Starting address 

    def lookup(self, lexeme):
        """
        Looks up a variable in the symbol table.
        """
        return self.table.get(lexeme)
    
    def insert(self, lexeme, type_name):
        """
        Inserts a variable into the symbol table.
        """
        if lexeme not in self.table:
            # Only allow 'integer' and 'boolean' types for the simplified Rat25S
            if type_name != 'integer' and type_name != 'boolean':
                raise Exception(f"Type '{type_name}' is not supported in simplified Rat25S. Only 'integer' and 'boolean' are allowed.")
                
            self.table[lexeme] = {
                "type": type_name,
                "address": self.memory_address
            }
            self.memory_address += 1
            return True
        else:
            raise Exception(f"Semantic Error: Variable '{lexeme}' already declared.")
    
    def print_table(self):
        """
        Prints the symbol table.
        """
        print("\nSymbol Table")
        print("Identifier\tMemoryLocation\tType")
        print("-" * 40)
        for lexeme, info in self.table.items():
            print(f"{lexeme}\t\t{info['address']}\t\t{info['type']}")

    def get_address(self, lexeme):
        """
        Gets the memory address of a variable in the symbol table.
        """
        if lexeme in self.table:
            return self.table[lexeme]["address"]
        else:
            raise Exception(f"Semantic Error: Variable '{lexeme}' used without declaration.")
    
    def get_type(self, lexeme):
        """
        Gets the type of a variable in the symbol table.
        """
        if lexeme in self.table:
            return self.table[lexeme]["type"]
        else:
            raise Exception(f"Semantic Error: Variable '{lexeme}' used without declaration.")
    
    def check_type_compatibility(self, type1, type2, operation=None):
        """
        Checks if the types are compatible for operations.
        - No arithmetic operations allowed for booleans
        - Types must match for arithmetic operations (no conversions)
        """
        # For simplified Rat25S, we don't allow arithmetic operations on booleans
        if operation in ['+', '-', '*', '/'] and (type1 == 'boolean' or type2 == 'boolean'):
            return False
            
        # Types must match exactly (no conversions)
        return type1 == type2
