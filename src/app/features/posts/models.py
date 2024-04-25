from sqlmodel import Field, Relationship, SQLModel


# sqlmodel base on prisma's schema

# model User {
#   id    Int     @id @default(autoincrement())
#   email String  @unique
#   name  String?
#   posts Post[]
# }

# model Post {
#   id        Int     @id @default(autoincrement())
#   title     String
#   content   String?
#   published Boolean @default(false)
#   author    User    @relation(fields: [authorId], references: [id])
#   authorId  Int
# }

# Shared properties
# TODO replace email str with EmailStr when sqlmodel supports it
class UserBase(SQLModel, table=True):
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


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
