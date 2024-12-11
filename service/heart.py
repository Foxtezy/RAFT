import logging
from random import randint
from threading import Event

from data.settings import Settings
from utils import Observable


class Heart(Observable):
    settings: Settings
    event = Event()

    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings


    def run(self):
        while True:
            if self.event.wait(self.settings.election_timeout()):
                self.event.clear()
            else:
                logging.warning("TIMEOUT")
                self.notify_all()


    def reset(self):
        self.event.set()


