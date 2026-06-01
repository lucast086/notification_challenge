from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.core.exception_handler import (
    exception_handler,
    request_validation_exception_handler,
)
from app.core.exceptions import DomainError
from app.routers.v1 import router

app = FastAPI()

app.include_router(router)

app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(DomainError, exception_handler)

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Challenge Acepted"}