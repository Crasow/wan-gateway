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

**Важно:** Генерация видео запускает локальный скрипт `generate.py` из соседней папки.

```bash
curl -X POST http://localhost:8000/api/generate/video \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Two anthropomorphic cats in comfy boxing gear and bright gloves fight intensely on a spotlighted stage",
    "duration": 5,
    "fps": 24,
    "size": "1280*704",
    "task": "ti2v-5B"
  }'
```

Параметры (все опциональны, кроме prompt):

- `prompt` - описание видео (обязательно)
- `size` - размер видео в формате "width*height" (по умолчанию "1280*704")
- `task` - задача для генерации (по умолчанию "ti2v-5B")
- `ckpt_dir` - путь к директории с чекпоинтами (по умолчанию "./Wan2.2-TI2V-5B")
- `generate_script_path` - путь к скрипту generate.py (по умолчанию "../generate.py")
- `timeout` - таймаут в секундах (рекомендуется минимум 600)

### Проверка здоровья сервиса

```bash
curl http://localhost:8000/api/health
```

## Конфигурация

### Настройка API WAN2.2

#### Для генерации текста и изображений

По умолчанию шлюз обращается к `http://127.0.0.1:8001`.

Для изменения адреса:

1. **Через переменные окружения**:

```bash
export WAN_API_URL=http://your-server:7860
```

2. **Через параметр запроса**:

```bash
curl -X POST http://localhost:8000/api/generate/text \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "тест",
    "api_url": "http://remote-server:7860"
  }'
```

#### Для генерации видео (локальный скрипт)

Настройка через переменные окружения:

```bash
# Путь к скрипту generate.py (относительно директории проекта)
export GENERATE_SCRIPT_PATH=../generate.py

# Путь к директории с чекпоинтами
export CKPT_DIR=./Wan2.2-TI2V-5B

# Размер видео по умолчанию
export VIDEO_SIZE=1280*704

# Задача по умолчанию
export TI2V_TASK=ti2v-5B

# Таймаут для генерации видео (в секундах)
export WAN_TIMEOUT=1800  # 30 минут
```

Или укажите параметры в запросе:

```bash
curl -X POST http://localhost:8000/api/generate/video \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Your prompt here",
    "size": "1280*704",
    "task": "ti2v-5B",
    "ckpt_dir": "./Wan2.2-TI2V-5B",
    "generate_script_path": "../generate.py"
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

| Метод | Endpoint              | Описание                         |
| ----- | --------------------- | -------------------------------- |
| GET   | `/`                   | Проверка работоспособности       |
| GET   | `/api/health`         | Проверка здоровья и возможностей |
| POST  | `/api/generate/text`  | Генерация текста                 |
| POST  | `/api/generate/image` | Генерация изображений            |
| POST  | `/api/generate/video` | Генерация видео                  |

## Структура проекта

```
wan-gateway/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI приложение
│   ├── config.py            # Конфигурация
│   ├── logger.py            # Настройка логирования
│   ├── metrics.py           # Метрики производительности
│   ├── routers/
│   │   └── generate.py      # API endpoints
│   └── services/
│       └── wan_client.py    # Клиент для WAN2.2 API
├── logs/                    # Логи (создается автоматически)
│   ├── gateway.log
│   └── errors.log
├── start_server.ps1         # Скрипт запуска (Windows)
├── start_server.sh          # Скрипт запуска (Unix)
├── test_api.py              # Тестовый скрипт
├── test_api.ps1             # Скрипт тестов (Windows)
├── load_test.py             # Нагрузочное тестирование
├── pyproject.toml           # Зависимости
└── README.md               # Документация
```

## Нагрузочное тестирование

Для проверки поведения при одновременных запросах:

```powershell
# Windows
uv run python load_test.py

# Linux/MacOS
python load_test.py
```

**Результаты тестирования (5 одновременных запросов):**

- ✅ Все запросы успешно обработаны
- Пропускная способность: ~1.6 запросов/сек
- Время обработки: 2.5-3 секунды на запрос
- Сервер обрабатывает все запросы параллельно благодаря async/await

**Как работает:**

- FastAPI обрабатывает запросы асинхронно
- Каждый запрос не блокирует другие
- При текущей настройке (1 worker) все запросы обрабатываются последовательно на уровне uvicorn
- Для production добавьте больше workers: `uvicorn app.main:app --workers 4`

## Следующие шаги

1. ✅ Локальное тестирование шлюза
2. ✅ Тестирование производительности
3. ⏳ Развертывание WAN2.2 модели на удаленном сервере
4. ⏳ Настройка шлюза для работы с удаленным сервером
5. ⏳ Настройка production конфигурации (workers, rate limiting)

## Логирование

Все запросы логируются в файлы и консоль:

- **Все логи**: `logs/gateway.log` (ротация 10MB, 5 файлов)
- **Ошибки**: `logs/errors.log` (только ERROR и выше)
- **Консоль**: вывод в реальном времени

### Формат логов

```
2025-10-26 17:00:00 - app.services.wan_client - INFO - [wan_client.py:45] - Request completed in 1.23s
```

### Структура директории logs

```
logs/
├── gateway.log      # Все логи (ротация 10MB)
├── gateway.log.1    # Старый лог
├── errors.log       # Только ошибки
└── errors.log.1     # Старые ошибки
```

### Просмотр логов

```powershell
# Windows
Get-Content logs\gateway.log -Tail 50
Get-Content logs\errors.log -Tail 50

# Linux/MacOS
tail -f logs/gateway.log
tail -f logs/errors.log
```
