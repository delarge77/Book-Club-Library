from pydantic import Field, field_validator, BaseModel, EmailStr


class Book(BaseModel):
    """A book with title, author name and first publish year."""
    title: str
    author_name: str
    publication_year: int | None = None

class ExternalBook(BaseModel):
     """External API Model from Open Library"""
     title: str
     author_name: list[str]
     first_publish_year: int | None = None


class Member(BaseModel):
    name: str = Field(min_length=5)
    email: EmailStr
    phone: str | None = None
    password: str = Field(min_length=3)

    @field_validator("name", "password", mode="before")
    @classmethod
    def reject_empty_or_whitespace(cls, value):
        if isinstance(value, str) and not value.strip():
            raise ValueError("This field cannot be empty")
        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class LoanCreate(BaseModel):
    """Create Loan using book_id and member_id"""

    book_id: int = Field(gt=0)
    member_id: int = Field(gt=0)

