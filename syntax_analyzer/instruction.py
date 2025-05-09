# Gobal Instruction table and counter
instr_table = []
instr_address = 1

class Instruction:
    def __init__(self, address, op, operand):
        self.address = address
        self.op = op
        self.operand = operand

def generate_instruciton(op, operand):
    global instr_address, instr_table
    instr = Instruction(instr_address, op, operand)
    instr_table.append(instr)
    instr_address += 1

def get_current_isntr_address():
    #Returns next instruction address(labels/Backpatching)
    return instr_address

# For jump backpatching 
jmp_stack = []

def push_jmp_stack(addr):
    jmp_stack.append(addr)

def pop_jmp_stack():
    if jmp_stack:
        return jmp_stack.pop()
    else: 
        raise Exception("JMP stack underflow")
    
def back_patch(exit_addr):

    #Pop previously saved jump position and update its operand it exit_addr
    jump_instr_index = pop_jmp_stack() # Address wehre JMP) generated

    #Since our instr_table is indexed from 0 and addressses start at 1:
    instr_table[jump_instr_index -1].operand = str(exit_addr)

#A dummy symbol table for demonstration
symbol_table = { 
    "i": {"memory": 10000, "type": "integer"},
    "max": {"memory": 10001, "type": "integer"}, 
    "sum": {"memory": 10002, "type": "integer"}
}

def get_Address(identifier):
    if identifier in symbol_table:
        return str(symbol_table[identifier]["memory"])
    else:
        raise Exception("Undefined indentifier: " + identifier)