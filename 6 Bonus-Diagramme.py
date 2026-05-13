##### Erweiterung 1.6: Umsatz-Dashboard mit RBAC und 3 Diagrammen #####
# 06_Umsatz_Dashboard.py
#
# === Bibliotheks-Dokumentation (Pflicht laut 01_Informationen) ===
# Bibliothek:        matplotlib
# Installation:      pip3 install matplotlib
# Verwendungszweck:  Erstellt drei Diagramme (Kreis + 2x Balken) und bettet sie
#                    via FigureCanvasTkAgg in ein Tkinter-Notebook (Tabs) ein.
#
# === Sinn / Zweck / Intuition ===
# Die Geschäftsführung benötigt für strategische Entscheidungen drei Sichten:
#   1) Wer sind die wichtigsten Kunden? (Top 5 + Sonstige, Anteil/Betrag)
#   2) Wie verläuft der Umsatz über Zeit? (Monatsverlauf)
#   3) Welche Artikel sind die Bestseller? (Top 10 Produkte)
# Diese sensiblen Zahlen sind durch RBAC geschützt (nur Geschäftsführung).

import tkinter as tk                                # GUI-Hauptmodul
from tkinter import ttk, messagebox                 # Themed Widgets + Dialoge
import mariadb                                      # DB-Zugriff
import matplotlib.pyplot as plt                     # Diagramm-Erstellung
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # matplotlib in tkinter
from config import DB_LOCAL                         # Zentrale DB-Zugangsdaten

# === Konfiguration =============================================================
ZUGRIFFSBERECHTIGTE = {"Geschäftsführung"}          # RBAC-Regel: nur Chef-Etage
TOP_N_KUNDEN = 5                                    # Top 5 Kunden, Rest = "Sonstige"

# === SQL-Queries (zentrale Sammlung, leichter zu pflegen) =====================
SQL_KUNDEN_UMSATZ = """
    SELECT k.Firma, SUM(bd.Anzahl * bd.Einzelpreis * (1 - bd.Rabatt)) AS Umsatz
    FROM kunde k
    JOIN bestellung b      ON k.KundenCode = b.KundenCode
    JOIN bestelldetails bd ON b.BestellNr  = bd.BestellNr
    GROUP BY k.KundenCode, k.Firma
    ORDER BY Umsatz DESC
"""                                                 # Alle Kunden mit Umsatz, sortiert

SQL_MONATSUMSATZ = """
    SELECT DATE_FORMAT(b.Bestelldatum, '%Y-%m') AS Monat,
           SUM(bd.Anzahl * bd.Einzelpreis * (1 - bd.Rabatt)) AS Umsatz
    FROM bestellung b
    JOIN bestelldetails bd ON b.BestellNr = bd.BestellNr
    GROUP BY Monat
    ORDER BY Monat
"""                                                 # Umsatz gruppiert nach Monat

SQL_TOP_ARTIKEL = """
    SELECT a.Artikelname, SUM(bd.Anzahl * bd.Einzelpreis * (1 - bd.Rabatt)) AS Umsatz
    FROM artikel a
    JOIN bestelldetails bd ON a.ArtikelNr = bd.ArtikelNr
    GROUP BY a.ArtikelNr, a.Artikelname
    ORDER BY Umsatz DESC
    LIMIT 10
"""                                                 # Top 10 Bestseller-Artikel

# === DB-Helfer (DRY) ===========================================================
def lade_daten(sql):                                # Universelle Abfrage-Funktion
    db = mariadb.connect(**DB_LOCAL)                # Verbindung aufbauen
    cur = db.cursor()                               # Cursor erstellen
    cur.execute(sql)                                # SQL ausführen
    daten = cur.fetchall()                          # Ergebnis als Liste holen
    cur.close()                                     # Cursor schließen
    db.close()                                      # Verbindung schließen
    return daten                                    # Liste von Tupeln zurückgeben

def zeichne_in_tab(parent, fig):                    # matplotlib-Figure in Tab einbetten
    canvas = FigureCanvasTkAgg(fig, master=parent)  # Adapter erzeugen
    canvas.draw()                                   # Zeichnen
    canvas.get_tk_widget().pack(fill="both", expand=True)  # Widget ins Tab packen

