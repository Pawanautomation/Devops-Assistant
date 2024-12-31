from app.services.supabase import SupabaseService

def main():
    try:
        supabase_service = SupabaseService()
        if supabase_service.supabase:
            print("Supabase client initialized successfully!")
        else:
            print("Failed to initialize Supabase client.")
    except Exception as e:
        print(f"Error initializing Supabase client: {e}")

if __name__ == "__main__":
    main()
