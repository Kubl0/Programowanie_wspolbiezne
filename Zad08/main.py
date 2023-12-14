import threading
import time


def calculate_chunk_sum(chunk, lock, result_list):
    partial_sum = sum(chunk)
    with lock:
        result_list.append(partial_sum)


def divide_chunks(lst, num_chunks):
    chunk_size = len(lst) // num_chunks
    remainder = len(lst) % num_chunks

    chunks = []
    start = 0

    for i in range(num_chunks):
        end = start + chunk_size + (1 if remainder > i else 0)
        chunks.append(lst[start:end])
        start = end

    return chunks


def sum_threads(lst, num_threads):
    if num_threads == 1:
        return sum(lst)
    else:
        # Divide list into chunks
        chunks = divide_chunks(lst, num_threads)

        results, chunk_sums = [], []
        result_lock = threading.Lock()

        # Create threads
        for chunk in chunks:
            thread = threading.Thread(target=calculate_chunk_sum, args=(chunk, result_lock, chunk_sums))
            results.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in results:
            thread.join()

        # print(chunks)
        # print(chunk_sums)

        return sum(chunk_sums)


def main():
    input_list = list(range(100000000))
    num_threads = 4

    result = sum_threads(input_list, num_threads)

    print(f'Suma:', result)


if __name__ == "__main__":
    main()
