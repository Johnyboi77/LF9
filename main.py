##### Hauptprogramm – Flask Web-App mit Login, RBAC, Dashboard, Features 1–6 #####
# main.py / 21_dropdown.py
# Autor: Johny | Datum: 2026-05-17
# Zweck: Browser-basierte App (http://localhost:5000) statt Tkinter-Fenster.
#        Alle Features 1–6 im Browser aufrufbar, Charts via Plotly.js.
#
# === Bibliotheks-Dokumentation ===
# Bibliothek:        flask
# Installation:      pip install flask
# Verwendungszweck:  Web-Framework – stellt Routen, Sessions und HTML-Templates bereit
#
# Bibliothek:        plotly.js (CDN – keine Installation)
# Verwendungszweck:  Interaktive Charts im Browser (ersetzt matplotlib)

from flask import (Flask, render_template, request,     # Flask-Kernfunktionen
                   session, redirect, url_for, jsonify) # Session, Routen, JSON-API
from functools import wraps                             # Für den Login-Decorator
import mariadb                                          # MariaDB-Datenbankzugriff
import csv                                              # CSV lesen/schreiben
import xml.etree.ElementTree as ET                      # XML schreiben
import pathlib                                          # Plattformübergreifende Pfade
from config import DB_LOCAL                             # Zentrale DB-Zugangsdaten

# === Flask-App initialisieren ====================================================
app = Flask(__name__)                                   # Flask-Instanz erstellen
app.secret_key = "lf9_heiner_2026_geheim"              # Schlüssel für Session-Verschlüsselung

# === RBAC-Mapping (Abteilung → erlaubte Feature-Schlüssel) =======================
TOOLS = {                                               # lt. LF9_Info.md Aufgabe 2.2
    "Lager":             ["f2", "f4"],
    "Verwaltung":        ["f2", "f3", "f4"],
    "Marketing":         ["f2", "f4", "f5"],
    "Geschäftsführung":  ["f2", "f3", "f4", "f5"],
}

# === SQL-Abfragen für Charts (Plotly.js via API) ==================================
SQL_KUNDEN_UMSATZ = """
    SELECT k.Firma, SUM(bd.Anzahl * bd.Einzelpreis * (1 - bd.Rabatt)) AS Umsatz
    FROM kunde k
    JOIN bestellung b      ON k.KundenCode = b.KundenCode
    JOIN bestelldetails bd ON b.BestellNr  = bd.BestellNr
    GROUP BY k.KundenCode, k.Firma ORDER BY Umsatz DESC
"""                                                     # Alle Kunden mit Umsatz

SQL_MONATSUMSATZ = """
    SELECT DATE_FORMAT(b.Bestelldatum, '%Y-%m') AS Monat,
           SUM(bd.Anzahl * bd.Einzelpreis * (1 - bd.Rabatt)) AS Umsatz
    FROM bestellung b
    JOIN bestelldetails bd ON b.BestellNr = bd.BestellNr
    GROUP BY Monat ORDER BY Monat
"""                                                     # Umsatz pro Monat

SQL_TOP_ARTIKEL = """
    SELECT a.Artikelname, SUM(bd.Anzahl * bd.Einzelpreis * (1 - bd.Rabatt)) AS Umsatz
    FROM artikel a
    JOIN bestelldetails bd ON a.ArtikelNr = bd.ArtikelNr
    GROUP BY a.ArtikelNr, a.Artikelname ORDER BY Umsatz DESC LIMIT 10
"""                                                     # Top 10 Bestseller-Artikel

# === DB-Hilfsfunktion =============================================================
def db_query(sql):                                      # SQL ausführen und Ergebnis zurückgeben
    conn = mariadb.connect(**DB_LOCAL)                  # Verbindung aufbauen
    cur  = conn.cursor()                                # Cursor erstellen
    cur.execute(sql)                                    # SQL ausführen
    cols = [d[0] for d in cur.description] if cur.description else []  # Spaltennamen
    rows = cur.fetchall()                               # Alle Zeilen laden
    cur.close(); conn.close()                           # Aufräumen
    return cols, rows                                   # Tupel zurückgeben

# === Login-Decorator (schützt alle Seiten außer /login) ===========================
def login_required(f):                                  # Decorator für geschützte Routen
    @wraps(f)                                           # Funktions-Metadaten beibehalten
    def decorated(*args, **kwargs):
        if "abteilung" not in session:                  # Nicht eingeloggt?
            return redirect(url_for("login"))           # → Weiterleitung zum Login
        return f(*args, **kwargs)                       # Eingeloggt → Funktion ausführen
    return decorated

# === Hilfsfunktion: Template-Kontext zusammenbauen ================================
def ctx(page, **extra):                                 # Standard-Kontext für alle Seiten
    abt = session.get("abteilung", "")                 # Aktuelle Abteilung aus Session
    return dict(page=page, abteilung=abt,              # Seiten-ID + Abteilung
                erlaubt=TOOLS.get(abt, []),             # Erlaubte Feature-Schlüssel
                **extra)                                # Weitere optionale Werte

# === Route: Login =================================================================
@app.route("/", methods=["GET", "POST"])                # GET = Login zeigen, POST = prüfen
def login():
    fehler = None                                       # Standard: kein Fehler
    if request.method == "POST":                        # Formular abgesendet?
        abt = request.form.get("abteilung", "")        # Gewählte Abteilung aus Formular
        pw  = request.form.get("passwort", "")         # Eingegebenes Passwort
        if pw == abt and abt:                           # Passwort = Abteilungsname (lt. Aufgabe)
            session["abteilung"] = abt                  # Abteilung in Session speichern
            return redirect(url_for("dashboard"))       # Weiterleitung zum Dashboard
        fehler = "Bitte versuche es erneut"
    return render_template("login.html", fehler=fehler) # Login-Seite mit opt. Fehlermeldung

