import os
import sysv_ipc

SERVER_INPUT_KEY = 1234

SERVER_OUTPUT_KEY = 5678

client_pid = os.getpid()

input_queue = sysv_ipc.MessageQueue(client_pid, sysv_ipc.IPC_CREAT)
output_queue = sysv_ipc.MessageQueue(client_pid, sysv_ipc.IPC_CREAT)

word_to_translate = "cat"

input_queue.send(str(client_pid).encode())
input_queue.send(word_to_translate.encode())

response, msg_type = output_queue.receive(type=client_pid)

print(f"Odpowiedź od serwera: {response.decode().split(':')[-1]}")

input_queue.remove()
output_queue.remove()
