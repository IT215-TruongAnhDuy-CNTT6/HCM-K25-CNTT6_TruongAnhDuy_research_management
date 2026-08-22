from fastapi import Request
from datetime import datetime, timezone
from typing import Any
from app.schemas.response import APIResponse

def success_response(statusCode: int, message: str, data: Any, request: Request) -> APIResponse:
    return APIResponse(
        statusCode=statusCode,
        message=message,
        data=data,
        error=None,
        timestamp=datetime.now(timezone.utc).isoformat(),
        path=request.url.path,
    )