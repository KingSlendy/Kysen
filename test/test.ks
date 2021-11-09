class Test(value) {
    this.value = value;

    func ToString() {
        return value;
    }
}

a = Test("Message");
Print(a.ToString());