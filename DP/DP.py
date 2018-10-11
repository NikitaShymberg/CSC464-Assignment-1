from threading import Semaphore, Thread
import queue
import time
from random import randint

state = ['thinking'] * 5
canEat = [Semaphore(value=0) for i in range(5)]
mutex = Semaphore()

runtimes = [0 for i in range(5)]

def right(i):
    return(i+1) % 5

def left(i):
    return i

def getFork(i):
    mutex.acquire()
    state[i] = 'hungry'
    print(i, "is hungry")
    test(i)
    mutex.release()
    canEat[i].acquire()

def putForkDown(i):
    mutex.acquire()
    state[i] = 'thinking'
    print(i, "is thinking")
    # Let those beside me know that I'm done eating
    test(right(i))
    test(left(i))
    mutex.release() 

def test(i):
    if state[i] == 'hungry' and state[left(i)] != 'eating' and state[right(i)] != 'eating':
        # Philosopher[i] can eat
        state[i] = 'eating'
        print(i, "is eating")
        canEat[i].release()

def philosoper(i):
    startTime = time.time()
    for j in range(2):
        getFork(i)
        time.sleep(0.2)
        putForkDown(i)
    runtimes[i] = time.time() - startTime

philosophers = [Thread(target=philosoper, args=(i,)) for i in range(5)]

startTime = time.time()

for philosoper in philosophers:
    philosoper.start()

for philosoper in philosophers:
    philosoper.join()

print("Total runtime:", time.time() - startTime)
print(runtimes)