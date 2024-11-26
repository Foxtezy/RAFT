from abc import ABC
from typing import List, Any


class Observable(ABC):
    observer_funcs: List[Any]

    def __init__(self):
        super().__init__()
        self.observer_funcs = []

    def subscribe(self, observer_func):
        self.observer_funcs.append(observer_func)

    def notify_all(self, *args, **kwargs):
        for func in self.observer_funcs:
            func(*args, **kwargs)
