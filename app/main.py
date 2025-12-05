"""
FastAPI Main Application
Entry point for the blockchain API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router
from .config.settings import settings

# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print("=" * 60)
    print("🚀 Blockchain API Starting...")
    print("=" * 60)
    print(f"📊 Mining Difficulty: {settings.MINING_DIFFICULTY}")
    print(f"💰 Mining Reward: {settings.MINING_REWARD}")
    print(f"🗄️  Supabase URL: {settings.SUPABASE_URL}")
    print("=" * 60)
    print("✓ Blockchain loaded and ready")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    print("\n" + "=" * 60)
    print("👋 Blockchain API Shutting Down...")
    print("=" * 60)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Blockchain API",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "api": "/api"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "blockchain-api"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
