from interpreter import Interpreter
from lexer import Lexer
from parser import Parser
from runtime import Runtime

class Runner:
    @staticmethod
    def execute(filename, text):
        if text == "":
            return None

        runtime = Runtime(filename, text)
        lexer = Lexer(text, runtime)
        #print(lexer.tokens)

        if len(lexer.tokens) == 1:
            return None

        parser = Parser(lexer.tokens, runtime)
        #print(parser.tree)
        interpreter = Interpreter(parser.tree, runtime)
        return interpreter.result