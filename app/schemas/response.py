from typing import Any, Optional
from pydantic import BaseModel


class APIResponse(BaseModel):
    statusCode: int
    message: str
    data: Optional[Any] = None
    error: Optional[Any] = None
    timestamp: str
    path: str