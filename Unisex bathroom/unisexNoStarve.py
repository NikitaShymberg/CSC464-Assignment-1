# NOTE: starvation can happen
import threading
from time import sleep, time
from random import random


class Lightswitch:
    def __init__(self):
        self.counter = 0
        self.mutex = threading.Semaphore()

    def lock(self, sem):
        self.mutex.acquire()
        self.counter += 1
        if self.counter == 1:
            sem.acquire()
        self.mutex.release()

    def unlock(self, sem):
        self.mutex.acquire()
        self.counter -= 1
        if self.counter == 0:
            sem.release()
        self.mutex.release()


empty = threading.Semaphore()
maleSwitch = Lightswitch()
femaleSwitch = Lightswitch()
maleMultiplex = threading.Semaphore(3)
femaleMultiplex = threading.Semaphore(3)
turnstile = threading.Semaphore()


def female(i, waitTimes):
    startTime = time()
    turnstile.acquire()
    femaleSwitch.lock(empty)
    turnstile.release()

    femaleMultiplex.acquire()
    sleep(0.5)
    print("Female : ", i)
    waitTimes[i] = {"gender": "F", "time": time() - startTime}
    femaleMultiplex.release()
    femaleSwitch.unlock(empty)

def male(i, waitTimes):
    startTime = time()
    turnstile.acquire()
    maleSwitch.lock(empty)
    turnstile.release()

    maleMultiplex.acquire()
    sleep(0.5)
    print("Male : ", i)
    waitTimes[i] = {"gender": "M", "time": time() - startTime}
    maleMultiplex.release()
    maleSwitch.unlock(empty)

waitTimes = [{} for i in range(50)]
threads = []

for i in range(50):
    q = random()
    if q > 0.5:
        threads.append(threading.Thread(target=female, args=(i, waitTimes)))
    else:
        threads.append(threading.Thread(target=male, args=(i, waitTimes)))

startTime = time()

for t in threads:
    t.start()

for t in threads:
    t.join()

avgTimes = {"M": [], "F": []}

for i in waitTimes:
    avgTimes[i["gender"]].append(i["time"])

print("Average waiting time for men:", sum(avgTimes["M"])/len(avgTimes["M"]))
print("Average waiting time for women:", sum(avgTimes["F"])/len(avgTimes["F"]))
print("Total runtime:", time() - startTime)