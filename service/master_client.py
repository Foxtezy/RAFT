import math
from random import randint
from threading import Thread, Event
from time import sleep

from data.rpc import AppendEntries
from data.settings import Settings
from data.state import MasterState, SlaveState, Role
import requests
import logging


class MasterClient(Thread):
    master_state: MasterState
    slave_state: SlaveState
    settings: Settings
    event = Event()

    def __init__(self, master_state: MasterState, slave_state: SlaveState, settings: Settings):
        super().__init__()
        self.slave_state = slave_state
        self.master_state = master_state
        self.settings = settings

    def run(self):
        def notifier(role):
            if role == Role.MASTER:
                self.event.set()

        self.slave_state.role.subscribe(notifier)
        while True:
            self.event.clear()
            if self.slave_state.role.get_role() != Role.MASTER:
                self.event.wait()
                self.master_state.init(self.slave_state)
                logging.info(f"{self.slave_state.my_id} BECOME MASTER")
            self.update_nodes()
            sleep(self.settings.timeout / 1000)


    def update_nodes(self):
        success_num = 0
        for node_id, _ in self.master_state.next_index.copy():
            status = self.update_node(node_id)
            if self.slave_state.role.get_role() != Role.MASTER:
                return
            if status:
                success_num += 1
        if success_num >= math.ceil(len(self.master_state.next_index) / 2):
            self.slave_state.commit_index = len(self.slave_state.log) - 1

    """
        return True if success
    """
    def update_node(self, node_id):
        try:
            resp = requests.post(url=f"{node_id}/append_entries",
                             json=AppendEntries(
                                 term=self.slave_state.current_term,
                                 leader_id=self.slave_state.my_id,
                                 prev_log_index=self.master_state.next_index[node_id] - 1,
                                 prev_log_term=self.slave_state.log[self.master_state.next_index[node_id] - 1].term,
                                 entries=self.slave_state.log[self.master_state.next_index[node_id]:],
                                 leader_commit=self.slave_state.commit_index
                             ).__dict__)
            if resp.json()['success']:
                self.master_state.next_index[node_id] = len(self.slave_state.log)
                self.master_state.match_index[node_id] = self.slave_state.commit_index
                return True
            else:
                if resp.json()['term'] > self.slave_state.current_term:
                    self.slave_state.role.set_role(Role.SLAVE)
                    return False
                else:
                    self.master_state.next_index[node_id] -= 1
                    return self.update_node(node_id)

        except requests.Timeout and requests.ConnectionError:
            return False
