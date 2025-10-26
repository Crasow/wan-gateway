from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.routers import generate

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="WAN2.2 API Gateway",
    description="API Gateway для работы с WAN2.2 моделью",
    version="0.1.0"
)

# Настройка CORS для работы с фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate.router)


@app.get("/")
async def root():
    """Корневой endpoint для проверки работы API"""
    return {
        "status": "ok",
        "service": "WAN2.2 API Gateway",
        "version": "0.1.0"
    }


@app.on_event("startup")
async def startup_event():
    logger.info("WAN2.2 API Gateway started")
