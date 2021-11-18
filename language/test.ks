class Test(value) {
    this.value = value;
}

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