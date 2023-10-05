import os


def main():
    while True:
        while not os.path.exists("input.txt"):
            pass
        f = open("input.txt", "r")
        value = f.read()
        f.close()
        os.remove("input.txt")
        result = int(value) * 2
        saveToFile(str(result))


def saveToFile(number):
    f = open("output.txt", "w")
    f.write(number)
    f.close()


if __name__ == "__main__":
    main()
