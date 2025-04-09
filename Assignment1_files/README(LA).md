# Lexical Analyzer for Rat25S Language

## Features
- **Tokenizes valid Rat25S syntax**
- **Ignores comments** (delimited by `[ * ... * ]`)
- **Recognizes**:
  - **Keywords** (`while`, `integer`, `real`, etc.)
  - **Identifiers** (`variable names`)
  - **Operators** (`=`, `+`, `-`, `<`, `>`, etc.)
  - **Separators** (`() { } ; ,` etc.)
  - **Integers** (`123`, `0`, etc.)
  - **Real Numbers** (`10.5`, `0.0`, etc.)
- **Handles syntax errors** by detecting invalid characters

## Setup
### **1. Clone the repository**
```sh
 git clone https://github.com/your-repo/lexical-analyzer.git
 cd lexical-analyzer
```

### **2. Run the Analyzer**
To run the lexical analyzer on a test case:
```sh
python main.py
```

### **3. Test Files**
Test cases are included in:
- `test_case1.txt`
- `test_case2.txt`
- `test_case3.txt`

### **4. Output Files**
Tokens are saved in:
- `output1.txt`
- `output2.txt`
- `output3.txt`

## Example Input
### **Input File (`test_case1.txt`)**
```
while (count < 10)
{
    count = count + 1;
    put(count);
}
```

### **Expected Output (`output1.txt`)**
```
Token(KEYWORD, while)
Token(SEPARATOR, ()
Token(IDENTIFIER, count)
Token(OPERATOR, <)
Token(INTEGER, 10)
Token(SEPARATOR, ))
Token(SEPARATOR, {)
Token(IDENTIFIER, count)
Token(OPERATOR, =)
Token(IDENTIFIER, count)
Token(OPERATOR, +)
Token(INTEGER, 1)
Token(SEPARATOR, ;)
Token(IDENTIFIER, put)
Token(SEPARATOR, ()
Token(IDENTIFIER, count)
Token(SEPARATOR, ))
Token(SEPARATOR, ;)
Token(SEPARATOR, })
```

## Error Handling
If an invalid character is encountered, the lexer will **throw an error**:
```sh
SyntaxError: Invalid Character '@' at line 4, column 5
```

## Contributors
- **Noah Sanderson**
- **Ryann Stock**
- **Bethany Garces**

## License
This project is licensed under the **MIT License**.
