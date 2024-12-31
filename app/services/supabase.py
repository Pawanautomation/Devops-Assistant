from supabase import create_client, Client
from typing import Optional, Dict, Any
import logging
from app.config.settings import get_settings

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get settings from the environment
settings = get_settings()

class SupabaseService:
    def __init__(self):
        """
        Initialize the Supabase client using the URL and service role key.
        """
        try:
            self.supabase: Client = create_client(
                settings.supabase_url,
                settings.supabase_service_role_key
            )
            logger.info("\u2713 Supabase client initialized successfully.")
        except Exception as e:
            logger.error(f"\u2717 Supabase client initialization failed: {e}")
            self.supabase = None

    def insert_data(self, table_name: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Insert data into the specified table in Supabase.
        :param table_name: Name of the Supabase table.
        :param data: Dictionary containing the data to insert.
        :return: The response data from Supabase, if successful; otherwise None.
        """
        if not self.supabase:
            logger.error("Supabase client is not initialized.")
            return None

        try:
            response = self.supabase.table(table_name).insert(data).execute()
            logger.info(f"\u2713 Data inserted into table '{table_name}' successfully.")
            return response.data
        except Exception as e:
            logger.error(f"\u2717 Failed to insert data into table '{table_name}': {e}")
            return None

    def fetch_data(self, table_name: str, filters: Dict[str, Any] = {}) -> Optional[list]:
        """
        Fetch data from the specified table with optional filters.
        :param table_name: Name of the Supabase table.
        :param filters: Dictionary containing the filters for the query.
        :return: A list of fetched data, if successful; otherwise None.
        """
        if not self.supabase:
            logger.error("Supabase client is not initialized.")
            return None

        try:
            query = self.supabase.table(table_name).select("*")
            for key, value in filters.items():
                query = query.eq(key, value)
            response = query.execute()
            logger.info(f"\u2713 Data fetched from table '{table_name}' successfully.")
            return response.data
        except Exception as e:
            logger.error(f"\u2717 Failed to fetch data from table '{table_name}': {e}")
            return None

    def update_data(self, table_name: str, filters: Dict[str, Any], updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update data in the specified table.
        :param table_name: Name of the Supabase table.
        :param filters: Dictionary containing the filters for the query.
        :param updates: Dictionary containing the fields to update.
        :return: The response data from Supabase, if successful; otherwise None.
        """
        if not self.supabase:
            logger.error("Supabase client is not initialized.")
            return None

        try:
            query = self.supabase.table(table_name)
            for key, value in filters.items():
                query = query.eq(key, value)
            response = query.update(updates).execute()
            logger.info(f"\u2713 Data updated in table '{table_name}' successfully.")
            return response.data
        except Exception as e:
            logger.error(f"\u2717 Failed to update data in table '{table_name}': {e}")
            return None

    def delete_data(self, table_name: str, filters: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Delete data from the specified table.
        :param table_name: Name of the Supabase table.
        :param filters: Dictionary containing the filters for the query.
        :return: The response data from Supabase, if successful; otherwise None.
        """
        if not self.supabase:
            logger.error("Supabase client is not initialized.")
            return None

        try:
            query = self.supabase.table(table_name)
            for key, value in filters.items():
                query = query.eq(key, value)
            response = query.delete().execute()
            logger.info(f"\u2713 Data deleted from table '{table_name}' successfully.")
            return response.data
        except Exception as e:
            logger.error(f"\u2717 Failed to delete data from table '{table_name}': {e}")
            return None
