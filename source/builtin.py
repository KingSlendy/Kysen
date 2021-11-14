from datatypes import *
from time import time

class UNITTEST:
    def __init__(self, value):
        self.value = value


    def copy(self):
        return self


def Func_UNITTEST(_, scope):
    value = scope.access("value")
    return UNITTEST(value)


def Class_Console(_, scope):
    pass


def Class_Console_Func_Print(_, scope):
    value = scope.access("value")
    print(value)


def Func_Timer(_, scope):
    return NumberCache(time())


def Func_Range(_, scope):
    start = scope.access("start")
    finish = scope.access("finish")
    step = scope.access("step")

    if finish.value == None:
        finish = start
        start = NumberCache(0)

    if step.value == 0:
        raise Exception("'step' argument must be non-zero.")
    
    return Array(scope.copy(), list(range(start.value, finish.value, step.value)))


def builtin_add_all(scope):
    # - Unit Test - #
    BuiltIn.func_assign(scope, "UNITTEST", ["value"], [], Func_UNITTEST)

    # Types

    # - Number - #
    BuiltIn.class_assign(scope, "Number", ["value"], [], Number.Constructor)

    # - Bool - #
    BuiltIn.class_assign(scope, "Bool", ["value"], [], Bool.Constructor)

    # - String - #
    BuiltIn.class_assign(scope, "String", ["value"], [], String.Constructor)

    # Misc
    BuiltIn.func_assign(scope, "Range", ["start"], [("finish", NULL_TYPE), ("step", NumberCache(1))], Func_Range)
    BuiltIn.func_assign(scope, "Timer", [], [], Func_Timer)

    # - Global - #
    BuiltIn.class_assign(scope, "Console", [], [], Class_Console)
    BuiltIn.static_assign(scope, "Console", "Print", ["value"], [], Class_Console_Func_Print)