# === Diagramm 1: Kreisdiagramm Top 5 Kunden + Sonstige =========================
def kreisdiagramm_kunden(parent):
    daten = lade_daten(SQL_KUNDEN_UMSATZ)           # Alle Kunden-Umsätze holen
    top = daten[:TOP_N_KUNDEN]                      # Erste 5 = Top-Kunden
    rest = daten[TOP_N_KUNDEN:]                     # Alle anderen
    namen = [d[0] for d in top] + ["Sonstige"]      # Labels: 5 Namen + "Sonstige"
    werte = [float(d[1]) for d in top] + [float(sum(d[1] for d in rest))]  # Beträge
    gesamt = sum(werte)                             # Gesamtumsatz für Anteil-Berechnung
    fig, ax = plt.subplots(figsize=(8, 6))          # Zeichenfläche erstellen
    # Donut-Style mit autopct für Prozent + Euro-Betrag pro Segment
    ax.pie(werte, labels=namen,
           autopct=lambda p: f"{p:.1f}%\n€{p/100*gesamt:,.0f}",  # Beschriftung pro Slice
           startangle=90,                           # Bei 12 Uhr starten
           wedgeprops=dict(width=0.4))              # Donut-Hole (statt Vollkreis)
    ax.set_title(f"Top {TOP_N_KUNDEN} Kunden + Sonstige – Gesamt: €{gesamt:,.0f}")
    fig.tight_layout()                              # Ränder optimieren
    zeichne_in_tab(parent, fig)                     # In den Tab einbetten

# === Diagramm 2: Balkendiagramm Monatsumsatz ===================================
def balkendiagramm_monatsumsatz(parent):
    daten = lade_daten(SQL_MONATSUMSATZ)            # Monatsumsätze laden
    monate = [d[0] for d in daten]                  # X-Achse: Monats-Labels
    umsaetze = [float(d[1]) for d in daten]         # Y-Achse: Beträge (in float)
    fig, ax = plt.subplots(figsize=(10, 5))         # Zeichenfläche
    balken = ax.bar(monate, umsaetze, color="steelblue")  # Vertikale Balken
    ax.set_xlabel("Monat")                          # X-Achsen-Beschriftung
    ax.set_ylabel("Umsatz (€)")                     # Y-Achsen-Beschriftung
    ax.set_title("Gesamtumsatz pro Monat")          # Titel
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")  # X-Labels schräg
    for balken_einzeln in balken:                   # Über alle Balken iterieren
        hoehe = balken_einzeln.get_height()         # Balkenhöhe = Umsatz
        ax.annotate(f"€{hoehe:,.0f}",               # Betrag als Text anzeigen
                    xy=(balken_einzeln.get_x() + balken_einzeln.get_width()/2, hoehe),
                    xytext=(0, 3), textcoords="offset points",  # 3px über Balken
                    ha="center", fontsize=8)
    fig.tight_layout()
    zeichne_in_tab(parent, fig)

# === Diagramm 3: Horizontales Balkendiagramm Top 10 Artikel ===================
def balkendiagramm_top_artikel(parent):
    daten = lade_daten(SQL_TOP_ARTIKEL)             # Top 10 Artikel laden
    artikel = [d[0] for d in daten]                 # Artikelnamen
    umsaetze = [float(d[1]) for d in daten]         # Umsätze als float
    fig, ax = plt.subplots(figsize=(10, 5))         # Zeichenfläche
    balken = ax.barh(artikel, umsaetze, color="seagreen")  # Horizontale Balken
    ax.set_xlabel("Umsatz (€)")                     # X-Achse beschriften
    ax.set_title("Top 10 Artikel nach Umsatz")      # Titel
    ax.invert_yaxis()                               # Höchster Wert nach oben
    for balken_einzeln in balken:                   # Beträge an die Balken schreiben
        breite = balken_einzeln.get_width()         # Balkenbreite = Umsatz
        ax.annotate(f"€{breite:,.0f}",              # Betrag als Label
                    xy=(breite, balken_einzeln.get_y() + balken_einzeln.get_height()/2),
                    xytext=(3, 0), textcoords="offset points",  # 3px rechts vom Balken
                    va="center", fontsize=8)
    fig.tight_layout()
    zeichne_in_tab(parent, fig)

