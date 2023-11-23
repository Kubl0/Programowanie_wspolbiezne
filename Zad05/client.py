import os
import sysv_ipc

# Klucz dla kolejki wejściowej serwera
SERVER_INPUT_KEY = 1234

# Klucz dla kolejki wyjściowej serwera
SERVER_OUTPUT_KEY = 5678

# PID klienta
client_pid = os.getpid()

# Utwórz kolejki wejściową i wyjściową klienta
input_queue = sysv_ipc.MessageQueue(client_pid, sysv_ipc.IPC_CREAT)
output_queue = sysv_ipc.MessageQueue(client_pid, sysv_ipc.IPC_CREAT)

# Słowo do przetłumaczenia
word_to_translate = "cat"

# Wyślij zapytanie do serwera
input_queue.send(str(client_pid).encode())
input_queue.send(word_to_translate.encode())

# Odbierz odpowiedź od serwera
response, msg_type = output_queue.receive(type=client_pid)

# Wypisz odpowiedź
print(f"Odpowiedź od serwera: {response.decode().split(':')[-1]}")

# Usuń kolejki klienta
input_queue.remove()
output_queue.remove()
