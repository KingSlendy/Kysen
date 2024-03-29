from exceptions import *
from nodes import *
from reporter import Position
from tokens import KEYWORDS, TOKENS

UNARY_OPERATOR_NODES = {
    TOKENS.ADD: PositiveNode,
    TOKENS.SUBT: NegativeNode,
    TOKENS.BITNOT: BitNotNode,
    TOKENS.NOT: NotNode
}

BINARY_OPERATOR_NODES = {
    TOKENS.POW: PoweringNode,
    TOKENS.MULT: MultiplicationNode,
    TOKENS.DIV: DivitionNode,
    TOKENS.FDIV: FlooringDivitionNode,
    TOKENS.MOD: ModNode,
    TOKENS.ADD: AdditionNode,
    TOKENS.SUBT: SubtractionNode,
    TOKENS.LSHIFT: LShiftNode,
    TOKENS.RSHIFT: RShiftNode,
    TOKENS.LESS: LessThanNode,
    TOKENS.LESSEQUALS: LessEqualsNode,
    TOKENS.GREATER: GreaterThanNode,
    TOKENS.GREATEREQUALS: GreaterEqualsNode,
    TOKENS.EQUALSEQUALS: EqualsEqualsNode,
    TOKENS.NOTEQUALS: NotEqualsNode,
    TOKENS.BITAND: BitAndNode,
    TOKENS.BITOR: BitOrNode,
    TOKENS.BITXOR: BitXorNode,
    TOKENS.AND: AndNode,
    TOKENS.OR: OrNode
}

def binary_operator_priority(token):
    match token.type:
        case TOKENS.POW:
            return 11

        case TOKENS.MULT | TOKENS.DIV | TOKENS.FDIV | TOKENS.MOD:
            return 10

        case TOKENS.ADD | TOKENS.SUBT:
            return 9

        case TOKENS.LSHIFT | TOKENS.RSHIFT:
            return 8

        case TOKENS.LESS | TOKENS.LESSEQUALS | TOKENS.GREATER | TOKENS.GREATEREQUALS:
            return 7

        case TOKENS.EQUALSEQUALS | TOKENS.NOTEQUALS:
            return 6
        
        case TOKENS.BITAND:
            return 5

        case TOKENS.BITOR:
            return 4

        case TOKENS.BITXOR:
            return 3

        case TOKENS.AND:
            return 2

        case TOKENS.OR:
            return 1

        case _:
            return -1

