import base64
from typing import Any

import dill
from flask import Response, jsonify
from flask_classful import FlaskView, route
from flask_pydantic import validate
from pydantic import BaseModel

from data.state import SlaveState, LogValue, Role


class SetRequest(BaseModel):
    key: Any
    value: Any


class ClientController(FlaskView):
    state: SlaveState

    def __init__(self, state: SlaveState):
        super().__init__()
        self.state = state

    @route('/get', methods=['GET'])
    def get(self):
        return jsonify({'sync_dict': str(self.state.storage[1])})

    @route('/set', methods=['POST'])
    @validate()
    def set(self, body: SetRequest):
        self.state.storage[1][body.key] = body.value
        if self.state.role.get_role() != Role.MASTER:
            return jsonify({'message': f'WARNING I AM NOT A MASTER. MASTER IS {self.state.leader_id}'}), 202
        else:
            return jsonify({'sync_dict': str(self.state.storage[1])})
