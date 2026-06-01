from passlib.context import CryptContext
from pydantic import SecretStr

hasher = CryptContext(schemes=["bcrypt"])

def hash_password(password: SecretStr) -> str:
    """Hash a plain-text password using bcrypt.

    Args:
        password: The plain-text password to hash.

    Returns:
        The bcrypt hash string.
    """
    return hasher.hash(password.get_secret_value())
