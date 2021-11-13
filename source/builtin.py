from datatypes import *
from time import time
def Class_Console(_, scope):
    pass
    #BuiltIn.func_assign(scope, "Print", ["value"], [], BuiltIn.Class_Global_Func_Print)
    #BuiltIn.func_assign(scope, "Timer", [], [], BuiltIn.Class_Global_Func_Timer)

    #BuiltIn.func_assign(scope, "Range", ["start"], [("finish", Null(scope.copy())), ("step", Number(scope.copy(), 1))], BuiltIn.Class_Global_Func_Range)


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