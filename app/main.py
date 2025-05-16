from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import secrets

from .models import create_db_and_tables, verify_user, create_user, get_user_by_username

app = FastAPI()
valid_tokens = {}

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/register")
async def register(data: RegisterRequest):
    if get_user_by_username(data.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    create_user(data.username, data.password)
    return {"detail": "User created"}

@app.post("/login")
async def login(data: LoginRequest):
    if verify_user(data.username, data.password):
        token = secrets.token_hex(16)
        valid_tokens[token] = data.username
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.url.path in ["/login", "/register", "/docs", "/openapi.json"]:
        return await call_next(request)
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"detail": "Missing token"})
    token = auth_header.split(" ")[1]
    if token not in valid_tokens:
        return JSONResponse(status_code=403, content={"detail": "Invalid or expired token"})
    request.state.user = valid_tokens[token]
    return await call_next(request)

@app.get("/user/preferences")
async def get_preferences(request: Request):
    return {"username": request.state.user, "theme": "dark"}

@app.get("/user/search/{username}")
async def search_user(username: str, request: Request):
    user = get_user_by_username(username)
    return {"username": username, "status": "active" if user else "not found"}
