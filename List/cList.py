from threading import Semaphore

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
            self.wMutex.release()
            self.rMutex.release()