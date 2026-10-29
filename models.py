from pydantic import Field, field_validator, BaseModel, EmailStr, ConfigDict


class Book(BaseModel):
    """A book with title, author name and first publish year."""
    title: str
    author_name: str
    publication_year: int | None = None

class BookUpdate(BaseModel):
    """Fields that can be updated on a book."""
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, min_length=1)
    author_name: str | None = Field(default=None, min_length=1)
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
    """Create Loan using book_id and logged in member"""

    book_id: int = Field(gt=0)
