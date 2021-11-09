class Scope:
    def __init__(self, table = {}):
        self.table = dict(table)


    def assign(self, key, value):
        self.table[key] = value
        return value


    def access(self, key):
        if key not in self.table:
            raise Exception(f"Variable '{key}' not declared in current scope.")

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