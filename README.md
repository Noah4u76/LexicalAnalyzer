# Lexical Analyzer, Syntax Analyzer, and Code Generator for Rat25S Language

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
- **Prints** tokens, lexemes, and production rules used in producing that token
- **Maintains Symbol Table** for variables and functions
- **Generates Assembly Code** for the Rat25S program

## Setup
### **1. Clone the repository**
```sh
 git clone https://github.com/your-repo/lexical-analyzer.git
 cd lexical-analyzer
```

### **2. Run the Analyzer**
To run the syntax analyzer and code generator on a test case:
```sh
python main.py
```

### **3. Test Files**
Test cases are included in:
- `test_syntax1.txt`
- `test_syntax2.txt`
- `test_syntax3.txt`

### **4. Output Files**
- **Syntax Analysis Output**:
  - `output_syntax1.txt`
  - `output_syntax2.txt`
  - `output_syntax3.txt`
- **Assembly Code Output**:
  - `output_syntax1_code_generator.txt`
  - `output_syntax2_code_generator.txt`
  - `output_syntax3_code_generator.txt`

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

### **Expected Output**
#### **Syntax Analysis (`output_syntax1.txt`)**
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

#### **Assembly Code (`output_syntax1_code_generator.txt, output_syntax2_code_generator.txt, output_syntax3_code_generator.txt`)**
```sh
Assembly Code Listing
====================================
1 PUSHI     0
2 POPM      10002
3 PUSHI     1
4 POPM      10000
5 SIN
6 POPM      10001
7 LABEL
8 PUSHM     10000
9 PUSHM     10001
10 LES
11 JMP0 21
12 PUSHM     10002
13 PUSHM     10000
14 A
15 POPM      10002
16 PUSHM     10000
17 PUSHI     1
18 A
19 POPM      10000
20 JMP 7
21 PUSHM     10002
22 PUSHM     10001
23 A
24 SOUT

Symbol Table
Identifier	MemoryLocation	Type
----------------------------------------
i		10000		integer
max		10001		integer
sum		10002		integer

```

## Error Handling
The system handles various types of errors:
- **Syntax Errors**: Invalid program structure
- **Semantic Errors**: Type mismatches, undefined variables
- **Code Generation Errors**: Invalid operations or memory access

## Contributors
- **Noah Sanderson**
- **Ryann Stock**
- **Bethany Garces**

## License
This project is licensed under the **MIT License**.
