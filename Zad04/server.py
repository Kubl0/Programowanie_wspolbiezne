import os
import json
import threading
import time

class Database:
    def __init__(self):
        self.data = {
            1: "Kowalski",
            2: "Nowak",
            3: "Smith"
        }

class Server:
    def __init__(self, database, input_queue_path):
        self.database = database
        self.input_queue_path = input_queue_path

    def process_request(self, request):
        try:
            request_data = json.loads(request)
            client_queue_path = request_data['client_queue']
            client_id = request_data['id']

            response = self.database.data.get(client_id, "Nie ma")

            time.sleep(10)
            with open(client_queue_path, 'w') as f:
                f.write(json.dumps([response]))

            with open(self.input_queue_path, 'r') as f:
                lines = f.readlines()

            with open(self.input_queue_path, 'w') as f:
                if lines:
                    f.writelines(lines[1:])

        except Exception as e:
            print(f"Błąd przetwarzania zapytania: {e}")

    def start(self):
        while True:
            with open(self.input_queue_path, 'r') as f:
                lines = f.readlines()

            for line in lines:
                request = line.strip()
                if request:
                    print(f"\nPrzetwarzanie zapytania: {request}")
                    self.process_request(request)
                    break

            time.sleep(1)

if __name__ == "__main__":
    database = Database()
    input_queue_path = "server_input_queue.txt"

    if not os.path.exists(input_queue_path):
        open(input_queue_path, 'w').close()

    server = Server(database, input_queue_path)
    server_thread = threading.Thread(target=server.start)
    server_thread.start()

    input("Wciśnij Enter, aby zakończyć program...")
