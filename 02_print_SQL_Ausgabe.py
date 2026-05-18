##### Mitarbeiter aus der Datenbank ausgeben #####
# 02_print_SQL_Ausgabe.py
# Autor: Johny | Datum: 2026-05-18
# Zweck: Alle Einträge der Tabelle personal auf der Konsole ausgeben
# Bibliothek: mariadb (pip install mariadb)

import mariadb                              # MariaDB-Bibliothek für DB-Zugriff
from config import DB_LOCAL                 # Zugangsdaten aus zentraler Config

try:                                        # Verbindungsaufbau mit Fehlerabfang
    db = mariadb.connect(**DB_LOCAL)        # ** entpackt Dict zu einzelnen Parametern
except mariadb.Error as fehler:             # Fängt mariadb-spezifische Fehler
    db = None                               # Bei Fehler: db auf None setzen
    print(f"Verbindung fehlgeschlagen: {fehler}")  # Fehlertext ausgeben

sql_Anweisung = "SELECT * FROM personal"    # Alle Spalten aller Mitarbeiter abfragen

# Führt die SQL-Abfrage aus und gibt jede Zeile in der Konsole aus
def testprint(dbc, sql_Anweisungc):         # dbc = Verbindung, sql_Anweisungc = Query
    if dbc is None:                         # Keine Verbindung vorhanden?
        print("Keine DB-Verbindung verfügbar")  # Nutzer informieren
        return                              # Funktion beenden
    cur = dbc.cursor()                      # Cursor erstellen – nötig zum SQL-Ausführen
    try:                                    # SQL ausführen mit Fehlerabfang
        cur.execute(sql_Anweisungc)         # SQL-Befehl an DB senden
        for zeile in cur.fetchall():        # Alle Ergebnis-Zeilen durchgehen
            print(zeile)                    # Zeile als Tupel ausgeben
    finally:                                # Immer ausführen (auch bei Fehler):
        cur.close()                         # Cursor schließen (Ressourcen freigeben)

testprint(db, sql_Anweisung)                # Abfrage ausführen und Ergebnis ausgeben
