from enum import Enum

class TOKENS(Enum):
    IDENTIFIER = "IDENTIFIER"
    KEYWORD = "KEYWORD"
    INT = "INT"
    FLOAT = "FLOAT"
    BOOL = "BOOL"
    STRING = "STRING"
    NOT = "!"
    BITNOT = "~"
    POW = "**"
    MULT = "*"
    DIV = "/"
    MOD = "%"
    ADD = "+"
    SUBT = "-"
    LSHIFT = "<<"
    RSHIFT = ">>"
    LESS = "<"
    LESSEQUALS = "<="
    GREATER = ">"
    GREATEREQUALS = ">="
    EQUALSEQUALS = "=="
    NOTEQUALS = "!="
    BITAND = "&"
    BITOR = "|"
    BITXOR = "^"
    AND = "&&"
    OR = "||"
    ASSIGNMENT = "X="
    EQUALS = "="
    LPAREN = "("
    RPAREN = ")"
    LBRACKET = "["
    RBRACKET = "]"
    LCURLY = "{"
    RCURLY = "}"
    COMMA = ","
    DOT = "."
    ARROW = "=>"
    SEMICOLON = ";"
    WHITESPACE = "WHITESPACE"
    ENDOFFILE = "ENDOFFILE"


class KEYWORDS(Enum):
    IMPORT = "import"
    TRUE = "true"
    FALSE = "false"
    NULL = "null"
    IF = "if"
    ELIF = "elif"
    ELSE = "else"
    FOR = "for"
    IN = "in"
    WHILE = "while"
    CONTINUE = "CONTINUE"
    BREAK = "break"
    FUNC = "func"
    RETURN = "return"
    CLASS = "class"
    STATIC = "static"
    OPLEFT = "opleft"
    OPRIGHT = "opright"
    ASSIGN = "assign"
    ACCESS = "access"


class Token():
    def __init__(self, type, value = None):
        self.type = type
        self.value = value


    def set_pos(self, start, end = None):
        self.pos = Position(start, end)
        return self


    def matches(self, type, value):
        return self.type == type and self.value == value


    def __repr__(self):
        if self.value != None:
            return f"{self.type.value}: {self.value}"
        else:
            return f"{self.type.value}"


class Position():
    def __init__(self, start, end = None):
        self.start = start
        self.end = end if end != None else start