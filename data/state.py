import enum
from dataclasses import dataclass, field
from typing import Dict, Any, List

from data.common import NodeId
from data.storage import Storage
from utils import Observable


@dataclass
class LogValue:
    term: int
    storage_idx: int
    value: bytes


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
    storage: Storage
    role: RoleObservable = RoleObservable()
    current_term: int = 0
    leader_id: NodeId = None
    voted_for: NodeId = None
    log: List[LogValue] = field(default_factory=lambda: [LogValue(0, None)])
    commit_index: int = 0
    last_applied: int = 0


class MasterState:
    node_ids: List[NodeId]
    next_index: Dict[NodeId, int] = field(default_factory=dict)
    match_index: Dict[NodeId, int] = field(default_factory=dict)

    def __init__(self, nodes: List[NodeId]):
        self.node_ids = nodes
        self.init()

    # вызывается при смене роли на мастера
    def init(self, slave_state: SlaveState = None):
        for k in self.node_ids:
            self.next_index[k] = 1 if slave_state is None else len(slave_state.log)
            self.match_index[k] = 0





