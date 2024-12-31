import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

def verify_database():
    # Connection parameters from environment variables
    params = {
        'host': os.getenv('POSTGRES_HOST', 'localhost'),
        'port': os.getenv('POSTGRES_PORT', '54322'),
        'user': os.getenv('POSTGRES_USER', 'postgres'),
        'password': os.getenv('POSTGRES_PASSWORD', 'devops_assistant_pwd_2024'),
        'database': os.getenv('POSTGRES_DB', 'postgres')
    }

    try:
        # Try connecting to the database
        print("Attempting to connect to database...")
        conn = psycopg2.connect(**params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        print("✓ Successfully connected to database")

        # Check if schema exists
        cur.execute("""
            SELECT schema_name 
            FROM information_schema.schemata 
            WHERE schema_name = 'devops_assistant';
        """)
        
        if cur.fetchone() is None:
            print("✗ Schema 'devops_assistant' does not exist")
            print("Creating schema...")
            cur.execute("CREATE SCHEMA IF NOT EXISTS devops_assistant;")
            print("✓ Schema created")
        else:
            print("✓ Schema 'devops_assistant' exists")

        # Check if questions table exists
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'devops_assistant' 
            AND table_name = 'questions';
        """)
        
        if cur.fetchone() is None:
            print("✗ Table 'questions' does not exist")
            print("Creating table...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS devops_assistant.questions (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    text TEXT NOT NULL,
                    topic VARCHAR(100),
                    difficulty VARCHAR(50),
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    vector_id UUID,
                    metadata JSONB DEFAULT '{}'::jsonb
                );
            """)
            print("✓ Table created")
        else:
            print("✓ Table 'questions' exists")

        # Verify uuid-ossp extension
        cur.execute("""
            SELECT EXISTS (
                SELECT 1 FROM pg_extension WHERE extname = 'uuid-ossp'
            );
        """)
        
        if not cur.fetchone()[0]:
            print("✗ Extension 'uuid-ossp' not installed")
            print("Installing extension...")
            cur.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
            print("✓ Extension installed")
        else:
            print("✓ Extension 'uuid-ossp' is installed")

        cur.close()
        conn.close()
        return True

    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Database Verification Script")
    print("-" * 30)
    success = verify_database()
    if success:
        print("\n✓ All database checks completed successfully")
    else:
        print("\n✗ Database verification failed")
        sys.exit(1)