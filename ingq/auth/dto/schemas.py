from pydantic import BaseModel
from auth.domain.role import Role


class AuthToken(BaseModel):
    access_token: str
    refresh_token: str
    token_expires_in: int


class CurrentUser(BaseModel):
    id: str
    role: Role
