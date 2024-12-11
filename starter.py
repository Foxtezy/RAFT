import logging
import random
import threading
from typing import List

from flask import Flask
from opyoid import Injector, InstanceBinding, SelfBinding

from data.common import NodeId
from data.settings import Settings
from data.state import MasterState, SlaveState
from data.storage import Storage
from service.candidate_client import CandidateClient
from service.heart import Heart
from service.master_client import MasterClient
from service.slave_client import SlaveClient
from service.slave_controller import SlaveController

app = Flask(__name__)

class Raft:
    injector: Injector
    storage: Storage

    def start(self, my_id: NodeId, node_ids: List[NodeId], storage: Storage):
        self.storage = storage
        self.injector = Injector(bindings=[
            InstanceBinding(Settings, bound_instance=Settings(heartbeat_timeout=0.2, election_timeout=lambda: random.uniform(0.5, 0.7))),
            InstanceBinding(SlaveState, bound_instance=SlaveState(my_id=my_id, storage=storage)),
            SelfBinding(CandidateClient),
            SelfBinding(MasterClient),
            SelfBinding(SlaveClient),
            SelfBinding(Heart),
            InstanceBinding(MasterState, bound_instance=MasterState(nodes=node_ids)),
        ])

        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        candidate_client = self.injector.inject(CandidateClient)
        candidate_client.daemon = True
        candidate_client.start()

        master_client = self.injector.inject(MasterClient)
        master_client.daemon = True
        master_client.start()

        SlaveController.register(app, route_base='/', init_argument={'state': self.injector.inject(SlaveState), 'heart': self.injector.inject(Heart)})
        host, port = my_id.split(':')
        port = int(port)
        threading.Thread(target=self.injector.inject(Heart).run, daemon=True).start()
        logging.getLogger('werkzeug').setLevel(logging.WARNING)
        app.run(host=host, port=port)

    def update_storage(self, storage_idx, func):
        self.injector.inject(SlaveClient).update_value_async(storage_idx, func)

