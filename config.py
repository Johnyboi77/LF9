# config.py - Zentrale Konfiguration für DB-Zugang
# Bibliothek: keine zusätzliche - reine Datenhaltung
# Verwendungszweck: Vermeidet doppelten Code (DRY-Prinzip)

import mariadb # Import für echte Database in VM

# Lokale Entwicklungs-Verbindung (auf eigenem Rechner)
DB_LOCAL = {                       # Dictionary mit Verbindungsdaten
    "host": "localhost",           # MariaDB läuft auf dem gleichen Rechner
    "port": 3306,                  # Standard-Port für MariaDB/MySQL
    "user": "root",                # DB-Benutzer
    "password": "root123",         # lokales Passwort
    "database": "heiner"           # Name der importierten Datenbank
}

# Schul-Server-Verbindung (für Server-Umzug am Projektende)
DB_SERVER = mariadb.connect (       # Wird später aktiviert
    host="10.145.240.124",      # IP aus dem Lehrer-PDF
    user="root",
    password="passwort",
    database="HeinerIT2025"
)
