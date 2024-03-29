from datatypes import *
from exceptions import *
from nodes import *
from time import time

def Class_Console(_, scope):
    pass


def Class_Console_Func_Print(interpreter, scope):
    value = scope.access("value")

    if type(value) == Instance and String.__name__ in value.specials:
        value = interpreter.visit(None, scope, CastNode(String.__name__, value))
        
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
        from runner import reporter
        reporter.report(KSArgumentException("'step' argument must be non-zero."))
    
    #r = [NumberCache(n) for n in range(start.value, finish.value, step.value)]
    return Iterable(range(start.value, finish.value, step.value))


def builtin_add_all(scope):
    # Types

    # - Number - #
    BuiltIn.class_assign(scope, "Number", ["value"], [], Number.Constructor)

    # - Bool - #
    BuiltIn.class_assign(scope, "Bool", ["value"], [], Bool.Constructor)

    # - String - #
    BuiltIn.class_assign(scope, "String", ["value"], [], String.Constructor)

    # - Array - #
    BuiltIn.class_assign(scope, "Array", ["value"], [], Array.Constructor)

    # - Global - #
    BuiltIn.class_assign(scope, "Console", [], [], Class_Console)
    BuiltIn.static_assign(scope, "Console", "Print", ["value"], [], Class_Console_Func_Print)

    BuiltIn.func_assign(scope, "Range", ["start"], [("finish", NULL_TYPE), ("step", NumberCache(1))], Func_Range)
    BuiltIn.func_assign(scope, "Timer", [], [], Func_Timer)