# === Route: Logout ================================================================
@app.route("/logout")                                   # Abmelden-Link
def logout():
    session.clear()                                     # Session vollständig löschen
    return redirect(url_for("login"))                   # Zurück zum Login

# === Route: Dashboard =============================================================
@app.route("/dashboard")
@login_required                                         # Nur für eingeloggte Nutzer
def dashboard():
    return render_template("app.html", **ctx("dashboard"))  # Dashboard-Seite rendern

# === Route: Feature 1 – Verbindung testen =========================================
@app.route("/feature/1", methods=["GET", "POST"])       # POST = Test ausführen
@login_required
def feature1():
    status = None                                       # Standard: kein Ergebnis
    if request.method == "POST":                        # Button "Test starten" gedrückt?
        try:
            conn = mariadb.connect(**DB_LOCAL)          # Verbindungsversuch
            conn.ping()                                 # Ping senden
            conn.close()
            status = ("success", "✓  Verbindung erfolgreich")   # Erfolg
        except mariadb.Error as e:
            status = ("error", f"✗  Fehlgeschlagen: {e}")       # Fehler
    return render_template("app.html", **ctx("f1", status=status,
                                             db=DB_LOCAL))       # DB-Details für Anzeige

# === Route: Feature 2 – SQL ausgeben ==============================================
@app.route("/feature/2")
@login_required
def feature2():
    cols, rows = db_query("SELECT * FROM personal")     # Alle Mitarbeiter abfragen
    return render_template("app.html", **ctx("f2", cols=cols, rows=rows))

# === Route: Feature 3 – SQL → CSV =================================================
@app.route("/feature/3", methods=["GET", "POST"])
@login_required
def feature3():
    status = None
    if request.method == "POST":                        # Export-Button gedrückt
        pfad = pathlib.Path(__file__).parent / "artikel.csv"
        cols, rows = db_query("SELECT * FROM artikel")  # Alle Artikel holen
        with open(pfad, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter=";")            # Semikolon-Trenner
            w.writerow(cols)                            # Kopfzeile
            w.writerows(rows)                           # Datenzeilen
        status = ("success", f"✓  {len(rows)} Zeilen exportiert → {pfad}")
    return render_template("app.html", **ctx("f3", status=status))

# === Route: Feature 4 – DB-Tabelle anzeigen =======================================
@app.route("/feature/4")
@login_required
def feature4():
    cols, rows = db_query(                              # Kundendaten abfragen
        "SELECT KundenCode, Firma, Kontaktperson, Ort, Land FROM kunde")
    return render_template("app.html", **ctx("f4", cols=cols, rows=rows))

# === Route: Feature 5 – CSV → XML =================================================
@app.route("/feature/5", methods=["GET", "POST"])
@login_required
def feature5():
    status = None
    if request.method == "POST":                        # Konvertier-Button gedrückt
        pfad_csv = pathlib.Path(__file__).parent / "artikel.csv"
        pfad_xml = pathlib.Path(__file__).parent / "artikel.xml"
        if not pfad_csv.exists():                       # CSV muss vorhanden sein
            status = ("error", "✗  artikel.csv nicht gefunden — zuerst Feature 3 ausführen")
        else:
            root_el = ET.Element("artikel_liste")       # XML-Wurzelelement
            with open(pfad_csv, newline="", encoding="utf-8") as f:
                for zeile in csv.DictReader(f, delimiter=";"):
                    eintrag = ET.SubElement(root_el, "artikel")
                    for k, v in zeile.items():
                        ET.SubElement(eintrag, k).text = v
            baum = ET.ElementTree(root_el)
            ET.indent(baum, space="  ")                 # Lesbar einrücken
            baum.write(str(pfad_xml), encoding="utf-8", xml_declaration=True)
            status = ("success", f"✓  XML geschrieben → {pfad_xml}")
    return render_template("app.html", **ctx("f5", status=status))

# === API-Routen für Plotly-Charts (JSON-Daten) ====================================
@app.route("/api/kunden")                               # Kundenumsatz-Daten als JSON
@login_required
def api_kunden():
    _, rows = db_query(SQL_KUNDEN_UMSATZ)               # DB abfragen
    top  = rows[:5]; rest = rows[5:]                    # Top 5 + Sonstige
    namen  = [r[0] for r in top] + (["Sonstige"] if rest else [])
    werte  = [float(r[1]) for r in top] + ([float(sum(r[1] for r in rest))] if rest else [])
    return jsonify(namen=namen, werte=werte)             # JSON zurückgeben

@app.route("/api/monat")                                # Monatsumsatz-Daten als JSON
@login_required
def api_monat():
    _, rows = db_query(SQL_MONATSUMSATZ)
    return jsonify(monate=[r[0] for r in rows],
                   umsaetze=[float(r[1]) for r in rows])

@app.route("/api/artikel")                              # Top-Artikel-Daten als JSON
@login_required
def api_artikel():
    _, rows = db_query(SQL_TOP_ARTIKEL)
    return jsonify(artikel=[r[0] for r in rows],
                   umsaetze=[float(r[1]) for r in rows])

# === App starten ==================================================================
if __name__ == "__main__":
    print("▸ LF9-App läuft auf  http://localhost:5000")  # Startmeldung im Terminal
    app.run(debug=False, port=5000)                     # Webserver starten
