##### Daten als CSV bereitstellen #####
# 03_DBinCSV.py
### BIBs ###
import mariadb                              # GEÄNDERT: war mysql.connector (Bug im Gerüst)
import csv                                  # CSV-Modul aus Python-Standardbibliothek
from config import DB_LOCAL                 # Zentrale DB-Zugangsdaten

# MySQL Verbindung zur DB herstellen
try:                                        # Fehlerbehandlung für Verbindungsaufbau
    db = mariadb.connect(**DB_LOCAL)        # Verbindung über Daten aus config.py
except mariadb.Error as fehler:             # Bei Verbindungs-Fehler:
    db = None                               # db auf None setzen
    print(f"Verbindung fehlgeschlagen: {fehler}")  # Fehlertext ausgeben

# Name der zu exportierenden Tabelle (laut Aufgabe: Lagerbestand = artikel)
tabelle = "artikel"                         # String mit dem Tabellennamen

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
    finally:                                # Egal ob Erfolg oder Fehler:
        cur.close()                         # Cursor sauber schließen

tabelle_to_csv(tabelle, db)                 # Aufruf mit Tabellenname + Verbindung