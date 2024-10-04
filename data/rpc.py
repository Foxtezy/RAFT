from typing import Any, List

from attr import dataclass

from data.common import NodeId
from data.state import LogValue


@dataclass(frozen=True)
class AppendEntries:
    term: int
    leader_id: NodeId
    prev_log_index: int
    prev_log_term: int
    entries: List[LogValue]
    leader_commit: int

@dataclass(frozen=True)
class AppendEntriesRes:
    term: int
    success: bool

@dataclass(frozen=True)
class RequestVote:
    term: int
    candidate_id: NodeId
    last_log_index: int
    last_log_term: int

@dataclass(frozen=True)
class RequestVoteRes:
    term: int
    voteGranted: bool