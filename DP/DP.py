from threading import Semaphore, Thread
import queue
import time
from random import randint

state = ['thinking'] * 5
canEat = [Semaphore(value=0) for i in range(5)]
mutex = Semaphore()

def right(i):
    return(i+1) % 5

def left(i):
    return i

def getFork(i):
    mutex.acquire()
    state[i] = 'hungry'
    print(i, "is hungry now")
    test(i)
    mutex.release()
    # Either let people on my left and right know that I need to be woken up
    # Or since I'm eating return to unknown
    canEat[i].acquire()

def putForkDown(i):
    mutex.acquire()
    state[i] = 'thinking'
    print(i, "is thinking now")
    # Let those beside me know that I'm done eating
    test(right(i))
    test(left(i))
    mutex.release() 

def test(i):
    if state[i] == 'hungry' and state[left(i)] != 'eating' and state[right(i)] != 'eating':
        # Philosopher[i] can eat
        state[i] = 'eating'
        print(i, "is eating now")
        canEat[i].release()

def philosoper(i):
    while(True):
        if(state[i] == 'thinking' and randint(0, 10000) > 9999):
            getFork(left(i))
            getFork(right(i))
            putForkDown(left(i))
            putForkDown(right(i))


philosophers = [Thread(target=philosoper, args=(i,)) for i in range(5)]
for philosoper in philosophers:
    philosoper.start()

while(True):
    time.sleep(5)
    print(".")