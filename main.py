
from fastapi import FastAPI
from database import engine, Base
from routes import router
from config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastApi app
app = FastAPI(
    title=settings.APP_NAME,
    description="A simple User Management API with authentication",
    version="1.0.0"
)

# Include routes
app.include_router(router, prefix="/api", tags=["users"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to User Mangement API",
        "docs": "/docs",
        "version": "1.0.0"
    }