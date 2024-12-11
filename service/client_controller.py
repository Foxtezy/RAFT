import base64

import dill
from flask import Response, jsonify
from flask_classful import FlaskView, route
from flask_pydantic import validate
from pydantic import BaseModel

from data.state import SlaveState, LogValue, Role


class SetRequest(BaseModel):
    key: str
    value: str


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
            return jsonify({'message': 'WARNING I AM NOT MASTER'}), 202
        else:
            return jsonify({'sync_dict': str(self.state.storage[1])})
