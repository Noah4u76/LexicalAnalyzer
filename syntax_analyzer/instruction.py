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
    return instr_address

jmp_stack = []

def push_jmp_stack(addr):
    jmp_stack.append(addr)

def pop_jmp_stack():
    if jmp_stack:
        return jmp_stack.pop()
    else: 
        raise Exception("JMP stack underflow")
    
def back_patch(exit_addr):

    jump_instr_index = pop_jmp_stack()

    instr_table[jump_instr_index -1].operand = str(exit_addr)

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