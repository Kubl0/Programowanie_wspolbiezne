import socket


def determine_winner(choices):

    players = list(choices.keys())
    player1 = players[0]
    player2 = players[1]

    choice1 = choices[player1]
    choice2 = choices[player2]

    if choice1 == choice2:
        return "Remis"
    elif choice1 == "P" and choice2 == "K":
        return player1
    elif choice1 == "P" and choice2 == "N":
        return player2
    elif choice1 == "K" and choice2 == "P":
        return player2
    elif choice1 == "K" and choice2 == "N":
        return player1
    elif choice1 == "N" and choice2 == "P":
        return player1
    elif choice1 == "N" and choice2 == "K":
        return player2


def server():
    host = "127.0.0.1"
    port = 55555

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print("Serwer nasłuchuje na porcie", port)
    end_count = 0

    scores = {}
    choices = {}

    addr = []

    while True:

        data, address = server_socket.recvfrom(1024)
        addr.append(address)
        data = data.decode()
        data = data.strip()
        data = data.split(", ")

        choice = data[0]
        id = data[1]

        if choice == "start":
            scores[id] = {"score": 0}
        elif choice == "end":
            end_count += 1
            if end_count == 2:
                print("Koniec")
                scores = {}
        else:
            if end_count == 1:
                print("Koniec")
                server_socket.sendto("Koniec".encode(), address)
                end_count = 0
                scores = {}
                addr = []

            choices[id] = choice

            if len(choices) == 2:
                winner_id = determine_winner(choices)
                if winner_id == "Remis":
                    print("Remis")
                    server_socket.sendto(winner_id.encode(), addr[0])
                    server_socket.sendto(winner_id.encode(), addr[1])
                    choices = {}
                else:
                    scores[winner_id]["score"] += 1
                    print("Wygrał", winner_id)
                    print("Wyniki:", scores)
                    choices = {}

                    server_socket.sendto(winner_id.encode(), addr[0])
                    server_socket.sendto(winner_id.encode(), addr[1])

                addr = []




if __name__ == "__main__":
    server()
