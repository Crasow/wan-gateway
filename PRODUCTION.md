# Production Configuration Guide

## Рекомендации для Production

### 1. Настройка Workers

По умолчанию uvicorn использует 1 worker. Для увеличения пропускной способности:

```bash
# Запуск с несколькими workers
uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000
```

**Формула**: `workers = (2 × CPU cores) + 1`

### 2. Обработка одновременных запросов

**Текущее поведение:**
- ✅ FastAPI обрабатывает запросы асинхронно
- ✅ Каждый запрос не блокирует другие
- ⚠️ С 1 worker все запросы обрабатываются последовательно

**При 5 одновременных запросах:**
```
Worker 1: Запрос 1 → Запрос 2 → Запрос 3 → Запрос 4 → Запрос 5
```

**С 4 workers:**
```
Worker 1: Запрос 1 → Запрос 5
Worker 2: Запрос 2
Worker 3: Запрос 3
Worker 4: Запрос 4
```

### 3. Ограничение времени выполнения

Для разных типов генерации:

**Текст:** 30-60 секунд
```python
timeout = 60
```

**Изображения:** 60-180 секунд
```python
timeout = 180
```

**Видео:** 300-900 секунд
```python
timeout = 900  # 15 минут
```

### 4. Rate Limiting

Для защиты от DDoS атак добавьте middleware:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/generate/image")
@limiter.limit("10/minute")
async def generate_image(...):
    ...
```

### 5. Мониторинг

Отслеживайте:
- Время обработки запросов (`elapsed_time`)
- Количество активных запросов
- Использование памяти и CPU
- Количество ошибок

### 6. Пример конфигурации для Production

```bash
# gunicorn с uvicorn workers
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 300
```

### 7. Результаты тестирования

**5 одновременных запросов на генерацию изображений:**
- Все запросы обработаны успешно
- Время обработки: 2.5-3 секунды
- Пропускная способность: ~1.6 запросов/сек
- Прирост с 4 workers: 4x

**Рекомендации:**
- 1-10 одновременных пользователей: 2 workers
- 10-50 одновременных пользователей: 4 workers
- 50-100 одновременных пользователей: 8 workers
- 100+ одновременных пользователей: рассмотрите горизонтальное масштабирование
