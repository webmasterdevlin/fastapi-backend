from sqlmodel import Field, Relationship, SQLModel


# sqlmodel base on prisma's schema

# model User {
#   id    Int     @id @default(autoincrement())
#   email String  @unique
#   name  String?
#   posts Post[]
# }


# Shared properties
# TODO replace email str with EmailStr when sqlmodel supports it
class UserBase(SQLModel):
    email: str = Field(max_length=254, unique=True)
    name: str | None = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: str
    name: str | None = None


# Properties to receive via API on update, all are optional
# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdate(UserBase):
    email: str | None = None  # type: ignore
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
