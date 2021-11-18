class Vehicle(price) {
    this.price = price;

    func Sound() {
        Console.Print("...");
    }
}

class Car(price) : Vehicle(price) {
    func Sound() {
        Console.Print("VROOOM");
    }
}

class Ferrari(name, price) : Car(price) {
    this.name = name;
    this.color = "Red";
    this.country = "Europe";

    func Info() {
        Console.Print("Name: " + String(this.name) + "\nPrice: " + String(this.price) + "\nColor: " + this.color + "\nCountry: " + this.country);
    }
}

class Ferrari488() : Ferrari("Ferrari488", 284700) {
    func Buy() {
        Console.Print("You bought the Ferrari488!");
    }
}

c = Ferrari488();
c.Sound();
c.Info();
c.Buy();

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