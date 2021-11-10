#>
class Test() {
    this.value = 10;
    Console.Print(this.value);
    this.value = 30;
    Console.Print(this.value);
}

Console.Print("A");
a = Test();
Console.Print(a.value);
<#

#>
Console.Print("Hello!");

static class Test() {
    static func Call() {
        Console.Print("Called.");
    }

    static value = 10;
    static value2 = 30;
}

Console.Print(Test.value2);
Test.Call(); # Called.
Console.Print(Test.value); # 10
a = Test(); # Error
<#

#>
class Test() {
    this.value = 10;
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
a.Print = func() {Console.Print("Hello");}
a.Print();
<#

#>
class Inside() {
    func Message() {
        return func() {Console.Print("Hey, it works!");}
    }
}

class Outside() {
    this.inside = Inside();
}

t = Outside();
t.inside.Message()();
<#

class Test() {
    func Inside() {
        return func() {return 0;}
    }
}

a = [100, 200, 300, 400];
b = 1;
Console.Print(a[b]);
t = Test();
Console.Print(a[t.Inside()()]);