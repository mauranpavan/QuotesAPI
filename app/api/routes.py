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

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/quotes", tags=["Quotes"])

@router.get("/random")
async def read_random_quote(
    request: Request,
    ratelimit: str = Depends(RateLimiter(times=2, seconds=1))  # 2 requests per second
):
    """Get a random quote"""
    return get_random_quote()

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