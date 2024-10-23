import math
from threading import Thread, Event
from time import sleep

import requests

from data.rpc import RequestVote
from data.state import MasterState, SlaveState, Role


class CandidateClient(Thread):
    slave_state: SlaveState
    master_state: MasterState
    event = Event()

    def __init__(self, master_state: MasterState, slave_state: SlaveState):
        super().__init__()
        self.slave_state = slave_state
        self.master_state = master_state

    def run(self):
        def notifier(role):
            if role == Role.CANDIDATE:
                self.event.set()

        self.slave_state.role.subscribe(notifier)
        while True:
            self.event.clear()
            if self.slave_state.role.get_role() != Role.CANDIDATE:
                self.event.wait()
            self.slave_state.current_term += 1
            while self.slave_state.role.get_role() == Role.CANDIDATE:
                self.request_vote()

    def request_vote(self):
        votes_count = 0
        for node_id, _ in self.master_state.next_index:
            try:
                resp = requests.post(url = f"{node_id}/request_vote",
                          json = RequestVote(
                              term=self.slave_state.current_term,
                              candidate_id=self.slave_state.my_id,
                              last_log_index=len(self.slave_state.log)-1,
                              last_log_term=self.slave_state.log[len(self.slave_state.log)-1].term
                          ).__dict__, timeout=0.5)
                if resp.json()['vote_granted']:
                    votes_count += 1
                if resp.json()['term'] > self.slave_state.current_term:
                    self.slave_state.current_term = resp.json()['term']
            except requests.Timeout and requests.ConnectionError:
                pass

        if votes_count >= math.ceil(len(self.master_state.next_index) / 2):
            self.slave_state.role.set_role(Role.MASTER)



