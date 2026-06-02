from sqlmodel import Field

from app.schemas.users import UserBase


class User(UserBase, table=True):
    """Database model representing a registered user."""
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(
    nullable=False,   
    exclude=True,     
    min_length=60,    
    max_length=128    
)
    