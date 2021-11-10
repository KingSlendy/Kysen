class Scope:
    def __init__(self, parent = None):
        self.parent = parent
        self.table = {}


    def assign(self, key, value):
        self.table[key] = value
        return value


    def access(self, key):
        #print(self)

        if key not in self.table:
            if self.parent != None:
                return self.parent.access(key)
            else:
                raise Exception(f"Variable '{key}' not declared in current scope.")

        return self.table[key]


    def remove(self, key):
        del self.table[key]


    def copy(self):
        return Scope(self.table)


    def items(self):
        return self.table.items()


    def __iter__(self):
        yield from self.table


    def __repr__(self):
        return str(self.table)