from fastapi import FastAPI, HTTPException, Header, Depends
from pwdlib import PasswordHash
from models import Member
import os, json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise RuntimeError("API_KEY not found. Check your .env file.")

app = FastAPI()
password_hash = PasswordHash.recommended()

def check_key(x_api_key: str | None = Header(default=None)):
    if not API_KEY or x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )


default_members = [
    {"id": 1, "user_name": "GodFather", "email": "francisford@coppola.com", "password": "test1234"},
    {"id": 2, "user_name": "Neuromancer", "email": "william@gibson.com", "password": "test1234"},
    {"id": 3, "user_name": "Hobbit", "email": "jrr@tolkien.com", "password": "test1234"},
    {"id": 4, "user_name": "Foundation", "email": "isaac@asimov.com", "password": "test1234"},
]

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
        new_user = {"id":new_id, "user_name":member.user_name, "password":hashed_password}
        members.append(new_user)
        # Store the user on database instead
        save_users()
        print(f"✅ User '{member.user_name}' registered successfully! (201 Created)")
        return  {"id": new_id, "user_name": member.user_name, "email": member.email}
    except Exception as error:
        print(f"❌ Error registering user: {error}")
        raise
