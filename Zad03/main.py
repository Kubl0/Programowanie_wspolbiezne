import os
from multiprocessing import Process, Queue


def process_file(file_name, queue):
    with open(os.path.join("./input/", file_name), 'r') as file:

        for line in file:
            if line.startswith("\\input{"):
                sub_file = line.split("{")[1].split("}")[0]
                p = Process(target=process_file, args=(sub_file, queue))
                p.start()
                p.join()
            else:
                queue.put(line)


def count_occurrences(file, word):
    queue = Queue()
    p = Process(target=process_file, args=(file, queue))
    p.start()
    p.join()

    count = 0

    while not queue.empty():
        line = queue.get()
        count += line.split().count(word)
        print(line.strip())

    return count


if __name__ == "__main__":
    start_file = "mainInput.txt"
    target_word = "Stoi"
    result = count_occurrences(start_file, target_word)
    print(f"\nWord '{target_word}' occurs {result} times in {start_file}")
