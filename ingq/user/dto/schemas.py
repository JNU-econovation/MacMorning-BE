from pydantic import BaseModel, EmailStr
from user.domain.provider import Provider
from datetime import datetime


# API 명세서 나오고 수정 필요
class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    nickname: str
    username: str
    phone_number: str


class OAuthSignUpRequest(BaseModel):
    pass


# API 명세서 나오고 수정 필요
class SignUpResponse(BaseModel):
    id: str
    email: EmailStr
    nickname: str
    profile_image: str
    username: str
    phone_number: str
    provider: Provider
    created_at: datetime
    updated_at: datetime


# API 명세서 나오고 수정 필요
class UserResponse(BaseModel):
    id: str
    email: EmailStr
    nickname: str
    profile_image: str
    username: str
    phone_number: str
    provider: Provider
