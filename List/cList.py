from threading import Semaphore, Thread
from random import randrange

# Concurrent list
class cList:
    def __init__(self):
        self.rMutex = Semaphore()
        self.wMutex = Semaphore()
        self.list = [0,0,0,0,0,0,0,0,0,0]
    
    def read(self, i):
        if i < len(self.list):
            self.rMutex.acquire()
            val = self.list[i]
            self.rMutex.release()
            return val
        else:
            return None
    
    def write(self, index, val):
        if index < len(self.list):
            self.rMutex.acquire()
            self.wMutex.acquire()
            self.list[index] = val
            print(self.list)
            self.wMutex.release()
            self.rMutex.release()

def reader(target, index):
    print("Read", target.read(index), "From", index)

def writer(target, index, val):
    target.write(index, val)
    print("Wrote", val, "To", index)

l = cList()

for i in range(5):
    Thread(target=writer, args=(l, randrange(0, 10), randrange(10, 20))).start()

for i in range(20):
    Thread(target=reader, args=(l, randrange(0, 10),)).start()

for i in range(5):
    Thread(target=writer, args=(l, randrange(0, 10), randrange(10, 20))).start()
