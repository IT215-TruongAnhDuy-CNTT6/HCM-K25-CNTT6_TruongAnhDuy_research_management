from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from http import HTTPStatus
from app.db.database import Base, engine, get_db
from app.models import research_project, research_task, user
from app.routers import auth, users
from app.schemas.response import APIResponse

app = FastAPI(
    title="Research Management FastAPI",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(
            statusCode=exc.status_code,
            message=str(exc.detail),
            data=None,
            error=HTTPStatus(exc.status_code).phrase,
            timestamp=datetime.now(timezone.utc).isoformat(),
            path=request.url.path,
        ).model_dump(),
        headers=exc.headers,
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=APIResponse(
            statusCode=422,
            message="Dữ liệu không hợp lệ",
            data=None,
            error=exc.errors(),
            timestamp=datetime.now(timezone.utc).isoformat(),
            path=request.url.path,
        ).model_dump(),
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=APIResponse(
            statusCode=500,
            message="Lỗi hệ thống, vui lòng thử lại sau",
            data=None,
            error=None,
            timestamp=datetime.now(timezone.utc).isoformat(),
            path=request.url.path,
        ).model_dump(),
    )

@app.get("/health-check")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": "ok"
        }
    except Exception:
        return {
            "status": "error",
            "database": "unavailable"
        }