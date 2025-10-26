# Запуск WAN2.2 API Gateway
Write-Host "Started WAN2.2 API Gateway..." -ForegroundColor Green
$env:PYTHONIOENCODING="utf-8"
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
