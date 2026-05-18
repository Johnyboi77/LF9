##### Hauptprogramm – Flask Web-App mit Login, RBAC und Features 1–5 #####
# 21_dropdown.py
# Autor: Johny | Datum: 2026-05-18
# Zweck: Browser-basierte App (http://localhost:5000) – Login, Rollen, alle Features
#
# === Bibliotheks-Dokumentation (Erweiterung – frei wählbare Bibliothek) ===
# Bibliothek:        flask
# Installation:      pip install flask
# Verwendungszweck:  Web-Framework – Routen, Sessions und HTML-Templates

from flask import (Flask, render_template, request,     # Flask-Kernfunktionen
                   session, redirect, url_for)           # Session, Weiterleitung
from functools import wraps                             # Für den Login-Decorator
import mariadb                                          # MariaDB-Datenbankzugriff
import csv                                              # CSV lesen/schreiben
import xml.etree.ElementTree as ET                      # XML schreiben
import pathlib                                          # Plattformübergreifende Pfade
from config import DB_LOCAL                             # Zentrale DB-Zugangsdaten

# === Flask-App initialisieren ====================================================
app = Flask(__name__)                                   # Flask-Instanz erstellen
app.secret_key = "lf9_heiner_2026_geheim"              # Schlüssel für Session-Verschlüsselung

# === RBAC-Mapping: Abteilung → erlaubte Feature-Schlüssel (lt. Aufgabe 2.2) ======
TOOLS = {
    "Lager":             ["f2", "f4"],                  # Lager: SQL + DB-Tabelle
    "Verwaltung":        ["f2", "f3", "f4"],            # Verwaltung: + CSV-Export
    "Marketing":         ["f2", "f4", "f5"],            # Marketing: + XML-Konvertierung
    "Geschäftsführung":  ["f2", "f3", "f4", "f5"],      # GF: alle Features
}

# === DB-Hilfsfunktion: SQL ausführen und Ergebnis zurückgeben ====================
def db_query(sql):                                      # sql = auszuführender SQL-String
    conn = mariadb.connect(**DB_LOCAL)                  # Verbindung aufbauen
    cur  = conn.cursor()                                # Cursor erstellen
    cur.execute(sql)                                    # SQL ausführen
    cols = [d[0] for d in cur.description] if cur.description else []  # Spaltennamen
    rows = cur.fetchall()                               # Alle Zeilen laden
    cur.close(); conn.close()                           # Cursor und Verbindung schließen
    return cols, rows                                   # Spaltennamen + Daten zurückgeben

# === Login-Decorator: schützt alle Routen außer /login ===========================
def login_required(f):                                  # f = zu schützende Funktion
    @wraps(f)                                           # Funktions-Metadaten beibehalten
    def decorated(*args, **kwargs):
        if "abteilung" not in session:                  # Nicht eingeloggt?
            return redirect(url_for("login"))           # → Weiterleitung zum Login
        return f(*args, **kwargs)                       # Eingeloggt → Funktion aufrufen
    return decorated

# === Hilfsfunktion: Standard-Kontext für alle Templates ==========================
def ctx(page, **extra):                                 # page = Seiten-ID (z.B. "f2")
    abt = session.get("abteilung", "")                 # Aktuelle Abteilung aus Session
    return dict(page=page, abteilung=abt,              # Seiten-ID + Abteilung
                erlaubt=TOOLS.get(abt, []),             # Erlaubte Feature-Schlüssel
                **extra)                                # Weitere optionale Template-Werte

# === Route: Login =================================================================
@app.route("/", methods=["GET", "POST"])                # GET = Formular zeigen, POST = prüfen
def login():
    fehler = None                                       # Standard: kein Fehler
    if request.method == "POST":                        # Formular abgesendet?
        abt = request.form.get("abteilung", "")        # Gewählte Abteilung aus Formular
        pw  = request.form.get("passwort", "")         # Eingegebenes Passwort
        if pw == abt and abt:                           # Passwort = Abteilungsname (lt. Aufgabe)
            session["abteilung"] = abt                  # Abteilung in Session speichern
            return redirect(url_for("dashboard"))       # Weiterleitung zum Dashboard
        fehler = "Bitte versuche es erneut"             # Falsches Passwort → Fehlermeldung
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
    return render_template("app.html", **ctx("dashboard"))  # Dashboard rendern

# === Route: Feature 1 – Verbindung testen =========================================
@app.route("/feature/1", methods=["GET", "POST"])       # POST = Test ausführen
@login_required
def feature1():
    status = None                                       # Standard: kein Ergebnis
    if request.method == "POST":                        # Button "Test starten" gedrückt?
        try:
            conn = mariadb.connect(**DB_LOCAL)          # Verbindungsversuch
            conn.ping()                                 # Ping an DB-Server senden
            conn.close()                                # Verbindung schließen
            status = ("success", "✓  Verbindung erfolgreich")   # Erfolg
        except mariadb.Error as e:
            status = ("error", f"✗  Fehlgeschlagen: {e}")       # Fehler mit Details
    return render_template("app.html", **ctx("f1", status=status, db=DB_LOCAL))

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
        pfad = pathlib.Path(__file__).parent / "artikel.csv"  # Zielpfad ermitteln
        cols, rows = db_query("SELECT * FROM artikel")  # Alle Artikel aus DB holen
        with open(pfad, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter=";")            # Semikolon-Trenner (Excel-DE)
            w.writerow(cols)                            # Kopfzeile schreiben
            w.writerows(rows)                           # Alle Datenzeilen schreiben
        status = ("success", f"✓  {len(rows)} Zeilen exportiert → {pfad}")
    return render_template("app.html", **ctx("f3", status=status))

# === Route: Feature 4 – DB-Tabelle anzeigen =======================================
@app.route("/feature/4")
@login_required
def feature4():
    cols, rows = db_query(                              # Ausgewählte Kundenspalten abfragen
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
            root_el = ET.Element("artikel_liste")       # XML-Wurzelelement erstellen
            with open(pfad_csv, newline="", encoding="utf-8") as f:
                for zeile in csv.DictReader(f, delimiter=";"):  # CSV Zeile für Zeile lesen
                    eintrag = ET.SubElement(root_el, "artikel")  # <artikel>-Element
                    for k, v in zeile.items():
                        ET.SubElement(eintrag, k).text = v       # Pro Spalte ein Subelement
            baum = ET.ElementTree(root_el)
            ET.indent(baum, space="  ")                 # XML lesbar einrücken (Python 3.9+)
            baum.write(str(pfad_xml), encoding="utf-8", xml_declaration=True)
            status = ("success", f"✓  XML geschrieben → {pfad_xml}")
    return render_template("app.html", **ctx("f5", status=status))

# === App starten ==================================================================
if __name__ == "__main__":
    print("▸ LF9-App läuft auf  http://localhost:5000")  # Startmeldung im Terminal
    app.run(debug=False, port=5000)                     # Webserver starten
