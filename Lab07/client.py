import random
import socket


def choose():
    choice = input("Papier, kamien czy nozyce (P/K/N) albo 'end' zeby zakonczyc >> ")
    if choice.lower() not in ["p", "k", "n", "end"]:
        print("Zły wybór")
        return choose()
    return choice


def client(id):
    host = "127.0.0.1"
    port = 55555

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    client_socket.sendto(f"start, {id}".encode(), (host, port))

    while True:
        choice = choose()

        if choice.lower() == "end":
            print("Koniec")
            break


        client_socket.sendto(f"{choice}, {id}".encode(), (host, port))

        result, _ = client_socket.recvfrom(1024)
        if result == "Remis":
            print(result)
        elif result == id:
            print("Wygrałeś!")
        else:
            print("Przegrałeś!")

    client_socket.close()

if __name__ == "__main__":
    id = random.randint(1,100)
    client(id)


