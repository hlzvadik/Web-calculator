from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: int
    name: str = ""
    email: EmailStr
    hash_password: str

class PostUser(BaseModel):
    name: str = ""
    email: EmailStr
    hash_password: str

class GetUser(BaseModel):
    email: EmailStr
    hash_password: str

class PatchUser(BaseModel):
    name: str = ""
    email: EmailStr
    hash_password: str

class DeleteUser(BaseModel):
    email: EmailStr
    hash_password: str

class ResponceUser(BaseModel):
    name: str = ""
    email: EmailStr
