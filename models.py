from pydantic import BaseModel, EmailStr

class User(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class LinkID(BaseModel):
    email: EmailStr
    password: str
    linked_id: str

class UserDetails(BaseModel):
    linked_id: str
    full_name: str
    age: int
    address: str
