import logging
import threading
from time import sleep

from batteries import SyncString, SyncDict
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
    data = SyncDict(raft)
    threading.Thread(target=lambda: raft.start(my_id=NodeId("127.0.0.1:5555"), node_ids=[NodeId("127.0.0.1:1111"), NodeId("127.0.0.1:2222"), NodeId("127.0.0.1:3333"), NodeId("127.0.0.1:4444"), NodeId("127.0.0.1:5555")],
               storage=Storage({1: data}), settings=Settings(timeout=1000)), daemon=True).start()


    while True:
        val = input("Enter your value: ")
        if val == "g":
            print(data)
        else:
            data[val.split(' ')[0]] = val.split(' ')[1]

