from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
from schema.user_schema import UserResponse, UserCreate, CreateUserResponse
from sqlalchemy.orm import Session
from models.user_model import User, UserRole
import random
import datetime
import bcrypt

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/create")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    digits = ''.join(random.choices('0123456780', k=5))
    uCode = "T" + digits
    try:
        
        existing_user = db.query(User).filter(User.user_code == uCode).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )
        
        hash_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt());
        
        new_user = User(
            user_code=uCode,
            username=user.username,
            name=user.name,
            password=hash_password,
            user_roles=user.user_roles,
            created_at=datetime.datetime.utcnow()
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "User created successfully",
                "new_user": new_user.to_dict()
            }
        )
        
    except HTTPException as http_err:
        raise http_err  # ปล่อย HTTPException ออกไปให้ FastAPI handle ต่อ
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "An unexpected error create user",
                "error": str(e)
            }
        )
    
@router.get("/users")
async def get_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        if not users:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "message": "No users found"
                }
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "show users successfully!",
                "users": [user.to_dict() for user in users]
            }
        )     
        pass  
    except HTTPException as http_err:
        raise http_err  # ปล่อย HTTPException ออกไปให้ FastAPI handle ต่อ
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "An unexpected error get users",
                "error": str(e)
            }
        )
        pass

@router.delete("/user/delete/{id}")
async def delete_user(id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == id).first()
        
        if not user:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "message": f"User with ID {id} not found"
                }
            )
        
        db.delete(user)
        db.commit()
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": f"User with ID {id} deleted successfully"
            }
        )
        
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "An unexpected error delete user",
                "error": str(e)
            }
        )

@router.put("/user/update/{id}")
async def update_user(id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == id).first()
        
        if not user:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "message": f"User ID: {id} to update not found"
                }
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": f"User ID: {id} update successfully!"
            }
        )
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "An unexpected error update user",
                "error": str(e)
            }
        )