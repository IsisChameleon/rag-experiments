"""
Authentication module for multi-provider OAuth flow and user management.
"""

from http.client import HTTPException, status
from typing import Annotated

import jwt
from application.interfaces.document_service import DocumentService
from application.interfaces.event_bus import EventBus
from application.interfaces.oauth_service import OAuthService
from application.services.user_service import UserService
from application.use_cases.handle_document_source_authentication import (
    HandleDocumentSourceAuthentication,
)
from containers import AppContainer
from dependency_injector.wiring import Provide, inject
from domain.models.user import User
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """Retrieve the current user based on the provided token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.JWTError:
        raise credentials_exception
    
    user = await UserService.get_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# @router.get("/oauth/init/{provider}")
# async def init_oauth(provider: str):
#     """Initiate OAuth flow for the specified provider."""
#     oauth_url = get_oauth_url(provider)
#     return {"url": oauth_url}

@router.post("/callback/{provider}")
@inject
async def oauth_callback(
    provider: str,
    code: str,
    current_user: User = Depends(get_current_user),
    oauth_service: OAuthService = Depends(Provide[AppContainer.oauth_service_factory]),
    document_source: DocumentService = Depends(Provide[AppContainer.document_source_factory]),
    event_bus: EventBus = Depends(Provide[AppContainer.event_bus])
):
    """Handle the OAuth callback for the specified provider."""
    
    # Create the use case with injected dependencies
    handle_auth = HandleDocumentSourceAuthentication(
        oauth_service=oauth_service,
        document_retrieval_service=document_source,
        event_bus=event_bus
    )
    
    # Handle the callback
    result = handle_auth.handle_callback(code, current_user)
    
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={"message": "Authentication request accepted", "result": result}
    )

    
    # Cod

# async def refresh_tokens_middleware(request: Request, call_next):
#     """Middleware to refresh OAuth tokens when necessary."""
#     response = await call_next(request)
#     user = request.state.user
#     if user:
#         for provider, token_data in user.provider_tokens.items():
#             if token_needs_refresh(token_data):
#                 new_token_data = await refresh_token(provider, token_data)
#                 await UserService.update_provider_token(user.id, provider, new_token_data)
#     return response

