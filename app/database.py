import psycopg2
from psycopg2.pool import SimpleConnectionPool
from typing import Generator
from app.config.settings import get_settings

settings = get_settings()

class Database:
    def __init__(self):
        self.connection_params = {
            "user": settings.postgres_user,
            "password": settings.postgres_password,
            "host": settings.postgres_host,
            "port": settings.postgres_port,
            "database": settings.postgres_db,
        }
        self.pool = SimpleConnectionPool(1, 10, **self.connection_params)

    def get_connection(self) -> Generator:
        conn = self.pool.getconn()
        try:
            yield conn
        finally:
            self.pool.putconn(conn)

    def test_connection(self):
        try:
            with self.pool.getconn() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1;")
                print("Database connection successful!")
        except Exception as e:
            print(f"Database connection failed: {str(e)}")
            raise e
