from enum import Enum

class TOKENS(Enum):
    IDENTIFIER = "IDENTIFIER"
    KEYWORD = "KEYWORD"
    INT = "INT"
    FLOAT = "FLOAT"
    BOOL = "BOOL"
    STRING = "STRING"
    EQUALS = "="
    DIV = "/"
    POW = "**"
    MULT = "*"
    ADD = "+"
    SUBT = "-"
    EQUALSEQUALS = "=="
    NOTEQUALS = "!="
    LESS = "<"
    LESSEQUALS = "<="
    GREATER = ">"
    GREATEREQUALS = ">="
    AND = "&&"
    OR = "||"
    BITAND = "&"
    BITOR = "|"
    NOT = "!"
    BITNOT = "~"
    LPAREN = "("
    RPAREN = ")"
    LBRACKET = "["
    RBRACKET = "]"
    LCURLY = "{"
    RCURLY = "}"
    COMMA = ","
    DOT = "."
    SEMICOLON = ";"
    WHITESPACE = "WHITESPACE"
    ENDOFFILE = "ENDOFFILE"


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