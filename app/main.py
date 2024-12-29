from fastapi import FastAPI, HTTPException, Depends, status
from typing import List, Optional
import os
from dotenv import load_dotenv
import logging
import uvicorn
from datetime import datetime

# Import models and services
from app.models.question import QuestionCreate, QuestionResponse
from app.services.database import DatabaseService, DatabaseError

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="DevOps Teaching Assistant",
    description="AI-powered DevOps learning platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Database configuration
db_config = {
    "dbname": os.getenv("POSTGRES_DB", "postgres"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "devops_assistant_pwd_2024"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "54322")
}

# Initialize database service
logger.info(f"Connecting to database at {db_config['host']}:{db_config['port']}")
db_service = DatabaseService(db_config)

# Middleware to log requests
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    duration = datetime.now() - start_time
    logger.info(
        f"Method: {request.method}, Path: {request.url.path}, "
        f"Status: {response.status_code}, Duration: {duration.total_seconds()}s"
    )
    return response

# Error handler for database errors
@app.exception_handler(DatabaseError)
async def database_error_handler(request, exc):
    logger.error(f"Database error: {str(exc)}")
    return {
        "status_code": status.HTTP_503_SERVICE_UNAVAILABLE,
        "detail": "Database service unavailable"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Check the health of the application and its dependencies
    """
    try:
        with db_service.get_connection() as conn:
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "database": "connected",
                "version": "1.0.0"
            }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "database": "disconnected",
            "error": str(e)
        }

# Question endpoints
@app.post(
    "/questions/",
    response_model=QuestionResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["questions"]
)
async def create_question(question: QuestionCreate):
    """
    Create a new question
    """
    try:
        return await db_service.create_question(question)
    except HTTPException as e:
        raise
    except Exception as e:
        logger.error(f"Error creating question: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get(
    "/questions/topic/{topic}",
    response_model=List[QuestionResponse],
    tags=["questions"]
)
async def get_questions_by_topic(topic: str):
    """
    Get all questions for a specific topic
    """
    try:
        questions = await db_service.get_questions_by_topic(topic)
        if not questions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No questions found for topic: {topic}"
            )
        return questions
    except HTTPException as e:
        raise
    except Exception as e:
        logger.error(f"Error getting questions by topic: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get(
    "/questions/{question_id}",
    response_model=QuestionResponse,
    tags=["questions"]
)
async def get_question(question_id: str):
    """
    Get a specific question by ID
    """
    try:
        question = await db_service.get_question_by_id(question_id)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question not found: {question_id}"
            )
        return question
    except HTTPException as e:
        raise
    except Exception as e:
        logger.error(f"Error getting question: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up DevOps Teaching Assistant")
    try:
        # Test database connection
        with db_service.get_connection() as conn:
            logger.info("Successfully connected to database")
    except Exception as e:
        logger.error(f"Failed to connect to database: {str(e)}")
        raise

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down DevOps Teaching Assistant")

# For running the application directly
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )