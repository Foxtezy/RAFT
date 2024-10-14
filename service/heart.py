from abc import ABC, abstractmethod
from random import randint
from threading import Event, Thread

class Observer(ABC):
    @abstractmethod
    def notify(self):
        pass

class Heart(Thread):
    timeout: int
    event = Event()
    observers: Observer

    def __init__(self, timeout: int):
        super().__init__()
        self.timeout = timeout


    def run(self):
        while True:
            if self.event.wait((self.timeout + randint(-self.timeout // 10, self.timeout // 10)) / 1000):
                self.event.clear()
            else:
                self.observers.notify()


    def reset(self):
        self.event.set()


