import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import time

def wait_for_postgres():
    """Wait for PostgreSQL to become available"""
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            conn = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password="devops_assistant_pwd_2024",
                host="localhost",
                port="54322"
            )
            conn.close()
            return True
        except psycopg2.OperationalError:
            print(f"Waiting for PostgreSQL... ({attempt + 1}/{max_attempts})")
            time.sleep(1)
    return False

def init_database():
    """Initialize the database schema"""
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="devops_assistant_pwd_2024",
        host="localhost",
        port="54322"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    # Create extensions
    cur.execute("""
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        CREATE EXTENSION IF NOT EXISTS "pg_trgm";
    """)

    # Create schema
    cur.execute("""
    CREATE SCHEMA IF NOT EXISTS devops_assistant;
    """)

    # Create tables
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

    CREATE TABLE IF NOT EXISTS devops_assistant.responses (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        question_id UUID REFERENCES devops_assistant.questions(id),
        text TEXT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        feedback_score INTEGER,
        metadata JSONB DEFAULT '{}'::jsonb
    );

    CREATE TABLE IF NOT EXISTS devops_assistant.topics (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        name VARCHAR(100) UNIQUE NOT NULL,
        description TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """)

    # Create indexes
    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_questions_topic ON devops_assistant.questions(topic);
    CREATE INDEX IF NOT EXISTS idx_questions_difficulty ON devops_assistant.questions(difficulty);
    CREATE INDEX IF NOT EXISTS idx_questions_vector_id ON devops_assistant.questions(vector_id);
    CREATE INDEX IF NOT EXISTS idx_responses_question_id ON devops_assistant.responses(question_id);
    CREATE INDEX IF NOT EXISTS idx_questions_text_trigram ON devops_assistant.questions USING gin (text gin_trgm_ops);
    """)

    # Insert some initial topics
    cur.execute("""
    INSERT INTO devops_assistant.topics (name, description)
    VALUES 
        ('Docker', 'Container platform and tooling'),
        ('Kubernetes', 'Container orchestration'),
        ('CI/CD', 'Continuous Integration and Deployment'),
        ('Infrastructure', 'Infrastructure and cloud services'),
        ('Monitoring', 'System and application monitoring')
    ON CONFLICT (name) DO NOTHING;
    """)

    cur.close()
    conn.close()

def main():
    print("Waiting for PostgreSQL to become available...")
    if not wait_for_postgres():
        print("Failed to connect to PostgreSQL")
        return

    print("Initializing database schema...")
    try:
        init_database()
        print("Database initialization completed successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == "__main__":
    main()