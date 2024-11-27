from decorator import SyncObject, replicated
from starter import Raft


class SyncString(SyncObject):
    string: str

    def __init__(self, raft: Raft, sync_id: int, string: str):
        super().__init__(raft, sync_id)
        self.string = string

    @replicated
    def update(self, new):
        self.string = new

    def get(self):
        return self.string