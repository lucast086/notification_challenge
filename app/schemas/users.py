from typing import Annotated

from pydantic import AfterValidator, EmailStr, SecretStr, model_validator
from sqlmodel import SQLModel
from typing_extensions import Self

from app.utils.constants import (
   INCLUDES_LOWERCASE,
   INCLUDES_NUMBERS,
   INCLUDES_SPECIAL_CHARS,
   INCLUDES_UPPERCASE,
   MAX_LENGTH,
   MIN_LENGTH,
   SPECIAL_CHARS,
)


def validate_password(v: SecretStr) -> SecretStr:

   if len(v.get_secret_value()) < MIN_LENGTH or len(v.get_secret_value()) > MAX_LENGTH:
      raise ValueError(f"length should be at least {MIN_LENGTH} but not more than {MAX_LENGTH}")

   if INCLUDES_NUMBERS and not any(char.isdigit() for char in v.get_secret_value()):
      raise ValueError("Password should have at least one numeral")

   if INCLUDES_UPPERCASE and not any(char.isupper() for char in v.get_secret_value()):
      raise ValueError("Password should have at least one uppercase letter")

   if INCLUDES_LOWERCASE and not any(char.islower() for char in v.get_secret_value()):
      raise ValueError("Password should have at least one lowercase letter")

   if INCLUDES_SPECIAL_CHARS and not any(
   char in SPECIAL_CHARS for char in v.get_secret_value()
):
      raise ValueError(
        f"Password should have at least one of the symbols {sorted(SPECIAL_CHARS)}"
    )

   return v


ValidatePassword = Annotated[SecretStr, AfterValidator(validate_password)]


class UserBase(SQLModel):
    email: EmailStr

class UserCreate(UserBase):
    password: ValidatePassword
    password_repeat: SecretStr
    
    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password.get_secret_value() != self.password_repeat.get_secret_value():
            raise ValueError('Passwords do not match')
        return self

class UserPublic(UserBase):
    pass