from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter
from app.services.quotes_loader import (
    get_random_quote, 
    get_all_quotes,
    get_quotes_by_category,
    get_quotes_by_author,
    get_available_categories,
    get_available_authors,
    get_stats
)
from typing import Optional
import logging
from prometheus_client import Counter, Histogram
import time

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/quotes", tags=["Quotes"])

# Create Prometheus metrics (put these at module level)
quote_requests_total = Counter('total_quote_requests', 'Total quote requests')
response_time_histogram = Histogram('average_response_time_seconds', 'Response time in seconds')

@router.get("/random")
async def read_random_quote(
    request: Request,
    ratelimit: str = Depends(RateLimiter(times=2, seconds=1))
):
    """Get a random quote"""
    start_time = time.time()
    
    # Increment the request counter
    quote_requests_total.inc()
    
    # Get the quote
    quote = get_random_quote()
    
    # Record response time
    response_time = time.time() - start_time
    response_time_histogram.observe(response_time)
    
    return quote

@router.get("/")
async def read_all_quotes(
    limit: int = 10,
    ratelimit: str = Depends(RateLimiter(times=5, seconds=60))  # 5 requests per minute
):
    """Get multiple random quotes"""
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be greater than 0")
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit cannot exceed 100")
    
    return {"quotes": get_all_quotes(limit), "count": limit}

@router.get("/categories")
async def get_categories(
    ratelimit: str = Depends(RateLimiter(times=10, seconds=60))
):
    """Get all available quote categories"""
    return {"categories": get_available_categories()}

@router.get("/authors")
async def get_authors(
    ratelimit: str = Depends(RateLimiter(times=10, seconds=60))
):
    """Get all available authors"""
    return {"authors": get_available_authors()}

@router.get("/category/{category}")
async def get_quotes_by_category_route(
    category: str,
    limit: int = 10,
    ratelimit: str = Depends(RateLimiter(times=10, seconds=60))
):
    """Get quotes from a specific category"""
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be greater than 0")
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit cannot exceed 100")
    
    quotes = get_quotes_by_category(category, limit)
    if not quotes:
        raise HTTPException(status_code=404, detail=f"No quotes found for category: {category}")
    
    return {"quotes": quotes, "category": category, "count": len(quotes)}

@router.get("/author/{author}")
async def get_quotes_by_author_route(
    author: str,
    limit: int = 10,
    ratelimit: str = Depends(RateLimiter(times=10, seconds=60))
):
    """Get quotes from a specific author"""
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be greater than 0")
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit cannot exceed 100")
    
    quotes = get_quotes_by_author(author, limit)
    if not quotes:
        raise HTTPException(status_code=404, detail=f"No quotes found for author: {author}")
    
    return {"quotes": quotes, "author": author, "count": len(quotes)}

@router.get("/stats")
async def get_quote_stats(
    ratelimit: str = Depends(RateLimiter(times=5, seconds=60))
):
    """Get statistics about the quotes dataset"""
    return get_stats()