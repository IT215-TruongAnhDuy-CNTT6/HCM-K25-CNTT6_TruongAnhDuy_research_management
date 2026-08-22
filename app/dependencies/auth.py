from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.database import get_db
from app.models.research_project import ResearchMember
from app.models.user import User
from app.utils.exceptions import forbidden

reusable_oauth2 = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(reusable_oauth2),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Không thể xác thực thông tin đăng nhập!",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise credentials_exception

    token = credentials.credentials

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "access":
            raise credentials_exception
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise credentials_exception

    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first() if email else None

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Người dùng không tồn tại trên hệ thống",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tài khoản này đã bị tạm khóa",
        )

    return user


class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(
        self,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> User:

        user_role = current_user.role
        if user_role not in self.allowed_roles:
            raise forbidden(
                f"Quyền truy cập bị từ chối. Yêu cầu một trong các role: {self.allowed_roles}"
            )
        return current_user