from fastapi import FastAPI
from app.api.routes import router
from app.middleware.rate_limit import init_limiter, close_limiter
import logging
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Quotes API", 
    version="1.0",
    description="A simple quotes API with rate limiting",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.on_event("startup")
async def startup():
    logger.info("Starting up Quotes API...")
    try:
        await init_limiter()
        logger.info("Rate limiter initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize rate limiter: {e}")
        raise

@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutting down Quotes API...")
    try:
        await close_limiter()
        logger.info("Rate limiter closed successfully")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {
        "message": "Welcome to the Quotes API",
        "version": "1.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    try:
        # Write code to check database connection or external services
        return {"status": "healthy"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}, 500

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

app.include_router(router)
logger.info("Quotes API application initialized")