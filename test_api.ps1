# Тестирование WAN2.2 API Gateway
Write-Host "Start testing API gateway..." -ForegroundColor Green
$env:PYTHONIOENCODING="utf-8"
uv run python test_api.py
