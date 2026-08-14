@echo off
cd /d "C:\Users\Lumbani\Desktop\digital-twin-farmer\backend"
call venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause