from abc import ABC

from starter import Raft
import dill


class SyncObject(ABC):
    _raft: Raft
    storage_idx: int

    def __init__(self, raft: Raft, storage_idx: int):
        self._raft = raft
        self.storage_idx = storage_idx




def replicated(func):
    def wrapper(self, *args, **kwargs):
        if type(self) == SyncObject:
            ret = func(self, *args, **kwargs)
            def curried(new_self):
                return func(new_self, *args, **kwargs)
            self._raft.update_storage(self.storage_idx, curried)
            return ret

    return wrapper