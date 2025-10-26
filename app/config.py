"""
Конфигурация для WAN2.2 API Gateway
"""
import os
from typing import Optional

# Настройки по умолчанию
DEFAULT_WAN_API_URL = os.getenv("WAN_API_URL", "http://127.0.0.1:7860")
DEFAULT_TIMEOUT = int(os.getenv("WAN_TIMEOUT", "300"))  # 5 минут

# Настройки для удаленного сервера wan2.2
# Раскомментируйте и настройте для работы с реальным сервером:
# DEFAULT_WAN_API_URL = "http://wan2.2:7860"
# или используйте переменную окружения:
# export WAN_API_URL=http://wan2.2:7860


def get_wan_api_url(override: Optional[str] = None) -> str:
    """Возвращает URL для WAN API"""
    return override or DEFAULT_WAN_API_URL


def get_timeout(override: Optional[int] = None) -> int:
    """Возвращает таймаут для запросов"""
    return override or DEFAULT_TIMEOUT
