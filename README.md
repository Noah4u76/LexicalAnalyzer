# Lexical Analyzer and Syntax Analyzer for Rat25S Language

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
- **[4/6] Prints** tokens, lexemes, and production rules used in producing that token

## Setup
### **1. Clone the repository**
```sh
 git clone https://github.com/your-repo/lexical-analyzer.git
 cd lexical-analyzer
```

### **2. Run the Analyzer**
To run the syntax analyzer on a test case:
```sh
python main.py
```

### **3. Test Files**
Test cases are included in:
- `test_syntax1.txt`
- `test_syntax2.txt`
- `test_syntax3.txt`

### **4. Output Files**
Tokens are saved in:
- `output_syntax1.txt`
- `output_syntax2.txt`
- `output_syntax3.txt`

## Example Input
### **Input File (`test_syntax1.txt`)**
```sh
[* Testing sample Rat25S Program *]
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
  { print (low);
    print (convertx (low));
    low = low + step;
  }
  endwhile
$$

```

### **Expected Output (`output_syntax1.txt`)**
```sh
Syntax Analyzer for Rat25S Language
----------------------------------
Test files created successfully.
Running syntax analysis on test files...
Parsing test_syntax1.txt...
Token: SEPARATOR, Lexeme: $$
Token: KEYWORD, Lexeme: function
Token: IDENTIFIER, Lexeme: convertx
Token: SEPARATOR, Lexeme: (
Token: IDENTIFIER, Lexeme: fahr
        Production: <IDs> -> <Identifier> | <Identifier>, <IDs>
Token: KEYWORD, Lexeme: integer
        Production: <Qualifier> -> integer | boolean | real
        Production: <Parameter> -> <IDs> <Qualifier>
        Production: <Parameter List> -> <Parameter> | <Parameter> , <Parameter List>
        Production: <Opt Parameter List> -> <Parameter List> | <Empty>
Token: SEPARATOR, Lexeme: )
        Production: <Opt Declaration List> -> <Declaration List> | <Empty>
Token: SEPARATOR, Lexeme: {
Token: KEYWORD, Lexeme: return
Debug: Recognized integer '5'
...
```

## Error Handling
If an invalid character is encountered, the lexer will **throw an error**:
```sh
SyntaxError: Expected '$$' at the beginning of the program
```

## Contributors
- **Noah Sanderson**
- **Ryann Stock**
- **Bethany Garces**

## License
This project is licensed under the **MIT License**.
