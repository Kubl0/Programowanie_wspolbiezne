import json
import subprocess

class Client:
    def __init__(self, id, server_queue_path):
        self.id = id
        self.server_queue_path = server_queue_path

    def send_request(self):
        request_data = {
            'id': self.id,
            'client_queue': f"client_{self.id}_queue.txt"
        }

        with open(self.server_queue_path, 'a') as f:
            f.write(json.dumps(request_data) + "\n")

        client_queue_path = request_data['client_queue']
        while True:
            with open(client_queue_path, 'r') as f:
                response = f.read().strip()
                if response:
                    print(f"Odpowiedź serwera dla ID {self.id}: {json.loads(response)[0]}")
                    break

if __name__ == "__main__":
    client_id = int(input("Podaj ID klienta: "))
    server_queue_path = "server_input_queue.txt"

    client_queue_path = f"client_{client_id}_queue.txt"
    open(client_queue_path, 'w').close()

    client = Client(client_id, server_queue_path)
    client.send_request()
