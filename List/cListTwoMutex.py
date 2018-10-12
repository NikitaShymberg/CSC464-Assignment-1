from threading import Semaphore, Thread
from random import randrange
from time import clock, sleep

# Concurrent list
class cList:
    def __init__(self):
        self.rMutex = Semaphore()
        self.wMutex = Semaphore()
        self.list = [0,0,0,0,0,0,0,0,0,0]
        self.readers = 0
    
    def read(self, i, times, timesIndex):
        if i < len(self.list):
            startTime = clock()

            self.rMutex.acquire()
            self.readers += 1
            if self.readers == 1:
                self.wMutex.acquire()
            self.rMutex.release()

            val = self.list[i]
            # sleep(0.05)

            self.rMutex.acquire()
            self.readers -= 1
            if self.readers == 0:
                self.wMutex.release()
            self.rMutex.release()

            times[timesIndex] = clock() - startTime
            return val
        else:
            return None
    
    def write(self, index, val, times, timesIndex):
        startTime = clock()

        if index < len(self.list):
            self.wMutex.acquire()
            self.list[index] = val
            print(self.list)
            self.wMutex.release()
        times[timesIndex] = clock() - startTime

def reader(target, index, times, timesIndex):
    print("Read", target.read(index, times, timesIndex), "From", index)

def writer(target, index, val, times, timesIndex):
    target.write(index, val, times, timesIndex)
    print("Wrote", val, "To", index)

l = cList()

startTime = clock()
threads = []

readerTimes = [0 for i in range(30 * 50)]
writerTimes = [0 for i in range(5 * 50)]

for i in range(5 * 50):
    threads.append(Thread(target=writer, args=(l, randrange(0, 10), randrange(10, 20), writerTimes, i)))

for i in range(30 * 50):
    threads.append(Thread(target=reader, args=(l, randrange(0, 10), readerTimes, i)))

for t in threads:
    t.start()

for t in threads:
    t.join()

print("Total running time:", clock() - startTime, "seconds")
print("Average writer runtime:", sum(writerTimes)/len(writerTimes))
print("Average reader runtime:", sum(readerTimes)/len(readerTimes))