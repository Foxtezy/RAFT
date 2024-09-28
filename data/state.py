from dataclasses import dataclass, field
from typing import Any, List, Dict

from data.nodeId import NodeId


@dataclass
class SlaveState:
    current_term: int = 0
    voted_for: int = None
    log: List[Any] = field(default_factory=list)

    commit_index: int = 0
    last_applied: int = 0

@dataclass
class MasterState:
    next_index: Dict[NodeId, int] = field(default_factory=dict)
    match_index: Dict[NodeId, int] = field(default_factory=dict)

@dataclass
class NodeState:
    slave: SlaveState
    master: MasterState


