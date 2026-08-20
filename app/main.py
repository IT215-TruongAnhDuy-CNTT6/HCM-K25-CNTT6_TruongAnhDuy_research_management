from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse
from app.db.database import Base, engine
from app.models import research_project, research_task, user

app = FastAPI(
    title="Research Management FastAPI",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return await http_exception_handler(request, exc)
    return JSONResponse(
        status_code=500, 
        content={"detail": "Lỗi hệ thống, vui lòng thử lại sau"}
    )

@app.get("/health-check")
def health_check():
    return {
        "status": "ok"
    }