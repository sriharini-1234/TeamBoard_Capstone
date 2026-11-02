from fastapi import APIRouter, HTTPException
from ..schemas import LoginRequest, UserOut
from ..security import create_token

router = APIRouter()
# Demo-only users. Change passwords and use a real user database before production.
USERS = {
    "viewer": {"id": "u1", "password": "viewer123", "role": "viewer"},
    "member": {"id": "u2", "password": "member123", "role": "member"},
    "admin": {"id": "u3", "password": "admin123", "role": "admin"},
}

@router.post("/login", response_model=UserOut)
def login(data: LoginRequest):
    user = USERS.get(data.username)
    if not user or user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_token(user["id"], data.username, user["role"])
    return UserOut(id=user["id"], username=data.username, role=user["role"], access_token=token)
