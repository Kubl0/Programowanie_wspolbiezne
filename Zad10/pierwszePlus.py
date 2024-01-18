import math
import multiprocessing
import time


def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


def sequential_primes(start, end):
    primes = []
    sqrt_end = int(math.sqrt(end))

    for num in range(2, sqrt_end + 1):
        if is_prime(num):
            primes.append(num)

    with multiprocessing.Pool() as pool:
        primes += pool.map(partial_check_prime, range(max(sqrt_end + 1, start), end + 1))

    return primes


def partial_check_prime(num):
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


def parallel_primes(start, end, num_processes, shared_data):
    global sqrt_end_primes
    sqrt_end_primes = shared_data

    primes = []

    with multiprocessing.Pool(num_processes, initializer=init_shared_data, initargs=(sqrt_end_primes,)) as pool:
        primes += pool.map(partial_check_prime_parallel, range(max(sqrt_end_primes[-1] + 1, start), end + 1))

    primes += sqrt_end_primes

    return primes


def init_shared_data(data):
    global sqrt_end_primes
    sqrt_end_primes = data


def partial_check_prime_parallel(num):
    for prime in sqrt_end_primes:
        if num % prime == 0:
            return False
    return True


def main():
    start = 1
    end = 10000
    num_processes = 4

    start_time = time.time()
    sequential_result = sequential_primes(start, end)
    sequential_time = time.time() - start_time

    start_time = time.time()
    parallel_result = parallel_primes(start, end, num_processes, sequential_result[:])
    parallel_time = time.time() - start_time

    # print("Sequential primes:", sequential_result)
    # print("Parallel primes:", parallel_result)

    print("Sequential time:", sequential_time)
    print("Parallel time:", parallel_time)


if __name__ == "__main__":
    main()
