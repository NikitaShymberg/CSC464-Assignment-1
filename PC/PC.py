# This is the classical producer consumer problem
import threading
import queue
import time

bufferLock = threading.Semaphore()
items = threading.Semaphore()
buffer = queue.Queue()

def produce(tokens):
    for token in tokens:
        # time.sleep(1) TODO: what
        bufferLock.acquire()
        print("Placing item number ", token)
        buffer.put(token)
        bufferLock.release()
        items.release()
#TODO: don't join this one?
def consume(last):
    while(True):
        items.acquire()
        bufferLock.acquire()
        token = buffer.get()
        print("Got item number ", token)
        bufferLock.release()
        items.release()
        if(token == last):
            break

tokens = [i for i in range(20)]

producer = threading.Thread(target=produce, args=(tokens,))
consumer = threading.Thread(target=consume, args=(len(tokens) - 1,))

print("Starting producer thread")
producer.start()
print("Starting consumer thread")
consumer.start()

producer.join()
consumer.join()

print("Done!")