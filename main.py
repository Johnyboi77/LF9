##### Hauptprogramm – Login mit Abteilungs-Dropdown (Tkinter) #####
# main.py
# Autor: Johny | Datum: 2026-05-18
# Zweck: Dropdown-Login mit RBAC + Tool-Auswahl (lt. Codegerüst Hr. Ullmann)
# Start: python main.py  (oder python3 21_dropdown.py)
# Bibliothek: tkinter (sudo pacman -S tk)

import tkinter as tk                               # Tkinter-Hauptmodul für GUI-Fenster
from tkinter import ttk, messagebox, scrolledtext  # Widgets + Fehler-Dialoge + Textfeld
import subprocess                                  # Startet andere Python-Dateien als Prozess
import ast                                         # Sicheres Parsen von Python-Tupeln
from dropdownmenu import (                         # Zentrale RBAC-Konfiguration (DRY)
    mitarbeiter_options,                           # Abteilungsliste für Login-Dropdown
    TOOLS,                                         # Abteilung → erlaubte Skript-Dateien
    ALLE_FEATURES,                                 # Feature-Liste für Übersicht nach Login
    FENSTER_TOOLS,                                 # Tools die ein eigenes Fenster öffnen
)

# Farbpalette – analog zur Browser-GUI (gleiche CSS-Variablen)
HDR  = "#1e3a5f"   # Header-Hintergrund
SIDE = "#243b55"   # Sidebar/Feature-Panel
BG   = "#f0f2f5"   # Inhaltsbereich-Hintergrund
CARD = "#ffffff"   # Karten und Panels
TXT  = "#2c3e50"   # Haupttext
MUT  = "#95a5a6"   # Gedimmter Text (gesperrte Features)
ACC  = "#2980b9"   # Blauer Akzent (Buttons, aktiv)
OK   = "#27ae60"   # Grün (freigeschaltete Features)
ERR  = "#e74c3c"   # Rot (Logout-Button)

# === Logik-Funktionen ================================================================

# Prüft Login – bei Erfolg Screen-Wechsel (lt. Codegerüst: testConnection-Prinzip)
def login():
    abt = abt_combo.get().strip()                  # Direkt vom Widget lesen (StringVar-Bug-Workaround)
    pw  = pw_var.get().strip()                     # Passwort ohne Leerzeichen
    if pw != abt:                                  # Passwort = Abteilungsname (lt. Aufgabe 2.1)
        messagebox.showerror("Fehler", "Falsches Passwort")
        return
    zeige_main(abt)                                # Zum Task-Screen wechseln

# Logout – Passwort leeren und zurück zum Login-Screen
def logout():
    pw_var.set("")                                 # Passwort-Feld leeren
    zeige_ausgabe("", ausgabe)                     # Ausgabe leeren
    zeige_login()                                  # Zurück zum Login-Screen

# Wechselt zum Login-Screen
def zeige_login():
    frame_main.place_forget()                      # Task-Screen ausblenden
    frame_login.place(relx=0, rely=0,              # Login-Screen einblenden
                      relwidth=1, relheight=1)

# Wechselt zum Task-Screen und befüllt Feature-Liste + Tool-Dropdown
def zeige_main(abt):
    frame_login.place_forget()                     # Login-Screen ausblenden
    erlaubt = TOOLS.get(abt, [])                   # Erlaubte Tools für diese Abteilung

    # Header aktualisieren
    lbl_abt.config(text=f"Abteilung: {abt}")

    # Feature-Liste auffrischen
    for widget in feat_frame.winfo_children():     # Alte Labels entfernen
        widget.destroy()

    # Navigations-Abschnitt (für alle Abteilungen sichtbar, kein RBAC)
    tk.Label(feat_frame, text="NAVIGATION", bg=SIDE,
             fg="#4a6a8a", font=("Arial", 9, "bold")).pack(anchor="w", padx=16, pady=(14, 6))
    tk.Button(feat_frame, text="  ⚡  Verbindung testen", bg=SIDE, fg=CARD,
              font=("Arial", 11), relief="flat", anchor="w", width=18,
              command=verbindung_testen).pack(anchor="w", padx=8, pady=3)

    tk.Label(feat_frame, text="FEATURES", bg=SIDE,
             fg="#4a6a8a", font=("Arial", 9, "bold")).pack(anchor="w", padx=16, pady=(14, 6))
    for datei, name, beschr in ALLE_FEATURES:      # Jedes Feature anzeigen
        freigesch = datei in erlaubt               # Freigeschaltet für diese Abteilung?
        symbol = "✓" if freigesch else "✗"
        farbe  = OK  if freigesch else MUT
        tk.Label(feat_frame, text=f"  {symbol}  {name}", bg=SIDE, fg=farbe,
                 font=("Arial", 11), anchor="w", width=18).pack(
                     anchor="w", padx=8, pady=3)   # Sichtbarer Eintrag mit Farb-Feedback

    # Tool-Dropdown befüllen
    tool_combo.config(values=erlaubt, state="readonly")
    tool_combo.set(erlaubt[0])                     # Erstes erlaubtes Tool vorauswählen

    frame_main.place(relx=0, rely=0,               # Task-Screen einblenden
                     relwidth=1, relheight=1)

