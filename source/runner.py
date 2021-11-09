from interpreter import Interpreter
from lexer import Lexer
from parser import Parser

class Runner:
    @staticmethod
    def execute(text):
        lexer = Lexer(text)
        #print(lexer.tokens)

        if len(lexer.tokens) == 1:
            return None

        parser = Parser(lexer.tokens)
        #print(parser.tree)
        interpreter = Interpreter(parser.tree)
        return interpreter.result