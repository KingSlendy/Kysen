from errors import *
from nodes import *
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

        case TOKENS.MULT | TOKENS.DIV | TOKENS.MOD:
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
    def __init__(self, tokens, runtime):
        self.tokens = tokens
        self.runtime = runtime
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
            pos = self.peek(-1).pos
            pos.start = pos.end + 1
            pos.end = pos.start
            self.runtime.report(SyntaxError(f"expected '{type.value}'."), pos)

        self.advance()

    
    def necessary_keyword_advance(self, keyword):
        if not self.current.value == keyword:
            pos = self.peek(-1).pos
            pos.start = pos.end + 1
            pos.end = pos.start
            self.runtime.report(SyntaxError(f"expected '{keyword.value}'."), pos)

        self.advance()


    def ignore_token_advance(self, type):
        if self.current.type == type:
            self.advance()


    def parse_factor(self):
        token = self.current

        match token.type:
            case TOKENS.LPAREN:
                self.advance()
                expression = self.parse_binary_expression()
                self.necessary_token_advance(TOKENS.RPAREN)
                return expression

            case TOKENS.LBRACKET:
                self.advance()
                values = []

                while self.current.type != TOKENS.RBRACKET:
                    values.append(self.parse_binary_expression())
                    self.ignore_token_advance(TOKENS.COMMA)

                self.advance()
                node = self.parse_accessors(ArrayNode(values))

                if self.current.type == TOKENS.EQUALS:
                    self.advance()
                    expression = self.parse_binary_expression()
                    node = self.parse_assigners(node, expression)

                return node

            case TOKENS.KEYWORD:
                match token.value:
                    case KEYWORDS.TRUE | KEYWORDS.FALSE:
                        self.advance()
                        return BOOL_NODES[0 if token.value.value == "false" else 1]

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
                        self.advance()
                        return CONTINUE_NODE
                    
                    case KEYWORDS.BREAK:
                        self.advance()
                        return BREAK_NODE

                    case KEYWORDS.FUNC:
                        return self.parse_function_statement()

                    case KEYWORDS.RETURN:
                        self.advance()
                        return ReturnNode(self.parse_binary_expression())

                    case KEYWORDS.CLASS:
                        return self.parse_class_statement()

                    case KEYWORDS.STATIC:
                        self.advance()
                        return StaticNode(self.parse_binary_expression())

                    case k:
                        raise Exception(f"Invalid keyword: '{k}'")

            case TOKENS.IDENTIFIER:
                name = token.value
                self.advance()

                if self.current.type == TOKENS.FLOAT:
                    self.runtime.report(SyntaxError("expected identifier."), self.current.pos)

                node = VarAccessNode(name)

                match self.current.type:
                    case TOKENS.ASSIGNMENT:
                        operation_node = BINARY_OPERATOR_NODES[self.current.value]
                        self.advance()
                        right = self.parse_binary_expression()
                        return operation_node(node, right, assignment = True)

                    case TOKENS.LBRACKET:
                        node = self.parse_accessors(node)

                    case TOKENS.LPAREN:
                        node = self.parse_function_access(node)

                    case TOKENS.DOT:
                        node = self.parse_property_access(node)

                    case TOKENS.ARROW:
                        return self.parse_attribute_expression(node)

                if self.current.type == TOKENS.EQUALS:
                    self.advance()
                    expression = self.parse_binary_expression()
                    node = self.parse_assigners(node, expression)

                return node

            case t if t in (TOKENS.ADD, TOKENS.SUBT, TOKENS.NOT, TOKENS.BITNOT):
                self.advance()
                factor = self.parse_factor()
                operation_node = UNARY_OPERATOR_NODES[token.type]
                return operation_node(factor)

            case t if t in (TOKENS.INT, TOKENS.FLOAT):
                self.advance()

                if token.value + 255 in NUMBER_NODES:
                    return NUMBER_NODES[token.value + 255]

                return NumberNode(token.value)

            case TOKENS.STRING:
                self.advance()
                return StringNode(token.value)

            case _:
                self.runtime.report(SyntaxError(f"unexpected syntax."), token.pos)
                #raise Exception(f"Invalid token: '{token}'")


    def parse_accessors(self, node):
        accessors = []

        while self.current.type == TOKENS.LBRACKET:
            self.advance()
            accessors.append(self.parse_binary_expression())
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

        if self.current.type != TOKENS.LPAREN:
            self.runtime.report(SyntaxError("expected '('."), self.current.pos)

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

        return node


    def parse_property_access(self, node):
        accessors = []

        while self.current.type == TOKENS.DOT:
            self.advance()

            if self.current.type != TOKENS.IDENTIFIER:
                self.runtime.report(SyntaxError("expected identifier."), self.current.pos)

            accessors.append(self.parse_factor())

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
            has_lparen = (self.current.type == TOKENS.LPAREN)

            self.ignore_token_advance(TOKENS.LPAREN)
            condition = self.parse_binary_expression()

            if has_lparen:
                self.necessary_token_advance(TOKENS.RPAREN)
            else:
                if self.current.type == TOKENS.RPAREN:
                    self.runtime.report(SyntaxError("unexpected ')'."), self.current.pos)

                self.ignore_token_advance(TOKENS.RPAREN)

        match self.current.type:
            case TOKENS.LCURLY:
                self.advance()
                expressions = self.parse_expressions()
                self.necessary_token_advance(TOKENS.RCURLY)

            case TOKENS.ARROW:
                self.advance()
                expressions = ExpressionsNode([ReturnNode(self.parse_binary_expression())])
            
            case _:
                expressions = self.parse_expressions(once = True)

        return (condition, expressions)


    def parse_if_statement(self):
        if_clauses = []

        while self.current.value in (KEYWORDS.IF, KEYWORDS.ELIF):
            if_clauses.append(self.parse_statement())

        else_expressions = None

        if self.current.value == KEYWORDS.ELSE:
            (_, else_expressions) = self.parse_statement(has_condition = False)

        return IfNode(if_clauses, else_expressions)


    def parse_for_statement(self):
        self.advance()
        self.ignore_token_advance(TOKENS.LPAREN)
        identifier = self.parse_binary_expression()
        self.necessary_keyword_advance(KEYWORDS.IN)
        iterable = self.parse_binary_expression()
        self.ignore_token_advance(TOKENS.RPAREN)

        (_, expressions) = self.parse_statement(first_advance = False, has_condition = False)
        return ForNode(identifier.name, iterable, expressions)


    def parse_while_statement(self):
        (condition, expressions) = self.parse_statement()
        return WhileNode(condition, expressions)


    def parse_function_statement(self):
        self.advance()
        name = None
        bound_name = None

        if self.current.type == TOKENS.IDENTIFIER:
            name = self.current.value
            self.advance()

        if self.current.type == TOKENS.DOT:
            self.advance()

            if self.current.type != TOKENS.IDENTIFIER:
                self.runtime.report(SyntaxError("expected identifier."), self.current.pos)

            bound_name = name
            name = self.current.value
            self.advance()

        self.necessary_token_advance(TOKENS.LPAREN)
        args = []
        self.parse_arguments(args)
        (_, expressions) = self.parse_statement(has_condition = False)
        return FunctionNode(name, args, expressions, bound_name)

    
    def parse_class_statement(self):
        self.advance()

        if self.current.type != TOKENS.IDENTIFIER:
            self.runtime.report(SyntaxError("expected identifier."), self.current.pos)
            
        name = self.current.value
        self.advance()
        self.necessary_token_advance(TOKENS.LPAREN)
        args = []
        self.parse_arguments(args)
        self.necessary_token_advance(TOKENS.RPAREN)
        inherit = None

        if self.current.type == TOKENS.DOTDOT:
            self.advance()

            if self.current.type != TOKENS.IDENTIFIER:
                self.runtime.report(SyntaxError("expected identifier."), self.current.pos)

            node = VarAccessNode(self.current.value)
            self.advance()
            inherit = self.parse_function_access(node)

        (_, expressions) = self.parse_statement(first_advance = False, has_condition = False)
        return ClassNode(name, args, expressions, inherit)


    def parse_arguments(self, args, detect_optional = True):
        has_optional = False

        while True:
            if self.current.type == TOKENS.RPAREN:
                break

            arg = self.parse_binary_expression()

            if isinstance(arg, VarAssignNode):
                node = KeywordArgumentNode(arg.name, arg.expression)
                has_optional = True
            else:
                if detect_optional and has_optional:
                    raise Exception("Keyword arguments must be at the end.")

                node = ArgumentNode(arg)

            args.append(node)

            if self.current.type not in (TOKENS.COMMA, TOKENS.RPAREN):
                self.runtime.report(SyntaxError("expected ',', ')'."), self.current.pos)
                #raise Exception("Expected ',' or ')'.")

            if self.current.type == TOKENS.COMMA:
                self.advance()


    def parse_attribute_expression(self, node):
        name = node.name
        self.advance()
        self.necessary_token_advance(TOKENS.LCURLY)

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
            self.runtime.report(SyntaxError("expected keyword(s) 'assign', 'access'."), self.current.pos)
            #raise Exception("Expected keyword(s): 'assign', 'access'.")

        return AttributeNode(name, assign_expressions, access_expressions)


    def parse_binary_expression(self, priority = 0):
        left = self.parse_factor()

        while (operator_priority := binary_operator_priority(self.current)) >= priority and operator_priority != -1:
            operator = self.current
            self.advance()
            right = self.parse_binary_expression(operator_priority)
            operation_node = BINARY_OPERATOR_NODES[operator.type]
            left = operation_node(left, right)

        return left


    def parse_expressions(self, once = False):
        expressions = []

        while True:
            if self.current.type == TOKENS.RCURLY or self.current.type == TOKENS.ENDOFFILE:
                break

            expressions.append(self.parse_binary_expression())
        
            if self.peek(-1).type not in (TOKENS.SEMICOLON, TOKENS.RCURLY):
                self.necessary_token_advance(TOKENS.SEMICOLON)

            if once:
                break

        return ExpressionsNode(expressions)


    def run(self):
        self.tree = self.parse_expressions()

        if self.current.type != TOKENS.ENDOFFILE:
            self.runtime.report(SyntaxError(f"invalid syntax."), self.current.pos)
            #raise Exception("Invalid syntax.")