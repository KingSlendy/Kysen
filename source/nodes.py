class DataTypeNode:
    def __init__(self, value = None):
        self.value = value
        self.typed = False


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
    def __init__(self, name, args, expressions, bound):
        self.name = name
        self.args = args
        self.expressions = expressions
        self.bound = bound
        self.typed = False

    
    def __repr__(self):
        return f"FUNC {self.name if self.name != None else '<anonymous>'}({self.args}) {self.expressions}"


class ClassNode(FunctionNode):
    def __init__(self, name, args, expressions, inherit):
        super().__init__(name, args, expressions, None)
        self.inherit = inherit


    def __repr__(self):
        return f"CLASS {self.name if self.name != None else '<anonymous>'}({self.args}) {self.expressions}"


class NullNode(DataTypeNode):
    pass


class VarAssignNode:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    
    def __repr__(self):
        return f"VAR ASSIGN: {self.name} = {self.expression}"


class VarAccessNode:
    def __init__(self, name):
        self.name = name


    def __repr__(self):
        return f"VAR ACCESS: {self.name}"


class AttributeNode(DataTypeNode):
    def __init__(self, name, assign_expressions, access_expressions):
        self.name = name
        self.assign_expressions = assign_expressions
        self.access_expressions = access_expressions


    def __repr__(self):
        return f"ATTRIBUTE: {{ ASSIGN = {self.assign_expressions} ACCESS = {self.access_expressions} }}"


class AccessorNode:
    def __init__(self, node, index_expression):
        self.node = node
        self.index_expression = index_expression

    
    def __repr__(self):
        return f"ACCESSOR: ({self.node}, {self.index_expression})"


class AssignerNode:
    def __init__(self, node, index_expression, value_expression):
        self.node = node
        self.index_expression = index_expression
        self.value_expression = value_expression

    
    def __repr__(self):
        return f"ASSIGNER: ({self.node}, {self.index_expression}) = {self.value_expression}"


class FunctionAccessNode:
    def __init__(self, node, args):
        self.node = node
        self.args = args

    
    def __repr__(self):
        return f"FUNC ACCESS: {self.node}({self.args})"


class PropertyAccessNode:
    def __init__(self, node, property):
        self.node = node
        self.property = property

    
    def __repr__(self):
        return f"PROPERY ACCESS: ({self.node}, {self.property})"


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


class UnaryOperationNode:
    def __init__(self, right):
        self.right = right


class PositiveNode(UnaryOperationNode):
    def __init__(self, right):
        super().__init__(right)


class NegativeNode(UnaryOperationNode):
    def __init__(self, right):
        super().__init__(right)


class BitNotNode(UnaryOperationNode):
    def __init__(self, right):
        super().__init__(right)


class NotNode(UnaryOperationNode):
    def __init__(self, right):
        super().__init__(right)


class BinaryOperationNode:
    def __init__(self, left, right, assignment = False):
        self.left = left
        self.right = right
        self.assignment = assignment

    
    def __repr__(self):
        return f"BINOP {type(self).__name__.replace('Node', '').upper()}: ({self.left}, {self.right})"


class PoweringNode(BinaryOperationNode):
    def __init__(self, left, right, assignment = False):
        super().__init__(left, right, assignment)


class MultiplicationNode(BinaryOperationNode):
    def __init__(self, left, right, assignment = False):
        super().__init__(left, right, assignment)


class DivitionNode(BinaryOperationNode):
    def __init__(self, left, right, assignment = False):
        super().__init__(left, right, assignment)


class ModNode(BinaryOperationNode):
    def __init__(self, left, right, assignment = False):
        super().__init__(left, right, assignment)


class AdditionNode(BinaryOperationNode):
    def __init__(self, left, right, assignment = False):
        super().__init__(left, right, assignment)


class SubtractionNode(BinaryOperationNode):
    def __init__(self, left, right, assignment = False):
        super().__init__(left, right, assignment)


class LShiftNode(BinaryOperationNode):
    def __init__(self, left, right, assignment = False):
        super().__init__(left, right, assignment)


class RShiftNode(BinaryOperationNode):
    def __init__(self, left, right, assignment = False):
        super().__init__(left, right, assignment)


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


class EqualsEqualsNode(BinaryOperationNode):
    def __init__(self, left, right):
        super().__init__(left, right)


class NotEqualsNode(BinaryOperationNode):
    def __init__(self, left, right):
        super().__init__(left, right)


class BitAndNode(BinaryOperationNode):
    def __init__(self, left, right, assignment = False):
        super().__init__(left, right, assignment)


class BitOrNode(BinaryOperationNode):
    def __init__(self, left, right, assignment = False):
        super().__init__(left, right, assignment)


class BitXorNode(BinaryOperationNode):
    def __init__(self, left, right, assignment = False):
        super().__init__(left, right, assignment)


class AndNode(BinaryOperationNode):
    def __init__(self, left, right):
        super().__init__(left, right)


class OrNode(BinaryOperationNode):
    def __init__(self, left, right):
        super().__init__(left, right)


class IfNode:
    def __init__(self, if_clauses, else_expressions):
        self.if_clauses = if_clauses
        self.else_expressions = else_expressions


    def __repr__(self):
        return f"IF ({self.if_clauses[0]}) {self.if_clauses[1]} ELSE {self.else_expressions}"


class ForNode:
    def __init__(self, identifier, iterable, expressions):
        self.identifier = identifier
        self.iterable = iterable
        self.expressions = expressions


    def __repr__(self):
        return f"FOR ({self.identifier} in {self.iterable}) {self.expressions}"


class WhileNode:
    def __init__(self, condition, expressions):
        self.condition = condition
        self.expressions = expressions


    def __repr__(self):
        return f"WHILE ({self.condition}) {self.expressions}"


class ContinueNode:
    def __repr__(self):
        return f"CONTINUE"


class BreakNode:
    def __repr__(self):
        return f"BREAK"


class StaticNode:
    def __init__(self, node):
        self.node = node


    def __repr__(self):
        return f"STATIC: {self.node}"


class BuiltInFunctionNode:
    def __init__(self, expressions):
        self.expressions = expressions


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


    def insert(self, index, value):
        self.expressions.insert(index, value)


    def __getitem__(self, index):
        return self.value[index]


    def __setitem__(self, index, value):
        self.value[index] = value


    def __iter__(self):
        yield from self.expressions


    def __repr__(self):
        return f"EXPRS: ({self.expressions})"


NUMBER_NODES = [NumberNode(n) for n in range(-255, 256)]
BOOL_NODES = [BoolNode(False), BoolNode(True)]
NULL_NODE = NullNode()