from sqlalchemy.orm import Session
from app.models.user import User

def list_users(db: Session, search: str | None = None) -> list[User]:
    user_list = db.query(User)
    if search:
        search_char = f"%{search}%"
        user_list = user_list.filter((User.full_name.like(search_char)) | (User.email.like(search_char)) | (User.is_active.like(search_char)))
    return user_list.order_by(User.id).all()