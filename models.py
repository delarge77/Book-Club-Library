from pydantic import BaseModel


class Book(BaseModel):
    """A book with title, author name, first publish year and isbn details."""
    title: str
    author_name: list[str]
    first_publish_year: int | None = None
    isbn: str | None = None
