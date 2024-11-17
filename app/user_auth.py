import sqlite3
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def register_user(username, password):
    with sqlite3.connect("user_database.sqlite") as connection:
        cursor = connection.cursor()

        # Prüfen ob Name schon vorhanden ist
        query_check = "SELECT * FROM users WHERE username = ?"
        cursor.execute(query_check, (username,))
        if cursor.fetchone():
            cursor.close()
            connection.close()
            return "Benutzername existiert bereits!"
        
        # Benutzer hinzufügen
        hashed_password = hash_password(password)
        query_insert = """
            INSERT INTO users (username, hashed_password)
            VALUES (?, ?)        
        """
        cursor.execute(query_insert, (username, hashed_password))
        connection.commit()
        return "Benutzer erfolgreich registriert"

def authenticate_user(username, password):
    with sqlite3.connect("user_database.sqlite") as connection:
        cursor = connection.cursor()
        connection.row_factory = sqlite3.Row

        # Benutzer anhand des Benutzernamens suchen
        query = "SELECT * FROM users WHERE username = ?"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        cursor.close()

        # Überprüfen, ob der Benutzer existiert und Passwort korrekt ist
        if username and bcrypt.checkpw(password.encode('utf-8'), username[2].encode('utf-8')):
            return "Login erfolgreich"
        return "Ungültiger Benutzername oder Passwort"
