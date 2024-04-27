from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: str = Field(max_length=254, unique=True)
    name: str | None = None


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    posts: list["Post"] = Relationship(back_populates="author")


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class PostBase(SQLModel):
    title: str
    content: str
    published: bool = False


# Database model, database table inferred from class name
class Post(PostBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    author_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    author: User | None = Relationship(back_populates="posts")


class PostsPublic(SQLModel):
    data: list[Post]
    count: int
