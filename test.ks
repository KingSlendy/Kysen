class Inside() {
    this.list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
}

class Outside() {
    this.inside = Inside();
}

t = Outside();
Print(t.inside.list);
modify = t.inside.list;
modify[0] = 20;
Print(t.inside.list);