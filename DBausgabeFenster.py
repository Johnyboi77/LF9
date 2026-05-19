##### Datenbank-Tabelle im GUI-Fenster anzeigen #####
# DBausgabeFenster.py
# Autor: Johny | Datum: 2026-05-18
# Zweck: Tabelle kunde in einem Tkinter-Fenster als Tabelle anzeigen
# Bibliothek: tkinter (sudo pacman -S tk) | mariadb (pip install mariadb)

import tkinter as tk                        # Tkinter-Hauptmodul für GUI-Fenster
from tkinter import ttk                     # Themed Tkinter – für Treeview und Scrollbar
import mariadb                              # MariaDB-Bibliothek für DB-Zugriff
from config import DB_SERVER                # Zugangsdaten (Schul-Server) aus zentraler Config

SQL = "SELECT KundenCode, Firma, Kontaktperson, Ort, Land FROM kunde"  # Abzufragende Spalten

def read_from_database():                   # Liest Spaltennamen und Daten aus der DB
    try:                                    # Verbindungsaufbau mit Fehlerabfang
        db = mariadb.connect(**DB_SERVER)   # Verbindung aufbauen
    except mariadb.Error as fehler:         # Bei Verbindungsfehler:
        print(f"Verbindung fehlgeschlagen: {fehler}")  # Fehler ausgeben
        return [], []                       # Leere Listen zurückgeben (kein Absturz)
    cur = db.cursor()                       # Cursor zum SQL-Ausführen erzeugen
    cur.execute(SQL)                        # SQL-Befehl senden
    spalten = [s[0] for s in cur.description]  # Spaltennamen aus Cursor-Metadaten
    daten = cur.fetchall()                  # Alle Zeilen laden
    cur.close(); db.close()                 # Cursor und Verbindung schließen
    return spalten, daten                   # Spaltennamen + Datenzeilen zurückgeben

def darstellung_tabelle():                  # Baut das Tkinter-Fenster mit Tabelle auf
    spalten, daten = read_from_database()   # Daten aus DB holen
    if not spalten:                         # Bei Verbindungsfehler: kein Fenster öffnen
        return
    fenster = tk.Tk()                       # Hauptfenster erzeugen
    fenster.title("Kunden-Übersicht")       # Titel in der Titelleiste
    fenster.geometry("800x400")             # Fenstergröße (Breite x Höhe in Pixel)
    tabelle = ttk.Treeview(fenster, columns=spalten, show="headings")  # Tabellen-Widget
    for spalte in spalten:                  # Für jede Spalte:
        tabelle.heading(spalte, text=spalte)    # Spaltenkopf-Text setzen
        tabelle.column(spalte, width=140)       # Spaltenbreite in Pixel
    for zeile in daten:                     # Für jede Datenzeile:
        tabelle.insert("", "end", values=zeile) # Zeile am Ende einfügen
    scrollbar = ttk.Scrollbar(fenster, orient="vertical", command=tabelle.yview)
    tabelle.configure(yscrollcommand=scrollbar.set)  # Scrollbar mit Tabelle verbinden
    tabelle.pack(side="left", fill="both", expand=True)  # Tabelle links, füllt Fenster
    scrollbar.pack(side="right", fill="y")  # Scrollbar rechts
    fenster.mainloop()                      # Fenster anzeigen und auf Events warten

darstellung_tabelle()                       # Programm starten
