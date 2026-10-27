from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel, Field, EmailStr, field_validator

import os, json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise RuntimeError("API_KEY not found. Check your .env file.")

app = FastAPI()

def check_key(x_api_key: str | None = Header(default=None)):
    if not API_KEY or x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )


default_users = [
    {"id": 1, "user_name": "GodFather", "email": "francisford@coppola.com", "password": "test1234"},
    {"id": 2, "user_name": "Neuromancer", "email": "william@gibson.com", "password": "test1234"},
    {"id": 3, "user_name": "Hobbit", "email": "jrr@tolkien.com", "password": "test1234"},
    {"id": 4, "user_name": "Foundation", "email": "isaac@asimov.com", "password": "test1234"},
]

def load_users():
    if os.path.exists("movies.json"):
        try:
            with open("movies.json", "r", encoding="utf-8") as fp:
                data = json.load(fp)
                if data:
                    return data
        except json.JSONDecodeError:
            pass
    return default_users

users = load_users()

def save_users():
    with open("movies.json", "w", encoding="utf-8") as fp:
        json.dump(users, fp, ensure_ascii=False, indent=4)


class User(BaseModel):
    user_name: str = Field(min_length=5)
    email: EmailStr
    password: str = Field(min_length=3)

    @field_validator("user_name", "password", mode="before")
    @classmethod
    def reject_empty_or_whitespace(cls, value):
        if isinstance(value, str) and not value.strip():
            raise ValueError("This field cannot be empty")
        return value

@app.post("/users/register", status_code=201, dependencies=[Depends(check_key)])
def add_new_user(user: User):
    try:
        new_id = max((m["id"] for m in users), default=0) + 1
        new_user = {"id":new_id, "user_name":user.user_name, "email":user.email, "password": user.password}
        users.append(new_user)
        # Store the user on database instead
        save_users()
        print(f"✅ User '{user.user_name}' registered successfully! (201 Created)")
        return new_user
    except Exception as error:
        print(f"❌ Error registering user: {error}")
        raise
