# complete crud for user
from sqlmodel import Session, select

from src.app.schemas.models import UserCreate, User, UserUpdate


# creating a user
def create_new_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(user_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


# getting all users
def get_all_users(*, session: Session) -> list[User]:
    statement = select(User)
    session_users = session.exec(statement).all()
    return list(session_users)


# getting a user by id
def get_user_by_id(*, session: Session, user_id: int) -> User | None:
    statement = select(User).where(User.id == user_id)
    session_user = session.exec(statement).first()
    return session_user


# getting a user by email
def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


# updating a user
def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> User:
    user_data = user_in.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


# deleting a user
def delete_user(*, session: Session, db_user: User) -> None:
    session.delete(db_user)
    session.commit()
