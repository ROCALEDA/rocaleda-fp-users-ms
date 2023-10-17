from typing import List
from app.commons.enums import RoleEnum
from pydantic import BaseModel, EmailStr, constr

PHONE_REGEX = "^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$"


class Role(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    phone: constr(pattern=PHONE_REGEX)
    role_id: int


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


class CandidateCreate(UserCreate):
    fullname: str
    soft_skills: List[str]
    tech_skills: List[str]
    role_id: int = RoleEnum.CANDIDATE.value


class Candidate(UserBase):
    fullname: str
    soft_skills: List[str]
    tech_skills: List[str]


class CustomerCreate(UserCreate):
    name: str
    role_id: int = RoleEnum.CUSTOMER.value


class Customer(UserBase):
    name: str
