from typing import Literal
from pydantic import BaseModel, Field

Role = Literal["viewer", "member", "admin"]
Status = Literal["todo", "doing", "done"]
Priority = Literal["low", "medium", "high"]

class LoginRequest(BaseModel):
    username: str = Field(min_length=2, max_length=40)
    password: str = Field(min_length=4, max_length=100)

class UserOut(BaseModel):
    id: str
    username: str
    role: Role
    access_token: str
    token_type: str = "bearer"

class TicketCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(default="", max_length=2000)
    priority: Priority = "medium"

class TicketUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=120)
    description: str | None = Field(default=None, max_length=2000)
    status: Status | None = None
    priority: Priority | None = None

class TicketOut(TicketCreate):
    id: int
    status: Status = "todo"
    owner: str

class TicketStats(BaseModel):
    todo: int
    doing: int
    done: int
