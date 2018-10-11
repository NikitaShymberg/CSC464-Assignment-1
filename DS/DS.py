import threading
from time import sleep, time

mutex = threading.Semaphore()
emptyPot = threading.Semaphore(0)
fullPot = threading.Semaphore(0)
pot = []
M = 10
runtimes = [0 for i in range(3)]

def cook():
    servings = 0
    for i in range(3):
        emptyPot.acquire()
        # Fill up the pot
        for i in range(M):
            pot.append(i)
        fullPot.release()

        servings += 1
        print('-'*16)
        print("Served : ", servings)

def savage(index):
    food = -1
    startTime = time()
    for i in range(10):
        mutex.acquire()
        if len(pot) == 0:
            emptyPot.release()
            fullPot.acquire()
        food = pot.pop()
        mutex.release()

        print("Eating : ", food)
        sleep(0.2)
    runtimes[index] = time() - startTime

chef = threading.Thread(target=cook)
savages = []
savages.append(threading.Thread(target=savage, args=(0,)))
savages.append(threading.Thread(target=savage, args=(1,)))
savages.append(threading.Thread(target=savage, args=(2,)))

print("Cooking")
chef.start()
print("Eating")

startTime = time()

for s in savages:
    s.start()

for s in savages:
    s.join()

print("Total runtime:", time() - startTime)
print(runtimes)

chef.join()