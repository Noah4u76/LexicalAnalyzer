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
        return self.current_instruction
    
    def print_assembly(self):
        """
        Prints the generated assembly code.
        """
        print("Generated Assembly Code:")
        print("=======================================")
        for i in range(1, self.current_instruction):
            print(f"{i} {self.instructions[i]}")

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
    
    def gen_stdout(self):
        """
        I4. Generates a standard out instruction.
        """
        return self.generate_instruction("SOUT")
    
    def gen_stdin(self):
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
    
    def gen_jump_false(self, address=None):
        """
        I16. Generates a jump if zero instruction.
        JMP0 {IL} - Pop the stack and if the value is 0 then jmp to {IL}
        """
        if address is None:
            # If no address is provided, use a placeholder that will be backpatched later
            jmp_addr = self.generate_instruction("JMP0 0")
            return jmp_addr
        else:
            return self.generate_instruction(f"JMP0 {address}")
    
    def gen_jump(self, address=None):
        """
        I17. Generates a JMP instruction.
        JMP {IL} - Unconditionally jmp to {IL}
        """
        if address is None:
            # If no address is provided, use a placeholder that will be backpatched later
            jmp_addr = self.generate_instruction("JMP 0")
            return jmp_addr
        else:
            return self.generate_instruction(f"JMP {address}")
    
    def gen_label(self):
        """
        I18. Generates a label instruction.
        LABEL - Empty Instruction; Provides the instruction location to jmp to.
        """
        label_addr = self.generate_instruction("LABEL")
        return label_addr
    
    # Additional methods for code generation patterns

    def backpatch(self, jump_addr, target_addr):
        """
        Backpatches a jump instruction with the target address.
        """
        instruction = self.instructions[jump_addr]
        if instruction.startswith("JMP0"):
            self.instructions[jump_addr] = f"JMP0 {target_addr}"
        elif instruction.startswith("JMP"):
            self.instructions[jump_addr] = f"JMP {target_addr}"
    
    def gen_assignment(self, identifier):
        """
        Generates code for an assignment statement.
        The value to be assigned should already be on the stack.
        """
        address = self.symbol_table.get_address(identifier)
        return self.gen_popm(address)
    
    def gen_arithmetic(self, operator):
        """
        Generates code for an arithmetic operation.
        The operands should already be on the stack.
        """
        if operator == '+':
            return self.gen_add()
        elif operator == '-':
            return self.gen_sub()
        elif operator == '*':
            return self.gen_mul()
        elif operator == '/':
            return self.gen_div()
    
    def gen_relational(self, operator):
        """
        Generates code for a relational operation.
        The operands should already be on the stack.
        """
        if operator == '>':
            return self.gen_greater()
        elif operator == '<':
            return self.gen_less()
        elif operator == '==':
            return self.gen_equal()
        elif operator == '!=':
            return self.gen_not_equal()
        elif operator == '>=':
            return self.gen_greater_equal()
        elif operator == '<=':
            return self.gen_less_equal()
    
    def gen_print(self):
        """
        Generates code for a print statement.
        The value to be printed should already be on the stack.
        """
        return self.gen_stdout()
    
    def gen_scan(self, identifier):
        """
        Generates code for a scan statement.
        """
        address = self.symbol_table.get_address(identifier)
        self.gen_stdin()
        return self.gen_popm(address)
    
    def start_while_loop(self):
        """
        Generates code for the start of a while loop.
        Returns the label address for the condition.
        """
        # Generate a label for the start of the loop
        self.generate_instruction("LABEL")
        return self.current_instruction - 1
    
    def while_condition(self):
        """
        Generates code for the while condition evaluation.
        The result of the condition should already be on the stack.
        Returns the jump address to be backpatched.
        """
        jmp_addr = self.gen_jump_false(0)
        return jmp_addr
    
    def end_while_loop(self, loop_start, condition_jmp):
        """
        Generates code for the end of a while loop.
        """
        # Jump back to the start of the loop
        self.gen_jump(loop_start)
        
        # Backpatch the condition jump to the current instruction
        self.backpatch(condition_jmp, self.current_instruction)
    
    def start_if_statement(self):
        """
        Generates code for the start of an if statement.
        The result of the condition should already be on the stack.
        Returns the jump address to be backpatched.
        """
        return self.gen_jump_false(0)
    
    def else_statement(self, if_jmp_addr):
        """
        Generates code for the else part of an if-else statement.
        Returns the jump address to be backpatched.
        """
        # First, add an unconditional jump to skip the else part
        else_jmp_addr = self.gen_jump(0)
        
        # Backpatch the if jump to the current instruction
        self.backpatch(if_jmp_addr, self.current_instruction)
        
        return else_jmp_addr
    
    def end_if_statement(self, jmp_addr):
        """
        Generates code for the end of an if statement.
        """
        # Backpatch the jump address
        self.backpatch(jmp_addr, self.current_instruction)
            