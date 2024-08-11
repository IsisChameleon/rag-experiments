from typing import Dict

from pydantic import BaseModel


class User(BaseModel):
    id: int
    internal_id: str
    email: str
    provider_identities: Dict[str, str]
    provider_tokens: Dict[str, Dict[str, str]]