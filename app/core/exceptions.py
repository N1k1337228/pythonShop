from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

async def http_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=getattr(exc, "status_code", 500),
        content={
            "error": {
                "code": "http_error",
                "message": str(getattr(exc, "detail", "Internal Server Error")),
                "details": {}
            }
        },
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "validation_error",
                "message": "Invalid input data",
                "details": exc.errors()
            }
        },
    )