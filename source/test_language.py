import unittest
from datatypes import *
from interpreter import Interpreter
from lexer import Lexer
from parser import Parser
from runtime import Runtime

def language(text):
    runtime = Runtime("<unittest>", text, unittest = True)
    lexer = Lexer(text, runtime)
    #print(lexer.tokens)

    if len(lexer.tokens) == 1:
        return None

    parser = Parser(lexer.tokens, runtime)
    #print(parser.tree)
    interpreter = Interpreter(parser.tree, runtime)

    return interpreter.result[-1].value


class TestLanguage(unittest.TestCase):
    def test_unary_operations(self):
        self.assertEqual(language("+10;"), 10)
        self.assertEqual(language("-5;"), -5)
        self.assertEqual(language("--3;"), 3)
        self.assertTrue(language("!false;"))
        self.assertFalse(language("!true;"))
        self.assertFalse(language("!!false;"))
        self.assertEqual(language("~3;"), -4)


    def test_binary_operations(self):
        self.assertEqual(language("5 * 9;"), 45)
        self.assertEqual(language("10 / 2;"), 5)
        self.assertEqual(language("18 % 12;"), 6)
        self.assertEqual(language("2 + 2;"), 4)
        self.assertEqual(language("10 - 9;"), 1)
        self.assertEqual(language("1 << 4;"), 16)
        self.assertEqual(language("10 >> 1;"), 5)
        self.assertTrue(language("1 < 4;"))
        self.assertFalse(language("6 <= 4;"))
        self.assertFalse(language("1 > 4;"))
        self.assertTrue(language("6 >= 4;"))
        self.assertTrue(language("2 == 2;"))
        self.assertFalse(language("3 != 3;"))
        self.assertEqual(language("3 & 1;"), 1)
        self.assertEqual(language("4 | 2;"), 6)
        self.assertEqual(language("10 ^ 5;"), 15)
        self.assertFalse(language("true && false;"))
        self.assertTrue(language("true || false;"))
        self.assertEqual(language("((2 ** 4 / 2 + 2) + 1 + 1 + 1 + 1 + 1 + 1 + 1 - (3 ** 3 / 9)) * (0.245 + 0.755) - ((-(10 ** 3 / 1000) + (3 * 25 / 5)) - 1);"), 1)


    def test_if_statement(self):
        self.assertEqual(language("a = 10; if (a == 10) { b = 100; } b;"), 100)
        self.assertEqual(language("a = 10; if (null) { a = 200; } a;"), 10)
        self.assertEqual(language("a = 10; if (!null) { a = 200; } a;"), 200)
        self.assertEqual(language("a = 20; if (a == 10) { a = 200; } else { a = 300; } a;"), 300)


    def test_for_statement(self):
        self.assertEqual(language("numbers = Range(1, 6); result = 0; for (n in numbers) { result += n; } result;"), 15)