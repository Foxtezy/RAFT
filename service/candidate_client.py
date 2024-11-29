import math
from threading import Thread, Event

import requests

from data.rpc import RequestVote
from data.settings import Settings
from data.state import MasterState, SlaveState, Role

headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

class CandidateClient(Thread):
    slave_state: SlaveState
    master_state: MasterState
    event = Event()
    settings: Settings

    def __init__(self, master_state: MasterState, slave_state: SlaveState, settings: Settings):
        super().__init__()
        self.slave_state = slave_state
        self.master_state = master_state
        self.settings = settings

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
            self.slave_state.voted_for = None
            while self.slave_state.role.get_role() == Role.CANDIDATE:
                self.request_vote()

    def request_vote(self):
        votes_count = 0
        for node_id, _ in self.master_state.next_index.items():
            try:
                resp = requests.post(url = f"http://{node_id}/request_vote",
                          data = RequestVote(
                              term=self.slave_state.current_term,
                              candidate_id=self.slave_state.my_id,
                              last_log_index=len(self.slave_state.log)-1,
                              last_log_term=self.slave_state.log[len(self.slave_state.log)-1].term
                          ).model_dump_json(), headers=headers, timeout=(self.settings.timeout / 1000) / 2)
                if resp.json()['vote_granted']:
                    votes_count += 1
                if resp.json()['term'] > self.slave_state.current_term:
                    self.slave_state.current_term = resp.json()['term']
            except requests.Timeout and requests.ConnectionError:
                pass

        if votes_count >= math.ceil(len(self.master_state.next_index) / 2):
            self.slave_state.role.set_role(Role.MASTER)



