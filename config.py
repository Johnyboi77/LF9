# config.py - Zentrale Konfiguration für DB-Zugang
# Bibliothek: keine zusätzliche - reine Datenhaltung (nur Dictionaries)
# Verwendungszweck: Vermeidet doppelten Code (DRY-Prinzip) – alle Dateien importieren von hier

# Lokale Entwicklungs-Verbindung (Fallback / Entwicklung auf eigenem Rechner)
DB_LOCAL = {                       # Dictionary mit Verbindungsdaten (für lokale Tests)
    "host":     "localhost",       # MariaDB läuft auf dem gleichen Rechner
    "port":     3306,              # Standard-Port für MariaDB/MySQL
    "user":     "root",            # DB-Benutzer
    "password": "root123",         # lokales Passwort
    "database": "heiner"           # Name der importierten Datenbank
}

# Schul-Server-Verbindung – aktiv im Projekt (IP aus Lehrer-PDF)
DB_SERVER = {                      # Dictionary mit Server-Verbindungsdaten
    "host":     "10.145.240.124",  # IP-Adresse des Schul-Servers
    "port":     3306,              # Standard-Port MariaDB/MySQL
    "user":     "root",            # DB-Benutzer auf dem Server
    "password": "passwort",        # Server-Passwort (lt. Aufgabenstellung)
    "database": "HeinerIT2025"     # Datenbankname auf dem Server
}
