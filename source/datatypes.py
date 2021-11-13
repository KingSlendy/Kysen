from nodes import ArgumentNode, BuiltInClassNode, BuiltInFunctionNode, ExpressionsNode, FunctionAccessNode, KeywordArgumentNode, VarAccessNode
from scope import Scope

TYPE_SCOPE = Scope()

class DataType:
    def __init__(self, scope, value = None):
        self.scope = scope
        self.value = value
        self.static = False


    def copy(self):
        return self


    def __repr__(self):
        return f"{self.value}"


class Number(DataType):
    def __init__(self, value):
        super().__init__(TYPE_SCOPE, value)


    @staticmethod
    def Constructor(_, scope):
        value = scope.access("value")

        match value:
            case _ if isinstance(value, Number):
                value = value.value
            
            case _ if isinstance(value, Bool):
                value = 0 if value.value == False else 1

            case _ if isinstance(value, String):
                try:
                    value = int(value.value)
                except ValueError:
                    value = float(value.value)

        return NumberCache(value)


    def __pos__(self):
        return self

    
    def __neg__(self):
        return NumberCache(-self.value)


    def __invert__(self):
        return NumberCache(~self.value)


    def __pow__(self, other):
        if isinstance(other, Number):
            return NumberCache(self.value ** other.value)

        return NotImplemented


    def __rpow__(self, other):
        if isinstance(other, Number):
            return NumberCache(other.value ** self.value)

        return NotImplemented


    def __mul__(self, other):
        if isinstance(other, Number):
            return NumberCache(self.value * other.value)

        return NotImplemented


    def __rmul__(self, other):
        if isinstance(other, Number):
            return NumberCache(other.value * self.value)

        return NotImplemented


    def __truediv__(self, other):
        if isinstance(other, Number):
            return NumberCache(self.value / other.value)

        return NotImplemented


    def __rtruediv__(self, other):
        if isinstance(other, Number):
            return NumberCache(other.value / self.value)

        return NotImplemented


    def __mod__(self, other):
        if isinstance(other, Number):
            return NumberCache(self.value % other.value)

        return NotImplemented


    def __rmod__(self, other):
        if isinstance(other, Number):
            return NumberCache(other.value % self.value)

        return NotImplemented


    def __add__(self, other):
        if isinstance(other, Number):
            return NumberCache(self.value + other.value)

        return NotImplemented
            
            
    def __radd__(self, other):
        if isinstance(other, Number):
            return NumberCache(other.value + self.value)

        return NotImplemented


    def __sub__(self, other):
        if isinstance(other, Number):
            return NumberCache(self.value - other.value)

        return NotImplemented
            
            
    def __rsub__(self, other):
        if isinstance(other, Number):
            return NumberCache(other.value - self.value)

        return NotImplemented


    def __lshift__(self, other):
        if isinstance(other, Number):
            return NumberCache(self.value << other.value)

        return NotImplemented


    def __rlshift__(self, other):
        if isinstance(other, Number):
            return NumberCache(other.value << self.value)

        return NotImplemented


    def __rshift__(self, other):
        if isinstance(other, Number):
            return NumberCache(self.value >> other.value)

        return NotImplemented


    def __rrshift__(self, other):
        if isinstance(other, Number):
            return NumberCache(other.value >> self.value)

        return NotImplemented


    def __lt__(self, other):
        if isinstance(other, Number):
            return BoolCache(self.value < other.value)
        else:
            return BoolCache(False)


    def __le__(self, other):
        if isinstance(other, Number):
            return BoolCache(self.value <= other.value)
        else:
            return BoolCache(False)


    def __gt__(self, other):
        if isinstance(other, Number):
            return BoolCache(self.value > other.value)
        else:
            return BoolCache(False)

    
    def __ge__(self, other):
        if isinstance(other, Number):
            return BoolCache(self.value >= other.value)
        else:
            return BoolCache(False)


    def __eq__(self, other):
        if isinstance(other, Number):
            return BoolCache(self.value == other.value)
        else:
            return BoolCache(False)


    def __ne__(self, other):
        if isinstance(other, Number):
            return BoolCache(self.value != other.value)
        else:
            return BoolCache(True)


    def __and__(self, other):
        if isinstance(other, Number):
            return NumberCache(self.value & other.value)

        return NotImplemented


    def __rand__(self, other):
        if isinstance(other, Number):
            return NumberCache(other.value & self.value)

        return NotImplemented

    
    def __or__(self, other):
        if isinstance(other, Number):
            return NumberCache(self.value | other.value)

        return NotImplemented


    def __ror__(self, other):
        if isinstance(other, Number):
            return NumberCache(other.value | self.value)

        return NotImplemented


    def __xor__(self, other):
        if isinstance(other, Number):
            return NumberCache(self.value ^ other.value)

        return NotImplemented


    def __rxor__(self, other):
        if isinstance(other, Number):
            return NumberCache(other.value ^ self.value)

        return NotImplemented


class Bool(DataType):
    def __init__(self, value):
        super().__init__(TYPE_SCOPE, value)


    @staticmethod
    def Constructor(_, scope):
        value = scope.access("value")

        match value:
            case _ if isinstance(value, Number):
                value = (value.value == 1)
            
            case _ if isinstance(value, Bool):
                value = value.value

            case _ if isinstance(value, String):
                value = (len(value.value) > 0)

        return BoolCache(value)


    def __eq__(self, other):
        if isinstance(other, Bool):
            return BoolCache(self.value == other.value)
        else:
            return BoolCache(self.value == other)


    def __ne__(self, other):
        if isinstance(other, Bool):
            return BoolCache(self.value != other.value)
        else:
            return BoolCache(self.value != other)


    def __repr__(self):
        return "true" if self.value == True else "false"


