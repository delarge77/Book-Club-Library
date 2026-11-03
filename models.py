from pydantic import Field, field_validator, BaseModel, EmailStr, ConfigDict


class Book(BaseModel):
    """A book with title, author name and first publish year."""
    title: str
    author_name: str
    publication_year: int | None = None

class BookUpdate(BaseModel):
    """Fields that can be updated on a book."""
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

class MemberUpdate(BaseModel):
    """Fields that can be updated on a member."""
    email: EmailStr
    phone: str
    @field_validator("email", "phone", mode="before")
    @classmethod
    def reject_empty_or_whitespace(cls, value):
        if isinstance(value, str) and not value.strip():
            raise ValueError("This field cannot be empty")
        return value

class MemberLoanResponse(BaseModel):
    """A loan included in a member's personal data."""

    loan_id: int
    book_id: int
    title: str
    author_name: str
    loan_date: str
    due_date: str
    return_date: str | None = None


class MemberProfileResponse(BaseModel):
    """Profile data stored about a library member."""

    member_id: int
    name: str
    email: EmailStr
    phone: str | None = None


class MemberPersonalDataResponse(BaseModel):
    """Profile and loan data stored about a library member."""

    profile: MemberProfileResponse
    loans: list[MemberLoanResponse] = Field(
        default_factory=list
    )
    

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class LoanCreate(BaseModel):
    """Create Loan using book_id and logged in member"""

    book_id: int = Field(gt=0)
