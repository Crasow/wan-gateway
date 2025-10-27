# Development Guide

## Отладка в Cursor/VS Code

### Настройка брейкпоинтов

1. **Откройте панель отладки** (Ctrl+Shift+D или ⌘+Shift+D)
2. **Выберите конфигурацию**: "Python: FastAPI"
3. **Установите брейкпоинты** кликом слева от номера строки
4. **Запустите отладку** (F5 или кнопка "Start Debugging")

### Доступные конфигурации

#### 1. Python: FastAPI

- С автоперезагрузкой при изменении кода (`--reload`)
- Брейкпоинты будут работать
- Подходит для разработки

#### 2. Python: FastAPI (без reload)

- Без автоперезагрузки
- Больше стабильности при отладке
- Подходит для сложной отладки

#### 3. Python: Debug Current File

- Отладка текущего файла
- Полезно для тестов

### Как использовать

1. **Установите брейкпоинт**:

   ```
   Откройте файл → Кликните слева от номера строки → Красная точка
   ```

2. **Запустите отладку**:

   - Нажмите F5
   - Или выберите в меню: Run → Start Debugging

3. **Сервер запустится в режиме отладки**

4. **Выполните запрос к API** (curl, Postman, браузер)

5. **Выполнение остановится на брейкпоинте**

### Полезные горячие клавиши

- **F5** - Запустить/Продолжить
- **F9** - Установить/Убрать брейкпоинт
- **F10** - Step Over (пропустить строку)
- **F11** - Step Into (войти в функцию)
- **Shift+F11** - Step Out (выйти из функции)
- **Ctrl+Shift+F5** - Перезапустить отладку

### Отладка переменных

Когда выполнение остановлено на брейкпоинте:

- **Variables panel** - показывает все локальные переменные
- **Watch panel** - можете добавить выражения для отслеживания
- **Call Stack** - показывает цепочку вызовов
- **Debug Console** - можете выполнить Python код в текущем контексте

### Пример отладки запроса

```python
# В файле app/routers/generate.py
@router.post("/api/generate/text")
async def generate_text_endpoint(request: GenerateRequest):
    # Установите брейкпоинт здесь
    prompt = request.prompt  # Наведите мышь - увидите значение

    result = await generate_text(
        prompt=prompt,
        api_url=request.api_url,
        timeout=request.timeout
    )

    return result  # И здесь тоже
```

### Troubleshooting

#### Брейкпоинты не срабатывают

1. Проверьте, что выбран правильный интерпретатор Python
2. Убедитесь, что `"justMyCode": false` в launch.json
3. Перезапустите сервер отладки (Shift+F5)

#### Сервер не запускается

1. Проверьте, что Python установлен
2. Убедитесь, что зависимости установлены: `uv sync`
3. Проверьте путь к Python в launch.json

#### Port already in use

Если порт 8000 занят:

```json
"args": [
    "app.main:app",
    "--port",
    "8001"  // Измените порт
]
```

## Запуск без отладчика

```bash
# С reload
uv run uvicorn app.main:app --reload

# С DEBUG логированием
uv run uvicorn app.main:app --reload --log-level debug
```

## Тестирование

```bash
# Запуск тестов
uv run python test_api.py

# Нагрузочное тестирование
uv run python load_test.py
```

## Проверка логов в режиме DEBUG

Логи будут показывать:

- Имена функций и номера строк
- Детальную информацию о запросах
- Stack traces при ошибках

Пример лога:

```
2025-10-26 17:30:15 - app.routers.generate - DEBUG - generate_text_endpoint:45 - Received text generation request with prompt length: 17
```
