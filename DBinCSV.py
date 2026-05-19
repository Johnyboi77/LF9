##### Daten als CSV bereitstellen #####
# DBinCSV.py
# Autor: Johny | Datum: 2026-05-18
# Zweck: Tabelle artikel aus der DB als CSV-Datei exportieren
# Bibliothek: mariadb (pip install mariadb) | csv (Python-Standard)
# Hinweis: Codegerüst hatte mysql.connector – wurde auf mariadb korrigiert

import mariadb                              # MariaDB-Bibliothek für DB-Zugriff
import csv                                  # CSV-Modul aus Python-Standardbibliothek
from config import DB_SERVER                # Zugangsdaten (Schul-Server) aus zentraler Config

# Verbindungsaufbau mit Fehlerabfang
try:                                        # Fehlerbehandlung für Verbindungsaufbau
    db = mariadb.connect(**DB_SERVER)       # Verbindung über Daten aus config.py
except mariadb.Error as fehler:             # Bei Verbindungs-Fehler:
    db = None                               # db auf None setzen
    print(f"Verbindung fehlgeschlagen: {fehler}")  # Fehlertext ausgeben

tabelle = "artikel"                         # Name der zu exportierenden Tabelle (Lagerbestand)

# Exportiert eine komplette Tabelle als CSV-Datei (Dateiname = Tabellenname.csv)
def tabelle_to_csv(tabellec, dbs):          # tabellec=Tabellenname, dbs=DB-Verbindung
    if dbs is None:                         # Ohne Verbindung kein Export möglich
        print("Keine DB-Verbindung verfügbar")
        return                              # Methode hier beenden
    cur = dbs.cursor()                      # Cursor erzeugen zum SQL-Ausführen
    try:                                    # Try/Finally für sauberes Schließen
        cur.execute(f"SELECT * FROM {tabellec}")    # Alle Spalten und Zeilen abfragen
        spalten = [s[0] for s in cur.description]   # Spaltennamen aus Metadaten holen
        daten = cur.fetchall()              # Alle Ergebnis-Zeilen in Liste laden
        # Datei öffnen: utf-8 für Umlaute, newline='' verhindert leere Zwischenzeilen
        with open(f"{tabellec}.csv", "w", newline="", encoding="utf-8") as datei:
            writer = csv.writer(datei, delimiter=";")  # ; als Trenner (Excel-DE-Standard)
            writer.writerow(spalten)        # Erste Zeile: Spaltenüberschriften
            writer.writerows(daten)         # Alle Datenzeilen darunter schreiben
        print(f"{len(daten)} Zeilen in {tabellec}.csv geschrieben")  # Erfolgsmeldung
    finally:                                # Immer ausführen (auch bei Fehler):
        cur.close()                         # Cursor schließen (Ressourcen freigeben)
        dbs.close()                         # Verbindung schließen (Ressourcen freigeben)

tabelle_to_csv(tabelle, db)                 # Export ausführen