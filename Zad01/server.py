import os


def main():
    while True:
        result = int(getInputFromFile()) * 2
        saveToFile(str(result))


def getInputFromFile():
    while not os.path.exists("input.txt"):
        pass
    f = open("input.txt", "r")
    value = f.read()
    f.close()
    os.remove("input.txt")
    return value


def saveToFile(number):
    f = open("output.txt", "w")
    f.write(number)
    f.close()


if __name__ == "__main__":
    main()
