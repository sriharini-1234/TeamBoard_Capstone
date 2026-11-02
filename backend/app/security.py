import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

SECRET = os.getenv("SECRET_KEY", "local-development-secret-key-change-me-123456")
ALGORITHM = "HS256"
RANK = {"viewer": 0, "member": 1, "admin": 2}
bearer = HTTPBearer(auto_error=False)

@dataclass
class User:
    id: str
    username: str
    role: str

def create_token(user_id: str, username: str, role: str) -> str:
    payload = {
        "sub": user_id, "username": username, "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=8)
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)

def verify_token(token: str) -> User:
    try:
        claims = jwt.decode(token, SECRET, algorithms=[ALGORITHM], options={"require": ["exp", "sub"]})
        role = claims.get("role")
        if role not in RANK:
            raise ValueError("Unknown role")
        return User(id=claims["sub"], username=claims.get("username", claims["sub"]), role=role)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def current_user(creds: HTTPAuthorizationCredentials | None = Depends(bearer)) -> User:
    if not creds:
        raise HTTPException(status_code=401, detail="Bearer token required")
    return verify_token(creds.credentials)

def require_role(minimum: str):
    def check(user: User = Depends(current_user)):
        if RANK[user.role] < RANK[minimum]:
            raise HTTPException(status_code=403, detail="Forbidden: insufficient role")
        return user
    return check
