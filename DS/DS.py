import threading
from time import sleep

mutex = threading.Semaphore()
emptyPot = threading.Semaphore(0)
fullPot = threading.Semaphore(0)
pot = []
M = 10

def cook():
    servings = 0
    while True:
        emptyPot.acquire()
        # Fill up the pot
        for i in range(M):
            pot.append(i)
        fullPot.release()

        servings += 1
        print('-'*16)
        print("Served : ", servings)

def savage():
    food = -1
    while True:
        mutex.acquire()
        if len(pot) == 0:
            emptyPot.release()
            fullPot.acquire()
        food = pot.pop()
        mutex.release()

        print("Eating : ", food)
        sleep(0.5)

chef = threading.Thread(target=cook)
savages = []
savages.append(threading.Thread(target=savage))
sleep(1)
savages.append(threading.Thread(target=savage))
sleep(1)
savages.append(threading.Thread(target=savage))

print("Cooking")
chef.start()
print("Eating")
for s in savages:
    s.start()

chef.join()