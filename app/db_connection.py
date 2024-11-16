import mysql.connector

def create_connection():
    connection = mysql.connector.connect(
        database="user_database"
    )
    return connection

def execute_sql_file(connection, file_path):
    # SQL-Datei laden und ausführen
    with open("setup_database.sql", "r") as file:
        sql_commands = file.read()

    cursor = connection.cursor()
    for command in sql_commands.split(';'):
        if command.strip():
            cursor.execute(command)
    connection.commit()
    cursor.close()
