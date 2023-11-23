import sysv_ipc
import os
import time

# Klucz dla kolejki wejściowej serwera
SERVER_INPUT_KEY = 1234

# Klucz dla kolejki wyjściowej serwera
SERVER_OUTPUT_KEY = 5678

# Utwórz kolejki wejściową i wyjściową serwera
input_queue = sysv_ipc.MessageQueue(SERVER_INPUT_KEY, sysv_ipc.IPC_CREAT)
output_queue = sysv_ipc.MessageQueue(SERVER_OUTPUT_KEY, sysv_ipc.IPC_CREAT)

# Słownik angielsko-polski
dictionary = {
    "cat": "kot",
    "dog": "pies",
    "apple": "jabłko",
}

while True:
    try:
        # Odbierz zapytanie z dowolnego klienta
        message, msg_type = input_queue.receive(type=0)

        # Pobierz PID klienta z treści komunikatu
        client_pid = int(message.decode())

        # Odczytaj słowo z komunikatu
        word = input_queue.receive(type=client_pid)[0].decode()

        # Szukaj tłumaczenia słowa w słowniku
        translation = dictionary.get(word, "Nie znam takiego słowa")

        # Odpowiedz klientowi
        response_msg = f"{os.getpid()}:{translation}"
        output_queue.send(response_msg.encode(), type=client_pid)

        # Symuluj opóźnienie w serwerze (do testowania)
        time.sleep(1)

    except KeyboardInterrupt:
        # Obsłuż przerwanie z klawiatury
        print("Serwer zakończony")
        input_queue.remove()
        output_queue.remove()
        break
