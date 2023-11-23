import os
import json
import threading
import subprocess

# Klasa reprezentująca bazę danych postaci
class Database:
    def __init__(self):
        # Przykładowa statyczna baza danych
        self.data = {
            1: "Kowalski",
            2: "Nowak",
            3: "Smith"
        }

# Klasa obsługująca komunikację serwera z klientem
class Server:
    def __init__(self, database, input_queue_path):
        self.database = database
        self.input_queue_path = input_queue_path

    def process_request(self, request):
        # Przetwarzanie zapytania od klienta
        try:
            request_data = json.loads(request)
            client_queue_path = request_data['client_queue']
            client_id = request_data['id']

            response = self.database.data.get(client_id, "Nie ma")

            # Odpowiedź do klienta
            with open(client_queue_path, 'w') as f:
                f.write(json.dumps([response]))
        except Exception as e:
            print(f"Błąd przetwarzania zapytania: {e}")

    def start(self):
        while True:
            # Odbieranie zapytań z kolejki wejściowej
            with open(self.input_queue_path, 'r') as f:
                request = f.read().strip()
                if request:
                    self.process_request(request)

if __name__ == "__main__":
    # Inicjalizacja serwera
    database = Database()
    input_queue_path = "server_input_queue.txt"

    # Utworzenie pliku kolejki wejściowej serwera
    if not os.path.exists(input_queue_path):
        open(input_queue_path, 'w').close()

    # Uruchomienie serwera w osobnym wątku
    server = Server(database, input_queue_path)
    server_thread = threading.Thread(target=server.start)
    server_thread.start()

    # Odbieranie zapytań od klienta
    while True:
        subprocess.run(["type", input_queue_path], shell=True)


