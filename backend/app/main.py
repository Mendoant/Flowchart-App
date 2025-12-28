from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import flow, balance, scenario

app = FastAPI(
    title="Smart Line Balancer API",
    description="Assembly flow optimization and line balancing system",
    version="0.1.0"
)

# CORS configuration for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(flow.router, prefix="/api/flow", tags=["flow"])
app.include_router(balance.router, prefix="/api/balance", tags=["balance"])
app.include_router(scenario.router, prefix="/api/scenario", tags=["scenario"])

@app.get("/")
async def root():
    return {
        "message": "Smart Line Balancer API",
        "status": "running",
        "version": "0.1.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
