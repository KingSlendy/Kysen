import os, sys
from runner import Runner

def run(text):
    #try:
    compiled = Runner.execute(text)

    if compiled != None:
        print(compiled)
    #except Exception as e:
        #print(e)

def main():
    if len(sys.argv) >= 2:
        run(open(sys.argv[1], "r").read())
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

        run(text)


if __name__ == "__main__":
    main()