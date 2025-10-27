import asyncio
import os
import time
from typing import Any, Dict, Optional

import httpx

from app.config import (
    get_ckpt_dir,
    get_generate_script_path,
    get_ti2v_task,
    get_timeout,
    get_video_size,
    get_wan_api_url,
)
from app.logger import logger


async def _make_request(
    endpoint: str,
    payload: Dict[str, Any],
    api_url: Optional[str] = None,
    timeout: Optional[int] = None
) -> dict:
    """
    Базовая функция для выполнения запросов к WAN2.2 API
    
    Args:
        endpoint: endpoint API (например, "/generate", "/generate/image", "/generate/video")
        payload: данные для отправки
        api_url: URL API (по умолчанию из конфига)
        timeout: таймаут запроса в секундах
        
    Returns:
        dict с полем result и метриками производительности
    """
    api_url = api_url or get_wan_api_url()
    timeout = timeout or get_timeout()
    
    full_url = f"{api_url}{endpoint}"
    
    start_time = time.time()
    
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            logger.info(f"Sending request to {full_url}")
            
            response = await client.post(
                full_url,
                json=payload,
            )
            response.raise_for_status()
            
            elapsed = time.time() - start_time
            
            result = response.json()
            
            logger.info(f"Request completed in {elapsed:.2f}s")
            
            return {
                "result": result,
                "elapsed_time": elapsed,
                "api_url": api_url
            }
            
    except httpx.ConnectError:
        elapsed = time.time() - start_time
        logger.warning(f"API недоступно по адресу {api_url}. Используется mock.")
        
        # Mock для тестирования когда API недоступно
        mock_result = {
            "content": f"Mock result for: {payload.get('prompt', 'N/A')}",
            "status": "mock",
            "note": f"Реальный API по адресу {api_url} недоступен"
        }
        
        return {
            "result": mock_result,
            "elapsed_time": elapsed,
            "api_url": api_url,
            "warning": "API недоступно, используется mock"
        }
        
    except httpx.TimeoutException:
        elapsed = time.time() - start_time
        logger.error(f"Request timeout after {elapsed:.2f}s")
        
        return {
            "result": None,
            "error": f"Timeout after {elapsed:.2f}s",
            "elapsed_time": elapsed,
            "api_url": api_url
        }
        
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"Error during request: {str(e)}")
        
        return {
            "result": None,
            "error": str(e),
            "elapsed_time": elapsed,
            "api_url": api_url
        }


async def generate_text(
    prompt: str,
    api_url: Optional[str] = None,
    timeout: Optional[int] = None
) -> dict:
    """
    Генерирует текст используя WAN2.2 API
    
    Args:
        prompt: Текст запроса пользователя
        api_url: URL API (по умолчанию из конфига)
        timeout: Таймаут запроса в секундах
        
    Returns:
        dict с полем result и метриками производительности
    """
    return await _make_request(
        endpoint="/generate",
        payload={"prompt": prompt},
        api_url=api_url,
        timeout=timeout
    )


async def generate_image(
    prompt: str,
    negative_prompt: Optional[str] = None,
    width: int = 1024,
    height: int = 1024,
    steps: int = 50,
    api_url: Optional[str] = None,
    timeout: Optional[int] = None
) -> dict:
    """
    Генерирует изображение используя WAN2.2 API
    
    Args:
        prompt: Описание изображения
        negative_prompt: Что не должно быть на изображении
        width: Ширина изображения
        height: Высота изображения
        steps: Количество шагов генерации
        api_url: URL API (по умолчанию из конфига)
        timeout: Таймаут запроса в секундах
        
    Returns:
        dict с URL изображения и метриками производительности
    """
    payload = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "steps": steps
    }
    
    if negative_prompt:
        payload["negative_prompt"] = negative_prompt
    
    return await _make_request(
        endpoint="/generate/image",
        payload=payload,
        api_url=api_url,
        timeout=timeout
    )


