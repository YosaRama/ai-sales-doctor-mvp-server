from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DBAPIError
from app.core.exception import AppException

def register_exception_handlers(app):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.message,
            },
        )

    @app.exception_handler(DBAPIError)
    async def db_exception_handler(request: Request, exc: DBAPIError):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Internal database error",
            },
        )
