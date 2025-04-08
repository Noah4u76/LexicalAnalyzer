from .lexical_analyzer import Lexer

class FileHandler: 
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def read_file(self):
        with open(self.input_file, 'r') as file:
            return file.read()
        
    def write_output_file(self, tokens):
        with open(self.output_file, 'w') as file:
            for token in tokens:
                file.write(f"{token}\n")

    def process(self):
        input_code = self.read_file()
        lexer = Lexer(input_code)
        tokens = lexer.tokenize()
        self.write_output_file(tokens)
        
        
def analyze_file(input_file, output_file):
    file_handler = FileHandler(input_file, output_file)
    file_handler.process()        
