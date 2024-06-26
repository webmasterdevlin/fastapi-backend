from sqlmodel import Field, Relationship, SQLModel
# from .database import engine


# Shared properties
class UserBase(SQLModel):
    email: str = Field(max_length=254, unique=True)
    name: str


# Database model, database table inferred from class name
class User(UserBase, table=True):
    __tablename__ = "Brukere"
    id: int | None = Field(default=None, primary_key=True)
    posts: list["Post"] = Relationship(back_populates="author")


class UserCreate(UserBase):
    email: str
    name: str


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int


# Shared properties
class PostBase(SQLModel):
    title: str
    content: str
    published: bool = False


# Database model, database table inferred from class name
class Post(PostBase, table=True):
    __tablename__ = "Innlegg"
    id: int | None = Field(default=None, primary_key=True)
    author_id: int | None = Field(
        default=None, foreign_key="Brukere.id", nullable=False
    )
    author: User | None = Relationship(back_populates="posts")


class PostCreate(PostBase):
    title: str
    content: str


class PostsPublic(SQLModel):
    data: list[Post]
    count: int


# SQLModel.metadata.create_all(bind=engine)
