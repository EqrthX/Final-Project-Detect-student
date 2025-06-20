# Student Monitoring with YOLOv11 + React

โปรเจคตรวจจับการตั้งใจเรียนของนักศึกษาแบบเรียลไทม์ผ่านกล้อง
- YOLOv11 + Flask (backend)
- React + Recharts (frontend)

## วิธีใช้งาน
uvicorn app:ชื่อไฟล์ที่รัน --reload

### Backend
```bash
cd backend
python -m venv yolov11_env
source yolov11_env/bin/activate
pip install -r requirements.txt
python app.py
