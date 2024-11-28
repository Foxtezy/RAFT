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