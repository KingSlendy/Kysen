from exceptions import RuntimeException

class Runtime:
    def __init__(self, filename, text, unittest = False):
        self.filename = filename
        self.text = text.split("\n")
        self.unittest = unittest
        self.place = "<program>"
        self.stacktrace = []


    def push(self, context, pos):
        self.stacktrace.append((context, pos))


    def pop(self):
        return self.stacktrace.pop()[0]

    
    def report(self, error, pos, syntax = False):
        #[pos.start:pos.end]
        self.stacktrace += [(self.place, pos)]
        stacktrace = "\n".join([f"  File {self.filename}, in {c} at line {p.line}\n    {self.text[p.line - 1].strip()}\n" for c, p in self.stacktrace])
        arrows = ""

        if syntax:
            last = "    " + self.text[pos.line - 1].strip()
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