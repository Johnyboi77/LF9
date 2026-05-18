##### Bonus – Browser-GUI: Flask Web-App mit Login, RBAC, Downloads und CEO-Charts #####
# BrowserGUI/app.py
# Autor: Johny | Datum: 2026-05-18
# Zweck: Browser-Darstellung des Hauptprogramms als Vergleich zum tkinter-Ansatz.
#        CSV/XML werden direkt im Browser als Download bereitgestellt (keine lokalen Dateien).
#        Geschäftsführung sieht zusätzlich 3 interaktive Umsatz-Diagramme (Plotly.js).
#
# Start: python BrowserGUI/app.py  →  http://localhost:5000
#
# === Bibliotheks-Dokumentation (Erweiterung – frei wählbare Bibliotheken) ===
# Bibliothek:        flask
# Installation:      pip install flask
# Verwendungszweck:  Web-Framework – Routen, Sessions, HTML-Templates, Datei-Downloads
#
# Bibliothek:        plotly.js (CDN, keine Installation)
# Verwendungszweck:  Interaktive Charts im Browser (Donut, Balken) für den Geschäftsführer

import sys, pathlib                                         # sys.path für Root-Import
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))  # Ermöglicht: from config import ...

from flask import (Flask, render_template, request,         # Flask-Kernfunktionen
                   session, redirect, url_for,              # Session + Weiterleitungen
                   jsonify, send_file)                      # JSON-API + Datei-Downloads
from functools import wraps                                 # Für den Login-Decorator
import mariadb                                              # MariaDB-Datenbankzugriff
import csv                                                  # CSV in-memory schreiben
import io                                                   # In-Memory-Streams (kein Dateisystem)
import xml.etree.ElementTree as ET                          # XML aufbauen
from config import DB_LOCAL                                 # Zentrale Zugangsdaten aus Root

app = Flask(__name__)                                       # Flask-App erstellen
app.secret_key = "lf9_heiner_2026_browsergui"              # Schlüssel für Session-Verschlüsselung

# === RBAC-Mapping: Abteilung → erlaubte Features =====================================
TOOLS = {
    "Lager":             ["f2", "f4"],                      # SQL + DB-Tabelle
    "Verwaltung":        ["f2", "f3", "f4"],                # + CSV-Download
    "Marketing":         ["f2", "f4", "f5"],                # + XML-Download
    "Geschäftsführung":  ["f2", "f3", "f4", "f5"],          # alle Features + Charts
}

# === SQL für CEO-Diagramme ===========================================================
SQL_KUNDEN = """
    SELECT k.Firma, SUM(bd.Anzahl * bd.Einzelpreis * (1 - bd.Rabatt)) AS Umsatz
    FROM kunde k
    JOIN bestellung b      ON k.KundenCode = b.KundenCode
    JOIN bestelldetails bd ON b.BestellNr  = bd.BestellNr
    GROUP BY k.KundenCode, k.Firma ORDER BY Umsatz DESC
"""                                                         # Alle Kunden mit Gesamtumsatz

SQL_MONAT = """
    SELECT DATE_FORMAT(b.Bestelldatum, '%Y-%m') AS Monat,
           SUM(bd.Anzahl * bd.Einzelpreis * (1 - bd.Rabatt)) AS Umsatz
    FROM bestellung b
    JOIN bestelldetails bd ON b.BestellNr = bd.BestellNr
    WHERE YEAR(b.Bestelldatum) = 2025
    GROUP BY Monat ORDER BY Monat
"""                                                         # Umsatz pro Monat (nur 2025)

SQL_ARTIKEL = """
    SELECT a.Artikelname, SUM(bd.Anzahl * bd.Einzelpreis * (1 - bd.Rabatt)) AS Umsatz
    FROM artikel a
    JOIN bestelldetails bd ON a.ArtikelNr = bd.ArtikelNr
    GROUP BY a.ArtikelNr, a.Artikelname ORDER BY Umsatz DESC LIMIT 10
"""                                                         # Top 10 Artikel nach Umsatz

# === Hilfsfunktionen =================================================================
def db_query(sql):                                          # SQL ausführen, Ergebnis zurückgeben
    conn = mariadb.connect(**DB_LOCAL)                      # Verbindung aufbauen
    cur  = conn.cursor()                                    # Cursor erstellen
    cur.execute(sql)                                        # SQL ausführen
    cols = [d[0] for d in cur.description] if cur.description else []  # Spaltennamen
    rows = cur.fetchall()                                   # Alle Zeilen laden
    cur.close(); conn.close()                               # Aufräumen
    return cols, rows                                       # Spaltennamen + Daten

def login_required(f):                                      # Decorator: Routen absichern
    @wraps(f)                                               # Funktions-Metadaten beibehalten
    def decorated(*args, **kwargs):
        if "abteilung" not in session:                      # Nicht eingeloggt?
            return redirect(url_for("login"))               # → zum Login umleiten
        return f(*args, **kwargs)                           # Eingeloggt → weiter
    return decorated

def ctx(page, **extra):                                     # Template-Kontext zusammenbauen
    abt = session.get("abteilung", "")                     # Abteilung aus Session
    return dict(page=page, abteilung=abt,                  # Seiten-ID + Abteilung
                erlaubt=TOOLS.get(abt, []), **extra)        # Erlaubte Features + Extras

