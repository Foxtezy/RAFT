import enum
import logging
from dataclasses import dataclass, field
from typing import Dict, Any, List

from pydantic import BaseModel

from data.common import NodeId
from data.storage import Storage
from utils import Observable


class LogValue(BaseModel):
    term: int
    storage_idx: int
    value: str # base64 string


class Role(enum.Enum):
    SLAVE = 0
    CANDIDATE = 1
    MASTER = 2


class RoleObservable(Observable):
    role: Role = Role.SLAVE

    def set_role(self, role: Role):
        if role != self.role:
            logging.info("ROLE CHANGED TO %s", role.name)
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
    log: List[LogValue] = field(default_factory=lambda: [LogValue(term=0, storage_idx=-1, value='')])
    commit_index: int = 0
    last_applied: int = 0


class MasterState:
    node_ids: List[NodeId]
    next_index: Dict[NodeId, int]
    match_index: Dict[NodeId, int]

    def __init__(self, nodes: List[NodeId]):
        self.node_ids = nodes
        self.next_index = {}
        self.match_index = {}
        self.init()

    # вызывается при смене роли на мастера
    def init(self, slave_state: SlaveState = None):
        for k in self.node_ids:
            self.next_index[k] = 1 if slave_state is None else len(slave_state.log)
            self.match_index[k] = 0





