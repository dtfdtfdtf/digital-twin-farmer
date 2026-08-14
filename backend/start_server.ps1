Set-Location "C:\Users\Lumbani\Desktop\digital-twin-farmer\backend"
& ".\venv\Scripts\Activate.ps1"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Read-Host "Press Enter to exit"
