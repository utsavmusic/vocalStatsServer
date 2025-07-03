from app.config.logger import get_logger
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = get_logger(__name__)

def add_exception_handlers(app):
  @app.exception_handler(StarletteHTTPException)
  async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(f"HTTP error: {exc.detail}")
    return JSONResponse(
      status_code=exc.status_code,
      content={"error": exc.detail},
    )

  @app.exception_handler(RequestValidationError)
  async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
      status_code=422,
      content={"error": "Validation Failed", "details": exc.errors()},
    )

  @app.exception_handler(Exception)
  async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error occurred")
    return JSONResponse(
      status_code=500,
      content={"error": "Internal Server Error"},
    )
