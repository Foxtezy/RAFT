import dill
import requests

from data.state import SlaveState


class SlaveClient:
    state: SlaveState

    def __init__(self, state: SlaveState):
        self.state = state

    def update_value_async(self, new_value):
        requests.post(url=f"{self.state.leader_id}/client_update", json={'value': dill.dumps(new_value)})
