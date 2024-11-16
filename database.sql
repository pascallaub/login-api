-- Datenbank erstellen
CREATE DATABASE IF NOT EXISTS user_database;

-- Zur Datenbank wechseln
USE user_database;

-- Tabelle für Benutzer erstellen
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);