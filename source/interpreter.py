from datatypes import *
from nodes import *
from scope import Scope

global_scope = Scope()

# Global
BuiltIn.func_assign(global_scope, "Range", ["start"], [("finish", NULL_TYPE), ("step", NumberCache(1))], BuiltIn.Func_Range)
BuiltIn.func_assign(global_scope, "Timer", [], [], BuiltIn.Func_Timer)

# Console
BuiltIn.class_assign(global_scope, "Console", [], [], BuiltIn.Class_Console)
BuiltIn.static_assign(global_scope, "Console", "Print", ["value"], [], BuiltIn.Class_Console_Func_Print)


last_scope = None

class Interpreter:
    def __init__(self, tree, runtime):
        self.tree = tree
        self.runtime = runtime
        self.result = None
        self.run()

    
    def visit(self, context, scope, node):
        global last_scope

        match node:
            case n if isinstance(n, ExpressionsNode):
                results = []

                for e in n.expressions:
                    value = self.visit(context, scope, e)

                    if isinstance(value, (ReturnNode, ContinueNode, BreakNode)):
                        return value

                    results.append(value)

                if len(results) == 1:
                    result = results[0]

                    if isinstance(result, DataType) and not isinstance(result, Null):
                        return result

                return None

            case n if isinstance(n, VarAssignNode):
                old_scope = scope

                if last_scope != None:
                    old_scope = last_scope
                    last_scope = None

                value = self.visit(context, old_scope, n.expression)

                if not issubclass(type(value), DataType):
                    raise Exception(f"Cannot assign a non-type value to variable '{n.name}'.")

                if n.name in scope:
                    attribute = scope.access(n.name)

                    if isinstance(attribute, Attribute):
                        last_value = None

                        if "value" in scope:
                            last_value = scope.access("value")

                        scope.assign("value", value)
                        value = self.visit(context, scope, attribute.assign_expressions)

                        if last_value != None:
                            scope.assign("value", last_value)
                        else:
                            scope.remove("value")

                        return value

                return scope.assign(n.name, value)

            case n if isinstance(n, VarAccessNode):
                try:
                    value = scope.access(n.name)

                    if isinstance(value, Attribute):
                        attribute = value
                        value = self.visit(context, scope, attribute.access_expressions)

                        if not isinstance(value, ReturnNode):
                            raise Exception("There's no return inside attribute access.")
                        
                        value = self.visit(context, scope, value.expression)

                    return value
                except Exception as ex:
                    if context != None:
                        raise Exception(f"{'Instance of type ' if context['instance'] else 'Class '}'{context['name']}' has no property or function '{n.name}'.")
                    else:
                        raise ex

            case n if isinstance(n, AccessorNode):
                context = None
                identifier = self.visit(context, scope, n.node)

                if last_scope != None:
                    scope = last_scope
                    last_scope = None

                if identifier == None:
                    raise Exception(f"Cannot use accessor for null.")

                index_expression = self.visit(context, scope, n.index_expression)
                return identifier[index_expression]

            case n if isinstance(n, AssignerNode):
                identifier = self.visit(context, scope, n.node)
                index_expression = self.visit(context, scope, n.index_expression)
                value_expression = self.visit(context, scope, n.value_expression)
                identifier[index_expression] = value_expression
                return identifier[index_expression]

            case n if isinstance(n, FunctionAccessNode):
                identifier = self.visit(context, scope, n.node)
                context = None
                old_scope = scope

                if last_scope != None:
                    old_scope = last_scope
                    last_scope = None

                if not isinstance(identifier, (Function, Class)):
                    raise Exception(f"Cannot instantiate or call a value of type '{type(identifier).__name__}'.")

                if isinstance(identifier, Class) and identifier.static:
                    raise Exception(f"Cannot instance the static class '{identifier.name}'.")

                args = [x for x in identifier.args if isinstance(x, ArgumentNode)]
                kw_args = [x for x in identifier.args if isinstance(x, KeywordArgumentNode)]
                passed_args = n.args
                arg_number = len(args) + len(kw_args)
                passed_arg_number = len(passed_args)

                if passed_arg_number < len(args):
                    raise Exception(f"Expected {len(args)} positional argument(s), got {passed_arg_number}.")
                elif passed_arg_number > arg_number:
                    raise Exception(f"Expected {arg_number} total argument(s), got {passed_arg_number}.")

                if isinstance(identifier, Class):
                    instance = Instance(scope.copy(), identifier.name)
                    scope = instance.scope
                else:
                    instance = None
                    scope = identifier.scope.copy()

                for i, arg in enumerate(args):
                    parg = passed_args[i]

                    if isinstance(parg, KeywordArgumentNode):
                        raise Exception(f"Expected positional argument: '{arg.expression.name}'.")

                    scope.assign(arg.expression.name, self.visit(context, old_scope, parg.expression))

                passed_args = passed_args[len(args):]
                declared_kw_arguments = []

                for i, pkw_arg in enumerate(passed_args):
                    kw_arg = kw_args[i]

                    if isinstance(pkw_arg, ArgumentNode):
                        scope.assign(kw_arg.name, self.visit(context, old_scope, pkw_arg.expression))
                        declared_kw_arguments.append(kw_arg.name)
                    elif isinstance(pkw_arg, KeywordArgumentNode):
                        if pkw_arg.name in declared_kw_arguments:
                            raise Exception(f"Already declared argument: {pkw_arg.name}")

                        scope.assign(pkw_arg.name, self.visit(context, old_scope, pkw_arg.expression))
                        declared_kw_arguments.append(pkw_arg.name)

                for kw_arg in [kw for kw in kw_args if kw.name not in declared_kw_arguments]:
                    scope.assign(kw_arg.name, self.visit(context, old_scope, kw_arg.expression))  

                value = self.visit(context, scope, identifier.expressions)

                if isinstance(value, ReturnNode):
                    if value.expression != None and not isinstance(value.expression, DataType):
                        value = self.visit(context, scope, value.expression)
                    else:
                        value = value.expression

                        if value is None:
                            value = NULL_TYPE
                    
                    return value.copy()

                return instance

            case n if isinstance(n, PropertyAccessNode):
                identifier = self.visit(context, scope, n.node)

                if not isinstance(identifier, (Class, Instance)):
                    raise Exception(f"Cannot check for properties in variable of type '{type(identifier).__name__}'.")

                if isinstance(n.property, VarAssignNode):
                    if scope != identifier.scope and not n.property.name in identifier.scope:
                        raise Exception(f"Cannot assign uninitialized property '{n.property.name}' for '{identifier.name}': '{n.node.name}'.")

                if last_scope == None:
                    last_scope = scope

                identifier.scope.look_back = False
                value = self.visit({"name": identifier.name, "instance": isinstance(identifier, Instance)}, identifier.scope, n.property)
                identifier.scope.look_back = True
                return value

            case n if issubclass(type(n), DataTypeNode):
                match n:
                    case _ if isinstance(n, ArrayNode):
                        for i, v in enumerate(n.value):
                            n.value[i] = self.visit(context, scope, v)

                        return Array(scope.copy(), n.value)

                    case _ if isinstance(n, (FunctionNode, ClassNode)):
                        if isinstance(n, FunctionNode):
                            object = Function(scope, n.name, n.args, n.expressions)
                        elif isinstance(n, ClassNode):
                            object = Class(scope.copy(), n.name, n.args, n.expressions)
                            statics = []

                            for i, e in enumerate(n.expressions.expressions):
                                if isinstance(e, StaticNode):
                                    self.visit(context, object.scope, e.node)
                                    statics.append(i)

                            statics.sort()
                            statics.reverse()

                            for s in statics:
                                del n.expressions.expressions[s]

                        if n.name != None:
                            scope.assign(n.name, object)

                        return object

                    case _ if isinstance(n, NullNode):
                        return NULL_TYPE

                    case _ if isinstance(n, AttributeNode):
                        value = Attribute(scope, n.assign_expressions, n.access_expressions)
                        return scope.assign(n.name, value)

                    case _:
                        cast_type = {
                            NumberNode: NumberCache,
                            BoolNode: BoolCache,
                            StringNode: String
                        }[type(n)]

                        return cast_type(n.value)

            case n if issubclass(type(n), BinaryOperationNode):
                if n.assignment:
                    scope.assign(n.left.name, self.visit(context, scope, type(n)(n.left, n.right)))
                    return None

                left = self.visit(context, scope, n.left)
                right = self.visit(context, scope, n.right)

                match type(n):
                    case _ if isinstance(n, PoweringNode):
                        return left ** right

                    case _ if isinstance(n, MultiplicationNode):
                        return left * right
                    
                    case _ if isinstance(n, DivitionNode):
                        return left / right

                    case _ if isinstance(n, ModNode):
                        return left % right

                    case _ if isinstance(n, AdditionNode):
                        return left + right

                    case _ if isinstance(n, SubtractionNode):
                        return left - right

                    case _ if isinstance(n, LShiftNode):
                        return left << right

                    case _ if isinstance(n, RShiftNode):
                        return left >> right

                    case _ if isinstance(n, LessThanNode):
                        return left < right

                    case _ if isinstance(n, LessEqualsNode):
                        return left <= right

                    case _ if isinstance(n, GreaterThanNode):
                        return left > right

                    case _ if isinstance(n, GreaterEqualsNode):
                        return left >= right

                    case _ if isinstance(n, EqualsEqualsNode):
                        return left == right

                    case _ if isinstance(n, NotEqualsNode):
                        return left != right

                    case _ if isinstance(n, BitAndNode):
                        return left & right

                    case _ if isinstance(n, BitOrNode):
                        return left | right

                    case _ if isinstance(n, BitXorNode):
                        return left ^ right

                    case _ if isinstance(n, AndNode):
                        if (isinstance(left, Bool) and left.value) and (isinstance(right, Bool) and right.value):
                            return BoolCache(True)

                        return BoolCache(False)

                    case _ if isinstance(n, OrNode):
                        if (isinstance(left, Bool) and left.value) or (isinstance(right, Bool) and right.value):
                            return BoolCache(True)

                        return BoolCache(False)

            case n if issubclass(type(n), UnaryOperationNode):
                right = self.visit(context, scope, n.right)

                match type(n):
                    case _ if isinstance(n, PositiveNode):
                        return right

                    case _ if isinstance(n, NegativeNode):
                        return -right

                    case _ if isinstance(n, NotNode):
                        return BoolCache(not right.value)

                    case _ if isinstance(n, BitNotNode):
                        return ~right

            case n if isinstance(n, IfNode):
                for c, e in n.if_clauses:
                    condition = self.visit(context, scope, c)

                    if condition.value:
                        return self.visit(context, scope, e)
                else:
                    if n.else_expressions != None:
                        return self.visit(context, scope, n.else_expressions)

            case n if isinstance(n, ForNode):
                iterable = self.visit(context, scope, n.iterable)

                for x in iterable:
                    scope.assign(n.identifier, x)
                    value = self.visit(context, scope, n.expressions)

                    if isinstance(value, ReturnNode):
                        return value
                    elif isinstance(value, ContinueNode):
                        continue
                    elif isinstance(value, BreakNode):
                        break

            case n if isinstance(n, WhileNode):
                while True:
                    condition = self.visit(context, scope, n.condition)

                    if not condition.value:
                        break

                    value = self.visit(context, scope, n.expressions)

                    if isinstance(value, ReturnNode):
                        return value
                    elif isinstance(value, ContinueNode):
                        continue
                    elif isinstance(value, BreakNode):
                        break

            case n if isinstance(n, (ReturnNode, ContinueNode, BreakNode, DataType)):
                return n

            case n if isinstance(n, StaticNode):
                if not isinstance(n.node, ClassNode):
                    raise Exception("Cannot use 'static' outside of a class definition.")
                
                node = self.visit(context, scope, n.node)
                node.static = True

                for e in n.node.expressions.expressions:
                    if not isinstance(e, StaticNode):
                        raise Exception("Static classes can't have non-static properties.")

                return node

            case n if isinstance(n, BuiltInFunctionNode):
                return ReturnNode(n.expressions(scope))

            case n if isinstance(n, BuiltInClassNode):
                return n.expressions(scope)

            case n:
                raise Exception(f"Invalid node: {n}")

    def run(self):
        self.result = self.visit(None, global_scope, self.tree)