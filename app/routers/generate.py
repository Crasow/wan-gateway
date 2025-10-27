from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.logger import logger
from app.services.wan_client import generate_image, generate_text, generate_video

router = APIRouter(prefix="/api", tags=["WAN Generation"])


# Базовые модели запросов
class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="Текст запроса для генерации")
    api_url: Optional[str] = None
    timeout: Optional[int] = None


class ImageGenerationRequest(BaseModel):
    prompt: str = Field(..., description="Описание изображения")
    negative_prompt: Optional[str] = Field(None, description="Что не должно быть на изображении")
    width: int = Field(1024, ge=256, le=2048, description="Ширина изображения")
    height: int = Field(1024, ge=256, le=2048, description="Высота изображения")
    steps: int = Field(50, ge=10, le=100, description="Количество шагов генерации")
    api_url: Optional[str] = None
    timeout: Optional[int] = None


class VideoGenerationRequest(BaseModel):
    prompt: str = Field(..., description="Описание видео")
    duration: int = Field(5, ge=1, le=30, description="Длительность в секундах")
    fps: int = Field(24, ge=12, le=60, description="Кадров в секунду")
    size: Optional[str] = Field(None, description="Размер видео в формате 'width*height' (например, '1280*704')")
    task: Optional[str] = Field(None, description="Задача для генерации (например, 'ti2v-5B')")
    ckpt_dir: Optional[str] = Field(None, description="Путь к директории с чекпоинтами")
    generate_script_path: Optional[str] = Field(None, description="Путь к скрипту generate.py")
    timeout: Optional[int] = None


# Endpoints
@router.post("/generate/text")
async def generate_text_endpoint(request: GenerateRequest):
    """
    Генерирует текст на основе промпта через WAN2.2
    
    Принимает:
    - prompt: текст запроса (обязательно)
    - api_url: URL API (опционально)
    - timeout: таймаут в секундах (опционально)
    
    Возвращает результат генерации с метриками производительности
    """
    if not request.prompt or not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt не может быть пустым")
    
    logger.info(f"Received text generation request with prompt length: {len(request.prompt)}")
    
    try:
        result = await generate_text(
            prompt=request.prompt,
            api_url=request.api_url,
            timeout=request.timeout
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error in text generation endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/image")
async def generate_image_endpoint(request: ImageGenerationRequest):
    """
    Генерирует изображение на основе промпта через WAN2.2
    
    Принимает:
    - prompt: описание изображения (обязательно)
    - negative_prompt: что не должно быть на изображении (опционально)
    - width: ширина изображения (опционально, по умолчанию 1024)
    - height: высота изображения (опционально, по умолчанию 1024)
    - steps: количество шагов генерации (опционально, по умолчанию 50)
    - api_url: URL API (опционально)
    - timeout: таймаут в секундах (опционально)
    
    Возвращает URL изображения и метрики производительности
    """
    if not request.prompt or not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt не может быть пустым")
    
    logger.info(f"Received image generation request: {request.width}x{request.height}, {request.steps} steps")
    
    try:
        result = await generate_image(
            prompt=request.prompt,
            negative_prompt=request.negative_prompt,
            width=request.width,
            height=request.height,
            steps=request.steps,
            api_url=request.api_url,
            timeout=request.timeout
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error in image generation endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/video")
async def generate_video_endpoint(request: VideoGenerationRequest):
    """
    Генерирует видео на основе промпта через локальный скрипт generate.py
    
    Принимает:
    - prompt: описание видео (обязательно)
    - duration: длительность в секундах (опционально, по умолчанию 5)
    - fps: кадров в секунду (опционально, по умолчанию 24)
    - size: размер видео в формате 'width*height' (опционально, по умолчанию '1280*704')
    - task: задача для генерации (опционально, по умолчанию 'ti2v-5B')
    - ckpt_dir: путь к директории с чекпоинтами (опционально)
    - generate_script_path: путь к скрипту generate.py (опционально)
    - timeout: таймаут в секундах (опционально, рекомендуется минимум 600)
    
    Возвращает путь к сгенерированному видео и метрики производительности
    
    ⚠️ Внимание: генерация видео может занимать много времени (5-15 минут)
    Запускает команду: python generate.py --task ti2v-5B --size 1280*704 --ckpt_dir ./Wan2.2-TI2V-5B --offload_model True --convert_model_dtype --t5_cpu --prompt "..."
    """
    if not request.prompt or not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt не может быть пустым")
    
    logger.info(f"Received video generation request: {request.duration}s, {request.fps}fps")
    
    try:
        result = await generate_video(
            prompt=request.prompt,
            duration=request.duration,
            fps=request.fps,
            size=request.size,
            task=request.task,
            ckpt_dir=request.ckpt_dir,
            generate_script_path=request.generate_script_path,
            timeout=request.timeout
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error in video generation endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Проверка здоровья API шлюза"""
    return {
        "status": "healthy",
        "service": "WAN2.2 API Gateway",
        "capabilities": {
            "text_generation": True,
            "image_generation": True,
            "video_generation": True
        }
    }