# === Dashboard öffnen (nach erfolgreichem Login) ===============================
def oeffne_dashboard(fenster, abteilung):
    for widget in fenster.winfo_children():         # Alle Login-Elemente entfernen
        widget.destroy()                            # ...damit Platz fürs Dashboard
    # Begrüßung oben
    tk.Label(fenster, text=f"Umsatz-Dashboard – angemeldet als: {abteilung}",
             font=("Arial", 14, "bold")).pack(pady=10)
    # Notebook = Tab-Container für die 3 Diagramme
    notebook = ttk.Notebook(fenster)                # Tab-Widget erzeugen
    notebook.pack(fill="both", expand=True, padx=10, pady=10)
    tab1 = ttk.Frame(notebook)                      # Tab-Container 1
    tab2 = ttk.Frame(notebook)                      # Tab-Container 2
    tab3 = ttk.Frame(notebook)                      # Tab-Container 3
    notebook.add(tab1, text="Top Kunden (Anteile)")  # Tab 1 hinzufügen
    notebook.add(tab2, text="Monatsumsatz")          # Tab 2 hinzufügen
    notebook.add(tab3, text="Top 10 Artikel")        # Tab 3 hinzufügen
    kreisdiagramm_kunden(tab1)                      # Diagramm 1 in Tab 1 zeichnen
    balkendiagramm_monatsumsatz(tab2)               # Diagramm 2 in Tab 2 zeichnen
    balkendiagramm_top_artikel(tab3)                # Diagramm 3 in Tab 3 zeichnen

# === Login + Berechtigungsprüfung =============================================
def login_pruefen(abteilung_var, passwort_entry, fenster):
    abteilung = abteilung_var.get()                 # Gewählte Abteilung
    passwort = passwort_entry.get()                 # Eingegebenes Passwort
    if passwort != abteilung:                       # Passwort = Abteilungsname (lt. Aufgabe)
        messagebox.showerror("Login fehlgeschlagen", "Falsches Passwort.")
        return                                      # Methode beenden
    if abteilung not in ZUGRIFFSBERECHTIGTE:        # Berechtigungs-Check (RBAC)
        messagebox.showwarning("Zugriff verweigert",
            f"Die Abteilung '{abteilung}' darf das Dashboard nicht sehen.\n"
            f"Berechtigt: {', '.join(ZUGRIFFSBERECHTIGTE)}")
        return                                      # Methode beenden
    oeffne_dashboard(fenster, abteilung)            # Login okay → Dashboard öffnen

# === GUI-Aufbau (Login-Maske) ==================================================
def start_gui():
    fenster = tk.Tk()                               # Hauptfenster
    fenster.title("Umsatz-Dashboard (Login erforderlich)")
    fenster.geometry("1100x650")                    # Etwas größer für die Charts
    tk.Label(fenster, text="Abteilung:", font=("Arial", 12)).pack(pady=(20, 5))
    abteilung_var = tk.StringVar(value="Lager")     # Vorauswahl Lager (zum Testen RBAC)
    ttk.Combobox(fenster, textvariable=abteilung_var,
                 values=["Lager", "Verwaltung", "Marketing", "Geschäftsführung"],
                 state="readonly", font=("Arial", 12)).pack()  # Dropdown
    tk.Label(fenster, text="Passwort:", font=("Arial", 12)).pack(pady=(15, 5))
    pw_entry = tk.Entry(fenster, show="*", font=("Arial", 12))  # Maskierte Eingabe
    pw_entry.pack()
    # Enter-Taste löst Login aus (laut Aufgabe 2.1 gewünschtes Verhalten)
    pw_entry.bind("<Return>", lambda e: login_pruefen(abteilung_var, pw_entry, fenster))
    tk.Button(fenster, text="Anmelden", font=("Arial", 12),
              command=lambda: login_pruefen(abteilung_var, pw_entry, fenster)).pack(pady=15)
    fenster.mainloop()                              # Event-Loop starten

start_gui()                                         # Programm starten