from threading import Thread
from queue import Queue

class ThreadedTask(Thread):
    def __init__(self, thread_queue):
        super().__init__()

        self.queue = thread_queue
        
    def process_incoming_tasks(self, ):
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                print(msg)
            except Queue.Empty:
                pass