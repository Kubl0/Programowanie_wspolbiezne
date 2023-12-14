import os
import time


def client():
    lock_file = "server.lock"
    client_file = input("Enter file name: ")
    while True:
        if not os.path.exists(client_file):
            with open(client_file, "w") as f:
                pass
        with open(client_file, "r") as clientInput:
            if os.stat(client_file).st_size == 0:
                pass
            else:
                print("Response:")
                for line in clientInput:
                    print(line)
                break

        if os.path.exists(lock_file):
            print("Waiting for server...")
            time.sleep(3)
            continue
        else:
            with open(lock_file, "w") as f:
                f.write("lock")

        server_input = "serverBuffer.txt"
        with open(server_input, "w") as f:
            f.write(client_file + "\n")
            while True:
                line = input("Enter line: (esc to exit) ")
                if line == "esc":
                    break
                f.write(line + "\n")

        os.remove(client_file)


if __name__ == "__main__":
    client()
