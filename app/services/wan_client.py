import httpx
import logging
import time
from typing import Optional, Dict, Any
from app.config import get_wan_api_url, get_timeout

logger = logging.getLogger(__name__)


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
    api_url: Optional[str] = None,
    timeout: Optional[int] = None
) -> dict:
    """
    Генерирует видео используя WAN2.2 API
    
    Args:
        prompt: Описание видео
        duration: Длительность в секундах
        fps: Кадров в секунду
        api_url: URL API (по умолчанию из конфига)
        timeout: Таймаут запроса в секундах (рекомендуется увеличить для видео)
        
    Returns:
        dict с URL видео и метриками производительности
    """
    payload = {
        "prompt": prompt,
        "duration": duration,
        "fps": fps
    }
    
    # Для видео используем увеличенный timeout по умолчанию
    if timeout is None:
        timeout = max(timeout or get_timeout(), 600)  # минимум 10 минут
    
    return await _make_request(
        endpoint="/generate/video",
        payload=payload,
        api_url=api_url,
        timeout=timeout
    )
