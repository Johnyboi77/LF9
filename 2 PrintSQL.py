##### Mitarbeiter aus der Datenbank ausgeben #####
# 02_print_SQL_Ausgabe.py
import mariadb                              # MariaDB-Bibliothek für DB-Zugriff
from config import DB_LOCAL                 # Zugangsdaten aus zentraler Config

# Connect to the MySQL database
# - Aufbau der Verbindung mit Fehlerbehandlung
try:                                        # Fehlerbehandlung für Verbindungsaufbau
    db = mariadb.connect(**DB_LOCAL)        # ** entpackt das Dict zu Parametern
except mariadb.Error as fehler:             # Fängt mariadb-spezifische Fehler ab
    db = None                               # Bei Fehler: db auf None setzen
    print(f"Verbindung fehlgeschlagen: {fehler}")  # Fehler im Klartext ausgeben

# definiere hier die SQL-Anweisung
sql_Anweisung = "SELECT * FROM personal"    # Alle Spalten aller Mitarbeiter holen

# gibt nach erfolgreicher Verbindung mit der Datenbank, die SQL-Abfrage zurück
def testprint(dbc, sql_Anweisungc):         # dbc=Verbindung, sql_Anweisungc=Query
    if dbc is None:                         # Wenn keine Verbindung übergeben wurde
        print("Keine DB-Verbindung verfügbar")  # Nutzer informieren
        return                              # Methode hier beenden
    cur = dbc.cursor()                      # Cursor zum Ausführen von SQL erzeugen
    try:                                    # Try/Finally um Cursor sauber zu schließen
        cur.execute(sql_Anweisungc)         # SQL-Befehl an DB senden
        for zeile in cur.fetchall():        # Alle Ergebnis-Zeilen durchgehen
            print(zeile)                    # Zeile als Tupel ausgeben
    finally:                                # Egal ob Erfolg oder Fehler:
        cur.close()                         # Cursor immer schließen (Ressourcen freigeben)

testprint(db, sql_Anweisung)                # Aufruf mit Verbindung + Query