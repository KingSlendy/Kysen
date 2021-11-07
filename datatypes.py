class DataType:
    def __init__(self, value):
        self.value = value


    def __repr__(self):
        return f"{self.value}"


class Number(DataType):
    def __init__(self, value):
        super().__init__(value)


    def __pow__(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value)

        return NotImplemented


    def __rpow__(self, other):
        if isinstance(other, Number):
            return Number(other.value ** self.value)

        return NotImplemented


    def __mul__(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value)

        return NotImplemented


    def __rmul__(self, other):
        if isinstance(other, Number):
            return Number(other.value * self.value)

        return NotImplemented


    def __div__(self, other):
        if isinstance(other, Number):
            return Number(self.value / other.value)

        return NotImplemented


    def __rdiv__(self, other):
        if isinstance(other, Number):
            return Number(other.value / self.value)

        return NotImplemented


    def __add__(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)

        return NotImplemented
            
            
    def __radd__(self, other):
        if isinstance(other, Number):
            return Number(other.value + self.value)

        return NotImplemented


    def __sub__(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value)

        return NotImplemented
            
            
    def __rsub__(self, other):
        if isinstance(other, Number):
            return Number(other.value - self.value)

        return NotImplemented


    def __eq__(self, other):
        if isinstance(other, Number):
            return Bool(self.value == other.value)
        else:
            return Bool(False)


    def __ne__(self, other):
        if isinstance(other, Number):
            return Bool(self.value != other.value)
        else:
            return Bool(True)


    def __lt__(self, other):
        if isinstance(other, Number):
            return Bool(self.value < other.value)
        else:
            return Bool(False)


    def __le__(self, other):
        if isinstance(other, Number):
            return Bool(self.value <= other.value)
        else:
            return Bool(False)


    def __gt__(self, other):
        if isinstance(other, Number):
            return Bool(self.value > other.value)
        else:
            return Bool(False)

    
    def __ge__(self, other):
        if isinstance(other, Number):
            return Bool(self.value >= other.value)
        else:
            return Bool(False)


class Bool(DataType):
    def __init__(self, value):
        super().__init__(value)


    def __eq__(self, other):
        if isinstance(other, Bool):
            return Bool(self.value == other.value)
        else:
            return self.value == other


    def __ne__(self, other):
        if isinstance(other, Bool):
            return Bool(self.value != other.value)
        else:
            return self.value != other


    def __repr__(self):
        return "true" if self.value == True else "false"


class String(DataType):
    def __init__(self, value):
        super().__init__(value)


    def __eq__(self, other):
        if isinstance(other, String):
            return Bool(self.value == other.value)
        else:
            return Bool(self.value == other)


    def __ne__(self, other):
        if isinstance(other, String):
            return Bool(self.value != other.value)
        else:
            return Bool(self.value != other)


    def __getitem__(self, index):
        if isinstance(index, Number):
            return self.value[index.value]


    def __setitem__(self, index, value):
        if isinstance(index, Number):
            self.value[index.value] = value


class Array(DataType):
    def __init__(self, value):
        super().__init__(value)


    def copy(self):
        return Array(list(self.value))


    def __mul__(self, other):
        if isinstance(other, Number):
            for i in range(other):
                for v in self.value:
                    self.value.append(v)

            return self.value

        return NotImplemented


    def __rmul__(self, other):
        if isinstance(other, Number):
            return self.__mul__(other)

        return NotImplemented


    def __getitem__(self, index):
        if isinstance(index, Number):
            return self.value[index.value]


    def __setitem__(self, index, value):
        if isinstance(index, Number):
            self.value[index.value] = value


    def __iter__(self):
        yield from self.value


class Function(DataType):
    def __init__(self, name, args, expressions):
        self.name = name
        self.args = args
        self.expressions = expressions


    def copy(self):
        return Function(self.args, self.expressions)

    
    def __repr__(self):
        return f"func {self.name}({self.args}) {self.expressions}"


class Class(DataType):
    def __init__(self, name, args, expressions):
        self.name = name
        self.args = args
        self.expressions = expressions


    def __repr__(self):
        return f"class {self.name}({self.args}) {self.expressions}"


class Null(DataType):
    def __repr__(self):
        return f"null"