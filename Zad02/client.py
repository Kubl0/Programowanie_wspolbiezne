import os
import time


def client():
    lockFile = "server.lock"
    clientFile = input("Enter file name: ")
    while True:
        if not os.path.exists(clientFile):
            with open(clientFile, "w") as f:
                pass
        with open(clientFile, "r") as clientInput:
            if os.stat(clientFile).st_size == 0:
                pass
            else:
                print("Response:")
                for line in clientInput:
                    print(line)
                break
        if os.path.exists(lockFile):
            print("Waiting for server...")
            time.sleep(1)
            continue
        with open(lockFile, "w") as f:
            f.write("lock")

        serverInput = "serverInput.txt"
        with open(serverInput, "w") as f:
            f.write(clientFile + "\n")
            while True:
                line = input("Enter line: (esc to exit) ")
                if line == "esc":
                    break
                f.write(line + "\n")

        os.remove(clientFile)


if __name__ == "__main__":
    client()
