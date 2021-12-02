

#>
class Test() : String("a") {

}

a = "a";
Console.Print(a.value);
t = new Test();
Console.Print(t.value);
<#

#>
time = Timer();
r = Range(100000);

for (i in r) {
    a = 1 + 1;
}

Console.Print(Timer() - time);
<#

#>
class Test(value) {
    this.value = value;

    cast String() {
        return this.value;
    }
}

class Test2() {
    this.value = 1234;

    cast Test() {
        Console.Print(this.value);
        return new Test(this.value);
    }
}

t = new Test(123);
Console.Print(<String>t);
<#

#>
for (i in [0, 1, 2, 3]) {
    for (j in [4, 5, 6, 7]) {
        if (i + j == 6) {
            break 2;
        }

        Console.Print(new String(i) + ", " + new String(j));
    }
}
<#

#>
for (i in [0, 1, 2, 3]) {
    for (j in [0, 1, 2, 3]) {
        for (k in [0, 1, 2, 3]) {
            if (i + j + k == 5) {
                break 3;
            }

            Console.Print(new String(i) + ", " + new String(j) + ", " + new String(k));
        }
    }
}
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