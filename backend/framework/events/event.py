from abc import ABC
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Event(ABC):
    payload: Dict[str, Any]

    def get_name(self) -> str:
        return self.__class__.__name__
