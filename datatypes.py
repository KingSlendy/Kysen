from nodes import ArgumentNode, BuiltInFunctionNode, ExpressionsNode, KeywordArgumentNode, VarAccessNode
from time import time

class DataType:
    def __init__(self, scope, value = None):
        self.scope = scope
        self.value = value


    def __repr__(self):
        return f"{self.value}"


class Number(DataType):
    def __init__(self, scope, value):
        super().__init__(scope, value)


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


    def __truediv__(self, other):
        if isinstance(other, Number):
            return Number(self.value / other.value)

        return NotImplemented


    def __rtruediv__(self, other):
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
    def __init__(self, scope, value):
        super().__init__(scope, value)


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
    def __init__(self, scope, value):
        super().__init__(scope, value)


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
    def __init__(self, scope, value):
        super().__init__(scope, value)
        self.scope.assign("Append", BuiltIn.assign(self.scope, "Append", ["value"], [], self.append))


    def append(self, scope):
        value = scope.access("value")
        self.value.append(value)


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
    def __init__(self, scope, name, args, expressions):
        self.scope = scope
        self.name = name
        self.args = args
        self.expressions = expressions


    def copy(self):
        return Function(self.args, self.expressions)

    
    def __repr__(self):
        return f"<function object {self.name}>"


class Class(DataType):
    def __init__(self, scope, name, args, expressions):
        self.scope = scope
        self.name = name
        self.args = args
        self.expressions = expressions


    def __repr__(self):
        return f"<class object {self.name}>"

    
class Instance(DataType):
    def __init__(self, scope, name):
        self.scope = scope
        self.name = name
        self.scope.assign("this", self)


    def __repr__(self):
        return f"<instance object {self.name}>"


class Null(DataType):
    def __repr__(self):
        return f"null"


class BuiltIn:
    @staticmethod
    def assign(scope, func_name, args, kw_args, func):
        total_args = []

        for a in args:
            total_args.append(ArgumentNode(VarAccessNode(a)))

        for kw in kw_args:
            total_args.append(KeywordArgumentNode(kw[0], kw[1]))

        return Function(scope, func_name, total_args, ExpressionsNode([BuiltInFunctionNode(func)]))


    @staticmethod
    def print(scope):
        value = scope.access("value")
        print(value)


    @staticmethod
    def timer(scope):
        return Number(scope, time())

    
    @staticmethod
    def range(scope):
        start = scope.access("start")
        finish = scope.access("finish")
        step = scope.access("step")

        if finish.value == None:
            finish = start
            start = Number(0)

        if step.value == 0:
            raise Exception("'step' argument must be non-zero.")
        
        return range(start.value, finish.value, step.value)