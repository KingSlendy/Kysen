from exceptions import RuntimeException

class Reporter:
    def __init__(self, filename = "", text = "", unittest = False):
        self.filename = filename
        self.text = text.split("\n")
        self.unittest = unittest
        self.place = "<program>"
        self.pos = None
        self.stacktrace = []


    def push(self, context):
        self.stacktrace.append((context, self.pos))


    def pop(self):
        self.place = self.stacktrace.pop()[0]


    def update(self, filename, text, unittest = False):
        self.__init__(filename, text, unittest)

    
    def report(self, error, syntax = False):
        #[pos.start:pos.end]
        self.stacktrace += [(self.place, self.pos)]
        stacktrace = "\n".join([f"  File {self.filename}, in {c} at line {p.line}\n    {self.text[p.line - 1].strip()}\n" for c, p in self.stacktrace])
        arrows = ""

        if syntax:
            last = "    " + self.text[self.pos.line - 1].strip()
            arrows = [" "] * (len(last) + 1)
            #arrows[pos.end] = "^"

            #for i in range(pos.start, pos.end + 1):
            #    arrows[i] = "^"

        arrows = "".join(arrows)
        raise RuntimeException(f"Stacktrace (most recent call last):\n{stacktrace}    {arrows}\n{error}")


class Position():
    def __init__(self, line, start, end = None):
        self.line = line
        self.start = start
        self.end = end if end != None else start


    def copy(self):
        return Position(self.line, self.start, self.end)


    def __repr__(self):
        return f"Line: {self.line} | Start : {self.start} | End: {self.end}"