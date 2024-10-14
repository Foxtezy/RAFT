from threading import Thread
from data.rpc import AppendEntries
from data.state import MasterState, SlaveState, Role
import requests


class MasterClient(Thread):
    master_state: MasterState
    slave_state: SlaveState

    def __init__(self, master_state: MasterState, slave_state: SlaveState):
        super().__init__()
        self.slave_state = slave_state
        self.master_state = master_state

    def run(self):
        pass

    def update_nodes(self):
        for node_id, next_idx in self.master_state.next_index.copy():
            # concurrency
            resp = requests.post(url = f"{node_id}/append_entries",
                          json = AppendEntries(
                                term=self.slave_state.current_term,
                                leader_id=self.slave_state.my_id,
                                prev_log_index=next_idx-1,
                                prev_log_term=self.slave_state.log[next_idx-1].term,
                                entries=self.slave_state.log[next_idx:],
                                leader_commit=self.slave_state.commit_index
                          ).__dict__)
            if resp.json()['success']:
                self.master_state.next_index[node_id] = len(self.slave_state.log)
                self.master_state.match_index[node_id] = self.slave_state.commit_index
            else:
                if resp.json()['term'] > self.slave_state.current_term:
                    self.slave_state.role = Role.SLAVE
                else:
                    self.master_state.next_index[node_id] -= 1