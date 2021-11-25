from nodes import ArgumentNode, BuiltInClassNode, BuiltInFunctionNode, ExpressionsNode, FunctionAccessNode, KeywordArgumentNode, VarAccessNode
from scope import Scope

TYPE_SCOPE = Scope()

class DataType:
    def __init__(self, scope, value = None, name = None):
        self.scope = scope
        self.value = value
        self.name = name
        self.static = False
        self.specials = Scope()


    def set_pos(self, pos):
        self.pos = pos
        return self


    def copy(self):
        return self


    def __repr__(self):
        return f"{self.value}"


class Number(DataType):
    def __init__(self, value):
        super().__init__(TYPE_SCOPE, value, self.__class__.__name__)
        BuiltIn.func_assign(self.specials, Number.__name__, ["object"], [], Number.Func_Cast_Number)
        BuiltIn.func_assign(self.specials, Bool.__name__, ["object"], [], Number.Func_Cast_Bool)
        BuiltIn.func_assign(self.specials, String.__name__, ["object"], [], Number.Func_Cast_String)


    @staticmethod
    def Func_Cast_Number(_, scope):
        object = scope.access("object")
        return object


    @staticmethod
    def Func_Cast_Bool(_, scope):
        object = scope.access("object")
        return BoolCache(bool(object.value))


    @staticmethod
    def Func_Cast_String(_, scope):
        object = scope.access("object")
        return String(scope.copy(), str(object.value))


    @staticmethod
    def Constructor(_, scope):
        value = scope.access("value")

        if type(value) == Number:
            return NumberCache(value.value)
        
        raise Exception("Cannot cast value to Number.")


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


    def __floordiv__(self, other):
        if isinstance(other, Number):
            return NumberCache(self.value // other.value)

        return NotImplemented


    def __rfloordiv__(self, other):
        if isinstance(other, Number):
            return NumberCache(other.value // self.value)

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
        super().__init__(TYPE_SCOPE, value, self.__class__.__name__)
        BuiltIn.func_assign(self.specials, Number.__name__, ["object"], [], Bool.Func_Cast_Number)
        BuiltIn.func_assign(self.specials, Bool.__name__, ["object"], [], Bool.Func_Cast_Bool)
        BuiltIn.func_assign(self.specials, String.__name__, ["object"], [], Bool.Func_Cast_String)


    @staticmethod
    def Func_Cast_Number(_, scope):
        object = scope.access("object")
        return NumberCache(int(object.value))


    @staticmethod
    def Func_Cast_Bool(_, scope):
        object = scope.access("object")
        return object


    @staticmethod
    def Func_Cast_String(_, scope):
        object = scope.access("object")
        return String(scope.copy(), str(object.value))


    @staticmethod
    def Constructor(_, scope):
        value = scope.access("value")

        if type(value) == Bool:
            return BoolCache(value.value)
        
        raise Exception("Cannot cast value to Bool.")


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
    def __init__(self, scope, value):
        super().__init__(scope, value, self.__class__.__name__)
        self.scope.assign("this", self)

        for b in String.bound:
            self.scope.assign(b.name, Function(self.scope, b.name, b.args, b.expressions).set_pos(None))

        BuiltIn.func_assign(self.specials, Number.__name__, ["object"], [], String.Func_Cast_Number)
        BuiltIn.func_assign(self.specials, Bool.__name__, ["object"], [], String.Func_Cast_Bool)
        BuiltIn.func_assign(self.specials, String.__name__, ["object"], [], String.Func_Cast_String)


    @staticmethod
    def Func_Cast_Number(_, scope):
        object = scope.access("object")
        return NumberCache(int(object.value))


    @staticmethod
    def Func_Cast_Bool(_, scope):
        object = scope.access("object")
        return BoolCache(bool(object.value))


    @staticmethod
    def Func_Cast_String(_, scope):
        object = scope.access("object")
        return object.copy()


    @staticmethod
    def Constructor(_, scope):
        value = scope.access("value")
        
        if type(value) == String:
            return String(scope, value.value)

        raise Exception("Cannot cast value to String.")


    def __mul__(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value)

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
            return String(self.scope, self.value[index.value])


    def __setitem__(self, index, value):
        if isinstance(index, Number):
            self.value[index.value] = value


    def __iter__(self):
        yield from self.value


class Array(DataType):
    def __init__(self, scope, value):
        super().__init__(scope, value, self.__class__.__name__)
        self.scope.assign("this", self)
        BuiltIn.func_assign(self.scope, "Append", ["value"], [], self.Func_Append)

        for b in Array.bound:
            self.scope.assign(b.name, Function(self.scope, b.name, b.args, b.expressions))


    @staticmethod
    def Constructor(_, scope):
        value = scope.access("value")

        if type(value) == Array:
            return Array(scope, list(value.value)).set_pos(value.pos)
        
        raise Exception("Cannot cast value to Array.")
    

    def Func_Append(self, _, scope):
        value = scope.access("value")
        self.value.append(value)


    def copy(self):
        new_value = []

        for v in self.value:
            new_value.append(v.copy())

        return Array(self.scope, new_value).set_pos(self.pos)


    def __mul__(self, other):
        if isinstance(other, Number):
            for _ in range(other):
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
        return Function(self.scope, self.name, self.args, self.expressions).set_pos(self.pos)

    
    def __repr__(self):
        return f"<function object {self.name}>"


class Class(Function):
    def __init__(self, scope, name, args, expressions, inherit):
        super().__init__(scope, name, args, expressions)
        self.name = name
        self.inherit = inherit
        self.static = False


    def __repr__(self):
        return f"<{'static' if self.static else ''}class object {self.name}>"

    
class Instance(DataType):
    def __init__(self, scope, name, parent):
        super().__init__(scope)
        self.name = name
        self.parent = parent
        self.scope.assign("this", self)
        self.value = True


    def __repr__(self):
        return f"<instance object {self.name}>"


class Attribute(DataType):
    def __init__(self, scope, assign_expressions, access_expressions):
        self.scope = scope
        self.assign_expressions = assign_expressions
        self.access_expressions = access_expressions


    def __repr__(self):
        return f"<property object>"


class Null(DataType):
    def __init__(self):
        self.value = None


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

        scope.assign(func_name, Function(scope.copy(), func_name, total_args, ExpressionsNode([BuiltInFunctionNode(func)])).set_pos(None))


    @staticmethod
    def class_assign(scope, class_name, args, kw_args, func):
        total_args = []

        for a in args:
            total_args.append(ArgumentNode(VarAccessNode(a)))

        for kw in kw_args:
            total_args.append(KeywordArgumentNode(kw[0], kw[1]))

        scope.assign(class_name, Class(scope.copy(), class_name, total_args, ExpressionsNode([BuiltInClassNode(func)]), None).set_pos(None))


    @staticmethod
    def static_assign(scope, class_name, func_name, args, kw_args, func):
        scope = scope.access(class_name).scope
        BuiltIn.func_assign(scope, func_name, args, kw_args, func)


    @staticmethod
    def func_access(interpreter, scope, func, args, kw_args, pos):
        total_args = []

        for a in args:
            total_args.append(ArgumentNode(a))

        for kw in kw_args:
            total_args.append(KeywordArgumentNode(kw[0], kw[1]))

        return interpreter.visit({"built-in": True}, scope, FunctionAccessNode(func, total_args).set_pos(pos))


def NumberCache(n):
    check_n = int(n) + 255
    as_float = float(n)

    if as_float.is_integer() and -1 < check_n < 510:
        return NUMBER_TYPES[check_n]

    return Number(n)


def BoolCache(v):
    return BOOL_TYPES[0 if v == False else 1]


NUMBER_TYPES = [Number(n) for n in range(-255, 256)]
BOOL_TYPES = [Bool(False), Bool(True)]
NULL_TYPE = Null()

Number.bound = []
Bool.bound = []
String.bound = []
Array.bound = []