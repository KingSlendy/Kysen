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

#>
class Test() {
    func Inside() {
        return func() {return 0;}
    }
}

#Test.Inside();
a = [100, 200, 300, 400];
b = 1;
Console.Print(a[b]);
t = Test();
Console.Print(a[t.Inside()()]);
<#

#>
a = 40;

if (a == 10) {
    a = 20;
    b = 10;
    Console.Print(a);
    Console.Print(b);
} elif (a == 20) {
    a = 30;
    b = 20;
    Console.Print(a);
    Console.Print(b);
} elif (a == 30) {
    a = 40;
    b = 30;
    Console.Print(a);
    Console.Print(b);
} else {
    a = -10;
    b = -20;
    Console.Print(a);
    Console.Print(b);
}

Console.Print(a);
<#

#>
i = 0;

while (i < 10) {
    if (i == 5) {
        i += 1;
        continue;
    }

    Console.Print(i);
    i += 1;
}
<#

#>
for (i in [0, 1, 2, 3, 4, 5]) {
    if (i == 3) {
        continue;
    }

    Console.Print(i);
}
<#

class Test() {
    this.value = 100;
}

outside_value = 200;
outside_call = func() {Console.Print(outside_value);}

t = Test();
t.Call = outside_call;
t.Call();


#>
func Print(value) {
    Console.Print(value);
}

class Test() {
    this.value = 100;
}

t = Test();
t.Print = func(value) {Print(value);}
t.Print(1);
<#