import base64
import logging
from typing import Dict

import dill
from flask import Flask, request, Response
from flask_classful import FlaskView, route
from flask_pydantic import validate
from werkzeug.utils import redirect

from data.rpc import AppendEntries, AppendEntriesRes, RequestVote, RequestVoteRes, ClientUpdate
from data.state import SlaveState, Role, LogValue
from service.heart import Heart


class SlaveController(FlaskView):
    state: SlaveState
    heart: Heart
    app = Flask(__name__)

    def __init__(self, params: Dict):
        super().__init__()
        self.state = params['state']
        self.heart = params['heart']
        self.heart.subscribe(lambda: self.state.role.set_role(Role.CANDIDATE))


    @route('/append_entries', methods=['POST'])
    @validate()
    def append_entries(self, body: AppendEntries):
        logging.debug("append_entries from %s, body [%s]", request.remote_addr, body)
        append = body

        self.heart.reset()
        if append.term > self.state.current_term or self.state.role.get_role() == Role.CANDIDATE:
            self.state.role.set_role(Role.SLAVE)

        if append.term < self.state.current_term or append.prev_log_index >= len(self.state.log) or self.state.log[append.prev_log_index].term != append.prev_log_term:
            return AppendEntriesRes(term=self.state.current_term, success=False)


        if append.prev_log_index + 1 < len(self.state.log):
            del self.state.log[append.prev_log_index + 1 : len(self.state.log)]

        self.state.log.extend(append.entries)
        self.state.current_term = append.term
        self.state.leader_id = append.leader_id

        if append.leader_commit > self.state.commit_index:
            for i in range(self.state.commit_index + 1, append.leader_commit + 1):
                func = dill.loads(base64.b64decode(self.state.log[i].value))
                func(self.state.storage[self.state.log[i].storage_idx])
            self.state.commit_index = append.leader_commit

        return AppendEntriesRes(term=self.state.current_term, success=True)



    @route('/request_vote', methods=['POST'])
    @validate()
    def request_vote(self, body: RequestVote):
        logging.debug("request_vote from %s, body [%s]", request.remote_addr, body)
        req = body
        self.heart.reset()
        if req.term < self.state.current_term:
            return RequestVoteRes(term=self.state.current_term, vote_granted=False)

        if self.state.voted_for is None or self.state.voted_for == req.candidate_id:
            if len(self.state.log) - 1 <= req.last_log_index and self.state.log[len(self.state.log) - 1].term <= req.last_log_term:
                self.state.voted_for = req.candidate_id
                return RequestVoteRes(term=self.state.current_term, vote_granted=True)

        return RequestVoteRes(term=self.state.current_term, vote_granted=False)

    @route('/client_update', methods=['POST'])
    @validate()
    def client_update(self, body: ClientUpdate):
        logging.debug("client_update from %s, body [%s]", request.remote_addr, body)
        data = body
        if self.state.role.get_role() != Role.MASTER:
            return redirect(f"{self.state.leader_id}/client_update")
        else:
            self.state.log.append(LogValue(term=self.state.current_term, storage_idx=data.storage_idx, value=data.value))
            return Response(status=200)




