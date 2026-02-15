from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.routes.analyze import router as analyze_router
from backend.routes.session import router as sessions_router
from backend.routes.stats import router as stats_router

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- API ROUTES ----------------
app.include_router(analyze_router, prefix="/api")
app.include_router(sessions_router, prefix="/api")
app.include_router(stats_router, prefix="/api")

# ---------------- FRONTEND ----------------

app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