# Führt den Verbindungstest (01_ConnectionTest.py) aus und zeigt das Ergebnis
def verbindung_testen():
    result = subprocess.run(
        ["python", "01_ConnectionTest.py"], capture_output=True, text=True)
    text = result.stdout or result.stderr or "(keine Ausgabe)"
    zeige_ausgabe(text, ausgabe)

# Startet das gewählte Tool – mit oder ohne eigenes Fenster
def run_tool():
    datei = tool_var.get()                         # Dateiname aus Dropdown lesen
    if not datei:
        return
    if datei in FENSTER_TOOLS:                     # 04: öffnet eigenes Fenster
        subprocess.Popen(["python", datei])        # Non-blocking starten
        zeige_ausgabe(f"▸ {datei} gestartet – Fenster öffnet sich separat\n", ausgabe)
    else:                                          # 02/03/05: Textausgabe einfangen
        result = subprocess.run(                   # Blockierend ausführen
            ["python", datei], capture_output=True, text=True)
        text = result.stdout or result.stderr or "(keine Ausgabe)"
        zeige_ausgabe(formatiere_ausgabe(text), ausgabe)  # Formatiert anzeigen

# Formatiert Tupel-Ausgabe (z.B. von 02) als ASCII-Tabelle
def formatiere_ausgabe(text):
    zeilen = [z.strip() for z in text.strip().splitlines() if z.strip()]
    tupel = []
    for z in zeilen:                               # Jede Zeile prüfen ob Tupel
        if z.startswith("(") and z.endswith(")"):
            try:   tupel.append(ast.literal_eval(z))  # Sicher parsen
            except: return text                    # Fallback: unformatiert
        else:   return text                        # Nicht alle Tupel → unformatiert
    if not tupel:
        return text
    breiten = [max(len(str(t[i])) for t in tupel) for i in range(len(tupel[0]))]
    trenner = "+" + "+".join("-" * (b + 2) for b in breiten) + "+"
    out = [trenner]
    for t in tupel:                                # Jede Zeile mit Padding formatieren
        out.append("|" + "|".join(f" {str(v):<{breiten[i]}} " for i, v in enumerate(t)) + "|")
    out.append(trenner)
    return "\n".join(out)

# Schreibt Text in das Ausgabe-Textfeld
def zeige_ausgabe(text, widget):
    widget.config(state="normal")                  # Schreibschutz aufheben
    widget.delete("1.0", "end")                    # Alten Inhalt löschen
    widget.insert("end", text)                     # Neuen Text einfügen
    widget.config(state="disabled")                # Wieder schreibgeschützt

# === GUI aufbauen ====================================================================
fenster = tk.Tk()                                  # Hauptfenster erstellen
fenster.title("Heiner IT-Systems GmbH")
fenster.configure(bg=HDR)
fenster.attributes("-fullscreen", True)            # Vollbild beim Start
fenster.bind("<Escape>",
             lambda e: fenster.attributes("-fullscreen", False))  # ESC = kein Vollbild

# ── SCREEN 1: Login ──────────────────────────────────────────────────────────────────
frame_login = tk.Frame(fenster, bg=HDR)            # Hintergrund: dunkles Blau

card = tk.Frame(frame_login, bg=CARD,              # Weiße Login-Karte (wie Browser .card)
                padx=52, pady=48, relief="flat")
card.place(relx=0.5, rely=0.5, anchor="center")    # Karte zentriert im Fenster

tk.Label(card, text="Heiner IT-Systems GmbH", bg=CARD, fg=HDR,
         font=("Arial", 22, "bold")).pack(pady=(0, 4))  # Firmenname
tk.Label(card, text="Datenbank-Verwaltungssystem", bg=CARD, fg=MUT,
         font=("Arial", 11)).pack(pady=(0, 32))    # Untertitel

tk.Label(card, text="ABTEILUNG", bg=CARD, fg=TXT,
         font=("Arial", 9, "bold"), anchor="w").pack(fill="x")
abt_var = tk.StringVar(value=mitarbeiter_options[0])
abt_combo = ttk.Combobox(card, textvariable=abt_var, values=mitarbeiter_options,
                          state="readonly", font=("Arial", 12), width=32)
