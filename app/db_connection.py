import sqlite3

def create_connection(database="user_database.sqlite"):
    try:
        connection = sqlite3.connect(database)
        print("Verbindung hergestellt.")
        return connection
    except Exception as e:
        print(f"Fehler beim Verbinden: {e}")
        return None
    
def execute_sql_file(connection, sql_file):
    try:
        with open(sql_file, "r") as file:
            sql_script = file.read()

        cursor = connection.cursor()
        cursor.executescript(sql_script)
        connection.commit()
    except sqlite3.Error as e:
        print(f"Fehler beim Ausführen: {e}")
    finally:
        cursor.close()

def initialize_database():
    with sqlite3.connect("user_database.sqlite") as connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                hashed_password TEXT NOT NULL
            )
        """)
        connection.commit()

