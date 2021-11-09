class Test() {
    this.value = 10;

    func Call() {
        Print("Called!");
    }
}

a = Test();
Print(a);
Print(a.value);
a.Print = func(message) {Print("Message");}
Print("Hello");
a.Print("a");