import string
from tokens import *

LETTERS = string.ascii_letters
DIGITS = string.digits
LETTERS_DIGITS = LETTERS + DIGITS
VALID_IDENTIFIER = LETTERS_DIGITS + "_"
WHITESPACE = string.whitespace

class Lexer:
    def __init__(self, text):
        self.text = text
        self.position = -1
        self.current = None
        self.tokens = []
        self.advance()
        self.run()


    def advance(self):
        self.position += 1
        self.current = self.text[self.position] if -1 < self.position < len(self.text) else None

    
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

                self.advance()
        else:
            while self.current != None and self.current != "\n":
                self.advance()


    def make_double_type_token(self, char_double, type_single, type_double):
        pos_start = self.position
        self.advance()

        if self.current == char_double:
            self.advance()
            return Token(type_double).set_pos(pos_start, self.position)

        return Token(type_single).set_pos(pos_start, self.position)

    
    def make_triple_type_token(self, char_double1, char_double2, type_single, type_double1, type_double2):
        pos_start = self.position
        self.advance()

        if self.current == char_double1:
            self.advance()
            return Token(type_double1).set_pos(pos_start, self.position)
        elif self.current == char_double2:
            self.advance()
            return Token(type_double2).set_pos(pos_start, self.position)

        return Token(type_single).set_pos(pos_start, self.position)


    def make_binary_token(self, char_double, type_single, type_double):
        pos_start = self.position
        self.advance()
        token_type = type_single

        if self.current == char_double:
            self.advance()
            token_type = type_double
        
        if self.current == "=":
            self.advance()
            return Token(TOKENS.ASSIGNMENT, token_type).set_pos(pos_start, self.position)

        return Token(token_type).set_pos(pos_start, self.position)

    
    def make_lessgreater_token(self, type_single, type_double1, type_double2):
        pos_start = self.position
        previous = self.current
        self.advance()

        if self.current == previous:
            self.advance()

            if self.current == "=":
                self.advance()
                return Token(TOKENS.ASSIGNMENT, type_double1).set_pos(pos_start, self.position)
            else:
                return Token(type_double1).set_pos(pos_start, self.position)
        elif self.current == "=":
            self.advance()
            return Token(type_double2).set_pos(pos_start, self.position)

        return Token(type_single).set_pos(pos_start, self.position)


    def make_whitespace_token(self):
        pos_start = self.position
        value = ""

        while self.current != None and self.current in WHITESPACE:
            value += self.current
            self.advance()

        return Token(TOKENS.WHITESPACE, value).set_pos(pos_start, self.position)


    def make_identifier_token(self):
        pos_start = self.position
        value = self.current
        self.advance()

        while self.current != None and self.current in VALID_IDENTIFIER:
            value += self.current
            self.advance()

        try:
            keyword = KEYWORDS[value.upper()]
            return Token(TOKENS.KEYWORD, keyword).set_pos(pos_start, self.position)
        except KeyError:
            return Token(TOKENS.IDENTIFIER, value).set_pos(pos_start, self.position)

    def make_number_token(self):
        pos_start = self.position
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
            return Token(TOKENS.INT, int(value)).set_pos(pos_start, self.position)
        else:
            return Token(TOKENS.FLOAT, float(value)).set_pos(pos_start, self.position)


    def make_string_token(self):
        pos_start = self.position
        value = ""
        self.advance()
        escape = False

        while self.current != None and (escape or self.current != "\""):
            escape = False
            value += self.current

            if self.current == "\\":
                escape = not escape

            self.advance()

        self.advance()
        return Token(TOKENS.STRING, value).set_pos(pos_start, self.position)


    def run(self):
        while True:
            match self.current:
                case None:
                    self.register_token(Token(TOKENS.ENDOFFILE).set_pos(self.position))
                    break

                case "#":
                    self.comment_skip()

                case ";":
                    self.register_token(Token(TOKENS.SEMICOLON).set_pos(self.position))
                    self.advance()

                case "\"":
                    self.register_token(self.make_string_token())

                case "*":
                    self.register_token(self.make_binary_token("*", TOKENS.MULT, TOKENS.POW))
                
                case "/":
                    self.register_token(self.make_binary_token("/", TOKENS.DIV, TOKENS.DIV))

                case "%":
                    self.register_token(self.make_binary_token(None, TOKENS.MOD, None))

                case "+":
                    self.register_token(self.make_binary_token(None, TOKENS.ADD, None))

                case "-":
                    self.register_token(self.make_binary_token(None, TOKENS.SUBT, None))

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

                case "(":
                    self.register_token(Token(TOKENS.LPAREN).set_pos(self.position))
                    self.advance()

                case ")":
                    self.register_token(Token(TOKENS.RPAREN).set_pos(self.position))
                    self.advance()

                case "[":
                    self.register_token(Token(TOKENS.LBRACKET).set_pos(self.position))
                    self.advance()

                case "]":
                    self.register_token(Token(TOKENS.RBRACKET).set_pos(self.position))
                    self.advance()

                case "{":
                    self.register_token(Token(TOKENS.LCURLY).set_pos(self.position))
                    self.advance()

                case "}":
                    self.register_token(Token(TOKENS.RCURLY).set_pos(self.position))
                    self.advance()

                case ",":
                    self.register_token(Token(TOKENS.COMMA).set_pos(self.position))
                    self.advance()

                case ".":
                    if self.peek(1) in DIGITS:
                        self.register_token(self.make_number_token())
                    else:
                        self.register_token(Token(TOKENS.DOT).set_pos(self.position))
                        self.advance()

                case c if c in WHITESPACE:
                    self.register_token(self.make_whitespace_token())

                case c if c in LETTERS + "_":
                    self.register_token(self.make_identifier_token())

                case c if c in DIGITS:
                    self.register_token(self.make_number_token())

                case c:
                    raise Exception(f"Invalid character: '{c}'")