class Parser:
    def __init__(self, tokens):
        from runner import reporter

        self.tokens = tokens
        self.reporter = reporter
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

    
    def token_advance(self):
        token = self.current
        self.advance()
        return token


    def necessary_token_check(self, type):
        if self.current.type != type:
            pos = self.peek(-1).pos
            pos.start = pos.end + 1
            pos.end = pos.start
            self.reporter.pos = pos
            self.reporter.report(KSSyntaxException(f"expected '{type.value}'."), syntax = True)
        else:
            return self.current


    def necessary_token_advance(self, type):
        token = self.necessary_token_check(type)
        self.advance()
        return token

    
    def necessary_keyword_advance(self, keyword):
        if self.current.value != keyword:
            pos = self.peek(-1).pos
            pos.start = pos.end + 1
            pos.end = pos.start
            self.reporter.pos = pos
            self.reporter.report(KSSyntaxException(f"expected '{keyword.value}'."), syntax = True)

        self.advance()


    def ignore_token_advance(self, type):
        if self.current.type == type:
            self.advance()


    def parse_factor(self):
        match self.current.type:
            case TOKENS.LPAREN:
                self.advance()
                expression = self.parse_binary_expression()
                self.necessary_token_advance(TOKENS.RPAREN)
                return expression

            case TOKENS.LBRACKET:
                token = self.token_advance()
                values = []

                while self.current.type != TOKENS.RBRACKET:
                    values.append(self.parse_binary_expression())
                    self.ignore_token_advance(TOKENS.COMMA)

                self.advance()
                node = self.parse_bracket_access(ArrayNode(values).set_pos(Position(token.pos.line, token.pos.start, self.current.pos.end)))

                if self.current.type == TOKENS.EQUALS:
                    self.advance()
                    expression = self.parse_binary_expression()
                    node = self.parse_assigners(node, expression)

                return node

            case TOKENS.LCURLY:
                self.advance()

                if self.current.value in (KEYWORDS.ASSIGN, KEYWORDS.ACCESS):
                    return self.parse_attribute_expression()

            case TOKENS.LESS:
                token = self.token_advance()
                name = self.necessary_token_advance(TOKENS.IDENTIFIER).value
                self.necessary_token_advance(TOKENS.GREATER)
                value = self.parse_factor()
                return CastNode(name, value).set_pos(Position(token.pos.line, token.pos.start, self.current.pos.end))

            case TOKENS.KEYWORD:
                match self.current.value:
                    case KEYWORDS.TRUE | KEYWORDS.FALSE:
                        token = self.token_advance()
                        return BOOL_NODES[0 if token.value.value == "false" else 1].set_pos(token.pos)

                    case KEYWORDS.NULL:
                        self.advance()
                        return NULL_NODE

                    case KEYWORDS.IF:
                        return self.parse_if_statement()

                    case KEYWORDS.FOR:
                        return self.parse_for_statement()

                    case KEYWORDS.WHILE:
                        return self.parse_while_statement()

                    case KEYWORDS.CONTINUE:
                        token = self.token_advance()
                        return CONTINUE_NODE.set_pos(Position(token.pos.line, token.pos.start, self.current.pos.end))
                    
                    case KEYWORDS.BREAK:
                        token = self.token_advance()
                        expression = NUMBER_NODES[1 + 255]

                        if self.current.type != TOKENS.SEMICOLON:
                            expression = self.parse_binary_expression()

                        return BreakNode(expression).set_pos(Position(token.pos.line, token.pos.start, self.current.pos.end))

                    case KEYWORDS.FUNC:
                        return self.parse_function_statement()

                    case KEYWORDS.RETURN:
                        token = self.token_advance()
                        expression = None

                        if self.current.type != TOKENS.SEMICOLON:
                            expression = self.parse_binary_expression()

                        return ReturnNode(expression).set_pos(Position(token.pos.line, token.pos.start, self.current.pos.end))

                    case KEYWORDS.CLASS:
                        return self.parse_class_statement()

                    case KEYWORDS.STATIC:
                        token = self.token_advance()
                        return StaticNode(self.parse_binary_expression()).set_pos(Position(token.pos.line, token.pos.start, self.current.pos.end))

                    case KEYWORDS.NEW:
                        token = self.token_advance()
                        self.necessary_token_check(TOKENS.IDENTIFIER)
                        factor = self.parse_factor()
                        return ClassAccessNode(factor.node, factor.args).set_pos(Position(token.pos.line, token.pos.start, self.current.pos.end))

                    case KEYWORDS.CAST:
                        token = self.current
                        func = self.parse_function_statement(special = True)
                        return SpecialFunctionNode(func).set_pos(Position(token.pos.line, token.pos.start, self.current.pos.end))

                    case k:
                        raise Exception(f"Invalid keyword: '{k}'")

            case TOKENS.IDENTIFIER:
                token = self.current
                name = self.necessary_token_advance(TOKENS.IDENTIFIER).value
                node = VarAccessNode(name).set_pos(Position(token.pos.line, token.pos.start, self.current.pos.end))

                match self.current.type:
                    case TOKENS.LBRACKET:
                        node = self.parse_bracket_access(node)

                    case TOKENS.LPAREN:
                        node = self.parse_function_access(node)

                    case TOKENS.DOT:
                        node = self.parse_property_access(node)

                if self.current.type in (TOKENS.EQUALS, TOKENS.ASSIGNMENT):
                    operation_node = None

                    if self.current.type == TOKENS.ASSIGNMENT:
                        operation_node = BINARY_OPERATOR_NODES[self.current.value]

                    self.advance()
                    expression = self.parse_binary_expression()
                    node = self.parse_assigners(node, expression, assignment_node = operation_node)

                return node

            case t if t in (TOKENS.ADD, TOKENS.SUBT, TOKENS.NOT, TOKENS.BITNOT):
                token = self.token_advance()
                factor = self.parse_factor()
                operation_node = UNARY_OPERATOR_NODES[token.type]
                return operation_node(factor).set_pos(Position(token.pos.line, token.pos.start, self.current.pos.end))

            case t if t in (TOKENS.INT, TOKENS.FLOAT):
                token = self.token_advance()
                as_float = float(token.value)

                if as_float.is_integer():
                    try:
                        return NUMBER_NODES[token.value]
                    except:
                        pass

                return NumberNode(token.value).set_pos(token.pos)

            case TOKENS.STRING:
                token = self.token_advance()
                return StringNode(token.value).set_pos(Position(token.pos.line, token.pos.start, self.current.pos.end))

            case _:
                self.reporter.pos = self.current.pos
                self.reporter.report(KSSyntaxException(f"unexpected syntax."), syntax = True)


    def parse_statement(self, first_advance = True, has_condition = True):
        condition = None

        if first_advance:
            self.advance()

        if has_condition:
            self.necessary_token_advance(TOKENS.LPAREN)
            condition = self.parse_binary_expression()
            self.necessary_token_advance(TOKENS.RPAREN)

        match self.current.type:
            case TOKENS.LCURLY:
                self.advance()
                expressions = self.parse_expressions()
                self.necessary_token_advance(TOKENS.RCURLY)

            case TOKENS.ARROW:
                token = self.token_advance()
                expressions = self.parse_expressions(once = True)
                expressions.expressions[0] = ReturnNode(expressions.expressions[0]).set_pos(Position(token.pos.line, token.pos.start, self.current.pos.end))
            
            case _:
                expressions = self.parse_expressions(once = True)

        return (condition, expressions)


    def parse_if_statement(self) -> IfNode:
        token = self.current
        if_clauses = []

        while self.current.value in (KEYWORDS.IF, KEYWORDS.ELIF):
            if_clauses.append(self.parse_statement())

        else_expressions = None

        if self.current.value == KEYWORDS.ELSE:
            (_, else_expressions) = self.parse_statement(has_condition = False)

        return IfNode(if_clauses, else_expressions).set_pos(Position(token.pos.line, token.pos.start, self.current.pos.end))


    def parse_for_statement(self) -> ForNode:
        token = self.token_advance()
        self.ignore_token_advance(TOKENS.LPAREN)
        self.necessary_token_check(TOKENS.IDENTIFIER)
        identifier = self.parse_factor()
        self.necessary_keyword_advance(KEYWORDS.IN)
        iterable = self.parse_factor()
        self.ignore_token_advance(TOKENS.RPAREN)

        (_, expressions) = self.parse_statement(first_advance = False, has_condition = False)
        return ForNode(identifier.name, iterable, expressions).set_pos(Position(token.pos.line, token.pos.start, self.current.pos.end))


    def parse_while_statement(self) -> WhileNode:
        token = self.current
        (condition, expressions) = self.parse_statement()
        return WhileNode(condition, expressions).set_pos(Position(token.pos.line, token.pos.start, self.current.pos.end))


    def parse_function_statement(self, special = False) -> FunctionNode:
        token = self.token_advance()
        name = None
        bound_name = None

        if not special:
            if self.current.type == TOKENS.IDENTIFIER:
                name = self.current.value
                self.advance()

            if self.current.type == TOKENS.DOT:
                self.advance()
                bound_name = name
                name = self.necessary_token_advance(TOKENS.IDENTIFIER).value
        else:
            name = self.token_advance()

        args = []
        self.parse_arguments(args)
        (_, expressions) = self.parse_statement(first_advance = False, has_condition = False)
        return FunctionNode(name, args, expressions, bound_name).set_pos(Position(token.pos.line, token.pos.start, self.current.pos.end))

    
    def parse_class_statement(self) -> ClassNode:
        token = self.token_advance()
        name = self.necessary_token_advance(TOKENS.IDENTIFIER).value
        args = []
        self.parse_arguments(args)
        inherit = None

        if self.current.type == TOKENS.COLON:
            self.advance()
            inherit_name = self.necessary_token_advance(TOKENS.IDENTIFIER)
            node = VarAccessNode(inherit_name.value).set_pos(self.current.pos)
            inherit = self.parse_function_access(node)
            inherit = ClassAccessNode(inherit.node, inherit.args).set_pos(inherit.pos)

        (_, expressions) = self.parse_statement(first_advance = False, has_condition = False)
        return ClassNode(name, args, expressions, inherit).set_pos(Position(token.pos.line, token.pos.start, self.current.pos.end))


    def parse_arguments(self, args, detect_optional = True):
        self.necessary_token_advance(TOKENS.LPAREN)
        has_optional = False

        while True:
            if self.current.type == TOKENS.RPAREN:
                break

            arg = self.parse_binary_expression()

            if isinstance(arg, VarAssignNode):
                node = KeywordArgumentNode(arg.name, arg.expression).set_pos(arg.pos)
                has_optional = True
            else:
                if detect_optional and has_optional:
                    self.reporter.pos = self.current.pos
                    self.reporter.report(KSArgumentException("keyword arguments must be at the end."), syntax = True)

                node = ArgumentNode(arg).set_pos(arg.pos)

            args.append(node)

            if self.current.type not in (TOKENS.COMMA, TOKENS.RPAREN):
                self.reporter.pos = self.current.pos
                self.reporter.report(KSSyntaxException("expected ',' or ')'."), syntax = True)

            if self.current.type == TOKENS.COMMA:
                self.advance()

        self.necessary_token_advance(TOKENS.RPAREN)


    def parse_attribute_expression(self) -> AttributeNode:
        token = self.current

        if self.current.value == KEYWORDS.ASSIGN:
            self.advance()
            (_, assign_expressions) = self.parse_statement(first_advance = False, has_condition = False)
            self.necessary_keyword_advance(KEYWORDS.ACCESS)
            (_, access_expressions) = self.parse_statement(first_advance = False, has_condition = False)
            self.necessary_token_advance(TOKENS.RCURLY)
        elif self.current.value == KEYWORDS.ACCESS:
            self.advance()
            (_, access_expressions) = self.parse_statement(first_advance = False, has_condition = False)
            self.necessary_keyword_advance(KEYWORDS.ASSIGN)
            (_, assign_expressions) = self.parse_statement(first_advance = False, has_condition = False)
            self.necessary_token_advance(TOKENS.RCURLY)
        else:
            self.reporter.pos = self.current.pos
            self.reporter.report(KSSyntaxException("expected keyword(s) 'assign', 'access'."), syntax = True)

        return AttributeNode(assign_expressions, access_expressions).set_pos(Position(token.pos.line, token.pos.start, self.current.pos.end))


    def parse_bracket_access(self, node) -> BracketAccessNode:
        token = self.current
        accessors = []

        while self.current.type == TOKENS.LBRACKET:
            self.advance()
            accessors.append(self.parse_binary_expression())
            self.necessary_token_advance(TOKENS.RBRACKET)

        for a in accessors:
            node = BracketAccessNode(node, a).set_pos(node.pos)

        match self.current.type:
            case TOKENS.LPAREN:
                node = self.parse_function_access(node)
            
            case TOKENS.DOT:
                node = self.parse_property_access(node)

        return node

    
    def parse_function_access(self, node) -> FunctionAccessNode:
        args = []
        index = 0

        if self.current.type != TOKENS.LPAREN:
            self.reporter.pos = self.current.pos
            self.reporter.report(KSSyntaxException("expected '('."), syntax = True)

        while self.current.type == TOKENS.LPAREN:
            args.append([])
            self.parse_arguments(args[index], detect_optional = False)
            index += 1

        for a in args:
            node = FunctionAccessNode(node, a).set_pos(node.pos)

        match self.current.type:
            case TOKENS.LBRACKET:
                node = self.parse_bracket_access(node)
            
            case TOKENS.DOT:
                node = self.parse_property_access(node)

        return node


    def parse_property_access(self, node) -> PropertyAccessNode:
        accessors = []

        while self.current.type == TOKENS.DOT:
            self.advance()
            self.necessary_token_check(TOKENS.IDENTIFIER)
            accessors.append(VarAccessNode(self.token_advance().value).set_pos(node.pos))

        for a in accessors:
            node = PropertyAccessNode(node, a).set_pos(node.pos)

        match self.current.type:
            case TOKENS.LBRACKET:
                node = self.parse_bracket_access(node)
            
            case TOKENS.LPAREN:
                node = self.parse_function_access(node)
            
        return node


    def parse_assigners(self, node, value_expression, assignment_node = None) -> Node:
        if assignment_node != None:
            value_expression = assignment_node(node, value_expression).set_pos(node.pos)

        match node:
            case n if type(n) == VarAccessNode:
                return VarAssignNode(node.name, value_expression).set_pos(node.pos)

            case n if type(n) == BracketAccessNode:
                return BracketAssignNode(node.node, node.index_expression, value_expression).set_pos(node.pos)

            case n if type(n) == PropertyAccessNode:
                return PropertyAssignNode(node.node, node.property, value_expression).set_pos(node.pos)


    def parse_binary_expression(self, priority = 0) -> Node:
        token = self.current
        left = self.parse_factor()

        while (operator_priority := binary_operator_priority(self.current)) > priority and operator_priority != -1:
            operator = self.token_advance()
            right = self.parse_binary_expression(operator_priority)
            operation_node = BINARY_OPERATOR_NODES[operator.type]
            left = operation_node(left, right).set_pos(Position(token.pos.line, token.pos.start, self.current.pos.end))

        if self.current.type == TOKENS.QUESTIONMARK:
            left = self.parse_ternary_expression(left)

        return left


    def parse_ternary_expression(self, node) -> TernaryNode:
        token = self.current
        self.advance()
        true_expression = self.parse_binary_expression()
        self.necessary_token_advance(TOKENS.COLON)
        false_expression = self.parse_binary_expression()
        return TernaryNode(node, true_expression, false_expression).set_pos(Position(token.pos.line, token.pos.start, self.current.pos.end))


    def parse_expressions(self, once = False):
        expressions = []

        while True:
            if self.current.type == TOKENS.RCURLY or self.current.type == TOKENS.ENDOFFILE:
                break

            expressions.append(self.parse_binary_expression())
        
            if self.peek(-1).type not in (TOKENS.SEMICOLON, TOKENS.RCURLY) and self.current.type != TOKENS.RPAREN:
                self.necessary_token_advance(TOKENS.SEMICOLON)

            if once:
                break

        return ExpressionsNode(expressions)


    def run(self):
        self.tree = self.parse_expressions()

        if self.current.type != TOKENS.ENDOFFILE:
            self.reporter.pos = self.current.pos
            self.reporter.report(KSSyntaxException(f"invalid syntax."), syntax = True)