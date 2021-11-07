ttt = [[[[[[func(message) {Print(message)}]]]]]];
ttt[0][0][0][0][0][0]("Hello");

func Test() {
    return [func() {Print("Hello 1");}, func() {Print("Hello 2");}, func() {Print("Hello 3");}]
}

prints = Test();
prints[0](); # Hello 1
prints[0] = func() {Print("Hello 69");}
prints[0](); # Hello 69

func Add(a = 1, b = 1) {
    return a + b;
}

Print(Add()); # 2
Print(Add(2)); # 3
Print(Add(2, 2)); # 4
Print(Add(b = 10)); # 11
Print(Add(a = 20)); # 21
Print(Add(a = 40, b = 40)); # 80