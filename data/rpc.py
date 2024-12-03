from typing import List

from pydantic import BaseModel

from data.common import NodeId
from data.state import LogValue


class AppendEntries(BaseModel):
    term: int
    leader_id: NodeId
    prev_log_index: int
    prev_log_term: int
    entries: List[LogValue]
    leader_commit: int

    def __str__(self) -> str:
        return f"term={self.term} leader_id={self.leader_id} prev_log_index={self.prev_log_index} prev_log_term={self.prev_log_term} entries={[str(item) for item in self.entries]} leader_commit={self.leader_commit}"


class AppendEntriesRes(BaseModel):
    term: int
    success: bool

class RequestVote(BaseModel):
    term: int
    candidate_id: NodeId
    last_log_index: int
    last_log_term: int

class RequestVoteRes(BaseModel):
    term: int
    vote_granted: bool

class ClientUpdate(BaseModel):
    storage_idx: int
    value: str