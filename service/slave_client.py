import requests

from data.state import SlaveState


class SlaveClient:
    state: SlaveState

    def __init__(self, state: SlaveState):
        self.state = state

    def update_value(self, new_value):
        #должны возвращать управление только после обновления
        requests.post(url=f"{self.state.leader_id}/client_update", json={'value': new_value})
