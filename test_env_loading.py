from app.config.settings import get_settings

def main():
    try:
        settings = get_settings()
        print("Environment variables loaded successfully:")
        print(settings.dict())
    except Exception as e:
        print(f"Error loading environment variables: {e}")

if __name__ == "__main__":
    main()
