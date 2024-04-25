from sqlmodel import Field, Relationship, SQLModel

from src.app.features.users.models import User


# sqlmodel base on prisma's schema

# model Post {
#   id        Int     @id @default(autoincrement())
#   title     String
#   content   String?
#   published Boolean @default(false)
#   author    User    @relation(fields: [authorId], references: [id])
#   authorId  Int
# }


# Shared properties
class PostBase(SQLModel):
    title: str
    content: str | None = None
    published: bool = False


# Properties to receive on item creation
class PostCreate(PostBase):
    title: str


# Properties to receive on item update
class PostUpdate(PostBase):
    title: str | None = None  # type: ignore


# Database model, database table inferred from class name
class Post(PostBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    author_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    author: User | None = Relationship(back_populates="posts")


# Properties to return via API, id is always required
class PostPublic(PostBase):
    id: int
    author_id: int


class PostsPublic(SQLModel):
    data: list[PostPublic]
    count: int
