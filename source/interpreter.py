from datatypes import *
from nodes import *
from scope import Scope

global_scope = Scope()
BuiltIn.class_assign(global_scope, "Test", [], [], BuiltIn.Class_Test)

BuiltIn.func_assign(global_scope, "Print", ["value"], [], BuiltIn.Func_Print)
BuiltIn.func_assign(global_scope, "Timer", [], [], BuiltIn.Func_Timer)

BuiltIn.func_assign(global_scope, "Range", ["start"], [("finish", Null(global_scope)), ("step", Number(global_scope, 1))], BuiltIn.Func_Range)

class Interpreter:
    def __init__(self, tree):
        self.tree = tree
        self.result = None
        self.run()

    
    def visit(self, node, scope):
        match node:
            case n if isinstance(n, ExpressionsNode):
                results = []

                for e in n.expressions:
                    results.append(self.visit(e, scope))

                return None if len(results) > 1 else results[0]

            case n if isinstance(n, VarAssignNode):
                value = self.visit(n.expression, scope)

                if not issubclass(type(value), DataType):
                    raise Exception(f"Cannot assign a non-type value to variable '{n.name}'")

                return scope.assign(n.name, value)

            case n if isinstance(n, VarAccessNode):
                return scope.access(n.name)

            case n if isinstance(n, AccessorNode):
                identifier = self.visit(n.node, scope)

                if identifier == None:
                    raise Exception(f"Cannot use accessor for null.")

                if isinstance(identifier, Instance) or issubclass(type(identifier), DataType):
                    return self.visit(n.index_expression, Scope({k: v for k, v in identifier.scope.items() if k not in global_scope}))
                else:
                    index_expression = self.visit(n.index_expression, scope)
                    return identifier[index_expression]

            case n if isinstance(n, AssignerNode):
                identifier = self.visit(n.node, scope)
                index_expression = self.visit(n.index_expression, scope)
                value_expression = None

                if n.value_expression != None:
                    value_expression = self.visit(n.value_expression, scope)
                    identifier[index_expression] = value_expression

                return identifier[index_expression]

            case n if isinstance(n, FunctionAccessNode):
                identifier = self.visit(n.node, scope)

                if not isinstance(identifier, (Function, Class)):
                    raise Exception(f"Trying to access a variable that's not a function or class.")

                args = [x for x in identifier.args if isinstance(x, ArgumentNode)]
                kw_args = [x for x in identifier.args if isinstance(x, KeywordArgumentNode)]
                passed_args = n.args
                arg_number = len(args) + len(kw_args)
                passed_arg_number = len(passed_args)

                if passed_arg_number < len(args):
                    raise Exception(f"Expected {len(args)} positional argument(s), got {passed_arg_number}.")
                elif passed_arg_number > arg_number:
                    raise Exception(f"Expected {arg_number} total argument(s), got {passed_arg_number}.")

                scope = scope.copy()

                for i, arg in enumerate(args):
                    parg = passed_args[i]

                    if isinstance(parg, KeywordArgumentNode):
                        raise Exception(f"Expected positional argument: '{arg.expression.name}'.")

                    scope.assign(arg.expression.name, self.visit(parg.expression, scope))

                passed_args = passed_args[len(args):]
                declared_kw_arguments = []

                for i, pkw_arg in enumerate(passed_args):
                    kw_arg = kw_args[i]

                    if isinstance(pkw_arg, ArgumentNode):
                        scope.assign(kw_arg.name, self.visit(pkw_arg.expression, scope))
                        declared_kw_arguments.append(kw_arg.name)
                    elif isinstance(pkw_arg, KeywordArgumentNode):
                        if pkw_arg.name in declared_kw_arguments:
                            raise Exception(f"Already declared argument: {pkw_arg.name}")

                        scope.assign(pkw_arg.name, self.visit(pkw_arg.expression, scope))
                        declared_kw_arguments.append(pkw_arg.name)

                for kw_arg in [kw for kw in kw_args if kw.name not in declared_kw_arguments]:
                    scope.assign(kw_arg.name, self.visit(kw_arg.expression, scope))
                
                if isinstance(identifier, Class):
                    instance = Instance(scope, identifier.name)
                else:
                    instance = None

                for e in identifier.expressions.expressions:
                    value = self.visit(e, scope)

                    if isinstance(e, ReturnNode):
                        try:
                            return value.copy()
                        except:
                            return value
                    
                    if isinstance(value, ReturnNode):
                        return value.expression

                return instance

            case n if isinstance(n, ReturnNode):
                return self.visit(n.expression, scope)

            case n if issubclass(type(n), DataTypeNode):
                match n:
                    case _ if isinstance(n, ArrayNode):
                        for i, v in enumerate(n.value):
                            n.value[i] = self.visit(v, scope)

                        return Array(scope.copy(), n.value)

                    case _ if isinstance(n, (FunctionNode, ClassNode)):
                        cast_type = Function if isinstance(n, FunctionNode) else Class
                        value = cast_type(scope.copy(), n.name, n.args, n.expressions)

                        if n.name != None:
                            scope.assign(n.name, value)

                        return value

                    case _ if isinstance(n, NullNode):
                        return NullNode(scope.copy())

                    case _:
                        cast_type = {
                            NumberNode: Number,
                            BoolNode: Bool,
                            StringNode: String
                        }[type(n)]

                        return cast_type(scope.copy(), n.value)

            case n if issubclass(type(n), BinaryOperationNode):
                left = self.visit(n.left, scope)
                right = self.visit(n.right, scope)

                match type(n):
                    case _ if isinstance(n, PoweringNode):
                        return left ** right

                    case _ if isinstance(n, MultiplicationNode):
                        return left * right
                    
                    case _ if isinstance(n, DivitionNode):
                        return left / right

                    case _ if isinstance(n, AdditionNode):
                        return left + right

                    case _ if isinstance(n, SubtractionNode):
                        return left - right

                    case _ if isinstance(n, LessThanNode):
                        return left < right

                    case _ if isinstance(n, LessEqualsNode):
                        return left <= right

                    case _ if isinstance(n, GreaterThanNode):
                        return left > right

                    case _ if isinstance(n, GreaterEqualsNode):
                        return left >= right

                    case _ if isinstance(n, CompareNode):
                        return left == right

                    case _ if isinstance(n, NotCompareNode):
                        return left != right

                    case _ if isinstance(n, AndNode):
                        return left and right

                    case _ if isinstance(n, OrNode):
                        return left or right

            case n if issubclass(type(n), UnaryOperationNode):
                right = self.visit(n.right, scope)

                match type(n):
                    case _ if isinstance(n, PositiveNode):
                        return right

                    case _ if isinstance(n, NegativeNode):
                        return -right

                    case _ if isinstance(n, NotNode):
                        return Bool(scope, not right.value)

                    case _ if isinstance(n, BitNotNode):
                        return ~right

            case n if isinstance(n, IfNode):
                if_condition = self.visit(n.if_condition, scope)

                if if_condition.value:
                    self.visit(n.if_expressions, scope)
                else:
                    elif_conditions = n.elif_conditions

                    for i, c in enumerate(elif_conditions):
                        condition = self.visit(c, scope)

                        if condition.value:
                            self.visit(n.elif_expressions[i], scope)
                            break
                    else:
                        if n.else_expressions != None:
                            self.visit(n.else_expressions, scope)

            case n if isinstance(n, ForNode):
                identifier = n.identifier
                iterable = self.visit(n.iterable, scope)
                scope = scope.copy()

                for x in iterable:
                    scope.assign(identifier, x)
                    value = self.visit(n.expressions, scope)

                    if isinstance(value, ContinueNode):
                        continue
                    elif isinstance(value, BreakNode):
                        break

            case n if isinstance(n, (ContinueNode, BreakNode, DataType)):
                return n

            case n if isinstance(n, BuiltInFunctionNode):
                return ReturnNode(n.expressions(scope))

            case n if isinstance(n, BuiltInClassNode):
                return n.expressions(scope)

            case n:
                raise Exception(f"Invalid node: {n}")

    def run(self):
        self.result = self.visit(self.tree, global_scope)