#!/bin/bash

# Запуск WAN2.2 API Gateway
echo "Started WAN2.2 API Gateway..."
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
