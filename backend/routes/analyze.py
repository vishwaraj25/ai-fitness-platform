from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import tempfile
import shutil
import os
import uuid

from backend.services.ml_service import MLService
from backend.db import DatabaseService

router = APIRouter()

ml_service = MLService()
db_service = DatabaseService()


@router.post("/analyze")
async def analyze_video(
    file: UploadFile = File(...),
    exercise_type: str = Form(...)
):

    if exercise_type != "squat":
        raise HTTPException(status_code=400, detail="Only squat supported for now")

    if not file.filename.endswith((".mp4", ".mov", ".avi", ".mkv")):
        raise HTTPException(status_code=400, detail="Invalid video format")

    session_id = str(uuid.uuid4())

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp:
            shutil.copyfileobj(file.file, temp)
            temp_path = temp.name

        result = ml_service.analyze_video(temp_path)

        if result is None:
            raise Exception("No pose detected")

        rep_count = result["rep_count"]
        duration_seconds = result["duration_seconds"]
        dominant_error = result["analysis"]["dominant_error"]

        db_service.save_session({
            "session_id": session_id,
            "exercise_type": exercise_type,
            "rep_count": rep_count,
            "duration_seconds": duration_seconds,
            "dominant_error": dominant_error
        })

        return {
            "session_id": session_id,
            "exercise_type": exercise_type,
            "metrics": {
                "rep_count": rep_count,
                "duration_seconds": duration_seconds
            },
            "analysis": result["analysis"],
            "recommendations": result["recommendations"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if "temp_path" in locals():
            os.remove(temp_path)
