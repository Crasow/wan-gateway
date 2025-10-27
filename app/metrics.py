"""
Модуль для отслеживания метрик производительности API
"""
import time
from collections import defaultdict
from threading import Lock
from typing import Dict, Any


class Metrics:
    """Класс для сбора и хранения метрик"""
    
    def __init__(self):
        self._lock = Lock()
        self.total_requests = 0
        self.total_latency = 0.0
        self.requests_by_status = defaultdict(int)
        self.requests_by_endpoint = defaultdict(int)
        self.start_time = time.time()
    
    def record(self, latency: float, status_code: int, endpoint: str = None):
        """Записывает метрику запроса"""
        with self._lock:
            self.total_requests += 1
            self.total_latency += latency
            self.requests_by_status[status_code] += 1
            if endpoint:
                self.requests_by_endpoint[endpoint] += 1
    
    def snapshot(self) -> Dict[str, Any]:
        """Возвращает снимок текущих метрик"""
        with self._lock:
            avg_latency = self.total_latency / self.total_requests if self.total_requests > 0 else 0
            uptime = time.time() - self.start_time
            
            return {
                "total_requests": self.total_requests,
                "average_latency_ms": round(avg_latency * 1000, 2),
                "uptime_seconds": round(uptime, 2),
                "requests_per_second": round(self.total_requests / uptime if uptime > 0 else 0, 2),
                "status_codes": dict(self.requests_by_status),
                "endpoints": dict(self.requests_by_endpoint)
            }
    
    def reset(self):
        """Сбрасывает все метрики"""
        with self._lock:
            self.total_requests = 0
            self.total_latency = 0.0
            self.requests_by_status.clear()
            self.requests_by_endpoint.clear()
            self.start_time = time.time()


# Глобальный экземпляр метрик
metrics = Metrics()
