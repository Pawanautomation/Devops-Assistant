from app.config.settings import get_settings
import psycopg2
import logging
from supabase import create_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database_connection():
    """
    Test PostgreSQL connection using psycopg2.
    """
    settings = get_settings()
    try:
        logger.info("Testing PostgreSQL connection...")
        connection = psycopg2.connect(
            host=settings.postgres_host,
            port=settings.postgres_port,
            user=settings.postgres_user,
            password=settings.postgres_password,
            dbname=settings.postgres_db
        )
        logger.info("✓ PostgreSQL connection successful!")
        connection.close()
    except Exception as e:
        logger.error(f"✗ PostgreSQL connection failed: {e}")

def test_supabase_connection():
    """
    Test Supabase connection using the Supabase Python client.
    """
    settings = get_settings()
    try:
        logger.info("Testing Supabase configuration...")
        supabase_client = create_client(settings.supabase_url, settings.supabase_anon_key)
        # Attempt to fetch tables or another lightweight call to confirm connectivity
        response = supabase_client.table("Questions").select("*").execute()
        if response.data:
            logger.info(f"✓ Supabase connection successful! Sample data: {response.data}")
        else:
            logger.warning("✓ Supabase connection successful, but no data found.")
    except Exception as e:
        logger.error(f"✗ Supabase connection failed: {e}")

def main():
    """
    Run all configuration tests for the application.
    """
    logger.info("Starting configuration tests...")
    test_database_connection()
    test_supabase_connection()
    logger.info("Configuration testing completed!")

if __name__ == "__main__":
    main()
