from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str
    password: str

class BookmarkCreate(BaseModel):
    url: str = Field(min_length=1, max_length=2048)

class PasswordReset(BaseModel):
    new_password: str = Field(min_length=8, max_length=128)
