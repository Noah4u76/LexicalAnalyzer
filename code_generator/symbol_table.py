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
            self.table[lexeme] = {
                "type": type_name,
                "address": self.memory_address
            }
            self.memory_address += 1
        else:
            raise Exception(f"Variable '{lexeme}' already declared.")
        return True
    
    def print_table(self):
        """
        Prints the symbol table.
        """
        print("Symbol Table:")
        print("-" * 20)
        print("Lexeme\tType\tAddress")
        print("-" * 20)
        for lexeme, info in self.table.items():
            print(f"{lexeme}: {info['type']} at address {info['address']}")

    def get_address(self, lexeme):
        """
        Gets the memory address of a variable in the symbol table.
        """
        return self.table[lexeme]["address"] if lexeme in self.table else None
    
    def get_type(self, lexeme):
        """
        Gets the type of a variable in the symbol table.
        """
        return self.table[lexeme]["type"] if lexeme in self.table else None
    
    def check_type_compatibility(self, type1, type2):
        """
        Checks if the type of two variables are compatible for arithmetic operations.
        """
        if type1 == type2 and type1 != 'boolean':
            return True
        return False
