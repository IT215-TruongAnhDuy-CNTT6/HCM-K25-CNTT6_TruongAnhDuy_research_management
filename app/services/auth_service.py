import jwt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password
from app.core.config import settings
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest
from app.utils.exceptions import bad_request

def register_user(db: Session, data: RegisterRequest) -> User:
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise bad_request("Email đã được sử dụng")

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        full_name=data.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, data: LoginRequest) -> User:
    user = db.query(User).filter(User.email == data.email).first()
    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không đúng",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản đã bị vô hiệu hoá",
        )
    return user

def issue_tokens(user: User) -> tuple[str, str]:
    role_name = user.role
    return (
        create_access_token(data={"sub": user.email, "id": user.id, "role": role_name}),
        create_refresh_token(data={"sub": user.email, "id": user.id, "role": role_name}),
    )

def refresh_access_token(refresh_token: str) -> str:
    try:
        payload = jwt.decode(
            refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token không hợp lệ hoặc đã hết hạn",
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token không hợp lệ hoặc đã hết hạn",
        )
    access_data = {
        "sub": payload["sub"],
        "id": payload["id"],
        "role": payload["role"],
    }
    return create_access_token(data=access_data)