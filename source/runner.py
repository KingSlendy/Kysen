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

        print(type(interpreter.result[0]))
        if len(interpreter.result) == 1 and interpreter.result[0].value != None:
            return interpreter.result[0]

        return None