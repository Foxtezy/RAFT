import logging
import threading

from batteries import SyncString
from data.common import NodeId
from data.settings import Settings
from data.storage import Storage
from starter import Raft

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S')

    raft = Raft()
    string = SyncString(raft, 1, 'aboba')
    threading.Thread(target=lambda: raft.start(my_id=NodeId("127.0.0.1:1111"), node_ids=[NodeId("127.0.0.1:1111"), NodeId("127.0.0.1:2222"), NodeId("127.0.0.1:3333")],
               storage=Storage({1: string}), settings=Settings(timeout=5000)), daemon=True).start()

    while True:
        val = input("Enter your value: ")
        if val == "g":
            print(string.get())
        else:
            string.update(val)

