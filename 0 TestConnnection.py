##### Verbindung zur Datenbank herstellen #####
# 01_ConnectionTest.py
import mariadb                              # MariaDB-Bibliothek für DB-Zugriff
from config import DB_LOCAL                 # Zugangsdaten aus zentraler Config

# Verbindung zur Datenbank herstellen
# - Die DB-Daten kommen aus config.py (host, port, user, password, database)
# - mariadb.connect() versucht den Aufbau, wirft Fehler bei Misserfolg
try:                                        # Fehlerbehandlung für Verbindungsaufbau
    db = mariadb.connect(**DB_LOCAL)        # ** entpackt das Dict zu Parametern
except mariadb.Error as fehler:             # Fängt alle mariadb-spezifischen Fehler
    db = None                               # Bei Fehler: db auf None setzen
    print(f"Verbindungsaufbau fehlgeschlagen: {fehler}")  # Fehlertext ausgeben


# Die Methode prüft, ob eine erfolgreiche Verbindung zur Datenbank hergestellt werden kann.
# Ausgabe: gibt "successful" oder "fail" als print-Ausgabe zurück
def testConnection(dbc):                    # dbc = übergebene DB-Verbindung
    if dbc is None:                         # Keine Verbindung übergeben?
        print("fail")                       # → Fehlschlag
        return                              # Methode verlassen
    try:                                    # Test ob Verbindung wirklich aktiv ist
        dbc.ping()                          # Sendet ein Ping an den DB-Server
        print("successful")                 # Antwort kam → Verbindung lebt
    except mariadb.Error:                   # Ping fehlgeschlagen?
        print("fail")                       # → Fehlschlag


# Aufruf der Methode zum Testen der Datenbankverbindung
testConnection(db)                          # Übergibt die oben aufgebaute Verbindung