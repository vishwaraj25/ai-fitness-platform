"""
Database Initialization Script
"""

import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from backend.services.db_service import DatabaseService, Base

def initialize_database():
    print("Initializing database...")

    db_service = DatabaseService()
    Base.metadata.create_all(db_service.engine)

    print("Database initialized successfully.")
    print("Tables created:")
    print(" - workout_sessions")

if __name__ == "__main__":
    initialize_database()
