from fastapi import HTTPException
from sqlmodel import Session, select

from src.app.helpers.dependencies import SessionDep
from src.app.schemas.models import User


def create_new_user(*, session: Session, user: User) -> User:
    db_obj = User.model_validate(user)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_user_by_id(*, session: SessionDep, user_id: int) -> User | None:
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    return user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def update_user(*, session: Session, user_id: int, updated_user: User) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_dict = updated_user.model_dump(exclude_unset=True)
    user.sqlmodel_update(user_dict)
    session.commit()
    session.refresh(user)
    return user


# deleting a user
def delete_user(*, session: Session, removed_user: User) -> None:
    session.delete(removed_user)
    session.commit()
