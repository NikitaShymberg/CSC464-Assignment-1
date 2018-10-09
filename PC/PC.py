# This is the classical producer consumer problem
import threading
import queue
import time

bufferLock = threading.Semaphore()
items = threading.Semaphore(0)
buffer = queue.Queue()

def produce(tokens):
    for token in tokens:
        bufferLock.acquire()
        print("Placing item number ", token)
        buffer.put(token)
        bufferLock.release()
        items.release()

def consume(last):
    for i in range(last):
        items.acquire()
        bufferLock.acquire()
        print("Got item number ", buffer.get())
        bufferLock.release()

startTime = time.clock()

tokens = [i for i in range(10000)]

producer1 = threading.Thread(target=produce, args=(tokens,))
producer2 = threading.Thread(target=produce, args=(tokens,))
consumer1 = threading.Thread(target=consume, args=(int(len(tokens)/2,)))
consumer2 = threading.Thread(target=consume, args=(int(len(tokens)/2,)))
consumer3 = threading.Thread(target=consume, args=(int(len(tokens)/2,)))
consumer4 = threading.Thread(target=consume, args=(int(len(tokens)/2,)))

producer1.start()
producer2.start()
consumer1.start()
consumer2.start()
consumer3.start()
consumer4.start()

producer1.join()
producer2.join()
consumer1.join()
consumer2.join()
consumer3.join()
consumer4.join()

print("Total runtime:", time.clock() - startTime)