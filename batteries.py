from typing import Generic, TypeVar

from decorator import SyncObject, replicated
from starter import Raft


class SyncString(SyncObject):
    string: str

    def __init__(self, raft: Raft, string: str):
        super().__init__(raft)
        self.string = string

    @replicated
    def update(self, new):
        self.string = new

    def get(self):
        return self.string

K = TypeVar('K')
V = TypeVar('V')

class SyncDict(Generic[K, V], SyncObject):
    __data: dict[K, V]

    def __init__(self, raft: Raft):
        super().__init__(raft)
        self.__data = {}

    def __getitem__(self, key):
        return self.__data[key]

    @replicated
    def __setitem__(self, key, value):
        self.__data[key] = value

    @replicated
    def __delitem__(self, key):
        del self.__data[key]

    def __str__(self):
        return self.__data.__str__()