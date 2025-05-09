from lexical_analyzer.lexical_analyzer import Lexer
from lexical_analyzer.file_handler import FileHandler
from syntax_analyzer.parser import Parser
from code_generator.symbol_table import SymbolTable
from code_generator.code_generator import AssemblyGenerator

def create_test_files():
    
    test_case1 = """ [* Testing sample Rat25S Program *]
    $$
        function convertx (fahr integer)
        {
            return 5 * (fahr -32) / 9;
        }
    $$
        integer low, high, step; [* declarations *]
    $$
        scan (low, high, step);
        while (low <= high )
        {   print (low);
            print (convertx (low));
            low = low + step;
        }
        endwhile
    $$
    """    
    test_case2 = """[* Testing Basic Expressions and Assignments *]
    $$
    $$
        integer a;
    $$
        a = 5;
        print(a);
    $$"""
        
    test_case3 = """[* Testing if-else and while statements *]
    $$
    $$
        integer value, counter;
    $$
        [* Conditional execution with if-else *]
        scan(value);
        
        if (value > 0) {
            print(value);
        }
        else {
            print(0);
        }
        endif
        
        [* Nested if statements *]
        if (value > 10) {
            if (value < 20) {
                print(value);
            }
            else {
                print(20);
            }
            endif
        }
        endif
        
        [* While loop *]
        counter = 1;
        while (counter <= 5) {
            print(counter);
            counter = counter + 1;
        }
        endwhile
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
    Run the syntax analyzer on the input file and output the results
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
    
    print(f"Results written to {output_file}")
    
def run_tests():
    """
    Run the syntax analyzer on the test files
    """
    print("Running syntax analysis on test files...")
    
    run_syntax_analysis("test_syntax1.txt", "output_syntax1.txt")
    run_syntax_analysis("test_syntax2.txt", "output_syntax2.txt")
    run_syntax_analysis("test_syntax3.txt", "output_syntax3.txt")
    
    print("All tests completed.")
    
def main():
    """
    Main function to run the syntax analyzer
    """
    print("Syntax Analyzer for Rat25S Language")
    print("----------------------------------")
    
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
