from typing import List

from opyoid import Injector, ClassBinding, InstanceBinding, SelfBinding

from data.common import NodeId
from data.settings import Settings
from data.state import MasterState, SlaveState
from data.storage import Storage
from decorator import SyncObject
from service.candidate_client import CandidateClient
from service.master_client import MasterClient
from service.slave_client import SlaveClient
from service.slave_controller import SlaveController


class Raft:
    injector: Injector

    def start(self, my_id: NodeId, node_ids: List[NodeId], storage: Storage, settings: Settings):
        self.injector = Injector(bindings=[
            InstanceBinding(Settings, bound_instance=settings),
            InstanceBinding(SlaveState, bound_instance=SlaveState(my_id=my_id, storage=storage)),
            SelfBinding(CandidateClient),
            SelfBinding(MasterClient),
            SelfBinding(SlaveClient),
            SelfBinding(SlaveController),
            InstanceBinding(MasterState, bound_instance=MasterState(nodes=node_ids)),
        ])
        slave_controller = self.injector.inject(SlaveController)
        slave_controller.run_flask()

        candidate_client = self.injector.inject(CandidateClient)
        candidate_client.start()

        master_client = self.injector.inject(MasterClient)
        master_client.start()

    def update_storage(self, storage_idx, func):
        self.injector.inject(SlaveClient).update_value_async(storage_idx, func)

