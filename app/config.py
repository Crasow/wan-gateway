"""
Конфигурация для WAN2.2 API Gateway
"""

import os
from typing import Optional

# Настройки по умолчанию
DEFAULT_WAN_API_URL = os.getenv("WAN_API_URL", "http://127.0.0.1:8000")
DEFAULT_TIMEOUT = int(os.getenv("WAN_TIMEOUT", "300"))  # 5 минут

# Настройки для генерации видео через локальный скрипт
# Путь к скрипту generate.py (относительно текущей директории или абсолютный)
DEFAULT_GENERATE_SCRIPT_PATH = os.getenv("GENERATE_SCRIPT_PATH", "../generate.py")
# Путь к директории с чекпоинтами
DEFAULT_CKPT_DIR = os.getenv("CKPT_DIR", "./Wan2.2-TI2V-5B")
# Размер видео по умолчанию
DEFAULT_VIDEO_SIZE = os.getenv("VIDEO_SIZE", "1280*704")
# Модель по умолчанию
DEFAULT_TASK = os.getenv("TI2V_TASK", "ti2v-5B")


def get_wan_api_url(override: Optional[str] = None) -> str:
    """Возвращает URL для WAN API"""
    return override or DEFAULT_WAN_API_URL


def get_timeout(override: Optional[int] = None) -> int:
    """Возвращает таймаут для запросов"""
    return override or DEFAULT_TIMEOUT


def get_generate_script_path() -> str:
    """Возвращает путь к скрипту generate.py"""
    return DEFAULT_GENERATE_SCRIPT_PATH


def get_ckpt_dir() -> str:
    """Возвращает путь к директории с чекпоинтами"""
    return DEFAULT_CKPT_DIR


def get_video_size() -> str:
    """Возвращает размер видео по умолчанию"""
    return DEFAULT_VIDEO_SIZE


def get_ti2v_task() -> str:
    """Возвращает задачу для генерации видео"""
    return DEFAULT_TASK
