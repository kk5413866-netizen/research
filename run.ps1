# ResearchEcho Windows PowerShell Launcher
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "  Starting ResearchEcho - Evidence-First Assistant" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Starting FastAPI Backend on port 8000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python -m uvicorn app:app --host 127.0.0.1 --port 8000"

Start-Sleep -Seconds 2

Write-Host "Starting Vite Frontend on port 5173..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm.cmd run dev -- --host 127.0.0.1 --port 5173"

Start-Sleep -Seconds 3

Write-Host ""
Write-Host "Opening ResearchEcho dashboard in browser..." -ForegroundColor Green
Start-Process "http://127.0.0.1:5173"

Write-Host ""
Write-Host "ResearchEcho is running!" -ForegroundColor Cyan
Write-Host "  Frontend: http://127.0.0.1:5173" -ForegroundColor White
Write-Host "  Backend:  http://127.0.0.1:8000" -ForegroundColor White
Write-Host "  Swagger:  http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host ""
