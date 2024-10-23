from opyoid import Injector, ClassBinding, InstanceBinding, SelfBinding

from data.settings import Settings
from data.state import MasterState, SlaveState
from service.candidate_client import CandidateClient
from service.master_client import MasterClient
from service.slave_client import SlaveClient
from service.slave_controller import SlaveController


class RaftStarter:
    injector: Injector

    def start(self, my_id, settings: Settings):
        self.injector = Injector(bindings=[
            InstanceBinding(Settings, bound_instance=settings),
            SelfBinding(CandidateClient),
            SelfBinding(MasterClient),
            SelfBinding(SlaveClient),
            SelfBinding(SlaveController),
            SelfBinding(MasterState),
            InstanceBinding(SlaveState, bound_instance=SlaveState(my_id=my_id)),
        ])
        slave_controller = self.injector.inject(SlaveController)
        slave_controller.run_flask()

        candidate_client = self.injector.inject(CandidateClient)
        candidate_client.start()

        master_client = self.injector.inject(MasterClient)
        master_client.start()
