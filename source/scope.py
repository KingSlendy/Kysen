from exceptions import KSVariableException

class Scope:
    def __init__(self, parent = None):
        self.parent = parent
        self.table = {}


    def assign(self, key, value):
        self.table[key] = value
        return value


    def access(self, key):
        if key not in self.table:
            if self.parent != None:
                return self.parent.access(key)
            else:
                from runner import reporter
                reporter.report(KSVariableException(f"'{key}' not declared in current scope."))

        return self.table[key]


    def remove(self, key):
        del self.table[key]


    def inherit(self):
        return Scope(self)


    def clear(self):
        self.parent = None
        self.table = {}


    def copy(self):
        scope = Scope()
        scope.table = dict(self.table)
        scope.parent = self.parent
        return scope


    def transfer(self, scope):
        from datatypes import Function, Class

        for k, v in self.items():
            if k != "this":
                value = v.copy()

                if type(v) in (Function, Class):
                    value.scope = scope.inherit()

                scope.assign(k, value)


    def items(self):
        return self.table.items()


    def __eq__(self, other):
        if isinstance(other, Scope):
            return self.table == other.table

        return NotImplemented


    def __iter__(self):
        yield from self.table


    def __repr__(self):
        return str(self.table)


class Context:
    pass