##### Datenbank-Tabelle im GUI-Fenster anzeigen #####
# 04_DBausgabeFenster.py
import tkinter as tk                        # Tkinter-Hauptmodul für GUI-Fenster
from tkinter import ttk                     # Themed Tkinter für moderne Widgets (Treeview)
import mariadb                              # GEÄNDERT: Codegerüst hatte keinen DB-Import
from config import DB_LOCAL                 # Zentrale DB-Zugangsdaten aus config.py

# SQL-Abfrage: "einige Spalten aus einer Tabelle Ihrer Wahl" (laut Aufgabe)
SQL = "SELECT KundenCode, Firma, Kontaktperson, Ort, Land FROM kunde"

# Daten auslesen
def read_from_database():                   # Liest Spaltennamen und Daten aus der DB
    db = mariadb.connect(**DB_LOCAL)        # Verbindung zur DB aufbauen
    cur = db.cursor()                       # Cursor zum Ausführen von SQL erzeugen
    cur.execute(SQL)                        # SQL-Befehl an die DB senden
    spalten = [s[0] for s in cur.description]  # Spaltennamen aus Cursor-Metadaten ziehen
    daten = cur.fetchall()                  # Alle Ergebnis-Zeilen in eine Liste laden
    cur.close()                             # Cursor schließen (Ressourcen freigeben)
    db.close()                              # Verbindung schließen
    return spalten, daten                   # Beide Listen an Aufrufer zurückgeben

# Tkinter-Setup
def darstellung_tabelle():                  # Baut das Fenster mit der Tabelle auf
    spalten, daten = read_from_database()   # Daten + Spaltennamen aus DB holen
    fenster = tk.Tk()                       # Hauptfenster (root window) erzeugen
    fenster.title("Kunden-Übersicht")       # Fenstertitel in der Titelleiste
    fenster.geometry("800x400")             # Fenstergröße in Pixeln (Breite x Höhe)

    # Treeview = Tkinter-Widget für tabellarische Daten (wie eine Excel-Ansicht)
    tabelle = ttk.Treeview(fenster, columns=spalten, show="headings")
    for spalte in spalten:                  # Schleife über alle Spalten:
        tabelle.heading(spalte, text=spalte)    # Spaltenkopf-Text setzen
        tabelle.column(spalte, width=140)       # Spaltenbreite in Pixel festlegen
    for zeile in daten:                     # Schleife über alle Datenzeilen:
        tabelle.insert("", "end", values=zeile) # Zeile am Ende der Tabelle einfügen

    # Scrollbar – damit man bei vielen Zeilen runterscrollen kann
    scrollbar = ttk.Scrollbar(fenster, orient="vertical", command=tabelle.yview)
    tabelle.configure(yscrollcommand=scrollbar.set)  # Tabelle mit Scrollbar verbinden
    tabelle.pack(side="left", fill="both", expand=True)  # Tabelle links, füllt Fenster
    scrollbar.pack(side="right", fill="y")  # Scrollbar rechts, vertikal füllen

    fenster.mainloop()                      # Fenster anzeigen + auf Events warten (Klicks)

darstellung_tabelle()                       # Programm starten – baut das Fenster auf