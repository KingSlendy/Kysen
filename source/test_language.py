import unittest
from datatypes import *
from interpreter import Interpreter
from lexer import Lexer
from parser import Parser
from runtime import Runtime

def language(text):
    if text == "":
        return None

    runtime = Runtime("<unittest>", text, unittest = True)
    lexer = Lexer(text, runtime)

    if len(lexer.tokens) == 1:
        return None

    parser = Parser(lexer.tokens, runtime)
    interpreter = Interpreter(parser.tree, runtime)

    return interpreter.result[-1].value


class TestLanguage(unittest.TestCase):
    def test_arrays(self):
        self.assertEqual(language("""
            a = [0, 1, 2];
            b = a;
            a[0] = 100;
            b[0];
        """), 100)

        self.assertEqual(language("""
            a = [[0, 1, 2], [3, 4, 5]];
            b = a;
            a[0] = 100;
            b[0];
        """), 100)

        self.assertEqual(language("""
            a = [[0, 1, 2], [3, 4, 5]];
            b = a;
            a[0] = 100;
            b[0];
        """), 100)


    def test_functions(self):
        self.assertEqual(language("""
            func Add(a, b) {
                return a + b;
            }
            
            Add(10, 5);
        """), 15)

        self.assertEqual(language("""
            func Add(a = 1, b = 1) {
                return a + b;
            }
            
            Add();
        """), 2)

        self.assertEqual(language("""
            func Add(a = 1, b = 1) {
                return a + b;
            }
            
            Add(2);
        """), 3)

        self.assertEqual(language("""
            func Add(a = 1, b = 1) {
                return a + b;
            }
            
            Add(2, 2);
        """), 4)

        self.assertEqual(language("""
            func Add(a = 1, b = 1) {
                return a + b;
            }
            
            Add(a = 10);
        """), 11)

        self.assertEqual(language("""
            func Add(a = 1, b = 1) {
                return a + b;
            }
            
            Add(a = 20, b = 20);
        """), 40)

        self.assertEqual(language("""
            func Add(a = 1, b = 1) {
                return a + b;
            }
            
            Add(b = 100);
        """), 101)

        self.assertEqual(language("""
            func Add(a = 1, b = 1) {
                return a + b;
            }
            
            Add(b = 200, a = 200);
        """), 400)

        self.assertEqual(language("""
            func Add(a, b) => a + b;
            Add(15, 30);
        """), 45)

        self.assertEqual(language("""
            func Test() => [[0, 1, 2, 3], [4, 5, 6, 7]];
            a = Test();
            a[0][0] = 100;
            b = Test();
            b[0][0];
        """), 0)

        self.assertEqual(language("""
            func Test() => [[0, 1, 2, 3], [4, 5, 6, 7]];
            a = Test();
            a[0][0] = 100;
            b = Test();
            a[0][0];
        """), 100)


    def test_classes(self):
        self.assertEqual(language("""
            class Test() {
                this.value = 10;
            }
            
            t = Test();
            t.value;
        """), 10)

        self.assertEqual(language("""
            class Test() {
                this.value = 10;
            }
            
            t = Test();
            t.value = 100;
            t.value;
        """), 100)

        self.assertEqual(language("""
            class Test2() {
                this.value = 30;
            }
            
            t = Test2();
            t.value;
        """), 30)

        self.assertEqual(language("""
            class Test(value) {
                this.value = value;
            }
            
            t = Test(150);
            t.value;
        """), 150)

        self.assertEqual(language("""
            class Test(left, right) {
                this.left = left;
                this.right = right;
            }
            
            t = Test(3, 9);
            t.left + t.right;
        """), 12)

        self.assertEqual(language("""
            class Test(left, right) {
                this.left = left;
                this.right = right;
                func Add() => this.left + this.right;
            }
            
            t = Test(12, 15);
            t.Add();
        """), 27)

        self.assertEqual(language("""
            class Test(left, right) {
                this.left = left;
                this.right = right;
                func Operation() => this.left + this.right;
            }
            
            class Test2(left, right) : Test(left, right) {
                func Operation() => this.left - this.right;
            }
            
            t = Test(5, 20);
            t2 = Test2(12, 8);
            t.Operation() + t2.Operation();
        """), 29)
        

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
        self.assertEqual(language("""
            a = 10;

            if (a == 10) {
                b = 100;
            }
            
            b;
        """), 100)

        self.assertEqual(language("""
            a = 10;

            if (a == 10)
                b = 100;
            
            b;
        """), 100)

        self.assertEqual(language("""
            a = 10;
            
            if (null) {
                a = 200;
            }
            
            a;
        """), 10)

        self.assertEqual(language("""
            a = 10;
            
            if (!null) {
                a = 200;
            }
            
            a;
        """), 200)

        self.assertEqual(language("""
            a = 20;
            
            if (a == 10) {
                a = 200;
            } else {
                a = 300;
            }
            
            a;
        """), 300)

        self.assertEqual(language("""
            a = 20;
            
            if (a == 10)
                a = 200;
            else
                a = 300;
            
            a;
        """), 300)

        self.assertEqual(language("""
            a = 30;
            
            if (a == 10) {
                a = 200;
            } elif (a == 30) {
                a = 500;
            } else {
                a = 300;
            }
            
            a;
        """), 500)

        self.assertEqual(language("""
            a = 50;
            
            if (a == 10) {
                a = 200;
            } elif (a == 30) {
                a = 500;
            } else {
                a = 300;
            }
            
            a;
        """), 300)

        self.assertEqual(language("""
            a = 50;
            
            if (a == 10)
                a = 200;
            elif (a == 30)
                a = 500;
            else
                a = 300;
            
            a;
        """), 300)

        self.assertEqual(language("""
            a = 50;
            
            if a == 10
                a = 200;
            elif a == 30
                a = 500;
            else
                a = 300;
            
            a;
        """), 300)


    def test_for_statement(self):
        self.assertEqual(language("""
            numbers = Range(1, 6);
            result = 0;
            
            for (n in numbers) {
                result += n;
            }
            
            result;
        """), 15)


        #self.assertEqual(language("""
        #    result = [];

        #    for (i in [0, 1, 2, 3, 4, 5]) {
        #        if (i == 3) {
        #            continue;
        #        }

        #        result.Append(i);
        #    }

        #    result;
        #"""), None)


    def test_code(self):
        self.assertEqual(language("""
            class Date() {
                seconds = 0;

                Hour => {
                    assign {
                        seconds = (value % 24) * 3600;
                    }

                    access {
                        return seconds / 3600;
                    }
                }
            }

            d = Date();
            d.Hour = 30;
            d.Hour;
        """), 6)

        self.assertEqual(language("""
            class Test() {
                this.value = 100;
                this.Call = null;
            }

            outside_value = 200;
            outside_call = func() { return outside_value; }

            t = Test();
            t.Call = outside_call;
            t.Call();
        """), 200)

        self.assertEqual(language("""
            class Test() {
                func Inside() {
                    return func() => 0;
                }
            }

            #Test.Inside();
            a = [100, 200, 300, 400];
            t = Test();
            a[t.Inside()()];
        """), 100)

        self.assertEqual(language("""
            class Inside() {
                func Message() {
                    return func() => "Hey, it works!";
                }
            }

            class Outside() {
                this.inside = Inside();
            }

            t = Outside();
            t.inside.Message()();
        """), "Hey, it works!")

        self.assertEqual(language("""
            static class Test() {
                static func Call() => "Called.";
                static value = 10;
                static value2 = 30;
            }

            Test.Call();
        """), "Called.")

        self.assertEqual(language("""
            static class Test() {
                static func Call() => "Called.";
                static value = 10;
                static value2 = 30;
            }

            Test.value;
        """), 10)

        self.assertEqual(language("""
            static class Test() {
                static func Call() => "Called.";
                static value = 10;
                static value2 = 30;
            }

            Test.value2;
        """), 30)

        self.assertRaises(Exception, language, """
            static class Test() {
                static class Test() {
                static func Call() => "Called.";
                static value = 10;
                static value2 = 30;
            }

                static value = 10;
                static value2 = 30;
            }

            t = Test();
        """)

        self.assertEqual(language("""
            class Iterable() {
                this.a = 100;

                this.Test => {
                    assign this.a = value;
                    access => this.a;
                }
            }

            i = Iterable();
            i.Test = 30;
            i.Test;
        """), 30)

        self.assertEqual(language("""
            class Test() {
                this.value = 100;

                func Call() =>
                    this.value + 15;
            }

            class Test2() : Test() {
                this.value = 3000;

                func Call() =>
                    base.Call() + base.value + this.value;
            }

            t = Test2();
            t.Call();
        """), 3215)