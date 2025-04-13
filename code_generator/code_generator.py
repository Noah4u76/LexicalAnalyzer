class AssemblyGenerator:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.instructions = [""] * 1000 # Array to hold assembly instructions
        self.current_instruction = 1   # Current instruction index
        self.jump_stack = []    # Stack to keep track of jump instructions
        self.temp_label_count = 0   # Counter for temporary labels

    def generate_instruction(self, instruction):
        """
        Generates an assembly instruction and adds it to the instructions list.
        """
        self.instructions[self.current_instruction] = instruction
        self.current_instruction += 1
        return self.current_instruction - 1
    
    def update_instruction(self, index, instruction):
        """
        Updates an existing assembly instruction at the given index.
        """
        self.instructions[index] = instruction

    def get_next_instruction(self): 
        """
        Returns the next instruction index.
        """
        return self.current_instruction + 1
    
    def print_assembly(self):
        """
        Prints the generated assembly code.
        """
        print("Generated Assembly Code:")
        print("=======================================")
        for i in range(1, self.current_instruction):
            print(f"{i}: {self.instructions[i]}")

    #=========================
    # ASSEMBLY INSTRUCTIONS
    #=========================
    
    def gen_pushi(self, value):
        """
        I1. Generates a push immediate instruction.
        """
        return self.generate_instruction(f"PUSHI     {value}")
    
    def gen_pushm(self, address):
        """
        I2. Generates a push memory instruction.
        """
        return self.generate_instruction(f"PUSHM     {address}")
    
    def gen_popm(self, address):
        """
        I3. Generates a pop memory instruction.
        """
        return self.generate_instruction(f"POPM      {address}")
    
    def gen_sout(self):
        """
        I4. Generates a standard out instruction.
        """
        return self.generate_instruction("SOUT")
    
    def gen_sin(self):
        """
        I5. Generates a standard in instruction.
        """
        return self.generate_instruction("SIN")
        
    def gen_add(self):
        """
        I6. Generates an add instruction.
        """
        return self.generate_instruction("A")
    
    def gen_sub(self):
        """
        I7. Generates a subtract instruction.
        """
        return self.generate_instruction("S")
    
    def gen_mul(self):
        """
        I8. Generates a multiply instruction.
        """
        return self.generate_instruction("M")
    
    def gen_div(self):
        """
        I9. Generates a divide instruction.
        """
        return self.generate_instruction("D")
    
    def gen_greater(self):
        """
        I10. Generates a greater than instruction.
        """
        return self.generate_instruction("GRT")
    
    def gen_less(self):
        """
        I11. Generates a less than instruction.
        """
        return self.generate_instruction("LES")

    def gen_equal(self):
        """
        I12. Generates an equal to instruction.
        """
        return self.generate_instruction("EQU")
    
    def gen_not_equal(self):
        """
        I13. Generates a not equal to instruction.
        """
        return self.generate_instruction("NEQ")
    
    def gen_greater_equal(self):
        """
        I14. Generates a greater than or equal to instruction.
        """
        return self.generate_instruction("GEQ")
    
    def gen_less_equal(self):
        """
        I15. Generates a less than or equal to instruction.
        """
        return self.generate_instruction("LEQ")
    
    def gen_jump0(self, address = None):
        """
        I16. Generates a jump if zero instruction.
        """
        if address is None:
            jmp0_addr = self.gen_instruction("JMP0      0")
            return jmp0_addr
        else:
            raise Exception("Semantic Error: Address should not be provided for JMP0 instruction.")
    
    def gen_jump(self, address):
        """
        I17. Generates a JMP instruction.
        """
        return self.generate_instruction(f"JMP      {address}")
    
    def gen_label(self, label):
        """
        I18. Generates a label instruction.
        """
        return self.generate_instruction(f"L{label}:")
    
    