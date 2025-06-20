from pydantic import BaseModel, ConfigDict
from enum import Enum

class UserRole(str,Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"

class UserCreate(BaseModel):
    id: int 
    user_code: str
    username: str
    name: str
    user_roles: UserRole = UserRole.teacher
    password: str
    ref_id: int | None = None
    created_at: str
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

UserCreate.model_rebuild()

class UserResponse(BaseModel):
    id: int
    user_code: str
    username: str
    name: str
    user_roles: UserRole
    ref_id: int | None = None
    created_at: str

    model_config = {
        "from_attributes": True,
    }
        
class CreateUserResponse(BaseModel):
    message: str
    new_user: UserResponse 
