from nodes import ArgumentNode, BuiltInClassNode, BuiltInFunctionNode, ExpressionsNode, KeywordArgumentNode, VarAccessNode
from scope import Scope
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


    def __pos__(self):
        return self

    
    def __neg__(self):
        return Number(self.scope, -self.value)


    def __invert__(self):
        return Number(self.scope, ~self.value)


    def __pow__(self, other):
        if isinstance(other, Number):
            return Number(self.scope, self.value ** other.value)

        return NotImplemented


    def __rpow__(self, other):
        if isinstance(other, Number):
            return Number(other.value ** self.value)

        return NotImplemented


    def __mul__(self, other):
        if isinstance(other, Number):
            return Number(self.scope, self.value * other.value)

        return NotImplemented


    def __rmul__(self, other):
        if isinstance(other, Number):
            return Number(self.scope, other.value * self.value)

        return NotImplemented


    def __truediv__(self, other):
        if isinstance(other, Number):
            return Number(self.scope, self.value / other.value)

        return NotImplemented


    def __rtruediv__(self, other):
        if isinstance(other, Number):
            return Number(self.scope, other.value / self.value)

        return NotImplemented


    def __mod__(self, other):
        if isinstance(other, Number):
            return Number(self.scope, self.value % other.value)

        return NotImplemented


    def __rmod__(self, other):
        if isinstance(other, Number):
            return Number(self.scope, other.value % self.value)

        return NotImplemented


    def __add__(self, other):
        if isinstance(other, Number):
            return Number(self.scope, self.value + other.value)

        return NotImplemented
            
            
    def __radd__(self, other):
        if isinstance(other, Number):
            return Number(self.scope, other.value + self.value)

        return NotImplemented


    def __sub__(self, other):
        if isinstance(other, Number):
            return Number(self.scope, self.value - other.value)

        return NotImplemented
            
            
    def __rsub__(self, other):
        if isinstance(other, Number):
            return Number(self.scope, other.value - self.value)

        return NotImplemented


    def __lshift__(self, other):
        if isinstance(other, Number):
            return Number(self.scope, self.value << other.value)

        return NotImplemented


    def __rlshift__(self, other):
        if isinstance(other, Number):
            return Number(self.scope, other.value << self.value)

        return NotImplemented


    def __rshift__(self, other):
        if isinstance(other, Number):
            return Number(self.scope, self.value >> other.value)

        return NotImplemented


    def __rrshift__(self, other):
        if isinstance(other, Number):
            return Number(self.scope, other.value >> self.value)

        return NotImplemented


    def __lt__(self, other):
        if isinstance(other, Number):
            return Bool(self.scope, self.value < other.value)
        else:
            return Bool(self.scope, False)


    def __le__(self, other):
        if isinstance(other, Number):
            return Bool(self.scope, self.value <= other.value)
        else:
            return Bool(self.scope, False)


    def __gt__(self, other):
        if isinstance(other, Number):
            return Bool(self.scope, self.value > other.value)
        else:
            return Bool(self.scope, False)

    
    def __ge__(self, other):
        if isinstance(other, Number):
            return Bool(self.scope, self.value >= other.value)
        else:
            return Bool(self.scope, False)


    def __eq__(self, other):
        if isinstance(other, Number):
            return Bool(self.scope, self.value == other.value)
        else:
            return Bool(self.scope, False)


    def __ne__(self, other):
        if isinstance(other, Number):
            return Bool(self.scope, self.value != other.value)
        else:
            return Bool(self.scope, True)


    def __and__(self, other):
        if isinstance(other, Number):
            return Number(self.scope, self.value & other.value)

        return NotImplemented


    def __rand__(self, other):
        if isinstance(other, Number):
            return Number(self.scope, other.value & self.value)

        return NotImplemented

    
    def __or__(self, other):
        if isinstance(other, Number):
            return Number(self.scope, self.value | other.value)

        return NotImplemented


    def __ror__(self, other):
        if isinstance(other, Number):
            return Number(self.scope, other.value | self.value)

        return NotImplemented


    def __xor__(self, other):
        if isinstance(other, Number):
            return Number(self.scope, self.value ^ other.value)

        return NotImplemented


    def __rxor__(self, other):
        if isinstance(other, Number):
            return Number(self.scope, other.value ^ self.value)

        return NotImplemented


class Bool(DataType):
    def __init__(self, scope, value):
        super().__init__(scope, value)


    def __eq__(self, other):
        if isinstance(other, Bool):
            return Bool(self.scope, self.value == other.value)
        else:
            return Bool(self.scope, self.value == other)


    def __ne__(self, other):
        if isinstance(other, Bool):
            return Bool(self.scope, self.value != other.value)
        else:
            return Bool(self.scope, self.value != other)


    def __repr__(self):
        return "true" if self.value == True else "false"


class String(DataType):
    def __init__(self, scope, value):
        super().__init__(scope, value)


    def __mul__(self, other):
        if isinstance(other, Number):
            return String(self.scope, self.value * other.value)

        return NotImplemented


    def __rmul__(self, other):
        self.__mul__(self, other)


    def __add__(self, other):
        if isinstance(other, String):
            return String(self.scope, self.value + other.value)
        
        return NotImplemented


    def __radd__(self, other):
        if isinstance(other, String):
            return String(self.scope, other.value + self.value)
        
        return NotImplemented


    def __eq__(self, other):
        if isinstance(other, String):
            return Bool(self.scope, self.value == other.value)
        else:
            return Bool(self.scope, self.value == other)


    def __ne__(self, other):
        if isinstance(other, String):
            return Bool(self.scope, self.value != other.value)
        else:
            return Bool(self.scope, self.value != other)


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


    def Func_Append(self, scope):
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
        self.name = name if name != None else "#anonymous"
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
        self.static = False


    def __repr__(self):
        return f"<{'static' if self.static else ''}class object {self.name}>"

    
class Instance(DataType):
    def __init__(self, scope, name):
        self.scope = scope
        self.name = name
        self.scope.assign("this", self)
        BuiltIn.func_assign(self.scope, "ToString", [], [], self.Func_ToString)


    def Func_ToString(self, scope):
        obj = scope.access("this")
        return String(scope, str(obj))


    def __repr__(self):
        return f"<instance object {self.name}>"


class Null(DataType):
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
    def Class_Console(_):
        pass
        #BuiltIn.func_assign(scope, "Print", ["value"], [], BuiltIn.Class_Global_Func_Print)
        #BuiltIn.func_assign(scope, "Timer", [], [], BuiltIn.Class_Global_Func_Timer)

        #BuiltIn.func_assign(scope, "Range", ["start"], [("finish", Null(scope.copy())), ("step", Number(scope.copy(), 1))], BuiltIn.Class_Global_Func_Range)


    @staticmethod
    def Class_Console_Func_Print(scope):
        value = scope.access("value")
        print(value)


    @staticmethod
    def Class_Global_Func_Timer(scope):
        return Number(scope, time())

    
    @staticmethod
    def Class_Global_Func_Range(scope):
        start = scope.access("start")
        finish = scope.access("finish")
        step = scope.access("step")

        if finish.value == None:
            finish = start
            start = Number(0)

        if step.value == 0:
            raise Exception("'step' argument must be non-zero.")
        
        return Array(scope.copy(), list(range(start.value, finish.value, step.value)))