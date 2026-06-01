from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import DomainError


async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    """Format Pydantic validation errors into a consistent JSON response.

    Args:
        request: The incoming request that triggered the error.
        exc: The validation exception raised by FastAPI/Pydantic.

    Returns:
        A JSONResponse with 422 status and a list of field-level error messages.
    """
    errors = [
          {
              "field": err["loc"][-1],
              "message": err["msg"]
          }
          for err in exc.errors()
      ]
    return JSONResponse(
          status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
          content={"detail": errors}
      )

async def exception_handler(request: Request, exc: DomainError):
    """Handle domain-level exceptions and return a structured JSON error response.

    Args:
        request: The incoming request that triggered the error.
        exc: The domain exception carrying a status code and message.

    Returns:
        A JSONResponse with the exception's status code and message.
    """
    return JSONResponse(
          status_code=exc.status_code,
          content={"message": exc.message}
      )