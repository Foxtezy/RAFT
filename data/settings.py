from dataclasses import dataclass
from typing import Callable


@dataclass
class Settings:
    heartbeat_timeout: float
    election_timeout: Callable[[], float]
