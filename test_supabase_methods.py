from app.services.supabase import SupabaseService

def test_supabase_service():
    service = SupabaseService()

    # Test data
    table_name = "test_table"
    test_data = {"id": 1, "name": "Test Entry", "description": "This is a test"}

    # Insert data
    print("Inserting data...")
    insert_response = service.insert_data(table_name, test_data)
    print("Insert Response:", insert_response)

    # Fetch data
    print("Fetching data...")
    fetch_response = service.fetch_data(table_name, filters={"id": 1})
    print("Fetch Response:", fetch_response)

    # Update data
    print("Updating data...")
    update_response = service.update_data(table_name, filters={"id": 1}, updates={"description": "Updated description"})
    print("Update Response:", update_response)

    # Delete data
    print("Deleting data...")
    delete_response = service.delete_data(table_name, filters={"id": 1})
    print("Delete Response:", delete_response)

if __name__ == "__main__":
    test_supabase_service()
