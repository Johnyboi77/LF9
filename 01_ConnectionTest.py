##### Verbindung zur Datenbank testen #####
# 01_ConnectionTest.py
# Autor: Johny | Datum: 2026-05-18
# Zweck: Prüft ob die MariaDB-Verbindung steht (lt. Codegerüst Hr. Ullmann)
# Bibliothek: mariadb (pip install mariadb)

import mariadb                              # MariaDB-Bibliothek für DB-Zugriff
from config import DB_LOCAL                 # Zugangsdaten aus zentraler Config

try:                                        # Verbindungsaufbau mit Fehlerabfang
    db = mariadb.connect(**DB_LOCAL)        # ** entpackt Dict zu einzelnen Parametern
except mariadb.Error as fehler:             # Fängt mariadb-spezifische Fehler
    db = None                               # Bei Fehler: db auf None setzen
    print(f"Verbindungsaufbau fehlgeschlagen: {fehler}")  # Fehlertext ausgeben

# Prüft ob die übergebene Verbindung aktiv ist
# Ausgabe: "successful" oder "fail" auf der Konsole
def testConnection(dbc):                    # dbc = die zu prüfende DB-Verbindung
    if dbc is None:                         # Keine Verbindung vorhanden?
        print("fail")                       # → Fehlschlag melden
        return                              # Funktion beenden
    try:                                    # Ping-Versuch
        dbc.ping()                          # Sendet Ping an DB-Server
        print("successful")                 # Antwort kam → Verbindung lebt
    except mariadb.Error:                   # Ping fehlgeschlagen?
        print("fail")                       # → Fehlschlag melden

testConnection(db)                          # Verbindung testen und Ergebnis ausgeben
