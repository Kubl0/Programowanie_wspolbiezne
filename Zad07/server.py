import socket


def determine_winner(players):
    player1_id = list(players.keys())[0]
    player2_id = list(players.keys())[1]

    player1_choice = players[player1_id]["choice"]
    player2_choice = players[player2_id]["choice"]

    if player1_choice == player2_choice:
        return "Remis"
    elif (
            (player1_choice == "k" and player2_choice == "n")
            or (player1_choice == "n" and player2_choice == "p")
            or (player1_choice == "p" and player2_choice == "k")
    ):
        return player1_id
    else:
        return player2_id


def server():
    host = "127.0.0.1"
    port = 55555

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print("Serwer nasłuchuje na porcie", port)

    players = {}

    counter = 0
    scores = []

    while True:

        data, addr = server_socket.recvfrom(1024)
        player_choice, player_id = data.decode().split(",")

        if player_choice == "start":
            scores.append({player_id: 0})

        if player_choice != "start" and counter < 2:
            counter += 1

        print("Otrzymano:", player_choice, player_id)
        players[player_id] = {"choice": player_choice, "addr": addr}

        if len(players) == 2:
            player1_id = list(players.keys())[0]
            player2_id = list(players.keys())[1]
            player1_addr = players[player1_id]["addr"]
            player2_addr = players[player2_id]["addr"]

        if player_choice == "end":
            print("Koniec")
            print(scores)
            server_socket.sendto("Koniec".encode(), player1_addr)
            server_socket.sendto("Koniec".encode(), player2_addr)
            break

        if counter == 2:
            winner = determine_winner(players)
            server_socket.sendto(winner.encode(), player1_addr)
            server_socket.sendto(winner.encode(), player2_addr)
            counter = 0
            scores[-1][winner] += 1
            print("Score:", scores)


if __name__ == "__main__":
    server()
