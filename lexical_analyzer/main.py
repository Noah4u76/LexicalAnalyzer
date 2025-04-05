from file_handler import analyze_file

def create_test_files():
    """
    Create test files for the lexical analyzer
    """
    # Test Case 1
    test_case1 = """while (fahr <= upper)
    a = 23.00;
endwhile [* this is a sample *]"""

    # Test Case 2
    test_case2 = """function int factorial(int n)
{
    if (n == 0)
        return 1;
    else
        return n * factorial(n-1);
    endif
}"""

    # Test Case 3
    test_case3 = """[* Test case with various tokens *]
integer count = 0;
real average = 0.0;
while (count < 10)
{
    get(value);
    average = average + value;
    count = count + 1;
}
average = average / 10.0;
put(average);"""

    # Write test cases to files
    with open("test_case1.txt", "w") as f:
        f.write(test_case1)
    
    with open("test_case2.txt", "w") as f:
        f.write(test_case2)
    
    with open("test_case3.txt", "w") as f:
        f.write(test_case3)
    
    print("Test files created successfully.")

def run_tests():
    """
    Run the lexical analyzer on test files
    """
    print("Running Test Case 1...")
    analyze_file("test_case1.txt", "output1.txt")
    
    print("\nRunning Test Case 2...")
    analyze_file("test_case2.txt", "output2.txt")
    
    print("\nRunning Test Case 3...")
    analyze_file("test_case3.txt", "output3.txt")

def main():
    """
    Main function
    """
    print("Lexical Analyzer for Rat25S Language")
    print("------------------------------------")
    
    create_test_files()
    
    run_tests()
    
    print("\nAll tests completed.")

if __name__ == "__main__":
    main()