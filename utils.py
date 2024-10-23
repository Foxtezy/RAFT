from abc import ABC, abstractmethod
from typing import List, Any


class Observable(ABC):
    observer_funcs: List[Any] = []

    def subscribe(self, observer_func):
        self.observer_funcs.append(observer_func)

    def notify_all(self, *args, **kwargs):
        for func in self.observer_funcs:
            func(*args, **kwargs)
