from interpreter import Interpreter
from lexer import Lexer
from parser import Parser
from reporter import Reporter

reporter = Reporter()

class Runner:
    @staticmethod
    def execute(filename, text):
        global runtime

        if text == "":
            return None

        reporter.update(filename, text)
        lexer = Lexer(text)
        #print(lexer.tokens)

        if len(lexer.tokens) == 1:
            return None

        parser = Parser(lexer.tokens)
        #print(parser.tree)
        interpreter = Interpreter(parser.tree)

        if len(interpreter.result) == 1:
            result = interpreter.result[0]

            if result != None and result.value != None:
                return result

        return None