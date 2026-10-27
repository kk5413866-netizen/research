@echo off
echo ===================================================
echo   Starting ResearchEcho - Evidence-First Assistant
echo ===================================================
echo.

echo Starting FastAPI Backend on port 8000...
start "ResearchEcho Backend" cmd /k "cd backend && python -m uvicorn app:app --host 127.0.0.1 --port 8000"

timeout /t 2 /nobreak >nul

echo Starting Vite Frontend on port 5173...
start "ResearchEcho Frontend" cmd /k "cd frontend && npm.cmd run dev -- --host 127.0.0.1 --port 5173"

timeout /t 3 /nobreak >nul

echo.
echo Opening ResearchEcho dashboard in default browser...
start http://127.0.0.1:5173

echo.
echo ResearchEcho is running!
echo - Frontend: http://127.0.0.1:5173
echo - Backend:  http://127.0.0.1:8000
echo - Swagger:  http://127.0.0.1:8000/docs
echo.
pause
