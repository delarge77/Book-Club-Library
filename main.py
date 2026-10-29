import os
from datetime import datetime, timedelta, timezone
import sqlite3
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError
from models import ( 
    Member, 
    LoginRequest, 
    TokenResponse, 
    Book, 
    BookUpdate, 
    LoanCreate
)

from database import (
    get_all_catalogued_books,
    get_catalogued_book_by_id,
    get_all_members,
    add_member,
    get_member_by_email,
    add_book,
    get_never_borrowed_books,
    get_most_borrowed_books,
    create_loan,
    get_loan_by_id,
    return_loan,
    get_overdue_loans,
    update_book_by_id, 
    get_member_by_id, 
    get_member_current_loans,
    search_members,
    delete_book,
    delete_member,
)

from external_api import search_books


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

def create_access_token(member_id: int) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(member_id),
        "exp": expires_at
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    token = credentials.credentials

    try:
        payload = jwt.decode( token, SECRET_KEY, algorithms=[ALGORITHM])
        member_id = payload.get("sub")

        if not member_id:
            raise ValueError("Missing subject")

    except (InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})

    user = next((m for m in get_all_members() if str(m["member_id"]) == member_id), None)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"})
    return user


import sqlite3
from fastapi import HTTPException, Depends

@app.post("/members/register", status_code=201, dependencies=[Depends(check_key)])
def add_new_user(member: Member):
    try:
        hashed_password = password_hash.hash(member.password)
        new_id = add_member( name = member.name, email=str(member.email), phone=member.phone, password_hash=hashed_password)
        print(f"✅ Member '{member.name}' registered successfully! (201 Created)")

        return {
            "member_id": new_id,
            "name": member.name,
            "email": str(member.email),
            "phone": member.phone,
        }

    except sqlite3.IntegrityError as error:
        print(f"❌ Could not register member: {error}")
        raise HTTPException(
            status_code=409,
            detail="Email already registered or invalid member data"
        )

    except Exception as error:
        print(f"❌ Error registering member: {error}")
        raise HTTPException(
            status_code=500,
            detail="Could not register member"
        )



@app.post("/members/login", response_model=TokenResponse, status_code=200, dependencies=[Depends(check_key)])
def login(member: LoginRequest):
    user = get_member_by_email(member.email)

    if user is None or not password_hash.verify(member.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )


    access_token = create_access_token(user["member_id"])
    print("✅ Login successful! Access token generated.")
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/books/add_new_book", status_code=201)
def add_new_book(book: Book, _: dict = Depends(get_current_user)):
    try:
            new_book_id = add_book( title = book.title, author_name=book.author_name, publication_year=book.publication_year)
            print(f"✅ Book '{book.title}' registered successfully! (201 Created)")
    
            return {
                "book_id": new_book_id,
                "title": book.title,
                "author_name": book.author_name,
                "publication_year": book.publication_year,
            }
    
    except sqlite3.IntegrityError as error:
        print(f"❌ Could not register book: {error}")
        raise HTTPException(
            status_code=409,
            detail="Book already registered or invalid book data"
    )
    
    except Exception as error:
        print(f"❌ Error registering book: {error}")
        raise HTTPException(
            status_code=500,
            detail="Could not register book"
    )


@app.get("/members/me", status_code=201)
def get_my_profile(current_user: dict = Depends(get_current_user)):
    return {
        "member_id": current_user["member_id"],
        "name": current_user["name"],
        "email": current_user["email"],
        "phone": current_user["phone"]
    }


@app.delete(
    "/members/{member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(check_key)],
)
def remove_member(member_id: int) -> None:
    """Delete a member who has no loan history."""
    try:
        deleted = delete_member(member_id)
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Member has loan history and cannot be removed",
        )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found",
        )


@app.get("/books")
def get_catalogued_books():
    """Return all books in the library catalogue."""
    return get_all_catalogued_books()


@app.get("/books/search")
def search_open_library(q: str):
    """Search Open Library and return the matching books."""
    if not q.strip():
        raise HTTPException(
            status_code=400, detail="Please type something to search for."
        )
    books = search_books(q)
    if books is None:
        raise HTTPException(
            status_code=503, detail="Open Library is not reachable. Try again later."
        )
    return books

@app.patch("/books/update/{book_id}")
def update_book(book_id: int, book_update: BookUpdate, _: dict = Depends(get_current_user),):

    update_data = book_update.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="At least one field must be provided"
        )

    try:
        updated_book = update_book_by_id(book_id, update_data)

        if updated_book is None:
            raise HTTPException(
                status_code=404,
                detail="Book not found"
            )

        return updated_book

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Could not update book due to a data conflict"
        )



@app.get("/books/never-borrowed")
def books_never_borrowed():
    """Return books that have never been borrowed."""
    return get_never_borrowed_books()


@app.get("/books/most-borrowed")
def books_most_borrowed():
    """Return the books that have been borrowed the most."""
    return get_most_borrowed_books()


@app.get("/books/{book_id}")
def get_catalogued_book(book_id: int):
    """Return one book using book_id"""
    book = get_catalogued_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.delete("/books/{book_id}", status_code=204, dependencies=[Depends(check_key)])
def remove_book(book_id: int):
    """Delete a book using book_id."""
    try:
        deleted = delete_book(book_id)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Book has loans and cannot be removed")
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")


@app.post("/loans", status_code=201)
def lend_book(loan: LoanCreate, current_user: dict = Depends(get_current_user)):
    """Create a new loan using book_id and logged in user"""
    book = get_catalogued_book_by_id(loan.book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    try:
        new_loan_id = create_loan(loan.book_id, current_user["member_id"])

    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Book is already on loan")
    return {"loan_id": new_loan_id}


@app.get("/loans/overdue")
def overdue_loans(_: dict = Depends(get_current_user)):
    """Return loans that are past their due date and not returned."""
    return get_overdue_loans()


@app.patch("/loans/{loan_id}/return")
def return_book(loan_id: int, _: dict = Depends(get_current_user)):
    """Return loan - anyone that's logged in can return a loan"""
    loan = get_loan_by_id(loan_id)
    if loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    if loan["return_date"] is not None:
        raise HTTPException(status_code=409, detail="Loan already returned")
    return_loan(loan_id)
    return {"loan_id": loan_id, "status": "returned"}


@app.get("/members")
def get_all_registered_members(_: dict = Depends(get_current_user)):
    """Return all registered members"""
    return get_all_members()

  
@app.get("/members/{member_id}/loans/current")
def get_current_loans(member_id: int, _: dict = Depends(get_current_user),):

    member = get_member_by_id(member_id)
    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found",
        )

    return get_member_current_loans(member_id)

@app.get("/members/search")
def filter_members(q: str, _: dict = Depends(get_current_user)):
    """Search members by name or email. Multiple words allowed"""
    words = q.split()
    results = {}
    for word in words:
        for member in search_members(word):
            results[member["member_id"]] = member

    return list(results.values())
