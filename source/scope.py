class Scope:
    def __init__(self, table = {}, parent = None):
        self.table = dict(table)
        self.parent = parent
        self.look_back = True


    def assign(self, key, value):
        self.table[key] = value
        return value


    def access(self, key):
        if key not in self.table:
            if self.look_back and self.parent == None:
                raise Exception(f"Variable '{key}' not declared in current scope.")
            else:
                return self.parent.access(key)

        return self.table[key]


    def remove(self, key):
        del self.table[key]


    def copy(self):
        return Scope(dict(self.table))


    def items(self):
        return self.table.items()


    def __iter__(self):
        yield from self.table


    def __repr__(self):
        return str(self.table)