from datatypes import *
from nodes import ArgumentNode, BuiltInFunctionNode, ExpressionsNode, VarAccessNode

class BuiltIn:
    @staticmethod
    def assign(func_name, arg_names, func):
        args = []

        for name in arg_names:
            args.append(ArgumentNode(VarAccessNode(name)))

        return Function(func_name, args, ExpressionsNode([BuiltInFunctionNode(func)]))


    @staticmethod
    def print(scope):
        value = scope.access("value")
        print(value)

    
    @staticmethod
    def range(scope):
        return
        start = 0
        step = 1

        match len(args):
            case 3:
                start = args[0]
                finish = args[1]
                step = args[2]

            case 2:
                start = args[0]
                finish = args[1]

            case 1:
                finish = args[0]

        return Array([x for x in range(start, finish, step)])