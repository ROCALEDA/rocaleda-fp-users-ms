from pydantic import BaseModel


class Role(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    phone: str
    role_id: int


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
