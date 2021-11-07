import string
from tokens import *
from types import NoneType
LETTERS = string.ascii_letters
DIGITS = string.digits
LETTERS_DIGITS = LETTERS + DIGITS
VALID_IDENTIFIER = LETTERS_DIGITS + "_"
WHITESPACE = string.whitespace
KEYWORDS = ["true", "false", "null", "if", "elif", "else", "for", "continue", "break", "in", "func", "return", "class", "override"]

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
        self.current = self.text[self.position] if self.position < len(self.text) else None


    def register_token(self, token):
        self.tokens.append(token)

    
    def skip_line(self):
        while self.current != None and self.current != "\n":
            self.advance()


    def make_double_token(self, char, type1, type2):
        pos_start = self.position
        self.advance()

        if self.current == char:
            self.advance()
            return Token(type1).set_pos(pos_start, self.position)

        return Token(type2).set_pos(pos_start, self.position)


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

        return Token(TOKENS.KEYWORD if value in KEYWORDS else TOKENS.IDENTIFIER, value).set_pos(pos_start, self.position)


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
                    self.skip_line()

                case ";":
                    self.register_token(Token(TOKENS.SEMICOLON).set_pos(self.position))
                    self.advance()

                case "\"":
                    self.register_token(self.make_string_token())

                case "=":
                    self.register_token(self.make_double_token("=", TOKENS.EQUALSEQUALS, TOKENS.EQUALS))

                case "<":
                    self.register_token(self.make_double_token("=", TOKENS.LESSEQUALS, TOKENS.LESS))

                case ">":
                    self.register_token(self.make_double_token("=", TOKENS.GREATEREQUALS, TOKENS.GREATER))

                case "&":
                    self.register_token(self.make_double_token("&", TOKENS.AND, TOKENS.BITAND))

                case "|":
                    self.register_token(self.make_double_token("|", TOKENS.OR, TOKENS.BITOR))

                case "*":
                    self.register_token(self.make_double_token("*", TOKENS.POW, TOKENS.MULT))
                
                case "/":
                    self.register_token(Token(TOKENS.DIV).set_pos(self.position))
                    self.advance()

                case "+":
                    self.register_token(Token(TOKENS.ADD).set_pos(self.position))
                    self.advance()

                case "-":
                    self.register_token(Token(TOKENS.SUBT).set_pos(self.position))
                    self.advance()

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