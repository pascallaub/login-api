from .db_connection import create_connection, execute_sql_file
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def register_user(username, password):
    connection = create_connection()

    cursor = connection.cursor()

    # Prüfen ob Name schon vorhanden ist
    query_check = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query_check, (username,))
    if cursor.fetchone():
        cursor.close()
        connection.close()
        return "Benutzername existiert bereits!"
    
    # Benutzer hinzufügen
    hashed_password = hash_password(password)
    query_insert = """
        INSERT INTO users (username, hashed_password)
        VALUES (%s, %s)        
    """
    cursor.execute(query_insert, (username, hashed_password))
    connection.commit()

    cursor.close()
    connection.close()
    return "Benutzer erfolgreich registriert"

def authenticate_user(username, password):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    # Benutzer anhand des Benutzernamens suchen
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    # Überprüfen, ob der Benutzer existiert und Passwort korrekt ist
    if user and bcrypt.checkpw(password.encode('utf-8'), user['hashed_password'].encode('utf-8')):
        return "Login erfolgreich"
    return "Ungültiger Benutzername oder Passwort"

if __name__ == "__main__":
    connection = create_connection()

    # SQL-Datei ausführen
    try:
        execute_sql_file(connection, "database.sql")
        print("Datenbank und Tabellen erfolgreich erstellt!")
    except Exception as e:
        print(f"Fehler beim Ausführen der SQL-Datei:", e)
    finally:
        connection.close()