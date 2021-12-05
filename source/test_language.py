import unittest
from datatypes import *
from exceptions import RuntimeException
from interpreter import Interpreter
from lexer import Lexer
from parser import Parser

def language(text):
    from runner import reporter

    if text == "":
        return None

    reporter.update("<unittest>", text, unittest = True)
    lexer = Lexer(text)

    if len(lexer.tokens) == 1:
        return None

    parser = Parser(lexer.tokens)
    interpreter = Interpreter(parser.tree)

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

        self.assertEqual(language("""
            a = [0, 1, 2, 3, 4];
            a[0] += 100;
            a[0];
        """), 100)

        self.assertEqual(language("""
            a = [[0, 1], [2, 3]];
            a[0][0] += 100;
            a[0][0];
        """), 100)

        self.assertEqual(language("""
            class Test() {
                this.value = 10;
            }

            t = [new Test()];

            t[0].value;
        """), 10)


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

        self.assertEqual(language("""
            func Test(array) {
                array[0] = 100;
            }

            a = [0, 1, 2, 3, 4];
            Test(a);
            a[0];
        """), 100)

        self.assertEqual(language("""
            class Test() {
                this.value = 10;
            }

            func Call() => new Test();

            Call().value;
        """), 10)

        self.assertEqual(language("""
            sign = func(n) => (n == 0) ? 0 : (n > 0) ? 1 : -1;
            sign(100);
        """), 1)


    def test_classes(self):
        self.assertEqual(language("""
            class Test() {
                this.value = 10;
            }
            
            t = new Test();
            t.value;
        """), 10)

        self.assertEqual(language("""
            class Test() {
                this.value = 10;
            }
            
            t = new Test();
            t.value = 100;
            t.value;
        """), 100)

        self.assertEqual(language("""
            class Test2() {
                this.value = 30;
            }
            
            t = new Test2();
            t.value;
        """), 30)

        self.assertEqual(language("""
            class Test(value) {
                this.value = value;
            }
            
            t = new Test(150);
            t.value;
        """), 150)

        self.assertEqual(language("""
            class Test(left, right) {
                this.left = left;
                this.right = right;
            }
            
            t = new Test(3, 9);
            t.left + t.right;
        """), 12)

        self.assertEqual(language("""
            class Test(left, right) {
                this.left = left;
                this.right = right;
                func Add() => this.left + this.right;
            }
            
            t = new Test(12, 15);
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
            
            t = new Test(5, 20);
            t2 = new Test2(12, 8);
            t.Operation() + t2.Operation();
        """), 29)

        self.assertEqual(language("""
            class Test() {
                static func Call() => "Hello!";
            }

            class Test2() : Test() { }

            Test2.Call();
        """), "Hello!")

        self.assertEqual(language("""
            class Test3() {
                this.value2 = 1000;
            }

            class Test(value) : Test3() {
                this.value = value;
            }

            class Test2() {
                this.value = 1234;

                cast Test() {
                    return new Test(this.value);
                }
            }

            t2 = new Test2();
            t = <Test>t2;
            t.value;
        """), 1234)

        self.assertEqual(language("""
            class Test3() {
                this.value2 = 1000;
            }

            class Test(value) : Test3() {
                this.value = value;
            }

            class Test2() {
                this.value = 1234;

                cast Test() {
                    return new Test(this.value);
                }
            }

            t2 = new Test2();
            t = <Test>t2;
            t.value2;
        """), 1000)

        self.assertEqual(language("""
            class Test() {
                this.value = 1000;

                cast Number() {
                    return this.value;
                }

                cast String() {
                    return <String>this.value;
                }
            }

            t = new Test();
            t2 = <Test>t;
            t2.value = 254;
            <String>t;
        """), "1000")

        self.assertEqual(language("""
            class Test() {
                this.value = 1000;

                cast Number() {
                    return this.value;
                }

                cast String() {
                    return <String>this.value;
                }
            }

            t = new Test();
            t2 = <Test>t;
            t2.value = 254;
            <String>t2;
        """), "254")

        self.assertEqual(language("""
            class Test() {
                this.value = 1000;

                cast Number() {
                    return this.value;
                }

                cast String() {
                    return <String>this.value;
                }
            }

            t = new Test();
            t2 = <Test>t;
            t2.value = 254;
            <Number>t;
        """), 1000)

        self.assertEqual(language("""
            class Test() {
                this.value = 1000;

                cast Number() {
                    return this.value;
                }

                cast String() {
                    return <String>this.value;
                }
            }

            t = new Test();
            t2 = <Test>t;
            t2.value = 254;
            <Number>t2;
        """), 254)

        self.assertEqual(language("""
            class Test() {
                this.ttt = 333;

                this.TTT = {
                    assign {
                        ttt = value;
                    }

                    access {
                        return ttt + 100;
                    }
                }
            }

            t = new Test();
            t.TTT += 200;
            t.TTT;
        """), 733)
        

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
        self.assertEqual(language("10 \\ 3;"), 3)
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
        self.assertEqual(language("40 / 10 / 2;"), 2)
        self.assertEqual(language("((2 ** 4 / 2 + 2) + 1 + 1 + 1 + 1 + 1 + 1 + 1 - (3 ** 3 / 9)) * (0.245 + 0.755) - ((-(10 ** 3 / 1000) + (3 * 25 / 5)) - 1);"), 1)

        self.assertEqual(language("""
            a = 10;
            a += 100;
            a;
        """), 110)

        self.assertEqual(language("""
            a = 10;
            a *= 100;
            a;
        """), 1000)


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
            
            if (a == 10)
                a = 200;
            elif (a == 30)
                a = 500;
            else
                a = 300;
            
            a;
        """), 300)

        self.assertEqual(language("""
            a = (2 == 2) ? 10 : 20;
            a;
        """), 10)


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


    def test_extensions(self):
        self.assertEqual(language("""
            class Operations(left, right) {
                this.left = left;
                this.right = right;

                func Add() {
                    return this.left + this.right;
                }

                func Subtract() {
                    return this.left - this.right;
                }
            }

            func Operations.Power() {
                return this.left ** this.right;
            }

            op = new Operations(3, 4);
            op.Power();
        """), 81)

        self.assertEqual(language("""
            class Test() {
                this.value = 10;
            }

            func Test.Call() => this.value;
            t = new Test();
            t.Call();
        """), 10)

        self.assertEqual(language("""
            func String.Reverse() {
                new_str = "";

                for (char in this) {
                    new_str = char + new_str;
                }

                return new_str;
            }

            a = "Hello";
            a.Reverse();
        """), "olleH")


    def test_codes(self):
        self.assertEqual(language("""
            class Date() {
                seconds = 0;

                Hour = {
                    assign {
                        seconds = (value % 24) * 3600;
                    }

                    access {
                        return seconds / 3600;
                    }
                }
            }

            d = new Date();
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

            t = new Test();
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
            t = new Test();
            a[t.Inside()()];
        """), 100)

        self.assertEqual(language("""
            class Inside() {
                func Message() {
                    return func() => "Hey, it works!";
                }
            }

            class Outside() {
                this.inside = new Inside();
            }

            t = new Outside();
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

            t = new Test();
        """)

        self.assertEqual(language("""
            class Iterable() {
                this.a = 100;

                this.Test = {
                    assign this.a = value;
                    access => this.a;
                }
            }

            i = new Iterable();
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

            t = new Test2();
            t.Call();
        """), 3215)

        self.assertEqual(language("""
            class Vehicle(price) {
                this.price = price;
                func Sound() => "...";
            }

            class Car(price) : Vehicle(price) {
                func Sound() => "Sound: VROOOM";
            }

            class Ferrari(name, price) : Car(price) {
                this.name = name;
                this.color = "Red";
                this.country = "Europe";

                func Info() =>
                    base.Sound() + "\nName: " + this.name + "\nPrice: " + <String>this.price + "\nColor: " + this.color + "\nCountry: " + this.country;
            }

            class Ferrari488() : Ferrari("Ferrari488", 284700) {
                func Buy() => "You bought a car with this info:\n" + base.Info();
            }

            c = new Ferrari488();
            c.Buy();
        """), "You bought a car with this info:\nSound: VROOOM\nName: Ferrari488\nPrice: 284700\nColor: Red\nCountry: Europe")

        self.assertEqual(language("""
            func Test(function) =>
                function(10, 5);

            Test(func(a, b) => a + b);
        """), 15)

        self.assertAlmostEqual(language("""
            class Day(seconds) {
                this.Seconds = seconds;

                this.Minutes = {
                    assign this.Seconds = value * 60;
                    access => this.Seconds / 60;
                }

                this.Hours = {
                    assign this.Seconds = value * 3600;
                    access => this.Seconds / 3600;
                }

                this.Days = {
                    assign this.Seconds = value * 3600 * 24;
                    access => this.Seconds / 3600 / 24;
                }
            }

            d = new Day(1482);
            d.Minutes = 100;
            d.Hours;
        """), 1.666666667)


    def test_errors(self):
        with self.assertRaisesRegex(RuntimeException, "SyntaxException: expected ';'."):
            language("3 + 2")

        with self.assertRaisesRegex(RuntimeException, "SyntaxException: unexpected syntax."):
            language("3+")

        with self.assertRaisesRegex(RuntimeException, "VariableException: 'a' not declared in current scope."):
            language("a;")

        with self.assertRaisesRegex(RuntimeException, "CastException: cannot cast type 'Test' to type 'Test2'."):
            language("""
                class Test() {

                }

                class Test2() {

                }

                t = new Test();
                <Test2>t;
            """)

        with self.assertRaisesRegex(RuntimeException, "StaticException: static classes can't have non-static properties."):
            language("""
                static class Test() {
                    a = 10;
                }
            """)