class Test() {
    this.value = 10;
    Console.Print(this.value);
}

a = Test();
Console.Print(a.value);

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
a.Print = func() {Console.Print("Hello");}
a.Print();
<#