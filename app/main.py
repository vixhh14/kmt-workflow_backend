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

app = FastAPI()
origins = [
    "http://localhost:5173",   # local frontend
    "https://kmt-workflow-tracker-qayt.vercel.app"  # deployed frontend
]
# CORS configuration – allow specific origins (including Vercel domain)
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
        print("Running startup tasks...")
        create_demo_users()
    except Exception as e:
        print(f"Error creating demo users: {e}")

@app.get("/")
def root():
    return {"message": "Workflow Tracker API running"}

# Include routers
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