async def generate_video(
    prompt: str,
    duration: int = 5,
    fps: int = 24,
    size: Optional[str] = None,
    task: Optional[str] = None,
    ckpt_dir: Optional[str] = None,
    generate_script_path: Optional[str] = None,
    timeout: Optional[int] = None
) -> dict:
    """
    Генерирует видео используя локальный скрипт generate.py
    
    Args:
        prompt: Описание видео
        duration: Длительность в секундах (используется для логирования)
        fps: Кадров в секунду (используется для логирования)
        size: Размер видео в формате "width*height" (например, "1280*704")
        task: Задача для генерации (например, "ti2v-5B")
        ckpt_dir: Путь к директории с чекпоинтами
        generate_script_path: Путь к скрипту generate.py
        timeout: Таймаут выполнения в секундах
        
    Returns:
        dict с результатом генерации и метриками производительности
    """
    start_time = time.time()
    
    # Параметры по умолчанию
    size = size or get_video_size()
    task = task or get_ti2v_task()
    ckpt_dir = ckpt_dir or get_ckpt_dir()
    script_path = generate_script_path or get_generate_script_path()
    timeout = timeout or get_timeout()
    
    # Проверяем существование скрипта
    if not os.path.exists(script_path):
        elapsed = time.time() - start_time
        error_msg = f"Скрипт generate.py не найден по пути: {script_path}"
        logger.error(error_msg)
        return {
            "result": None,
            "error": error_msg,
            "elapsed_time": elapsed
        }
    
    logger.info(f"Запуск генерации видео: task={task}, size={size}, prompt='{prompt[:50]}...'")
    
    try:
        # Формируем команду для запуска скрипта
        cmd = [
            "python",
            script_path,
            "--task", task,
            "--size", size,
            "--ckpt_dir", ckpt_dir,
            "--offload_model", "True",
            "--convert_model_dtype",
            "--t5_cpu",
            "--prompt", prompt
        ]
        
        logger.info(f"Выполнение команды: {' '.join(cmd)}")
        
        # Запускаем процесс асинхронно
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=os.path.dirname(script_path) or os.getcwd()
        )
        
        # Ждем завершения с таймаутом
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            elapsed = time.time() - start_time
            error_msg = f"Таймаут генерации видео после {elapsed:.2f}s"
            logger.error(error_msg)
            return {
                "result": None,
                "error": error_msg,
                "elapsed_time": elapsed
            }
        
        elapsed = time.time() - start_time
        
        # Декодируем вывод
        stdout_text = stdout.decode('utf-8', errors='ignore') if stdout else ""
        stderr_text = stderr.decode('utf-8', errors='ignore') if stderr else ""
        
        if process.returncode == 0:
            logger.info(f"Генерация видео завершена успешно за {elapsed:.2f}s")
            
            # Пытаемся найти путь к сгенерированному видео в выводе
            video_path = None
            for line in stdout_text.split('\n'):
                if '.mp4' in line or '.avi' in line or 'output' in line.lower():
                    # Простая эвристика для поиска пути к видео
                    if os.path.exists(line.strip()):
                        video_path = line.strip()
                        break
            
            return {
                "result": {
                    "status": "success",
                    "video_path": video_path,
                    "stdout": stdout_text[-500:] if stdout_text else "",  # Последние 500 символов
                    "duration": duration,
                    "fps": fps,
                    "size": size
                },
                "elapsed_time": elapsed,
                "task": task
            }
        else:
            error_msg = f"Ошибка генерации видео: код возврата {process.returncode}"
            logger.error(f"{error_msg}\nSTDERR: {stderr_text}")
            
            return {
                "result": None,
                "error": error_msg,
                "stderr": stderr_text[-500:] if stderr_text else "",
                "elapsed_time": elapsed,
                "return_code": process.returncode
            }
            
    except Exception as e:
        elapsed = time.time() - start_time
        error_msg = f"Исключение при генерации видео: {str(e)}"
        logger.error(error_msg, exc_info=True)
        
        return {
            "result": None,
            "error": error_msg,
            "elapsed_time": elapsed
        }
