import threading

class PCQueue:
    def __init__(self):
        self.queue = []
        self.size = 0
        self.active = True
        self.lock = threading.Lock()
        self.full = threading.Semaphore(0)
        self.empty = threading.Semaphore(10)

    def enqueue(self, item):
        self.empty.acquire()
        self.lock.acquire()
        self.queue.append(item)
        self.lock.release()
        self.full.release()

    def deque(self):
        self.full.acquire()
        self.lock.acquire()
        item = self.queue.pop(0)
        self.lock.release()
        self.empty.release()
        return item

    def isEmpty(self):
        self.lock.acquire()
        retVal = len(self.queue) == 0
        self.lock.release()
        return retVal

    def kill(self):
        self.active = False

    def isActive(self):
        return self.active
