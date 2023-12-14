import os
import time


def server():
    while True:
        lockfile = "server.lock"
        if os.path.exists(lockfile):
            with open("serverBuffer.txt", "r") as f:
                client_file = f.readline().strip()
            if not client_file:
                continue
            with open("serverBuffer.txt", "r") as f:
                print("Client file:")
                for line in f:
                    print(line)
                with open(client_file, "w") as file:
                    while True:
                        line = input("Enter line: (esc to exit) ")
                        if line == "esc":
                            break
                        file.write(line + "\n")
            os.remove(lockfile)
            os.remove("serverBuffer.txt")
        else:
            time.sleep(1)
            continue


if __name__ == "__main__":
    server()
