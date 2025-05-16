from fastapi import HTTPException
import hashlib
from .models import verify_user

# Mock user database
users_db = {
    "admin": {
        "username": "admin",
        "password_hash": hashlib.sha256("adminpass".encode()).hexdigest()
    },
    "user1": {
        "username": "user1",
        "password_hash": hashlib.sha256("user123".encode()).hexdigest()
    }
}

def verify_user(username: str, password: str) -> bool:
    user = users_db.get(username)
    if not user:
        return False
    return user["password_hash"] == hashlib.sha256(password.encode()).hexdigest()
