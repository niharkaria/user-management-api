from fastapi import FastAPI
from database import engine, Base
from routes import router
from config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="A simple User Management API with authentication",
    version="1.0.0"
)

# Create tables on startup (async)
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Include routers
app.include_router(router, prefix="/api", tags=["users"])


# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to User Management API",
        "docs": "/docs",
        "version": "1.0.0"
    }
