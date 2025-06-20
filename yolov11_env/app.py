from fastapi import FastAPI
from routes import user_route
from models import user_model
from database import engine

user_model.Base.metadata.create_all(bind=engine)  # สร้างตารางในฐานข้อมูล

# สร้าง table ในฐานข้อมูล

app = FastAPI()
app.include_router(user_route.router)