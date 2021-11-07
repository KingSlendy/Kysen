import sys
from runner import Runner

def main():
    if len(sys.argv) >= 2:
        Runner.execute(open(sys.argv[1], "r").read())
        return

    while True:
        text = input(">>> ")

        match text.split(" "):
            case ["run", filename]:
                text = open(filename, "r").read()

            case ["exit"]:
                break

        #try:
        compiled = Runner.execute(text)

        if compiled != None:
            print(compiled)
        #except Exception as e:
            #print(e)


if __name__ == "__main__":
    main()