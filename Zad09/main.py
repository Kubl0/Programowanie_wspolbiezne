import threading
from threading import Barrier


def is_prime(number):
    if number < 2:
        return False
    for i in range(2, number // 2 + 1):
        if number % i == 0:
            return False
    return True


def find_primes(start, end, barrier_e, result_list, lock):
    primes = [num for num in range(start, end) if is_prime(num)]
    with lock:
        result_list.extend(primes)
    barrier_e.wait()


def main():
    start_range = 1
    end_range = 1000
    num_threads = 4

    thread_ranges = [(i * (end_range - start_range) // num_threads,
                      (i + 1) * (end_range - start_range) // num_threads)
                     for i in range(num_threads)]

    print(thread_ranges)

    barrier_e = Barrier(num_threads + 1)

    result_list = []
    lock = threading.Lock()

    threads = []
    for i in range(num_threads):
        start, end = thread_ranges[i]
        thread = threading.Thread(target=find_primes, args=(start, end, barrier_e, result_list, lock))
        threads.append(thread)

    for thread in threads:
        thread.start()

    barrier_e.wait()

    print(result_list)


if __name__ == "__main__":
    main()
