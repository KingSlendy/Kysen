import unittest
from datatypes import *
from interpreter import Interpreter
from lexer import Lexer
from parser import Parser
from runtime import Runtime

def syntax(text):
    runtime = Runtime("<unittest>", text)
    lexer = Lexer(text, runtime)
    #print(lexer.tokens)

    if len(lexer.tokens) == 1:
        return None

    parser = Parser(lexer.tokens, runtime)
    #print(parser.tree)
    interpreter = Interpreter(parser.tree, runtime)
    return interpreter.result


class TestLanguage(unittest.TestCase):
    def test_unary_operations(self):
        self.assertEqual(syntax("+10;").value, 10)
        self.assertEqual(syntax("-5;").value, -5)
        self.assertEqual(syntax("--3;").value, 3)
        self.assertEqual(syntax("!false;").value, True)
        self.assertEqual(syntax("!!false;").value, False)
        self.assertEqual(syntax("~3;").value, -4)


    def test_binary_operations(self):
        self.assertEqual(syntax("5 * 9;").value, 45)
        self.assertEqual(syntax("10 / 2;").value, 5)
        self.assertEqual(syntax("18 % 12;").value, 6)
        self.assertEqual(syntax("2 + 2;").value, 4)
        self.assertEqual(syntax("10 - 9;").value, 1)
        self.assertEqual(syntax("true && false;").value, False)
        self.assertEqual(syntax("((2 ** 4 / 2 + 2) + 1 + 1 + 1 + 1 + 1 + 1 + 1 - (3 ** 3 / 9)) * (0.245 + 0.755) - ((-(10 ** 3 / 1000) + (3 * 25 / 5)) - 1);").value, 1)