from sqlalchemy import Column, Integer, String, Enum as SQLEnum, ForeignKey, DateTime
from enum import Enum
from database import Base

class UserRole(str,Enum):
    admin = "admin"
    teacher = "TEACHER"
    student = "student"
    
    
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_code = Column(String(10), unique=True, index=True)
    username = Column(String(50), index=True, nullable=False)
    name = Column(String(100), index=True)
    user_roles = Column(SQLEnum(UserRole), nullable=False, default=UserRole.teacher)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_code": self.user_code,
            "username": self.username,
            "name": self.name,
            "user_roles": self.user_roles,
            "created_at": self.created_at.isoformat()  # datetime ต้องแปลงก่อน
        }
