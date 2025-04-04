from lexical_analyzer.lexical_analyzer import Lexer
from lexical_analyzer.file_handler import FileHandler
from syntax_analyzer.parser import Parser

def create_test_files():
    
    
    
    
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
    
    # Create a parser and parse the input
    parser = Parser(lexer, output_file)
    
    print(f"Parsing {input_file}...")
    parser.parse()
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