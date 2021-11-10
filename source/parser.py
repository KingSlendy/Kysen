from nodes import *
from tokens import TOKENS

BINARY_OPERATOR_NODES = {
    TOKENS.POW: PoweringNode,
    TOKENS.MULT: MultiplicationNode,
    TOKENS.DIV: DivitionNode,
    TOKENS.ADD: AdditionNode,
    TOKENS.SUBT: SubtractionNode,
    TOKENS.LESS: LessThanNode,
    TOKENS.LESSEQUALS: LessEqualsNode,
    TOKENS.GREATER: GreaterThanNode,
    TOKENS.GREATEREQUALS: GreaterEqualsNode,
    TOKENS.EQUALSEQUALS: CompareNode,
    TOKENS.NOTEQUALS: NotCompareNode,
    TOKENS.AND: AndNode,
    TOKENS.OR: OrNode
}

UNARY_OPERATOR_NODES = {
    TOKENS.ADD: PositiveNode,
    TOKENS.SUBT: NegativeNode,
    TOKENS.NOT: NotNode,
    TOKENS.BITNOT: BitNotNode
}

def binary_operator_priority(token):
    match token.type:
        case TOKENS.POW:
            return 7

        case TOKENS.MULT | TOKENS.DIV:
            return 6

        case TOKENS.ADD | TOKENS.SUBT:
            return 5

        case TOKENS.LESS | TOKENS.LESSEQUALS | TOKENS.GREATER | TOKENS.GREATEREQUALS:
            return 4

        case TOKENS.EQUALSEQUALS | TOKENS.NOTEQUALS:
            return 3

        case TOKENS.AND:
            return 2

        case TOKENS.OR:
            return 1

        case _:
            return -1

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = -1
        self.current = None
        self.tree = None
        self.advance()
        self.run()

    
    def advance(self):
        while True:
            self.position += 1
            self.current = self.tokens[self.position] if -1 < self.position < len(self.tokens) else None

            if self.current.type != TOKENS.WHITESPACE:
                break

    
    def peek(self, offset):
        pos = self.position
        times = 0

        while True:
            pos += 1 if offset > 0 else -1
            token = self.tokens[pos] if -1 < pos < len(self.tokens) else None

            if token.type == TOKENS.WHITESPACE:
                continue

            times += 1

            if times >= abs(offset):
                break

        return token


    def necessary_token_advance(self, type):
        if self.current.type != type:
            raise Exception(f"Expected '{type.value}'")

        self.advance()

    
    def necessary_keyword_advance(self, type, value):
        if not self.current.matches(type, value):
            raise Exception(f"Expected keyword '{value}'")

        self.advance()


    def ignore_token_advance(self, type):
        if self.current.type == type:
            self.advance()


    def parse_factor(self):
        token = self.current

        match token.type:
            case TOKENS.LPAREN:
                self.advance()
                expression = self.parse_primary_expression()
                self.necessary_token_advance(TOKENS.RPAREN)
                return expression

            case TOKENS.LBRACKET:
                self.advance()
                values = []

                while self.current.type != TOKENS.RBRACKET:
                    values.append(self.parse_primary_expression())
                    self.ignore_token_advance(TOKENS.COMMA)

                self.advance()
                node = self.parse_accessors(ArrayNode(values))

                if self.current.type == TOKENS.EQUALS:
                    self.advance()
                    expression = self.parse_primary_expression()
                    node = self.parse_assigners(node, expression)

                return node


            case TOKENS.KEYWORD:
                match token.value:
                    case "true" | "false":
                        self.advance()
                        return BoolNode(token.value)

                    case "null":
                        self.advance()
                        return NullNode()

                    case "if":
                        return self.parse_if_statement()

                    case "for":
                        return self.parse_for_statement()

                    case "continue":
                        self.advance()
                        return ContinueNode()
                    
                    case "break":
                        self.advance()
                        return BreakNode()

                    case "func":
                        return self.parse_function_statement()

                    case "return":
                        self.advance()
                        return ReturnNode(self.parse_primary_expression())

                    case "class":
                        return self.parse_class_statement()

                    case "static":
                        self.advance()
                        return StaticNode(self.parse_primary_expression())

                    case k:
                        raise Exception(f"Invalid keyword: '{k}'")

            case TOKENS.IDENTIFIER:
                name = token.value
                self.advance()
                node = VarAccessNode(name)

                match self.current.type:
                    case TOKENS.LBRACKET:
                        node = self.parse_accessors(node)

                    case TOKENS.LPAREN:
                        node = self.parse_function_access(node)

                    case TOKENS.DOT:
                        node = self.parse_property_access(node)

                if self.current.type == TOKENS.EQUALS:
                    self.advance()
                    expression = self.parse_primary_expression()
                    node = self.parse_assigners(node, expression)

                return node

            case t if t in (TOKENS.ADD, TOKENS.SUBT, TOKENS.NOT, TOKENS.BITNOT):
                self.advance()
                factor = self.parse_factor()
                operation_node = UNARY_OPERATOR_NODES[token.type]
                return operation_node(factor)

            case t if t in (TOKENS.INT, TOKENS.FLOAT):
                self.advance()
                return NumberNode(token.value)

            case TOKENS.STRING:
                self.advance()
                return StringNode(token.value)

            case _:
                raise Exception(f"Invalid token: '{token}'")


    def parse_accessors(self, node):
        accessors = []

        while self.current.type == TOKENS.LBRACKET:
            self.advance()
            accessors.append(self.parse_primary_expression())
            self.necessary_token_advance(TOKENS.RBRACKET)

        for a in accessors:
            node = AccessorNode(node, a)

        match self.current.type:
            case TOKENS.LPAREN:
                node = self.parse_function_access(node)
            
            case TOKENS.DOT:
                node = self.parse_property_access(node)

        return node

    
    def parse_function_access(self, node):
        args = []
        index = 0

        while self.current.type == TOKENS.LPAREN:
            self.advance()
            args.append([])
            self.parse_arguments(args[index], detect_optional = False)
            self.necessary_token_advance(TOKENS.RPAREN)
            index += 1

        for a in args:
            node = FunctionAccessNode(node, a)

        match self.current.type:
            case TOKENS.LBRACKET:
                node = self.parse_accessors(node)
            
            case TOKENS.DOT:
                node = self.parse_property_access(node)

        if self.current.type == TOKENS.EQUALS:
            self.advance()
            expression = self.parse_primary_expression()
            node = self.parse_assigners(node, expression)

        return node


    def parse_property_access(self, node):
        accessors = []

        while self.current.type == TOKENS.DOT:
            self.advance()
            accessors.append(self.parse_primary_expression())

        for a in accessors:
            node = PropertyAccessNode(node, a)

        match self.current.type:
            case TOKENS.LBRACKET:
                node = self.parse_accessors(node)
            
            case TOKENS.LPAREN:
                node = self.parse_function_access(node)
            
        return node


    def parse_assigners(self, node, value_expression):
        try:
            return AssignerNode(node.node, node.index_expression, value_expression)
        except:
            return VarAssignNode(node.name, value_expression)


    def parse_statement(self, first_advance = True, has_condition = True):
        condition = None

        if first_advance:
            self.advance()

        if has_condition:
            self.ignore_token_advance(TOKENS.LPAREN)
            condition = self.parse_primary_expression()
            self.ignore_token_advance(TOKENS.RPAREN)

        if self.current.type == TOKENS.LCURLY: # Fix this when just doing {}
            self.advance()
            expressions = self.parse_expressions()
            self.necessary_token_advance(TOKENS.RCURLY)
        else:
            expressions = self.parse_expressions(once = True)

        return (condition, expressions)


    def parse_if_statement(self):
        (if_condition, if_expressions) = self.parse_statement()
        (elif_conditions, elif_expressions) = ([], [])

        while self.current.matches(TOKENS.KEYWORD, "elif"):
            (condition, expressions) = self.parse_statement()
            elif_conditions.append(condition)
            elif_expressions.append(expressions)

        else_expressions = None

        if self.current.matches(TOKENS.KEYWORD, "else"):
            (_, else_expressions) = self.parse_statement(has_condition = False)

        return IfNode(if_condition, if_expressions, elif_conditions, elif_expressions, else_expressions)


    def parse_for_statement(self):
        self.advance()
        self.ignore_token_advance(TOKENS.LPAREN)
        identifier = self.parse_primary_expression()
        self.necessary_keyword_advance(TOKENS.KEYWORD, "in")
        iterable = self.parse_primary_expression()
        self.ignore_token_advance(TOKENS.RPAREN)

        (_, expressions) = self.parse_statement(first_advance = False, has_condition = False)
        return ForNode(identifier.name, iterable, expressions)


    def parse_function_statement(self):
        self.advance()
        name = None

        if self.current.type == TOKENS.IDENTIFIER:
            name = self.current.value
            self.advance()

        self.necessary_token_advance(TOKENS.LPAREN)
        args = []
        self.parse_arguments(args)
        (_, expressions) = self.parse_statement(has_condition = False)
        return FunctionNode(name, args, expressions)

    
    def parse_class_statement(self):
        self.advance()

        if self.current.type != TOKENS.IDENTIFIER:
            raise Exception("Expected identifier.")
            
        name = self.current.value
        self.advance()
        self.necessary_token_advance(TOKENS.LPAREN)
        args = []
        self.parse_arguments(args)
        (_, expressions) = self.parse_statement(has_condition = False)
        return ClassNode(name, args, expressions)


    def parse_arguments(self, args, detect_optional = True):
        has_optional = False

        while True:
            if self.current.type == TOKENS.RPAREN:
                break

            arg = self.parse_primary_expression()

            if isinstance(arg, VarAssignNode):
                node = KeywordArgumentNode(arg.name, arg.expression)
                has_optional = True
            else:
                if detect_optional and has_optional:
                    raise Exception("Keyword arguments must be at the end.")

                node = ArgumentNode(arg)

            args.append(node)

            if self.current.type not in (TOKENS.COMMA, TOKENS.RPAREN):
                raise Exception("Expected ',' or ')'.")

            if self.current.type == TOKENS.COMMA:
                self.advance()


    def parse_primary_expression(self, priority = 0):
        left = self.parse_factor()

        while (operator_priority := binary_operator_priority(self.current)) >= priority and operator_priority != -1:
            operator = self.current
            self.advance()
            right = self.parse_primary_expression(operator_priority)
            operation_node = BINARY_OPERATOR_NODES[operator.type]
            left = operation_node(left, right)

        return left


    def parse_expressions(self, once = False):
        expressions = []

        while True:
            if self.current.type == TOKENS.RCURLY or self.current.type == TOKENS.ENDOFFILE:
                break

            expressions.append(self.parse_primary_expression())

            if self.peek(-1).type != TOKENS.RCURLY:
                self.necessary_token_advance(TOKENS.SEMICOLON)

            if once:
                break

        return ExpressionsNode(expressions)


    def run(self):
        self.tree = self.parse_expressions()

        if self.current.type != TOKENS.ENDOFFILE:
            raise Exception("Invalid syntax.")