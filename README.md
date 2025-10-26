# WAN2.2 API Gateway

API шлюз для работы с WAN2.2 моделью. Предназначен для тестирования локально и последующего развертывания на удаленном сервере.

## Возможности

- ✅ Генерация текста через WAN2.2
- ✅ Генерация изображений (с настройками размера, качества и negative prompts)
- ✅ Генерация видео (с настройками длительности и FPS)
- ✅ Автоматическое fallback на mock когда API недоступно
- ✅ Метрики производительности (время выполнения)
- ✅ Логирование всех запросов
- ✅ CORS поддержка
- ✅ Настраиваемые timeout'ы
- ✅ Публичный API для внешних клиентов

## Установка

### Требования

- Python >= 3.13
- uv (или pip)

### Установка зависимостей

```bash
# Используя uv (рекомендуется)
uv sync

# Или используя pip
pip install -e .
```

## Запуск

### Локальная разработка

#### Windows (PowerShell)

```powershell
# С помощью скрипта (рекомендуется)
.\start_server.ps1

# Или вручную
uv run uvicorn app.main:app --reload
```

#### Linux/MacOS

```bash
# С помощью скрипта (рекомендуется)
chmod +x start_server.sh
./start_server.sh

# Или вручную
uv run uvicorn app.main:app --reload
```

**Примечание**: Всегда используйте `uv run` для запуска команд, чтобы гарантировать работу с правильным окружением!

API будет доступно по адресу: http://localhost:8000

### Документация API

После запуска доступна автоматическая документация:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Использование

### Проверка работоспособности

```bash
curl http://localhost:8000/
```

### Генерация текста

```bash
curl -X POST http://localhost:8000/api/generate/text \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Привет, как дела?"}'
```

### Генерация изображения

```bash
curl -X POST http://localhost:8000/api/generate/image \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Beautiful sunset over mountains",
    "width": 1024,
    "height": 1024,
    "steps": 50
  }'
```

### Генерация видео

```bash
curl -X POST http://localhost:8000/api/generate/video \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A cat playing with a ball",
    "duration": 5,
    "fps": 24
  }'
```

### Проверка здоровья сервиса

```bash
curl http://localhost:8000/api/health
```

## Конфигурация

### Настройка API WAN2.2

По умолчанию шлюз обращается к `http://127.0.0.1:7860`. 

Для изменения адреса можно:

1. **В коде** (app/services/wan_client.py):
```python
WAN_API_URL = "http://your-server:7860"
```

2. **Через параметр запроса**:
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "тест",
    "api_url": "http://remote-server:7860"
  }'
```

## Тестирование

### Автоматическое тестирование

```powershell
# Windows
.\test_api.ps1

# Linux/MacOS
python test_api.py
```

### Локальное тестирование (без реального API)

Если WAN2.2 API недоступно, шлюз автоматически использует mock данные для тестирования.

```bash
# Mock режим
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "тест запроса"}'
```

### Тестирование с удаленным сервером

Когда будет готов удаленный сервер wan2.2:

```bash
# Укажите URL удаленного сервера
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Ваш запрос",
    "api_url": "http://wan2.2:7860"
  }'
```

## API Endpoints

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/` | Проверка работоспособности |
| GET | `/api/health` | Проверка здоровья и возможностей |
| POST | `/api/generate/text` | Генерация текста |
| POST | `/api/generate/image` | Генерация изображений |
| POST | `/api/generate/video` | Генерация видео |

## Структура проекта

```
wan-gateway/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI приложение
│   ├── config.py            # Конфигурация
│   ├── routers/
│   │   └── generate.py      # API endpoints
│   └── services/
│       └── wan_client.py    # Клиент для WAN2.2 API
├── start_server.ps1         # Скрипт запуска (Windows)
├── start_server.sh          # Скрипт запуска (Unix)
├── test_api.py              # Тестовый скрипт
├── test_api.ps1             # Скрипт тестов (Windows)
├── pyproject.toml           # Зависимости
└── README.md               # Документация
```

## Следующие шаги

1. ✅ Локальное тестирование шлюза
2. ⏳ Развертывание WAN2.2 модели на удаленном сервере
3. ⏳ Настройка шлюза для работы с удаленным сервером
4. ⏳ Тестирование производительности
5. ⏳ Оценка необходимой мощности сервера

## Логирование

Все запросы логируются с метаданными:
- Время выполнения
- URL API
- Ошибки (если есть)

Логи выводятся в консоль в формате:
```
2024-01-01 12:00:00 - app.services.wan_client - INFO - Request completed in 1.23s
```
