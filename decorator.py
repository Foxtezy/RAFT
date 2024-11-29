from abc import ABC

from data.storage import Storage
from starter import Raft


class SyncObject(ABC):
    _raft: Raft

    def __init__(self, raft: Raft):
        self._raft = raft




def replicated(func):
    def wrapper(self, *args, **kwargs):
        if isinstance(self, SyncObject):
            def curried(new_self):
                return func(new_self, *args, **kwargs)
            storage_idx = None
            for k, v in self._raft.storage.items():
                if v is self:
                    storage_idx = k
                    break
            self._raft.update_storage(storage_idx, curried)

    return wrapper