# === Login / Logout ==================================================================
@app.route("/", methods=["GET", "POST"])                    # GET = Formular, POST = Login prüfen
def login():
    fehler = None
    if request.method == "POST":
        abt = request.form.get("abteilung", "")            # Abteilung aus Formular
        pw  = request.form.get("passwort", "")             # Passwort aus Formular
        if pw == abt and abt:                               # Passwort = Abteilungsname
            session["abteilung"] = abt                      # In Session speichern
            return redirect(url_for("dashboard"))           # → Dashboard
        fehler = "Bitte versuche es erneut"
    return render_template("login.html", fehler=fehler)

@app.route("/logout")
def logout():
    session.clear()                                         # Session löschen
    return redirect(url_for("login"))                       # → Login

# === Dashboard =======================================================================
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("app.html", **ctx("dashboard"))

# === Feature 1: Verbindung testen ====================================================
@app.route("/feature/1", methods=["GET", "POST"])
@login_required
def feature1():
    status = None
    if request.method == "POST":
        try:
            conn = mariadb.connect(**DB_LOCAL)              # Verbindung aufbauen
            conn.ping()                                     # Ping senden
            conn.close()
            status = ("success", "✓  Verbindung erfolgreich")
        except mariadb.Error as e:
            status = ("error", f"✗  Fehlgeschlagen: {e}")
    return render_template("app.html", **ctx("f1", status=status, db=DB_LOCAL))

# === Feature 2: SQL ausgeben =========================================================
@app.route("/feature/2")
@login_required
def feature2():
    cols, rows = db_query("SELECT * FROM personal")         # Alle Mitarbeiter abfragen
    return render_template("app.html", **ctx("f2", cols=cols, rows=rows))

# === Feature 3: CSV-Download =========================================================
@app.route("/feature/3", methods=["GET", "POST"])
@login_required
def feature3():
    if request.method == "POST":                            # Download-Button gedrückt
        cols, rows = db_query("SELECT * FROM artikel")     # Artikeldaten aus DB
        buf = io.StringIO()                                 # In-Memory-Puffer (kein Dateisystem)
        w = csv.writer(buf, delimiter=";")                  # Semikolon-Trenner (Excel-DE)
        w.writerow(cols)                                    # Kopfzeile
        w.writerows(rows)                                   # Alle Datenzeilen
        buf.seek(0)                                         # Zurück an Anfang des Puffers
        return send_file(                                   # Als Datei-Download senden
            io.BytesIO(buf.getvalue().encode("utf-8")),     # In Bytes konvertieren
            mimetype="text/csv",
            as_attachment=True,
            download_name="artikel.csv")                    # Dateiname im Browser
    return render_template("app.html", **ctx("f3"))

# === Feature 4: DB-Tabelle anzeigen ==================================================
@app.route("/feature/4")
@login_required
def feature4():
    cols, rows = db_query(
        "SELECT KundenCode, Firma, Kontaktperson, Ort, Land FROM kunde")
    return render_template("app.html", **ctx("f4", cols=cols, rows=rows))

# === Feature 5: XML-Download (direkt aus DB, kein CSV nötig) =========================
@app.route("/feature/5", methods=["GET", "POST"])
@login_required
def feature5():
    if request.method == "POST":                            # Download-Button gedrückt
        cols, rows = db_query("SELECT * FROM artikel")     # Direkt aus DB (kein CSV nötig)
        root_el = ET.Element("artikel_liste")               # XML-Wurzelelement
        for zeile in rows:                                  # Jede Zeile = ein <artikel>
            eintrag = ET.SubElement(root_el, "artikel")
            for k, v in zip(cols, zeile):                   # Pro Spalte ein Subelement
                ET.SubElement(eintrag, k).text = str(v) if v is not None else ""
        baum = ET.ElementTree(root_el)
        ET.indent(baum, space="  ")                         # Lesbar einrücken
        buf = io.BytesIO()                                  # In-Memory-Puffer
        baum.write(buf, encoding="utf-8", xml_declaration=True)
        buf.seek(0)
        return send_file(buf, mimetype="application/xml",
                         as_attachment=True, download_name="artikel.xml")
    return render_template("app.html", **ctx("f5"))

# === CEO-Chart-APIs (Plotly.js holt diese Daten per fetch()) =========================
@app.route("/api/kunden")
@login_required
def api_kunden():
    _, rows = db_query(SQL_KUNDEN)
    top = rows[:5]; rest = rows[5:]                         # Top 5 + Sonstige zusammenfassen
    namen = [r[0] for r in top] + (["Sonstige"] if rest else [])
    werte = [float(r[1]) for r in top] + ([float(sum(r[1] for r in rest))] if rest else [])
    return jsonify(namen=namen, werte=werte)                # JSON für Plotly

@app.route("/api/monat")
@login_required
def api_monat():
    _, rows = db_query(SQL_MONAT)
    return jsonify(monate=[r[0] for r in rows],
                   umsaetze=[float(r[1]) for r in rows])

@app.route("/api/artikel")
@login_required
def api_artikel():
    _, rows = db_query(SQL_ARTIKEL)
    return jsonify(artikel=[r[0] for r in rows],
                   umsaetze=[float(r[1]) for r in rows])

# === Start ===========================================================================
if __name__ == "__main__":
    print("▸ BrowserGUI läuft auf  http://localhost:5000")
    app.run(debug=False, port=5000)                         # Webserver starten