abt_combo.pack(pady=(4, 18))                       # Referenz gespeichert für direktes .get()

tk.Label(card, text="PASSWORT", bg=CARD, fg=TXT,
         font=("Arial", 9, "bold"), anchor="w").pack(fill="x")
pw_var = tk.StringVar()
pw_entry = tk.Entry(card, textvariable=pw_var, show="*",
                    font=("Arial", 12), width=34,
                    bg="#f8f9fa", fg=TXT, relief="solid", bd=1)
pw_entry.pack(pady=(4, 28))

tk.Button(card, text="▶   Anmelden", bg=ACC, fg=CARD,
          font=("Arial", 12, "bold"), relief="flat", width=30, pady=10,
          command=login).pack(pady=(0, 8))
tk.Button(card, text="✕   Beenden", bg=ERR, fg=CARD,
          font=("Arial", 11), relief="flat", width=30, pady=8,
          command=fenster.destroy).pack()

pw_entry.bind("<Return>", lambda e: login())       # Enter = Login

# ── SCREEN 2: Task-Screen ────────────────────────────────────────────────────────────
frame_main = tk.Frame(fenster, bg=BG)              # Inhaltsbereich: helles Grau

# Header-Leiste
header = tk.Frame(frame_main, bg=HDR, height=52)   # Wie Browser <header>
header.pack(fill="x", side="top")
header.pack_propagate(False)                        # Höhe fixieren

tk.Label(header, text="▸ Heiner IT-Systems GmbH", bg=HDR, fg=CARD,
         font=("Arial", 13, "bold")).pack(side="left", padx=20, pady=14)

tk.Button(header, text="🔓  Abmelden", bg=ERR, fg=CARD,
          font=("Arial", 10, "bold"), relief="flat", padx=14, pady=6,
          command=logout).pack(side="right", padx=20, pady=10)  # Roter Logout-Button

lbl_abt = tk.Label(header, text="", bg=HDR, fg="#bdc3c7",
                   font=("Arial", 11))             # Zeigt aktuelle Abteilung
lbl_abt.pack(side="right", padx=8)

# Body: Sidebar + Inhalt
body = tk.Frame(frame_main, bg=BG)
body.pack(fill="both", expand=True)

# Sidebar – Feature-Übersicht (wie Browser <nav>)
sidebar = tk.Frame(body, bg=SIDE, width=200)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)                       # Breite fixieren
feat_frame = tk.Frame(sidebar, bg=SIDE)             # Auffrischbarer Bereich für Feature-Labels
feat_frame.pack(fill="both", expand=True)

# Inhalt rechts – Tool-Auswahl + Ausgabe
inhalt = tk.Frame(body, bg=BG)
inhalt.pack(side="left", fill="both", expand=True, padx=24, pady=24)

# Tool-Auswahl (Karte)
tool_karte = tk.Frame(inhalt, bg=CARD, relief="flat", bd=0)
tool_karte.pack(fill="x", pady=(0, 16))

tk.Label(tool_karte, text="Tool auswählen", bg=CARD, fg=MUT,
         font=("Arial", 9, "bold")).pack(anchor="w", padx=16, pady=(14, 4))

tool_zeile = tk.Frame(tool_karte, bg=CARD)
tool_zeile.pack(fill="x", padx=16, pady=(0, 16))

tool_var = tk.StringVar()
tool_combo = ttk.Combobox(tool_zeile, textvariable=tool_var,
                           state="disabled", font=("Arial", 11), width=36)
tool_combo.pack(side="left", padx=(0, 12))

tk.Button(tool_zeile, text="▶  Ausführen", bg=ACC, fg=CARD,
          font=("Arial", 11, "bold"), relief="flat", padx=16, pady=7,
          command=run_tool).pack(side="left")       # Ausführen-Button

# Ausgabe-Bereich (Karte)
ausgabe_karte = tk.Frame(inhalt, bg=CARD)
ausgabe_karte.pack(fill="both", expand=True)

tk.Label(ausgabe_karte, text="Ausgabe", bg=CARD, fg=MUT,
         font=("Arial", 9, "bold")).pack(anchor="w", padx=16, pady=(14, 4))

ausgabe = scrolledtext.ScrolledText(               # Scrollbares Textfeld für Ausgabe
    ausgabe_karte, font=("Courier", 10),
    bg="#f8f9fa", fg=TXT, relief="flat",
    state="disabled", padx=12, pady=8)
ausgabe.pack(fill="both", expand=True, padx=16, pady=(0, 16))

# Start: Login-Screen anzeigen
zeige_login()
fenster.mainloop()                                 # Event-Loop starten
