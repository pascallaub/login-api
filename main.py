import uvicorn
from app.api import app
from app.db_connection import initialize_database

if __name__ == "__main__":
    initialize_database()
    uvicorn.run(app, host="127.0.0.1", port=8000)