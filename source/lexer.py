import string
from exceptions import *
from reporter import Position
from tokens import *

LETTERS = string.ascii_letters
DIGITS = string.digits
LETTERS_DIGITS = LETTERS + DIGITS
VALID_IDENTIFIER = LETTERS_DIGITS + "_"
WHITESPACE = string.whitespace

class Lexer:
    def __init__(self, text):
        from runner import reporter

        self.text = text
        self.reporter = reporter
        self.position = -1
        self.current = None
        self.runline = 1
        self.runpos = -1
        self.tokens = []
        self.advance()
        self.run()


    def advance(self):
        self.position += 1
        self.current = self.text[self.position] if -1 < self.position < len(self.text) else None
        self.runpos += 1

    
    def peek(self, offset):
        pos = self.position + offset
        return self.text[pos] if -1 < pos < len(self.text) else None


    def register_token(self, token):
        self.tokens.append(token)

    
    def comment_skip(self):
        self.advance()

        if self.current == ">":
            while self.current != None:
                if self.current == "<" and self.peek(1) == "#":
                    self.advance()
                    self.advance()
                    break

                if self.current == "\n":
                    self.runline += 1
                    self.runpos = 0

                self.advance()
        else:
            while self.current != None and self.current != "\n":
                self.advance()


    def make_double_type_token(self, char_double, type_single, type_double):
        pos_start = self.runpos
        token_type = type_single
        self.advance()

        if self.current == char_double:
            self.advance()
            token_type = type_double

        return Token(token_type).set_pos(self.runline, pos_start, self.runpos - 1)

    
    def make_triple_type_token(self, char_double1, char_double2, type_single, type_double1, type_double2):
        pos_start = self.runpos
        token_type = type_single
        self.advance()

        if self.current == char_double1:
            self.advance()
            token_type = type_double1
        elif self.current == char_double2:
            self.advance()
            token_type = type_double2

        return Token(token_type).set_pos(self.runline, pos_start, self.runpos - 1)


    def make_binary_token(self, char_double, type_single, type_double):
        pos_start = self.runpos
        self.advance()
        token_type = type_single

        if self.current == char_double:
            self.advance()
            token_type = type_double
        elif self.current == "=":
            self.advance()
            return Token(TOKENS.ASSIGNMENT, token_type).set_pos(self.runline, pos_start, self.runpos - 1)

        return Token(token_type).set_pos(self.runline, pos_start, self.runpos - 1)

    
    def make_lessgreater_token(self, type_single, type_double1, type_double2):
        pos_start = self.runpos
        previous = self.current
        token_type = type_single
        self.advance()

        if self.current == previous:
            self.advance()

            if self.current == "=":
                self.advance()
                return Token(TOKENS.ASSIGNMENT, type_double1).set_pos(self.runline, pos_start, self.runpos - 1)
            else:
                token_type = type_double1
        elif self.current == "=":
            self.advance()
            token_type = type_double2

        return Token(token_type).set_pos(self.runline, pos_start, self.runpos - 1)


    def make_whitespace_token(self):
        line_start = self.runline
        pos_start = self.runpos
        value = ""

        while self.current != None and self.current in WHITESPACE:
            if self.current == "\n":
                self.runline += 1
                self.runpos = 0

            value += self.current
            self.advance()

        return Token(TOKENS.WHITESPACE, value).set_pos(line_start, pos_start, self.runpos - 1)


    def make_identifier_token(self):
        pos_start = self.runpos
        value = self.current
        self.advance()

        while self.current != None and self.current in VALID_IDENTIFIER:
            value += self.current
            self.advance()

        try:
            keyword = KEYWORDS[value.upper()]

            if keyword.value != value:
                raise KeyError()

            return Token(TOKENS.KEYWORD, keyword).set_pos(self.runline, pos_start, self.runpos - 1)
        except KeyError:
            return Token(TOKENS.IDENTIFIER, value).set_pos(self.runline, pos_start, self.runpos - 1)


    def make_number_token(self):
        pos_start = self.runpos
        value = ""
        has_dot = False

        while self.current != None and self.current in DIGITS + ".":
            if self.current == ".":
                if has_dot:
                    break
                    
                has_dot = True

            value += self.current
            self.advance()

        if not has_dot:
            return Token(TOKENS.INT, int(value)).set_pos(self.runline, pos_start, self.runpos - 1)
        else:
            return Token(TOKENS.FLOAT, float(value)).set_pos(self.runline, pos_start, self.runpos - 1)


    def make_string_token(self):
        pos_start = self.runpos
        value = ""
        self.advance()
        escape_chars = {"n": "\n", "r": "\r", "t": "\t"}
        escape = False

        while self.current != None and (escape or self.current != "\""):
            if escape:
                value += escape_chars[self.current]
                escape = False
            else:
                if self.current == "\\":
                    escape = not escape
                else:
                    value += self.current

            self.advance()

        self.advance()
        return Token(TOKENS.STRING, value).set_pos(self.runline, pos_start, self.position)


    def run(self):
        while True:
            match self.current:
                case None:
                    self.register_token(Token(TOKENS.ENDOFFILE).set_pos(self.runline, self.runpos))
                    break

                case "#":
                    self.comment_skip()

                case ";":
                    self.register_token(Token(TOKENS.SEMICOLON).set_pos(self.runline, self.runpos))
                    self.advance()

                case "\"":
                    self.register_token(self.make_string_token())

                case "*":
                    self.register_token(self.make_binary_token("*", TOKENS.MULT, TOKENS.POW))
                
                case "/":
                    self.register_token(self.make_binary_token("/", TOKENS.DIV, TOKENS.DIV))

                case "\\":
                    self.register_token(Token(TOKENS.FDIV).set_pos(self.runline, self.runpos))
                    self.advance()

                case "%":
                    self.register_token(self.make_binary_token("  ", TOKENS.MOD, "  "))

                case "+":
                    self.register_token(self.make_binary_token("  ", TOKENS.ADD, "  "))

                case "-":
                    self.register_token(self.make_binary_token("  ", TOKENS.SUBT, "  "))

                case "<":
                    self.register_token(self.make_lessgreater_token(TOKENS.LESS, TOKENS.LSHIFT, TOKENS.LESSEQUALS))

                case ">":
                    self.register_token(self.make_lessgreater_token(TOKENS.GREATER, TOKENS.RSHIFT, TOKENS.GREATEREQUALS))

                case "=":
                    self.register_token(self.make_triple_type_token("=", ">", TOKENS.EQUALS, TOKENS.EQUALSEQUALS, TOKENS.ARROW))

                case "!":
                    self.register_token(self.make_double_type_token("=", TOKENS.NOT, TOKENS.NOTEQUALS))

                case "&":
                    self.register_token(self.make_binary_token("&", TOKENS.BITAND, TOKENS.AND))

                case "|":
                    self.register_token(self.make_binary_token("|", TOKENS.BITOR, TOKENS.OR))

                case "^":
                    self.register_token(self.make_binary_token("??", TOKENS.BITXOR, TOKENS.BITXOR))

                case "~":
                    self.register_token(Token(TOKENS.BITNOT).set_pos(self.runline, self.runpos))
                    self.advance()

                case "(":
                    self.register_token(Token(TOKENS.LPAREN).set_pos(self.runline, self.runpos))
                    self.advance()

                case ")":
                    self.register_token(Token(TOKENS.RPAREN).set_pos(self.runline, self.runpos))
                    self.advance()

                case "[":
                    self.register_token(Token(TOKENS.LBRACKET).set_pos(self.runline, self.runpos))
                    self.advance()

                case "]":
                    self.register_token(Token(TOKENS.RBRACKET).set_pos(self.runline, self.runpos))
                    self.advance()

                case "{":
                    self.register_token(Token(TOKENS.LCURLY).set_pos(self.runline, self.runpos))
                    self.advance()

                case "}":
                    self.register_token(Token(TOKENS.RCURLY).set_pos(self.runline, self.runpos))
                    self.advance()

                case ",":
                    self.register_token(Token(TOKENS.COMMA).set_pos(self.runline, self.runpos))
                    self.advance()

                case ".":
                    if self.peek(1) in DIGITS:
                        self.register_token(self.make_number_token())
                    else:
                        self.register_token(Token(TOKENS.DOT).set_pos(self.runline, self.runpos))
                        self.advance()

                case ":":
                    self.register_token(Token(TOKENS.COLON).set_pos(self.runline, self.runpos))
                    self.advance()

                case c if c in WHITESPACE:
                    self.register_token(self.make_whitespace_token())

                case c if c in LETTERS + "_":
                    self.register_token(self.make_identifier_token())

                case c if c in DIGITS:
                    self.register_token(self.make_number_token())

                case c:
                    self.reporter.report(KSIllegalCharException(c), Position(self.runline, self.runpos), syntax = True)