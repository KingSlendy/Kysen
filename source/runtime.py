from errors import RuntimeException

class Runtime:
    def __init__(self, filename, text):
        self.filename = filename
        self.text = text.split("\n")
        self.stacktrace = []


    def push(self, context, pos):
        self.stacktrace.append((context, pos))


    def pop(self):
        self.stacktrace.pop()

    
    def report(self, error, pos):
        #[pos.start:pos.end]
        print((pos.line, pos.start, pos.end))
        self.stacktrace = [("<program>", pos)] + self.stacktrace
        stacktrace = "\n".join([f"  File {self.filename}, {c} at line {p.line}\n    {self.text[p.line - 1]}\n" for c, p in self.stacktrace])
        last = self.text[pos.line - 1]
        print(last)
        arrows = [" "] * (len(last) + 1)

        for i in range(pos.start, pos.end + 1):
            arrows[i] = "^"

        arrows = "".join(arrows)
        raise RuntimeException(f"Stacktrace (most recent call last):\n{stacktrace}    {arrows}\n{error}")


class Position():
    def __init__(self, line, start, end = None):
        self.line = line
        self.start = start
        self.end = end if end != None else start