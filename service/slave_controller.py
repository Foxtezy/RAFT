from flask import Flask, request, jsonify
from werkzeug.utils import redirect

from data.rpc import AppendEntries, AppendEntriesRes, RequestVote, RequestVoteRes
from data.state import SlaveState, Role, LogValue
from service.heart import Heart


class SlaveController:
    state: SlaveState
    heart: Heart
    app = Flask(__name__)

    def __init__(self, state: SlaveState, heart: Heart):
        self.state = state
        self.heart = heart

    def run_flask(self):
        self.app.run(debug=True, use_reloader=False)

    @app.route('/append_entries', methods=['POST'])
    def append_entries(self):
        data = request.json
        append = AppendEntries(**data)
        self.heart.reset()
        if append.term < self.state.current_term or append.prev_log_index >= len(self.state.log) or self.state.log[append.prev_log_index].term != append.prev_log_term:
            return jsonify(AppendEntriesRes(term=self.state.current_term, success=False))

        if append.prev_log_index + 1 < len(self.state.log):
            del self.state.log[append.prev_log_index + 1 : len(self.state.log)]

        self.state.log.extend(append.entries)
        self.state.current_term = append.term
        self.state.leader_id = append.leader_id

        if append.leader_commit > self.state.commit_index:
            self.state.commit_index = append.leader_commit if append.leader_commit < len(self.state.log) - 1 else len(self.state.log) - 1

        return jsonify(AppendEntriesRes(term=self.state.current_term, success=True))



    @app.route('/request_vote', methods=['POST'])
    def request_vote(self):
        data = request.json
        req = RequestVote(**data)
        self.heart.reset()
        if req.term < self.state.current_term:
            return jsonify(RequestVoteRes(self.state.current_term, False))

        if self.state.voted_for is None or self.state.voted_for == req.candidate_id:
            if len(self.state.log) - 1 <= req.last_log_index and self.state.log[len(self.state.log) - 1].term <= req.last_log_term:
                return jsonify(RequestVoteRes(self.state.current_term, True))

        return jsonify(RequestVoteRes(self.state.current_term, False))

    @app.route('/client_update', methods=['POST'])
    def client_update(self):
        data = request.json
        if self.state.role != Role.MASTER:
            return redirect(f"{self.state.leader_id}/client_update")
        else:
            self.state.log.append(LogValue(self.state.current_term, data["value"]))




