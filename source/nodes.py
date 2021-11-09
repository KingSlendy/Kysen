class DataTypeNode:
    def __init__(self, value = None):
        self.value = value


    def __repr__(self):
        return f"{type(self).__name__}: {self.value}"


class NumberNode(DataTypeNode):
    def __init__(self, token):
        super().__init__(token)


class BoolNode(DataTypeNode):
    def __init__(self, value):
        super().__init__(value)


class StringNode(DataTypeNode):
    def __init__(self, value):
        super().__init__(value)


class ArrayNode(DataTypeNode):
    def __init__(self, value):
        super().__init__(value)


class FunctionNode(DataTypeNode):
    def __init__(self, name, args, expressions):
        self.name = name
        self.args = args
        self.expressions = expressions

    
    def __repr__(self):
        return f"Func {self.name if self.name != None else '<anonymous>'}({self.args}) {self.expressions}"


class ClassNode(DataTypeNode):
    def __init__(self, name, args, expressions):
        self.name = name
        self.args = args
        self.expressions = expressions


    def __repr__(self):
        return f"Class {self.name if self.name != None else '<anonymous>'}({self.args}) {self.expressions}"


class NullNode(DataTypeNode):
    pass


class VarAssignNode:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    
    def __repr__(self):
        return f"Identifier Assign: {self.name} = {self.expression}"


class VarAccessNode:
    def __init__(self, name):
        self.name = name


    def __repr__(self):
        return f"Identifier Access: {self.name}"


class AccessorNode:
    def __init__(self, node, index_expression):
        self.node = node
        self.index_expression = index_expression

    
    def __repr__(self):
        return f"Accessor: ({self.node}, {self.index_expression})"


class AssignerNode:
    def __init__(self, node, index_expression, value_expression = None):
        self.node = node
        self.index_expression = index_expression
        self.value_expression = value_expression

    
    def __repr__(self):
        if self.value_expression != None:
            return f"Assigner: ({self.node}, {self.index_expression}) = {self.value_expression}"
        else:
            return f"Assigner: ({self.node}, {self.index_expression})"


class FunctionAccessNode:
    def __init__(self, node, args):
        self.node = node
        self.args = args

    
    def __repr__(self):
        return f"FUNC ACCESS: {self.node}({self.args})"


class PropertyAccessNode:
    def __init__(self, node):
        self.node = node

    
    def __repr__(self):
        return f"PROPERY ACESS: {self.node}"


class PropertyAssignNode:
    def __init__(self, node, expression):
        self.node = node
        self.expression = expression

    
    def __repr__(self):
        return f"PROPERY ASSIGN: {self.node} = {self.expression}"


class ArgumentNode:
    def __init__(self, expression):
        self.expression = expression


    def __repr__(self):
        return f"ARGUMENT: {self.expression}"


class KeywordArgumentNode:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression


    def __repr__(self):
        return f"KEYWORD ARGUMENT: {self.name} = {self.expression}"


class ReturnNode:
    def __init__(self, expression):
        self.expression = expression


    def __repr__(self):
        return f"RETURN {self.expression}"


class BinaryOperationNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    
    def __repr__(self):
        return f"BINOP {type(self).__name__.replace('Node', '').upper()}: ({self.left}, {self.right})"


class PoweringNode(BinaryOperationNode):
    def __init__(self, left, right):
        super().__init__(left, right)


class MultiplicationNode(BinaryOperationNode):
    def __init__(self, left, right):
        super().__init__(left, right)


class DivitionNode(BinaryOperationNode):
    def __init__(self, left, right):
        super().__init__(left, right)


class AdditionNode(BinaryOperationNode):
    def __init__(self, left, right):
        super().__init__(left, right)


class SubtractionNode(BinaryOperationNode):
    def __init__(self, left, right):
        super().__init__(left, right)


class CompareNode(BinaryOperationNode):
    def __init__(self, left, right):
        super().__init__(left, right)


class NotCompareNode(BinaryOperationNode):
    def __init__(self, left, right):
        super().__init__(left, right)


class LessThanNode(BinaryOperationNode):
    def __init__(self, left, right):
        super().__init__(left, right)

    
class LessEqualsNode(BinaryOperationNode):
    def __init__(self, left, right):
        super().__init__(left, right)


class GreaterThanNode(BinaryOperationNode):
    def __init__(self, left, right):
        super().__init__(left, right)

    
class GreaterEqualsNode(BinaryOperationNode):
    def __init__(self, left, right):
        super().__init__(left, right)


class AndNode(BinaryOperationNode):
    def __init__(self, left, right):
        super().__init__(left, right)


class OrNode(BinaryOperationNode):
    def __init__(self, left, right):
        super().__init__(left, right)


class UnaryOperationNode:
    def __init__(self, right):
        self.right = right


class PositiveNode(UnaryOperationNode):
    def __init__(self, right):
        super().__init__(right)


class NegativeNode(UnaryOperationNode):
    def __init__(self, right):
        super().__init__(right)


class NotNode(UnaryOperationNode):
    def __init__(self, right):
        super().__init__(right)


class BitNotNode(UnaryOperationNode):
    def __init__(self, right):
        super().__init__(right)


class IfNode:
    def __init__(self, if_condition, if_expressions, elif_conditions, elif_expressions, else_expressions):
        self.if_condition = if_condition
        self.if_expressions = if_expressions
        self.elif_conditions = elif_conditions
        self.elif_expressions = elif_expressions
        self.else_expressions = else_expressions


    def __repr__(self):
        return f"if ({self.if_condition}) {self.if_expressions} elifs {self.elif_conditions} {self.elif_expressions} else {self.else_expressions}"


class ForNode:
    def __init__(self, identifier, iterable, expressions):
        self.identifier = identifier
        self.iterable = iterable
        self.expressions = expressions


    def __repr__(self):
        return f"for ({self.identifier} in {self.iterable}) {self.expressions}"


class ContinueNode:
    def __repr__(self):
        return f"CONTINUE"


class BreakNode:
    def __repr__(self):
        return f"BREAK"


class BuiltInFunctionNode:
    def __init__(self, expression):
        self.expressions = expression


    def __repr__(self):
        return f"BUILTIN FUNC: {self.expression}"


class BuiltInClassNode:
    def __init__(self, expressions):
        self.expressions = expressions


    def __repr__(self):
        return f"BUILTIN CLASS: {self.expressions}"


class ExpressionsNode:
    def __init__(self, expressions):
        self.expressions = expressions


    def __repr__(self):
        return f"EXPRS: ({self.expressions})"