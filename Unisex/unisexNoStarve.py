# NOTE: starvation can happen
import threading
from time import sleep
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


def female(i):
	turnstile.acquire()
	femaleSwitch.lock(empty)
	turnstile.release()
	femaleMultiplex.acquire()
	print("Female : ", i)
	sleep(0.5)
	femaleMultiplex.release()
	femaleSwitch.unlock(empty)

def male(i):
	turnstile.acquire()
	maleSwitch.lock(empty)
	turnstile.release()
	maleMultiplex.acquire()
	sleep(0.5)
	print("Male : ", i)
	maleMultiplex.release()
	maleSwitch.unlock(empty)

maleCounter = 0
femaleCounter = 0

for i in range(50):
    sleep(0.2)
    q = random() #TODO: wtf this is odd
    if q > 0.5:
        print(q)
        femaleCounter += 1
        threading.Thread(target=female, args=(femaleCounter,)).start()
    else:
        maleCounter += 1
        threading.Thread(target=male, args=(maleCounter,)).start()
