from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from fastapi import HTTPException
import logging
from datetime import datetime

# Import models
from app.models.question import QuestionCreate, QuestionResponse

# Custom exceptions
class DatabaseError(Exception):
    """Base exception for database errors"""
    pass

class ConnectionError(DatabaseError):
    """Raised when database connection fails"""
    pass

class QueryError(DatabaseError):
    """Raised when query execution fails"""
    pass

class DatabaseService:
    def __init__(self, connection_params):
        self.connection_params = connection_params
        self.logger = logging.getLogger(__name__)

    @contextmanager
    def get_connection(self):
        try:
            conn = psycopg2.connect(**self.connection_params, cursor_factory=RealDictCursor)
            yield conn
        except psycopg2.OperationalError as e:
            self.logger.error(f"Failed to connect to database: {str(e)}")
            raise ConnectionError(f"Database connection failed: {str(e)}")
        except Exception as e:
            self.logger.error(f"Unexpected error during database connection: {str(e)}")
            raise DatabaseError(f"Unexpected database error: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    async def create_question(self, question: QuestionCreate) -> QuestionResponse:
        query = """
        INSERT INTO devops_assistant.questions (text, topic, difficulty, metadata)
        VALUES (%(text)s, %(topic)s, %(difficulty)s, %(metadata)s)
        RETURNING id, text, topic, difficulty, created_at, vector_id, metadata;
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    try:
                        cur.execute(query, question.model_dump())
                        result = cur.fetchone()
                        if not result:
                            raise QueryError("Failed to create question: No result returned")
                        conn.commit()
                        return QuestionResponse(**result)
                    except psycopg2.Error as e:
                        conn.rollback()
                        self.logger.error(f"Query execution failed: {str(e)}")
                        raise QueryError(f"Failed to execute query: {str(e)}")
        except ConnectionError as e:
            raise HTTPException(status_code=503, detail=str(e))
        except QueryError as e:
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            self.logger.error(f"Unexpected error in create_question: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    async def get_questions_by_topic(self, topic: str) -> List[QuestionResponse]:
        query = """
        SELECT id, text, topic, difficulty, created_at, vector_id, metadata
        FROM devops_assistant.questions
        WHERE topic = %(topic)s
        ORDER BY created_at DESC;
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    try:
                        cur.execute(query, {'topic': topic})
                        results = cur.fetchall()
                        return [QuestionResponse(**row) for row in results]
                    except psycopg2.Error as e:
                        conn.rollback()
                        self.logger.error(f"Query execution failed: {str(e)}")
                        raise QueryError(f"Failed to execute query: {str(e)}")
        except ConnectionError as e:
            raise HTTPException(status_code=503, detail=str(e))
        except QueryError as e:
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            self.logger.error(f"Unexpected error in get_questions_by_topic: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")