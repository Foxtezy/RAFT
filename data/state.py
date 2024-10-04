from dataclasses import dataclass, field
from typing import Dict, Any, List

from data.common import NodeId

@dataclass
class LogValue:
    term: int
    value: Any

@dataclass
class SlaveState:
    current_term: int = 0
    leader_id: NodeId = None
    voted_for: NodeId = None
    log: List[LogValue] = field(default_factory=lambda: [LogValue(0, None)])
    commit_index: int = 0
    last_applied: int = 0

@dataclass
class MasterState:
    next_index: Dict[NodeId, int] = field(default_factory=dict)
    match_index: Dict[NodeId, int] = field(default_factory=dict)


