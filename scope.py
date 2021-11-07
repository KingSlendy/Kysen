class Scope:
    def __init__(self, global_table, local_table = None):
        self.global_table = global_table
        self.local_table = local_table if local_table != None else self.global_table


    def assign(self, name, value):
        self.local_table[name] = value
        return value


    def access(self, name):
        if name not in self.local_table:
            raise Exception(f"Variable '{name}' not declared in current scope.")

        return self.local_table[name]


    def copy(self):
        return Scope(self.global_table, dict(self.local_table))


    def __repr__(self):
        return str(self.local_table)