from lexical_analyzer.lexical_analyzer import Lexer
from lexical_analyzer.file_handler import FileHandler
from syntax_analyzer.parser import Parser
from code_generator.symbol_table import SymbolTable
from code_generator.code_generator import AssemblyGenerator

def create_test_files():
    
    # Sample code from assignment 3
    test_case1 = """[* this is comment for this sample code for assignment 3 *]
$$
[* NO function definitions *]
$$
integer i, max, sum; [* declarations *]
$$
sum = 0;
i = 1;
scan (max);
while (i < max) {
sum = sum + i;
i = i + 1;
} endwhile
print (sum + max);
$$
    """    
    
    test_case2 = """[* Testing Basic Expressions and Assignments *]
$$
$$
integer a, b;
boolean flag;
$$
a = 5;
b = 10;
flag = true;
if (a < b) {
  print(a);
} else {
  print(b);
}
endif
flag = false;
print(flag);
$$"""
        
    test_case3 = """[* Testing if-else and while statements *]
$$
$$
integer value, counter, result;
boolean done;
$$
[* Conditional execution with if-else *]
scan(value);
done = false;

if (value > 0) {
    result = value * 2;
    print(result);
}
else {
    result = 0;
    print(result);
}
endif

[* While loop *]
counter = 1;
while (counter <= value) {
    print(counter);
    counter = counter + 1;
    if (counter == 3) {
        done = true;
    }
    endif
}
endwhile

print(done);
$$"""

    with open("test_syntax1.txt", "w") as f:
        f.write(test_case1)
    
    with open("test_syntax2.txt", "w") as f:
        f.write(test_case2)
    
    with open("test_syntax3.txt", "w") as f:
        f.write(test_case3)
    
    print("Test files created successfully.")
    
def run_syntax_analysis(input_file, output_file):
    """
    Run the syntax analyzer and code generator on the input file and output the results
    """
    # Read the input file
    with open(input_file, 'r') as f:
        input_text = f.read()
    
    # Create a lexer for the input
    lexer = Lexer(input_text)
    
    # Create symbol table and assembly generator
    symbol_table = SymbolTable()
    assembly_gen = AssemblyGenerator(symbol_table)
    
    # Create a parser and parse the input
    parser = Parser(lexer, output_file, symbol_table, assembly_gen)
    
    print(f"Parsing {input_file}...")
    parser.parse()
    
    # Print symbol table and assembly code
    symbol_table.print_table()
    assembly_gen.print_assembly()
    
    # Write to the output file for syntax analysis
    with open(output_file, 'a') as f:
        f.write("\nSymbol Table\n")
        f.write("Identifier\tMemoryLocation\tType\n")
        f.write("-" * 40 + "\n")
        for lexeme, info in symbol_table.table.items():
            f.write(f"{lexeme}\t\t{info['address']}\t\t{info['type']}\n")
        
        f.write("\nAssembly Code Listing\n")
        f.write("====================================\n")
        for i in range(1, assembly_gen.current_instruction):
            f.write(f"{i} {assembly_gen.instructions[i]}\n")
    
    # Create a separate file for the assembly code output
    assembly_output_file = output_file.replace('.txt', '_code_generator.txt')
    with open(assembly_output_file, 'w') as f:
        f.write("Assembly Code Listing\n")
        f.write("====================================\n")
        for i in range(1, assembly_gen.current_instruction):
            f.write(f"{i} {assembly_gen.instructions[i]}\n")
        
        f.write("\nSymbol Table\n")
        f.write("Identifier\tMemoryLocation\tType\n")
        f.write("-" * 40 + "\n")
        for lexeme, info in symbol_table.table.items():
            f.write(f"{lexeme}\t\t{info['address']}\t\t{info['type']}\n")
    
    print(f"Results written to {output_file}")
    print(f"Assembly code written to {assembly_output_file}")
    
def run_tests():
    """
    Run the syntax analyzer on the test files
    """
    print("Running syntax analysis and code generation on test files...")
    
    run_syntax_analysis("test_syntax1.txt", "output_syntax1.txt")
    run_syntax_analysis("test_syntax2.txt", "output_syntax2.txt")
    run_syntax_analysis("test_syntax3.txt", "output_syntax3.txt")
    
    print("All tests completed.")
    
def main():
    """
    Main function to run the syntax analyzer and code generator
    """
    print("Syntax Analyzer and Code Generator for Simplified Rat25S Language")
    print("------------------------------------------------------------------")
    
    # Create test files
    create_test_files()
    
    # Run tests
    run_tests()
    
    # Ask the user if they want to analyze a specific file
    user_choice = input("\nDo you want to analyze a specific file? (y/n): ")
    
    if user_choice.lower() == 'y':
        input_file = input("Enter the input file path: ")
        output_file = input("Enter the output file path: ")
        run_syntax_analysis(input_file, output_file)

if __name__ == "__main__":
    main()
