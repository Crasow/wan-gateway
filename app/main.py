import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.logger import logger
from app.metrics import metrics
from app.routers import generate

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

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.perf_counter()
    try:
        response = await call_next(request)
        return response
    finally:
        latency = time.perf_counter() - start
        status = getattr(request.state, "status_code", None)
        if status is None:
            try:
                status = response.status_code
            except Exception:
                status = 500
        metrics.record(latency, status)

app.include_router(generate.router)


@app.get("/")
async def root():
    """Корневой endpoint для проверки работы API"""
    return {
        "status": "ok",
        "service": "WAN2.2 API Gateway",
        "version": "0.1.0"
    }

@app.get("/metrics")
async def get_metrics():
    return metrics.snapshot()

@app.on_event("startup")
async def startup_event():
    logger.info("WAN2.2 API Gateway started")
    logger.info("Server configuration:")
    logger.info(f"  - Default timeout: 300s")
    logger.info(f"  - Max concurrent requests: depends on uvicorn workers")
    logger.info("  - For production, configure uvicorn with proper workers")


# Rate limiting and concurrency control would be added here for production
