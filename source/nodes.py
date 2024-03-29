from copy import deepcopy

class Node:
    def __init__(self):
        self.pos = None


    def set_pos(self, pos):
        self.pos = pos
        return self


    def copy(self):
        return deepcopy(self)


class DataTypeNode(Node):
    def __init__(self, value = None):
        super().__init__()
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
        super().__init__()
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
    def __init__(self):
        super().__init__()


class VarAccessNode(Node):
    def __init__(self, name):
        super().__init__()
        self.name = name


    def __repr__(self):
        return f"VAR ACCESS: {self.name}"


class VarAssignNode(VarAccessNode):
    def __init__(self, name, expression):
        super().__init__(name)
        self.expression = expression

    
    def __repr__(self):
        return f"VAR ASSIGN: {self.name} = {self.expression}"


class BracketAccessNode(Node):
    def __init__(self, node, index_expression):
        super().__init__()
        self.node = node
        self.index_expression = index_expression

    
    def __repr__(self):
        return f"BRACKET ACCESS: ({self.node}, {self.index_expression})"


class BracketAssignNode(BracketAccessNode):
    def __init__(self, node, index_expression, value_expression):
        super().__init__(node, index_expression)
        self.value_expression = value_expression

    
    def __repr__(self):
        return f"BRACKET ASSIGN: ({self.node}, {self.index_expression}) = {self.value_expression}"


class FunctionAccessNode(Node):
    def __init__(self, node, args):
        super().__init__()
        self.node = node
        self.args = args

    
    def __repr__(self):
        return f"FUNC ACCESS: {self.node}({self.args})"


class ClassAccessNode(FunctionAccessNode):
    def __init__(self, node, args):
        super().__init__(node, args)

    
    def __repr__(self):
        return f"CLASS ACCESS: {self.node}({self.args})"


class PropertyAccessNode(Node):
    def __init__(self, node, property):
        super().__init__()
        self.node = node
        self.property = property

    
    def __repr__(self):
        return f"PROPERTY ACCESS: ({self.node}, {self.property})"


class PropertyAssignNode(PropertyAccessNode):
    def __init__(self, node, property, value_expression):
        super().__init__(node, property)
        self.value_expression = value_expression

    
    def __repr__(self):
        return f"PROPERTY ASSIGN: ({self.node}, {self.property}) = {self.value_expression}"


class ArgumentNode(Node):
    def __init__(self, expression):
        super().__init__()
        self.expression = expression


    def __repr__(self):
        return f"ARGUMENT: {self.expression}"


class KeywordArgumentNode(Node):
    def __init__(self, name, expression):
        super().__init__()
        self.name = name
        self.expression = expression


    def __repr__(self):
        return f"KEYWORD ARGUMENT: {self.name} = {self.expression}"


class AttributeNode(DataTypeNode):
    def __init__(self, assign_expressions, access_expressions):
        super().__init__()
        self.assign_expressions = assign_expressions
        self.access_expressions = access_expressions


    def __repr__(self):
        return f"ATTRIBUTE: {{ ASSIGN = {self.assign_expressions} ACCESS = {self.access_expressions} }}"


class CastNode(Node):
    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.value = value


    def __repr__(self):
        return f"CAST: {self.name} => {self.identifier}"


class ReturnNode(Node):
    def __init__(self, expression):
        super().__init__()
        self.expression = expression


    def __repr__(self):
        return f"RETURN {self.expression}"


class UnaryOperationNode(Node):
    def __init__(self, right):
        super().__init__()
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


class BinaryOperationNode(Node):
    def __init__(self, left, right, assignment = False):
        super().__init__()
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


class FlooringDivitionNode(BinaryOperationNode):
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


class IfNode(Node):
    def __init__(self, if_clauses, else_expressions):
        super().__init__()
        self.if_clauses = if_clauses
        self.else_expressions = else_expressions


    def __repr__(self):
        return f"IFS {self.if_clauses} ELSE {self.else_expressions}"


class TernaryNode(Node):
    def __init__(self, condition, true_expression, false_expression):
        super().__init__()
        self.condition = condition
        self.true_expression = true_expression
        self.false_expression = false_expression


    def __repr__(self):
        return f"TERNARY: {self.condition} ? {self.true_expression} : {self.false_expression}"


class ForNode(Node):
    def __init__(self, identifier, iterable, expressions):
        super().__init__()
        self.identifier = identifier
        self.iterable = iterable
        self.expressions = expressions


    def __repr__(self):
        return f"FOR ({self.identifier} in {self.iterable}) {self.expressions}"


class WhileNode(Node):
    def __init__(self, condition, expressions):
        super().__init__()
        self.condition = condition
        self.expressions = expressions


    def __repr__(self):
        return f"WHILE ({self.condition}) {self.expressions}"


class ContinueNode(Node):
    def __repr__(self):
        return f"CONTINUE"


class BreakNode(ReturnNode):
    def __init__(self, expression):
        super().__init__(expression)


    def __repr__(self):
        return f"BREAK {self.expression}"


class StaticNode(Node):
    def __init__(self, node):
        super().__init__()
        self.node = node


    def __repr__(self):
        return f"STATIC: {self.node}"


class SpecialFunctionNode(Node):
    def __init__(self, func):
        super().__init__()
        self.func = func

    
    def __repr__(self):
        return f"SPECIAL FUNC: {self.func}"


class BuiltInFunctionNode(Node):
    def __init__(self, expressions):
        super().__init__()
        self.expressions = expressions


    def __repr__(self):
        return f"BUILTIN FUNC: {self.expressions}"


class BuiltInClassNode(Node):
    def __init__(self, expressions):
        super().__init__()
        self.expressions = expressions


    def __repr__(self):
        return f"BUILTIN CLASS: {self.expressions}"


class ExpressionsNode(Node):
    def __init__(self, expressions):
        super().__init__()
        self.expressions = expressions


    def insert(self, index, value):
        self.expressions.insert(index, value)


    def __getitem__(self, index):
        if index < len(self.expressions):
            return self.expressions[index]
        
        return None


    def __delitem__(self, index):
        del self.expressions[index]


    def __iter__(self):
        yield from self.expressions


    def __repr__(self):
        return f"EXPRS: ({self.expressions})"


NUMBER_NODES = {n: NumberNode(n) for n in range(-255, 256)}
BOOL_NODES = [BoolNode(False), BoolNode(True)]
NULL_NODE = NullNode()

CONTINUE_NODE = ContinueNode()