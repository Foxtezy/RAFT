import base64
import logging
from time import sleep

import dill
import requests

from data.rpc import ClientUpdate
from data.state import SlaveState

headers = {'Content-type': 'application/json'}

class SlaveClient:
    state: SlaveState

    def __init__(self, state: SlaveState):
        self.state = state

    def update_value_async(self, storage_idx, func):
        if self.state.leader_id is None:
            while True:
                sleep(1)
                if self.state.leader_id is not None:
                    break

        try:
            requests.post(url=f"http://{self.state.leader_id}/client_update", data=ClientUpdate(
                            storage_idx=storage_idx,
                            value=base64.b64encode(dill.dumps(func)).decode()).model_dump_json(),
                      headers=headers)
        except Exception:
            logging.warning("COULD NOT SEND NEW VALUE TO %s", self.state.leader_id)
            sleep(1)
            self.update_value_async(storage_idx, func)



