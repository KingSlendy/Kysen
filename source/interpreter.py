from builtin import builtin_add_all
from datatypes import *
from exceptions import *
from nodes import *
from scope import Scope

global_scope = Scope()
builtin_add_all(global_scope)

last_scope = None

class Interpreter:
    def __init__(self, tree, runtime):
        self.tree = tree
        self.runtime = runtime
        self.result = None
        self.run()

    
    def visit(self, context, scope, node) -> Node:
        global last_scope

        match node:
            case n if type(n) == ExpressionsNode:
                declaration_expressions = ExpressionsNode([e for e in n.expressions if type(e) in (FunctionNode, ClassNode)])
                normal_expressions = ExpressionsNode([e for e in n.expressions if type(e) not in (FunctionNode, ClassNode)])

                for e in declaration_expressions:
                    self.visit(context, scope, e)

                results = []

                for e in normal_expressions:
                    value = self.visit(context, scope, e)

                    if type(value) in (ReturnNode, ContinueNode, BreakNode):
                        return value

                    results.append(value)

                return results

            case n if type(n) == VarAssignNode:
                old_scope = scope

                if last_scope != None:
                    old_scope = last_scope
                    last_scope = None

                value = self.visit(context, old_scope, n.expression)

                #if not issubclass(type(value), DataType):
                #    raise Exception(f"Cannot assign a non-Type value to variable '{n.name}'.")

                if n.name in scope:
                    attribute = scope.access(n.name, self, n.pos)

                    if type(attribute) == Attribute:
                        last_value = None

                        if "value" in scope:
                            last_value = scope.access("value", self, n.pos)

                        scope.assign("value", value)
                        value = self.visit(context, scope, attribute.assign_expressions)

                        if last_value != None:
                            scope.assign("value", last_value)
                        else:
                            scope.remove("value")

                        return value

                return scope.assign(n.name, value)

            case n if type(n) == VarAccessNode:
                value = scope.access(n.name, self, n.pos)

                if type(value) == Attribute:
                    attribute = value
                    value = self.visit(context, scope, attribute.access_expressions)

                    if type(value) != ReturnNode:
                        raise Exception("There's no return inside attribute access.")
                    
                    value = self.visit(context, scope, value.expression)

                return value

            case n if type(n) == AccessorNode:
                context = None
                identifier = self.visit(context, scope, n.node)

                if last_scope != None:
                    scope = last_scope
                    last_scope = None

                if identifier == None:
                    raise Exception(f"Cannot use accessor for null.")

                index_expression = self.visit(context, scope, n.index_expression)
                return identifier[index_expression]

            case n if type(n) == AssignerNode:
                identifier = self.visit(context, scope, n.node)
                index_expression = self.visit(context, scope, n.index_expression)
                value_expression = self.visit(context, scope, n.value_expression)
                identifier[index_expression] = value_expression
                return identifier[index_expression]

            case n if type(n) in (FunctionAccessNode, ClassAccessNode):
                identifier = self.visit(context, scope, n.node)
                old_scope = scope

                if last_scope != None:
                    old_scope = last_scope
                    last_scope = None

                if type(n) == FunctionAccessNode and type(identifier) != Function:
                    self.runtime.report(KSTypeException(f"'{type(identifier).__name__}' type is not callable."), n.pos)

                if type(n) == ClassAccessNode and type(identifier) != Class:
                    self.runtime.report(KSTypeException(f"'{type(identifier).__name__}' type cannot be instantiated."), n.pos)

                if type(identifier) == Class and identifier.static:
                    self.runtime.report(KSTypeException(f"cannot instantiate static class '{identifier.name}'."), n.pos)

                args = [x for x in identifier.args if type(x) == ArgumentNode]
                kw_args = [x for x in identifier.args if type(x) == KeywordArgumentNode]
                passed_args = n.args
                arg_number = len(args) + len(kw_args)
                passed_arg_number = len(passed_args)

                if passed_arg_number < len(args):
                    self.runtime.report(KSArgumentException(f"expected '{len(args)}' positional argument(s), got '{passed_arg_number}'."), n.pos)
                elif passed_arg_number > arg_number:
                    self.runtime.report(KSArgumentException(f"expected '{arg_number}' total argument(s), got '{passed_arg_number}'."), n.pos)

                if type(identifier) == Class:
                    scope = scope.copy()
                    instance = Instance(scope, identifier.name, identifier)
                else:
                    instance = None

                    if context == None or context.get("built-in") == None:
                        scope = identifier.scope.copy()
                    else:
                        scope = scope.copy()

                for i, arg in enumerate(args):
                    parg = passed_args[i]

                    if type(parg) == KeywordArgumentNode:
                        self.runtime.report(KSArgumentException(f"expected positional argument '{arg.expression.name}'."), n.pos)

                    scope.assign(arg.expression.name, self.visit(context, old_scope, parg.expression))

                passed_args = passed_args[len(args):]
                declared_kw_arguments = []

                for i, pkw_arg in enumerate(passed_args):
                    kw_arg = kw_args[i]

                    if type(pkw_arg) == ArgumentNode:
                        scope.assign(kw_arg.name, self.visit(context, old_scope, pkw_arg.expression))
                        declared_kw_arguments.append(kw_arg.name)
                    elif type(pkw_arg) == KeywordArgumentNode:
                        if pkw_arg.name in declared_kw_arguments:
                            self.runtime.report(KSArgumentException(f"already declared argument '{pkw_arg.name}'."), n.pos)

                        scope.assign(pkw_arg.name, self.visit(context, old_scope, pkw_arg.expression))
                        declared_kw_arguments.append(pkw_arg.name)

                for kw_arg in [kw for kw in kw_args if kw.name not in declared_kw_arguments]:
                    scope.assign(kw_arg.name, self.visit(context, old_scope, kw_arg.expression))  

                if instance != None:
                    # This instance inherits from another class.
                    if instance.parent.inherit != None:
                        base = self.visit(context, scope, instance.parent.inherit)
                        base.scope.transfer(scope)
                        scope.assign("base", base)

                if context == None:
                    self.runtime.push(self.runtime.place, n.pos)
                    self.runtime.place = identifier.name

                # Visit all the Function/Class expressions.
                value = self.visit({"instance": instance}, scope, identifier.expressions)

                if type(value) == ReturnNode:
                    if value.expression != None and type(value.expression) != DataType:
                        value = self.visit(context, scope, value.expression)
                    else:
                        value = value.expression

                        if value is None:
                            value = NULL_TYPE
                    
                    return value.copy()

                if context == None:
                    self.runtime.place = self.runtime.pop()
                
                context = None
                return instance if instance != None else NULL_TYPE

            case n if type(n) == PropertyAccessNode:
                identifier = self.visit(context, scope, n.node)

                #if type(identifier) not in (String, Array, Class, Instance):
                #    self.runtime.report(KSPropertyException(f"cannot check properties inside object of type '{identifier.name}'."), identifier.pos)

                if type(n.property) == VarAssignNode:
                    if scope != identifier.scope and not n.property.name in identifier.scope:
                        self.runtime.report(KSPropertyException(f"cannot assign uninitialized property '{n.property.name}' in '{identifier.name}'."), n.pos)

                check_property = n.property

                while type(check_property) not in (VarAssignNode, VarAccessNode, AttributeNode):
                    check_property = check_property.node

                if (n.node.name != "this" or type(check_property) == VarAccessNode) and check_property.name not in identifier.scope:
                    raise Exception(f"{'Instance of type ' if type(identifier) == Instance else 'Class '}'{identifier.name}' has no property '{check_property.name}'.")

                if last_scope == None:
                    last_scope = scope

                value = self.visit({"name": identifier.name, "instance": type(identifier) == Instance}, identifier.scope, n.property)
                return value

            case n if isinstance(n, DataTypeNode):
                match n:
                    case _ if type(n) == StringNode:
                        return String(scope.copy(), n.value).set_pos(n.pos)

                    case _ if type(n) == ArrayNode:
                        for i, v in enumerate(n.value):
                            n.value[i] = self.visit(context, scope, v)

                        return Array(scope.copy(), n.value).set_pos(n.pos)

                    case _ if type(n) in (FunctionNode, ClassNode):
                        object = None

                        if type(n) == FunctionNode:
                            if n.bound != None:
                                try:
                                    globals()[n.bound].bound.append(n)
                                except KeyError:
                                    bind = scope.access(n.bound, self, n.pos)
                                    bind.expressions.insert(0, n)

                                n.bound = None
                            else:
                                object = Function(scope, n.name, n.args, n.expressions).set_pos(n.pos)
                        elif type(n) == ClassNode:
                            object = Class(scope.copy(), n.name, n.args, n.expressions, n.inherit).set_pos(n.pos)
                            
                            if n.inherit != None:
                                parent = scope.access(n.inherit.node.name, self, n.pos)
                                parent.scope.transfer(object.scope)

                            statics = []

                            for i, e in enumerate(n.expressions):
                                if type(e) == StaticNode:
                                    self.visit(context, object.scope, e.node)

                                    if n.inherit != None:
                                        self.visit(context, parent.scope, e.node)

                                    statics.append(i)

                            statics.sort()
                            statics.reverse()

                            for s in statics:
                                del n.expressions[s]

                        if n.name != None and n.bound == None:
                            scope.assign(n.name, object)
                        else:
                            return object

                    case _ if type(n) == NullNode:
                        return NULL_TYPE

                    case _ if type(n) == AttributeNode:
                        value = Attribute(scope, n.assign_expressions, n.access_expressions).set_pos(n.pos)
                        return scope.assign(n.name, value)

                    case _:
                        cast_type = {
                            NumberNode: NumberCache,
                            BoolNode: BoolCache
                        }[type(n)]

                        return cast_type(n.value).set_pos(n.pos)

            case n if type(n) == CastNode:
                cast = scope.access(n.name, self, n.pos)

                if type(cast) != Class:
                    self.runtime.report(KSCastException(f"'{n.name}' must be a class."), n.pos)

                value = self.visit(context, scope, n.value)

                if not cast.name in value.specials:
                    self.runtime.report(KSCastException(f"cannot cast type '{value.name}' to type '{cast.name}'."), n.pos)

                if type(value) == Instance:
                    return BuiltIn.func_access(self, value.scope, value.specials.access(cast.name), [], [], n.pos)
                else:
                    return BuiltIn.func_access(self, scope, value.specials.access(cast.name), [value], [], n.pos)

            case n if isinstance(n, UnaryOperationNode):
                right = self.visit(context, scope, n.right)

                match n:
                    case _ if type(n) == PositiveNode:
                        return right

                    case _ if type(n) == NegativeNode:
                        return -right

                    case _ if type(n) == NotNode:
                        return BoolCache(not right.value)

                    case _ if type(n) == BitNotNode:
                        return ~right

            case n if isinstance(n, BinaryOperationNode):
                if n.assignment:
                    scope.assign(n.left.name, self.visit(context, scope, type(n)(n.left, n.right)))
                    return None

                left = self.visit(context, scope, n.left)
                right = self.visit(context, scope, n.right)

                match n:
                    case _ if type(n) == PoweringNode:
                        try:
                            return left ** right
                        except:
                            self.runtime.report(KSBinaryOperationException("**", type(left), type(right)), n.pos)

                    case _ if type(n) == MultiplicationNode:
                        try:
                            return left * right
                        except:
                            self.runtime.report(KSBinaryOperationException("*", type(left), type(right)), n.pos)
                    
                    case _ if type(n) == DivitionNode:
                        try:
                            return left / right
                        except:
                            self.runtime.report(KSBinaryOperationException("/", type(left), type(right)), n.pos)

                    case _ if type(n) == FlooringDivitionNode:
                        try:
                            return left // right
                        except:
                            self.runtime.report(KSBinaryOperationException("\\", type(left), type(right)), n.pos)

                    case _ if type(n) == ModNode:
                        try:
                            return left % right
                        except:
                            self.runtime.report(KSBinaryOperationException("%", type(left), type(right)), n.pos)

                    case _ if type(n) == AdditionNode:
                        try:
                            return left + right
                        except:
                            self.runtime.report(KSBinaryOperationException("+", type(left), type(right)), n.pos)

                    case _ if type(n) == SubtractionNode:
                        try:
                            return left - right
                        except:
                            self.runtime.report(KSBinaryOperationException("-", type(left), type(right)), n.pos)

                    case _ if type(n) == LShiftNode:
                        try:
                            return left << right
                        except:
                            self.runtime.report(KSBinaryOperationException("<<", type(left), type(right)), n.pos)

                    case _ if type(n) == RShiftNode:
                        try:
                            return left >> right
                        except:
                            self.runtime.report(KSBinaryOperationException(">>", type(left), type(right)), n.pos)

                    case _ if type(n) == LessThanNode:
                        return left < right

                    case _ if type(n) == LessEqualsNode:
                        return left <= right

                    case _ if type(n) == GreaterThanNode:
                        return left > right

                    case _ if type(n) == GreaterEqualsNode:
                        return left >= right

                    case _ if type(n) == EqualsEqualsNode:
                        return left == right

                    case _ if type(n) == NotEqualsNode:
                        return left != right

                    case _ if type(n) == BitAndNode:
                        try:
                            return left & right
                        except:
                            self.runtime.report(KSBinaryOperationException("&", type(left), type(right)), n.pos)

                    case _ if type(n) == BitOrNode:
                        try:
                            return left | right
                        except:
                            self.runtime.report(KSBinaryOperationException("|", type(left), type(right)), n.pos)

                    case _ if type(n) == BitXorNode:
                        try:
                            return left ^ right
                        except:
                            self.runtime.report(KSBinaryOperationException("^", type(left), type(right)), n.pos)

                    case _ if type(n) == AndNode:
                        if (type(left) == Bool and left.value) and (type(right) == Bool and right.value):
                            return BoolCache(True)

                        return BoolCache(False)

                    case _ if type(n) == OrNode:
                        if (type(left) == Bool and left.value) or (type(right) == Bool and right.value):
                            return BoolCache(True)

                        return BoolCache(False)

            case n if type(n) == IfNode:
                for c, e in n.if_clauses:
                    condition = self.visit(context, scope, c)

                    if condition.value:
                        return self.visit(context, scope, e)
                else:
                    if n.else_expressions != None:
                        return self.visit(context, scope, n.else_expressions)

            case n if type(n) == ForNode:
                iterable = self.visit(context, scope, n.iterable)

                for x in iterable:
                    if type(x) == str:
                        x = String(scope.copy(), x)

                    scope.assign(n.identifier, x)
                    value = self.visit(context, scope, n.expressions)

                    match value:
                        case _ if type(value) == ReturnNode:
                            return value

                        case _ if type(value) == ContinueNode:
                            continue

                        case _ if type(value) == BreakNode:
                            if value.expression.value > 1:
                                value.expression.value -= 1
                                return value
                            else:
                                break

            case n if type(n) == WhileNode:
                while True:
                    condition = self.visit(context, scope, n.condition)

                    if not condition.value:
                        break

                    value = self.visit(context, scope, n.expressions)

                    match value:
                        case _ if type(value) == ReturnNode:
                            return value

                        case _ if type(value) == ContinueNode:
                            continue

                        case _ if type(value) == BreakNode:
                            if value.expression.value > 1:
                                value.expression.value -= 1
                                return value
                            else:
                                break

            case n if type(n) in (ReturnNode, ContinueNode) or isinstance(n, DataType):
                return n

            case n if type(n) == BreakNode:
                value = self.visit(context, scope, n.expression)

                if type(value) != Number:
                    raise Exception("Cannot use non-Number expressions on 'break' statement.")

                value = Number(value.value)
                return BreakNode(value).set_pos(n.pos)

            case n if type(n) == StaticNode:
                if type(n.node) != ClassNode:
                    raise Exception("Cannot use 'static' outside of a class definition.")
                
                node = self.visit(context, scope, n.node)
                scope.access(n.node.name, self, n.pos).static = True

                for e in n.node.expressions:
                    if type(e) != StaticNode:
                        raise Exception("Static classes can't have non-Static properties.")

                return node

            case n if type(n) == SpecialFunctionNode:
                instance = context["instance"]
                n.func.name = n.func.name.value
                self.visit(context, instance.specials, n.func)

            case n if type(n) in (BuiltInFunctionNode, BuiltInClassNode):
                return ReturnNode(n.expressions(self, scope))

            case n:
                raise Exception(f"Invalid node: {type(n).__name__}")

    def run(self):
        global global_scope, last_scope

        if self.runtime.unittest:
            global_scope.clear()
            builtin_add_all(global_scope)
            last_scope = None

        self.result = self.visit(None, global_scope, self.tree)

        match self.result:
            case r if type(r) == ReturnNode:
                self.runtime.report(KSSyntaxException("cannot use 'return' statement outside of function context."), r.pos)

            case r if type(r) == ContinueNode:
                self.runtime.report(KSSyntaxException("cannot use 'continue' statement outside of loop context."), r.pos)

            case r if type(r) == BreakNode:
                self.runtime.report(KSSyntaxException("cannot use 'break' statement outside of loop context."), r.pos)
