import random
import socket


def choose():
    choice = input("Papier, kamien czy nozyce (P/K/N) albo 'end' zeby zakonczyc >> ")
    if choice.lower() not in ["p", "k", "n", "end"]:
        print("Zły wybór")
        return choose()
    return choice


def client(id):
    print("Twoj ID:", id)
    host = "127.0.0.1"
    port = 55555

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    client_socket.sendto(f"start, {id}".encode(), (host, port))

    scores = {"won": 0, "lost": 0, "draw": 0}

    while True:
        choice = choose()

        if choice.lower() == "end":
            client_socket.sendto(f"end, {id}".encode(), (host, port))
            print("Koniec")
            break

        client_socket.sendto(f"{choice}, {id}".encode(), (host, port))

        result, _ = client_socket.recvfrom(1024)
        result = result.decode()
        result = result.strip()

        if result == "Remis":
            print(result)
            scores["draw"] += 1
        elif result == "Koniec":
            print("Koniec")
            break
        elif int(result) == id:
            print("Wygrałeś!")
            scores["won"] += 1
        else:
            print("Przegrałeś!")
            scores["lost"] += 1

        print("Wyniki:", scores)

    client_socket.close()


if __name__ == "__main__":
    id = random.randint(1, 100)
    client(id)
