import os
import time

def server():
    while True:
        lockfile = "server.lock"
        if os.path.exists(lockfile):
            clientFile = ""
            with open("serverInput.txt", "r") as f:
                clientFile = f.readline().strip()
            if not clientFile:
                continue
            with open("serverInput.txt", "r") as f:
                print("Client file:")
                for line in f:
                    print(line)
                with open(clientFile, "w") as file:
                    while True:
                        line = input("Enter line: (esc to exit) ")
                        if line == "esc":
                            break
                        file.write(line + "\n")
            os.remove(lockfile)
            os.remove("serverInput.txt")
        else:
            time.sleep(1)
            continue

if __name__ == "__main__":
    server()