class String(DataType):
    def __init__(self, value):
        super().__init__(TYPE_SCOPE, value)


    @staticmethod
    def Constructor(interpreter, scope):
        value = scope.access("value")

        if isinstance(value, Instance) and "ToString" in value.scope:
            func_ToString = value.scope.access("ToString")
            value = BuiltIn.func_access(interpreter, value.scope, func_ToString, [], [])
        else:
            value = value.value

        return String(str(value))


    def __mul__(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value)

        return NotImplemented


    def __rmul__(self, other):
        self.__mul__(self, other)


    def __add__(self, other):
        if isinstance(other, String):
            return String(self.value + other.value)
        
        return NotImplemented


    def __radd__(self, other):
        if isinstance(other, String):
            return String(other.value + self.value)
        
        return NotImplemented


    def __eq__(self, other):
        if isinstance(other, String):
            return BoolCache(self.value == other.value)
        else:
            return BoolCache(self.value == other)


    def __ne__(self, other):
        if isinstance(other, String):
            return BoolCache(self.value != other.value)
        else:
            return BoolCache(self.value != other)


    def __getitem__(self, index):
        if isinstance(index, Number):
            return self.value[index.value]


    def __setitem__(self, index, value):
        if isinstance(index, Number):
            self.value[index.value] = value


class Array(DataType):
    def __init__(self, scope, value):
        super().__init__(scope, value)
        BuiltIn.func_assign(self.scope, "Append", ["value"], [], self.Func_Append)


    @staticmethod
    def Constructor(_, scope):
        value = scope.access("value")
        return Array(list(value.value))
    

    def Func_Append(self, _, scope):
        value = scope.access("value")
        self.value.append(value)


    def copy(self):
        return Array(self.scope, list(self.value))


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
        self.name = name if name != None else "anonymous"
        self.args = args
        self.expressions = expressions
        self.value = True


    def copy(self):
        return Function(self.scope, self.name, self.args, self.expressions)

    
    def __repr__(self):
        return f"<function object {self.name}>"


class Class(Function):
    def __init__(self, scope, name, args, expressions):
        super().__init__(scope, name, args, expressions)
        self.name = name
        self.static = False


    def __repr__(self):
        return f"<{'static' if self.static else ''}class object {self.name}>"

    
class Instance(DataType):
    def __init__(self, scope, name):
        self.scope = scope
        self.name = name
        self.scope.assign("this", self)
        BuiltIn.func_assign(self.scope, "ToString", [], [], Instance.Func_ToString)
        self.value = True


    @staticmethod
    def Func_ToString(scope):
        self = scope.access("this")
        return String(str(self))


    def __repr__(self):
        return f"<instance object {self.name}>"


class Attribute(DataType):
    def __init__(self, scope, assign_expressions, access_expressions):
        self.scope = scope
        self.assign_expressions = assign_expressions
        self.access_expressions = access_expressions


    def copy(self):
        return self


    def __repr__(self):
        return f"<property object>"


class Null(DataType):
    def copy(self):
        return self


    def __lt__(self):
        return Bool(False)


    def __le__(self, other):
        return Bool(isinstance(other, Null))


    def __gt__(self):
        return Bool(False)

    
    def __ge__(self, other):
        return Bool(isinstance(other, Null))


    def __eq__(self, other):
        return Bool(isinstance(other, Null))


    def __ne__(self, other):
        return Bool(not isinstance(other, Null))


    def __repr__(self):
        return f"null"


class BuiltIn:
    @staticmethod
    def func_assign(scope, func_name, args, kw_args, func):
        total_args = []

        for a in args:
            total_args.append(ArgumentNode(VarAccessNode(a)))

        for kw in kw_args:
            total_args.append(KeywordArgumentNode(kw[0], kw[1]))

        scope.assign(func_name, Function(scope.copy(), func_name, total_args, ExpressionsNode([BuiltInFunctionNode(func)])))


    @staticmethod
    def class_assign(scope, class_name, args, kw_args, func):
        total_args = []

        for a in args:
            total_args.append(ArgumentNode(VarAccessNode(a)))

        for kw in kw_args:
            total_args.append(KeywordArgumentNode(kw[0], kw[1]))

        scope.assign(class_name, Class(scope.copy(), class_name, total_args, ExpressionsNode([BuiltInClassNode(func)])))


    @staticmethod
    def static_assign(scope, class_name, func_name, args, kw_args, func):
        scope = scope.access(class_name).scope
        BuiltIn.func_assign(scope, func_name, args, kw_args, func)


    @staticmethod
    def func_access(interpreter, scope, func, args, kw_args):
        expressions = func.expressions.expressions

        if len(expressions) > 0 and not isinstance(expressions[0], BuiltInFunctionNode):
            total_args = []

            for a in args:
                total_args.append(ArgumentNode(VarAccessNode(a)))

            for kw in kw_args:
                total_args.append(KeywordArgumentNode(kw[0], kw[1]))

            return interpreter.visit(None, scope, FunctionAccessNode(func, total_args))
        else:
            return interpreter.visit(None, scope, func)


def NumberCache(n):
    check_n = n + 255
    as_float = float(n)

    if as_float.is_integer() and -1 < check_n < 510:
        return NUMBER_TYPES[check_n]

    return Number(n)


def BoolCache(v):
    return BOOL_TYPES[0 if v == False else 1]


NUMBER_TYPES = [Number(n) for n in range(-255, 256)]
BOOL_TYPES = [Bool(False), Bool(True)]
NULL_TYPE = Null(None)