from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime

class Teacher(Base):
    __tablename__ = 'teachers'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    # subject_id = Column(Integer, nullable=True)