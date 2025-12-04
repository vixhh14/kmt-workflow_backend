from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    users_router,
    machines_routers,
    tasks_router,
    analytics_router,
    outsource_router,
    auth_router,
    planning_router,
    units_router,
    machine_categories_router,
    user_skills_router,
    approvals_router,
    admin_router,
)
from app.core.config import CORS_ORIGINS
import uvicorn

# Create FastAPI app with metadata
app = FastAPI(
    title="Workflow Tracker API",
    description="Backend API for KMT Workflow Tracker",
    version="1.0.0",
)

# CORS configuration
origins = [
    "http://localhost:5173",
    "https://kmt-workflow-tracker-qayt.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Startup event – create demo users if needed
@app.on_event("startup")
async def startup_event():
    from create_demo_users import create_demo_users
    try:
        print("🚀 Running startup tasks...")
        create_demo_users()
        print("✅ Startup complete")
    except Exception as e:
        print(f"❌ Error creating demo users: {e}")

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Workflow Tracker API running",
        "version": "1.0.0",
        "status": "healthy"
    }

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Include routers (NO /api prefix - routes are already prefixed)
app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(admin_router.router)
app.include_router(machines_routers.router)
app.include_router(tasks_router.router)
app.include_router(analytics_router.router)
app.include_router(outsource_router.router)
app.include_router(planning_router.router)
app.include_router(units_router.router)
app.include_router(machine_categories_router.router)
app.include_router(user_skills_router.router)
app.include_router(approvals_router.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
