from abc import ABC, abstractmethod
from typing import List

from domain.value_objects import DocumentId


class DocumentService(ABC):
    @abstractmethod
    def get_documents(self, access_token: str) -> List[DocumentId]: pass