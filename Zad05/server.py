import sysv_ipc
import os
import time

SERVER_INPUT_KEY = 1234

SERVER_OUTPUT_KEY = 5678

input_queue = sysv_ipc.MessageQueue(SERVER_INPUT_KEY, sysv_ipc.IPC_CREAT)
output_queue = sysv_ipc.MessageQueue(SERVER_OUTPUT_KEY, sysv_ipc.IPC_CREAT)

dictionary = {
    "cat": "kot",
    "dog": "pies",
    "apple": "jabłko",
}

while True:
    try:
        message, msg_type = input_queue.receive(type=0)

        client_pid = int(message.decode())

        word = input_queue.receive(type=client_pid)[0].decode()

        translation = dictionary.get(word, "Nie znam takiego słowa")

        response_msg = f"{os.getpid()}:{translation}"
        output_queue.send(response_msg.encode(), type=client_pid)

        time.sleep(1)

    except KeyboardInterrupt:
        print("Serwer zakończony")
        input_queue.remove()
        output_queue.remove()
        break
