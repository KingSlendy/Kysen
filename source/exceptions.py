class RuntimeException(Exception):
    pass


class KSException:
    def __init__(self, message):
        self.message = message


    def __repr__(self):
        return f"{type(self).__name__[2:]}: {self.message}"


class KSIllegalCharException(KSException):
    def __init__(self, char):
        self.message = f"illegal character '{char}'."


class KSSyntaxException(KSException):
    pass


class KSArgumentException(KSException):
    pass


class KSBinaryOperationException(KSException):
    def __init__(self, operator, type_left, type_right):
        self.message = f"unsupported operator '{operator}' for types '{type_left.__name__}' and '{type_right.__name__}'."


class KSTypeException(KSException):
    pass


class KSValueException(KSException):
    pass


class KSPropertyException(KSException):
    pass


class KSCastException(KSException):
    pass

class KSVariableException(KSException):
    pass

class KSStaticException(KSException):
    pass