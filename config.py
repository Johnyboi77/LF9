# config.py - Zentrale Konfiguration für DB-Zugang
# Bibliothek: keine zusätzliche - reine Datenhaltung
# Verwendungszweck: Vermeidet doppelten Code (DRY-Prinzip)

# Lokale Entwicklungs-Verbindung (auf eigenem Rechner)
DB_LOCAL = {                       # Dictionary mit Verbindungsdaten
    "host": "localhost",           # MariaDB läuft auf dem gleichen Rechner
    "port": 3306,                  # Standard-Port für MariaDB/MySQL
    "user": "root",                # DB-Benutzer
    "password": "root123",         # lokales Passwort
    "database": "heiner"           # Name der importierten Datenbank
}

# Schul-Server-Verbindung (für Server-Umzug am Projektende)
DB_SERVER = {                      # Wird später aktiviert
    "host": "10.145.240.124",      # IP aus dem Lehrer-PDF
    "port": 3306,
    "user": "root",
    "password": "kwW2iQBhRxtiLs",  # Aus dem Lehrer-PDF
    "database": "heiner"
}