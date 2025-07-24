from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import time
from typing import Callable

# Import your Redis client
from app.core.redis_client import redis

router = APIRouter(prefix="/metrics", tags=["metrics"])

# Global metrics (consider using a class or proper state management)
class MetricsState:
    def __init__(self):
        self.total_quote_requests = 0
        self.total_response_time = 0.0
        self.start_time = time.time()

metrics_state = MetricsState()

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        if request.url.path == "/api/quote/random":
            start = time.time()
            response = await call_next(request)
            duration = time.time() - start
            metrics_state.total_quote_requests += 1
            metrics_state.total_response_time += duration
            return response
        return await call_next(request)

@router.get("/", response_class=PlainTextResponse)  # /metrics/
async def get_metrics():
    try:
        # Test Redis connection first
        ping_result = await redis.ping()
        print(f"Redis ping successful: {ping_result}")  # For debugging
        
        # Get Redis stats
        redis_stats = await redis.info(section="stats")
        redis_keyspace_hits = redis_stats.get("keyspace_hits", 0)
        redis_keyspace_misses = redis_stats.get("keyspace_misses", 0)
        
    except Exception as e:
        # If Redis is down, return default values
        print(f"Redis error in metrics: {str(e)}")  # For debugging
        redis_keyspace_hits = 0
        redis_keyspace_misses = 0
    
    # Calculate average response time
    avg_response_time = (
        metrics_state.total_response_time / metrics_state.total_quote_requests 
        if metrics_state.total_quote_requests > 0 else 0.0
    )
    
    # Format metrics text
    metrics_text = (
        f"redis_keyspace_hits {redis_keyspace_hits}\n"
        f"redis_keyspace_misses {redis_keyspace_misses}\n"
        f"total_quote_requests {metrics_state.total_quote_requests}\n"
        f"average_response_time_seconds {avg_response_time:.6f}\n"
    )
    
    return metrics_text

@router.get("/status", response_class=JSONResponse)
async def get_status():
    uptime = time.time() - metrics_state.start_time
    try:
        redis_up = await redis.ping()
    except Exception:
        redis_up = False
    return {
        "status": "ok",
        "redis_connected": redis_up,
        "total_quote_requests": metrics_state.total_quote_requests,
        "average_response_time_seconds": (
            metrics_state.total_response_time / metrics_state.total_quote_requests
            if metrics_state.total_quote_requests > 0 else 0.0
        ),
        "uptime_seconds": int(uptime),
        "app_version": "1.0.0"
    }