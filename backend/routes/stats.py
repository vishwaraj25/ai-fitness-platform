from fastapi import APIRouter
from backend.db import DatabaseService

router = APIRouter()
db_service = DatabaseService()


@router.get("/stats")
async def get_stats():

    stats = db_service.get_stats()
    sessions = db_service.get_sessions(20)

    return {
        "stats": stats,
        "recent_sessions": sessions
    }
