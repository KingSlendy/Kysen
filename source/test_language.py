import unittest
from builtin import UNITTEST
from datatypes import *
from interpreter import global_scope, Interpreter
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

    if isinstance(interpreter.result, UNITTEST):
        return interpreter.result.value.value
    else:
        return interpreter.result.value


class TestLanguage(unittest.TestCase):
    def test_unary_operations(self):
        self.assertEqual(syntax("+10;"), 10)
        self.assertEqual(syntax("-5;"), -5)
        self.assertEqual(syntax("--3;"), 3)
        self.assertEqual(syntax("!false;"), True)
        self.assertEqual(syntax("!!false;"), False)
        self.assertEqual(syntax("~3;"), -4)


    def test_binary_operations(self):
        self.assertEqual(syntax("5 * 9;"), 45)
        self.assertEqual(syntax("10 / 2;"), 5)
        self.assertEqual(syntax("18 % 12;"), 6)
        self.assertEqual(syntax("2 + 2;"), 4)
        self.assertEqual(syntax("10 - 9;"), 1)
        self.assertEqual(syntax("1 << 4;"), 16)
        self.assertEqual(syntax("10 >> 1;"), 5)
        self.assertTrue(syntax("1 < 4;"))
        self.assertFalse(syntax("6 <= 4;"))
        self.assertFalse(syntax("1 > 4;"))
        self.assertTrue(syntax("6 >= 4;"))
        self.assertTrue(syntax("2 == 2;"))
        self.assertFalse(syntax("3 != 3;"))
        self.assertEqual(syntax("3 & 1;"), 1)
        self.assertEqual(syntax("4 | 2;"), 6)
        self.assertEqual(syntax("10 ^ 5;"), 15)
        self.assertFalse(syntax("true && false;"))
        self.assertTrue(syntax("true || false;"))
        self.assertEqual(syntax("((2 ** 4 / 2 + 2) + 1 + 1 + 1 + 1 + 1 + 1 + 1 - (3 ** 3 / 9)) * (0.245 + 0.755) - ((-(10 ** 3 / 1000) + (3 * 25 / 5)) - 1);"), 1)


    def test_if_statement(self):
        self.assertEqual(syntax("a = 10; if (a == 10) { b = 100; } UNITTEST(b);"), 100)
        self.assertEqual(syntax("b;"), 100)