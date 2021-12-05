from enum import Enum
from reporter import Position

class TOKENS(Enum):
    IDENTIFIER = "identifier"
    KEYWORD = "keyword"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    STRING = "string"
    NOT = "!"
    BITNOT = "~"
    POW = "**"
    MULT = "*"
    DIV = "/"
    FDIV = "\\"
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
    COLON = ":"
    SEMICOLON = ";"
    QUESTIONMARK = "?"
    WHITESPACE = "whitespace"
    ENDOFFILE = "endoffile"


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
    CONTINUE = "continue"
    BREAK = "break"
    FUNC = "func"
    RETURN = "return"
    CLASS = "class"
    STATIC = "static"
    NEW = "new"
    CAST = "cast"
    OPLEFT = "opleft"
    OPRIGHT = "opright"
    ASSIGN = "assign"
    ACCESS = "access"


class Token():
    def __init__(self, type, value = None):
        self.type = type
        self.value = value


    def set_pos(self, line, start, end = None):
        self.pos = Position(line, start, end)
        return self


    def matches(self, type, value):
        return self.type == type and self.value == value


    def __repr__(self):
        if self.value != None:
            return f"{self.type.value}: {self.value}"
        else:
            return f"{self.type.value}"