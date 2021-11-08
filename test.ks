class Test() {
    value = 1;
}

func Add(a = 1, b = 1) {
    return a + b;
}

Print(Add()); # 2
Print(Add(2)); # 3
Print(Add(2, 2)); # 4
Print(Add(b = 10)); # 11
Print(Add(a = 20)); # 21
Print(Add(a = 40, b = 40)); # 80