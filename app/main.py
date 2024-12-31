from fastapi import FastAPI, Depends, HTTPException, status
from psycopg2 import sql
from psycopg2.errors import DatabaseError
from app.database import Database
from app.config.settings import get_settings
from pydantic import BaseModel, Field
from typing import Optional

# Load settings
settings = get_settings()

# Initialize database instance
db = Database()

# Initialize FastAPI app
app = FastAPI(
    title="DevOps Teaching Assistant",
    version=settings.api_version,
    debug=settings.debug
)


# Item Model for Validation
class Item(BaseModel):
    name: str = Field(..., example="New-Item1")
    description: Optional[str] = Field(None, example="This is a new item")
    price: float = Field(..., example=490.99)


@app.on_event("startup")
async def startup():
    """Runs on application startup."""
    try:
        db.test_connection()
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get(f"{settings.api_prefix}/v1/items", tags=["Items"])
async def get_items(limit: int = 10, conn=Depends(db.get_connection)):
    """Fetch items from the database."""
    try:
        cursor = conn.cursor()
        cursor.execute(sql.SQL("SELECT * FROM items LIMIT %s;"), [limit])
        items = cursor.fetchall()
        return {"items": items}
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch items: {str(e)}")
    finally:
        conn.close()


@app.post(f"{settings.api_prefix}/v1/items", tags=["Items"], status_code=status.HTTP_201_CREATED)
async def create_item(item: Item, conn=Depends(db.get_connection)):
    """Create a new item in the database."""
    try:
        cursor = conn.cursor()
        cursor.execute(
            sql.SQL("INSERT INTO items (name, description, price) VALUES (%s, %s, %s) RETURNING id;"),
            [item.name, item.description, item.price]
        )
        item_id = cursor.fetchone()[0]
        conn.commit()
        return {"id": item_id, "message": "Item created successfully"}
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Failed to create item: {str(e)}")
    finally:
        cursor.close()
        conn.close()
