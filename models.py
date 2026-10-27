from pydantic import BaseModel


class Book(BaseModel):
    """A book with title, author name and first publish year."""
    title: str
    author_name: list[str]
    first_publish_year: int | None = None

