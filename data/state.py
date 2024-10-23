import enum
from dataclasses import dataclass, field
from typing import Dict, Any, List

from data.common import NodeId
from utils import Observable


@dataclass
class LogValue:
    term: int
    value: Any


class Role(enum.Enum):
    SLAVE = 0
    CANDIDATE = 1
    MASTER = 2


class RoleObservable(Observable):
    role: Role = Role.SLAVE

    def set_role(self, role: Role):
        self.role = role
        self.notify_all(role)

    def get_role(self) -> Role:
        return self.role

@dataclass
class SlaveState:
    my_id: NodeId
    role: RoleObservable = RoleObservable()
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



