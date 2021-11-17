#>
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

op = Operations(10, 15);
Console.Print(op.Add());
Console.Print(op.Subtract());
Console.Print(op.Power());
<#

#>
class Test() {
    this.value = 10;
}

func Test.Call() {
    Console.Print("Hello World!");
    Console.Print(this.value);
}

t = Test();
t.Call();
<#

#>
func String.Reverse() {
    new_str = "";

    for (char in this) {
        new_str = char + new_str;
    }

    return new_str;
}

a = "Hello";
Console.Print(a.Reverse());
<#

#>
func Array.Filter(function) {
    new_array = [];

    for (x in this) {
        if (function(x)) {
            new_array.Append(x);
        }
    }

    return new_array;
}

a = [0, 0, 1, 2, 3, 0, 5, 11, 0, 0, 10];
a = a.Filter(func(x) => (x != 0));
Console.Print(a); # [1, 2, 3, 5, 11, 10]
<#

#>
class Test() {
    this.value = 10;

    func Call() {
        Console.Print(this.value);
        Console.Print(this.value2);
    }
}

class Test2() : Test {
    base();
    this.value = 100;
    this.value2 = 1000;
}

t = Test2();
t.Call(); # 100, 100
t = Test();
t.Call(); # 10, Error
<#

#>
class Operator(left, op, right) {
    this.left = left;
    this.op = op;
    this.right = right;

    func ToString() {
        return "(" + String(this.left) + this.op + String(this.right) + ")";
    }
}

class Addition(left, right) : Operator {
    base(left, "+", right);
}

a = Addition(10, 10);
Console.Print(String(a));
<#

#>
class Test() {}
t = Test();
Console.Print(String(t));

class Test2() {
    this.value = 25;
    this.value2 = 50;

    func ToString() {
        return "(" + String(this.value) + ", " + String(this.value2) + ")";
    }
}

t = Test2();
Console.Print(String(t));
t = Test();
Console.Print(String(t));
<#


#>
class Test() {
    this.value = 10;
    this.Print = null;
    Console.Print(this.value);

    func Call(value) {
        Console.Print("Start Call");
        Console.Print(this);
        Console.Print(this.value);
        Console.Print(value);
        value = 50;
        this.value = 100;
        Console.Print(this.value);
        Console.Print(value);
    }
}

a = Test();
Console.Print(a.value);
Console.Print("Passed");
a.Call(1);
Console.Print(a.value);
Print = Console.Print;
a.Print = func() { Print("Hello"); }
a.Print();
<#