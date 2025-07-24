import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
import logging
from app.core.redis_client import redis_client 

logger = logging.getLogger(__name__)

async def init_limiter():
    """Initialize the rate limiter with Redis connection"""
    try:
        # redis_client = redis.from_url("redis://redis:6379", decode_responses=True)
        await FastAPILimiter.init(redis_client)
        logger.info("Rate limiter initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize rate limiter: {e}")
        raise

async def close_limiter():
    """Close the rate limiter connection"""
    try:
        await FastAPILimiter.close()
        logger.info("Rate limiter closed successfully")
    except Exception as e:
        logger.error(f"Error closing rate limiter: {e}")