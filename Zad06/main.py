import random
import time
import sysv_ipc


def remove_semaphores():
    try:
        sem1 = sysv_ipc.Semaphore(1)
        sem1.remove()
    except sysv_ipc.ExistentialError:
        pass

    try:
        sem2 = sysv_ipc.Semaphore(2)
        sem2.remove()
    except sysv_ipc.ExistentialError:
        pass

    try:
        sem3 = sysv_ipc.SharedMemory(3)
        sem3.remove()
    except sysv_ipc.ExistentialError:
        pass

    try:
        sem4 = sysv_ipc.SharedMemory(4)
        sem4.remove()
    except sysv_ipc.ExistentialError:
        pass


def player1():
    print("Player1")
    remove_semaphores()
    sem1 = sysv_ipc.Semaphore(1, sysv_ipc.IPC_CREX, 0o777, 0)
    sem2 = sysv_ipc.Semaphore(2, sysv_ipc.IPC_CREX, 0o777, 0)
    memory1 = sysv_ipc.SharedMemory(3, sysv_ipc.IPC_CREX, 0o777)
    memory2 = sysv_ipc.SharedMemory(4, sysv_ipc.IPC_CREX, 0o777)
    p1_score = 0
    p2_score = 0

    for _ in range(3):
        choice = input("Wybierz (1-3) >> ")
        sem1.release()
        memory1.write(choice)

        print("Czekam na drugiego gracza...")

        sem2.acquire()

        wybor = memory2.read()
        wybor = wybor.decode("utf-8")
        wybor = int(wybor)

        print("Wybór drugiego gracza: ", wybor)

        if wybor == int(choice):
            print("Player2 wins!")
            p2_score += 1
        else:
            print("Player1 wins!")
            p1_score += 1

    print("Player1 score: ", p1_score)
    print("Player2 score: ", p2_score)


def player2():
    print("Player2")
    sem1 = sysv_ipc.Semaphore(1)
    sem2 = sysv_ipc.Semaphore(2)
    memory1 = sysv_ipc.SharedMemory(3)
    memory2 = sysv_ipc.SharedMemory(4)
    p1_score = 0
    p2_score = 0

    for _ in range(3):
        print("Czekam na pierwszego gracza...")

        sem1.acquire()
        time.sleep(1)

        wybor = memory1.read()
        wybor = wybor.decode("utf-8")
        wybor = int(wybor)

        choice = input("Wybierz (1-3) >> ")

        memory2.write(choice)

        print("Wybór pierwszego gracza: ", wybor)

        sem2.release()

        if wybor == int(choice):
            print("Player2 wins!")
            p2_score += 1
        else:
            print("Player1 wins!")
            p1_score += 1

    print("Player1 score: ", p1_score)
    print("Player2 score: ", p2_score)


def remove_test():
    try:
        sem = sysv_ipc.Semaphore(111)
        sem.remove()
    except sysv_ipc.ExistentialError:
        pass


def main():
    try:
        sem = sysv_ipc.Semaphore(111, sysv_ipc.IPC_CREX, 0o700, 1)
        p1 = True
    except sysv_ipc.ExistentialError:
        sem = sysv_ipc.Semaphore(111)
        p1 = False
        remove_test()
        time.sleep(1)

    if p1:
        player1()
    else:
        player2()


if __name__ == "__main__":
    main()
