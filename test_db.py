from app.database import Database

db = Database()

try:
    db.test_connection()
    print("PostgreSQL connection verified successfully!")
except Exception as e:
    print(f"PostgreSQL connection verification failed: {str(e)}")
