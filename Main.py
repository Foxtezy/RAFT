from batteries import SyncString
from data.common import NodeId
from data.settings import Settings
from data.storage import Storage
from starter import Raft

if __name__ == "__main__":

    raft = Raft()
    string = SyncString(raft, 1, 'aboba')
    raft.start(my_id=NodeId("127.0.0.1:1111"), node_ids=[NodeId("127.0.0.1:1111"), NodeId("127.0.0.1:2222")],
               storage=Storage({1: string}), settings=Settings(timeout=500))

