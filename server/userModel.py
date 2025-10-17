from pydantic import BaseModel
from uuid import UUID

class UserBase(BaseModel):
    firstName: str
    lastName: str | None = None
    email: str 

class UserFormData(UserBase):
    password: str
    model_config = {"extra":"forbid"}

class UserPublic(UserBase):
    id: UUID
    role: str
    


class UserInDB(UserBase):
    id: UUID
    password: str
    role: str

class UserLoginFromData(BaseModel):
    email: str
    password: str