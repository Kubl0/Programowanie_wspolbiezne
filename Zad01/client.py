import os


def main():
    value = input("Enter a number >> ")
    saveToFile(value)
    print("Result: " + getResponseFromFile())


def saveToFile(number):
    f = open("input.txt", "w")
    f.write(number + "\n")
    f.close()


def getResponseFromFile():
    while not os.path.exists("output.txt"):
        pass
    f = open("output.txt", "r")
    result = f.read()
    f.close()
    os.remove("output.txt")
    return result


if __name__ == "__main__":
    main()
