from app.models.users import User
from app.schemas.users import UserCreate, UserPublic
from app.utils.functions import hash_password


def toUser(user: UserCreate)-> User:
    """Map a UserCreate schema to the ORM User model, hashing the password.

    Args:
        user: The registration schema with email and plain-text password.

    Returns:
        A User model instance with the password already hashed.
    """
    hashed_password = hash_password(user.password)
    return User(email=user.email,hashed_password=hashed_password)

def toUserPublic(user: User)-> UserPublic:
    """Map a User ORM model to its public schema.

    Args:
        user: The User model instance from the database.

    Returns:
        A UserPublic schema exposing only the safe fields.
    """
    return UserPublic(email=user.email)