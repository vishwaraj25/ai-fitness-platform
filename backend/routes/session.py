from fastapi import APIRouter
from backend.db import DatabaseService

router = APIRouter()
db_service = DatabaseService()


@router.get("/sessions")
async def get_sessions(limit: int = 50):
    sessions = db_service.get_sessions(limit)
    return {
        "sessions": sessions,
        "total": len(sessions)
    }
