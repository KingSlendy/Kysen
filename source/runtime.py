class Runtime:
    def __init__(self, ctx, line, start, end = None):
        self.ctx = ctx
        self.line = line
        self.start = start
        self.end = end if end != None else end


class RuntimeContext:
    def __init__(self, stack):
        self.stack = stack


    def add(self, name):
        self.stack.append(name)
        return self


    def copy(self):
        return RuntimeContext(list(self.stack))