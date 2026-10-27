from pydantic import Field, field_validator, BaseModel, EmailStr

class Member(BaseModel):
    user_name: str = Field(min_length=5)
    email: EmailStr
    password: str = Field(min_length=3)

    @field_validator("user_name", "password", mode="before")
    @classmethod
    def reject_empty_or_whitespace(cls, value):
        if isinstance(value, str) and not value.strip():
            raise ValueError("This field cannot be empty")
        return value

class LoginRequest(BaseModel):
    user_name: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


