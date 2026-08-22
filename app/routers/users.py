from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.dependencies.auth import RoleChecker, get_current_user
from app.models.user import User
from app.schemas.user import UserResponse
from app.services import user_service
from app.utils.response import success_response

router = APIRouter(
    prefix="/users", 
    tags=["Users"]
)

@router.get("/me", summary="Xem thông tin cá nhân")
def get_me(request: Request, current_user: User = Depends(get_current_user)):
    return success_response(200, "Lấy thông tin thành công", UserResponse.model_validate(current_user), request)

@router.get("", summary="Xem danh sách user (chỉ Admin)")
def list_users(
    request: Request,
    search: str | None = None,
    db: Session = Depends(get_db),
    admin: User = Depends(RoleChecker(["ADMIN"])),
):
    return success_response(
        200, 
        "Lấy danh sách thành công", 
        [UserResponse.model_validate(user) for user in user_service.list_users(db, search)], 
        request
    )