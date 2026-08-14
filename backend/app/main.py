# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import (
    farmers_router,
    auth_router,
    loans_router,
    dashboard_router,
    ai_router,
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Digital Twin Farmer API",
    version="1.0.0",
    description="AI-powered digital twin platform for agricultural finance and farmer empowerment"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Digital Twin Farmer API is running.",
        "version": "1.0.0",
        "docs": "/docs"
    }

# Health check
@app.get("/health")
def health():
    return {"status": "healthy"}

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(farmers_router, prefix="/api/farmers", tags=["Farmers"])
app.include_router(loans_router, prefix="/api/loans", tags=["Loans"])
app.include_router(dashboard_router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(ai_router, prefix="/api/ai", tags=["AI"])