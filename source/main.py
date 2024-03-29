import os, sys
from exceptions import RuntimeException
from runner import Runner

def run(filename, text):
    try:
        compiled = Runner.execute(filename, text)

        if filename == "<stdin>" and compiled != None:
            print(compiled)
    except RuntimeException as e:
        print(e)


def main():
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
        run(filename, open(filename, "r").read())
        return

    while True:
        text = input(">>> ")

        match text.split(" "):
            case ["run", filename]:
                text = open(filename, "r").read()

            case ["clear"]:
                os.system('cls' if os.name == 'nt' else 'clear')
                return

            case ["exit"]:
                break

        run("<stdin>", text)


if __name__ == "__main__":
    main()