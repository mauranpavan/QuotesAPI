from fastapi import FastAPI
from app.api.routes import router
from app.middleware.rate_limit import init_limiter, close_limiter
import logging
from app.api.metrics_router import router as metrics_router, MetricsMiddleware

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Quotes API", 
    version="1.0",
    description="A simple quotes API with rate limiting",
    docs_url="/docs",
    redoc_url="/redoc"
)

# app.include_router(metrics_router.router)
# app.middleware("http")(metrics_router.track_metrics)

# Add middleware
app.add_middleware(MetricsMiddleware)
app.include_router(metrics_router)

@app.on_event("startup")
async def startup():
    await init_limiter()

@app.on_event("shutdown")
async def shutdown():
    await close_limiter()

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Quotes API",
        "version": "1.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

app.include_router(router)