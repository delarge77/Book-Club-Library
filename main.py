import json
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException, status
from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError
from database import get_all_catalogued_books, get_catalogued_book_by_id
from models import Member, LoginRequest, TokenResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not configured")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

bearer_scheme = HTTPBearer()

if not API_KEY:
    raise RuntimeError("API_KEY not found. Check your .env file.")

app = FastAPI()
password_hash = PasswordHash.recommended()


def check_key(x_api_key: str | None = Header(default=None)):
    if not API_KEY or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

def create_access_token(user_id: int) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expires_at
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    token = credentials.credentials

    try:
        payload = jwt.decode( token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if not user_id:
            raise ValueError("Missing subject")

    except (InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})

    user = next((m for m in members if str(m["id"]) == user_id), None)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"})
    return user


default_members = []


def load_members():
    if os.path.exists("members.json"):
        try:
            with open("members.json", "r", encoding="utf-8") as fp:
                data = json.load(fp)
                if data:
                    return data
        except json.JSONDecodeError:
            pass
    return default_members


members = load_members()


def save_users():
    with open("members.json", "w", encoding="utf-8") as fp:
        json.dump(members, fp, ensure_ascii=False, indent=4)


@app.post("/members/register", status_code=201, dependencies=[Depends(check_key)])
def add_new_user(member: Member):
    try:
        new_id = max((m["id"] for m in members), default=0) + 1
        hashed_password = password_hash.hash(member.password)
        new_user = {
            "id": new_id,
            "user_name": member.user_name,
            "email": member.email,
            "password": hashed_password,
        }
        members.append(new_user)
        # Store the user on database instead
        save_users()
        print(f"✅ User '{member.user_name}' registered successfully! (201 Created)")
        return {"id": new_id, "user_name": member.user_name, "email": member.email}
    except Exception as error:
        print(f"Error registering user: {error}")
        raise HTTPException(status_code=500, detail="Could not register user")


@app.post("/members/login", response_model=TokenResponse, status_code=201, dependencies=[Depends(check_key)])
def login(member: LoginRequest):
    user = next((m for m in members if m["user_name"] == member.user_name), None)
    if user is None or not password_hash.verify(member.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password")

    access_token = create_access_token(user["id"])
    print("Access Token: {access_token}")
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/members/me", status_code=201)
def get_my_profile(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "user_name": current_user["user_name"],
        "email": current_user["email"]
    }

@app.get("/books")
def list_catalogued_books():
    """Return all books in the library catalogue."""
    return get_all_catalogued_books()


@app.get("/books/{book_id}")
def list_catalogued_book(book_id: int):
    """Return one book using book_id"""
    book = get_catalogued_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
