"""
Настройка логирования для приложения
"""
import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging(log_dir: str = "logs"):
    """
    Настраивает логирование для приложения
    
    Args:
        log_dir: Директория для хранения логов
    """
    # Создаем директорию для логов если её нет
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Настройка формата логов
    log_format = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Создаем root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Очищаем существующие handlers (для предотвращения дублирования при hot-reload)
    root_logger.handlers.clear()
    
    # Handler для файла с ротацией (10MB, 5 файлов бэкапа)
    file_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, 'gateway.log'),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format, date_format))
    
    # Handler для консоли
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format, date_format))
    
    # Handler для файла с ошибками (только ERROR и выше)
    error_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, 'errors.log'),
        maxBytes=10*1024*1024,
        backupCount=5,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(log_format, date_format))
    
    # Добавляем handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(error_handler)
    
    # Возвращаем настроенный root logger
    return root_logger


# Автоматически настраиваем логирование при импорте
logger = setup_logging()
