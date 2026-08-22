from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserResponse
from app.services import auth_service
from app.utils.response import success_response

router = APIRouter(
    prefix="/auth", 
    tags=["Auth"]
)

@router.post("/register", summary="Đăng ký tài khoản mới")
def register(data: RegisterRequest, request: Request, db: Session = Depends(get_db)):
    user = UserResponse.model_validate(auth_service.register_user(db, data))
    return success_response(201, "Đăng ký thành công", user, request)

@router.post("/login", summary="Đăng nhập, nhận access + refresh token")
def login(data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, data)
    access_token, refresh_token = auth_service.issue_tokens(user)
    return success_response(
        200,
        "Đăng nhập thành công",
        TokenResponse(access_token=access_token, refresh_token=refresh_token),
        request,
    )

@router.post("/refresh", summary="Cấp lại access token từ refresh token")
def refresh(data: RefreshRequest, request: Request):
    new_access_token = auth_service.refresh_access_token(data.refresh_token)
    return success_response(
        200, 
        "Cấp lại token thành công", 
        {"access_token": new_access_token, "token_type": "bearer"}, 
        request
    )