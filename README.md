# LF9 – Heiner IT-Systems GmbH

Schulprojekt: Daten aus einer MariaDB-Datenbank holen und in verschiedenen Formaten ausgeben –
vereint in einem Login-Programm mit Rollen (RBAC).

---

## Projektstruktur

```
LF9/
├── config.py                  ← Datenbankzugangsdaten (zentral, DRY-Prinzip)
├── 01_ConnectionTest.py       ← Feature 1: DB-Verbindung testen
├── 02_print_SQL_Ausgabe.py    ← Feature 2: Mitarbeiter in der Konsole ausgeben
├── 03_DBinCSV.py              ← Feature 3: Artikel-Tabelle als CSV exportieren
├── 04_DBausgabeFenster.py     ← Feature 4: Kunden-Tabelle als Tkinter-Fenster
├── 05_csv_to_xml.py           ← Feature 5: artikel.csv → artikel.xml
├── 21_dropdown.py             ← Hauptprogramm: Tkinter-Login mit Rollen + Tool-Auswahl
├── BrowserGUI/                ← Bonus: Browser-Darstellung (Flask)
│   ├── app.py                 ← Flask-Webserver mit Login, RBAC, Downloads, Charts
│   └── templates/
│       ├── login.html         ← Login-Seite
│       └── app.html           ← Haupt-App (Features + CEO-Diagramme)
├── Datenbank/
│   └── HeinerIT2025.sql       ← SQL-Dump zum Importieren
└── config.py                  ← DB-Zugangsdaten (wird von allen Dateien verwendet)
```

---

## Setup

### 1. Voraussetzungen installieren

```bash
# tkinter (für 04_DBausgabeFenster.py und 21_dropdown.py)
sudo pacman -S tk

# MariaDB Python-Treiber
pip install mariadb

# Flask (nur für den Browser-Bonus)
pip install flask
```

### 2. MariaDB starten und Datenbank importieren

```bash
# MariaDB-Dienst starten
sudo systemctl start mariadb

# Datenbank importieren (einmalig)
sudo mariadb -u root -p heiner < Datenbank/HeinerIT2025.sql
```

### 3. Zugangsdaten anpassen

In [config.py](config.py) das `password` unter `DB_LOCAL` auf das eigene MariaDB-Root-Passwort setzen:

```python
DB_LOCAL = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "root123",   # ← hier anpassen
    "database": "heiner"
}
```

---

## Starten

### Einzelne Pflicht-Dateien (direkt ausführbar)

```bash
python 01_ConnectionTest.py       # → "successful" wenn DB erreichbar
python 02_print_SQL_Ausgabe.py    # → Mitarbeiterliste in der Konsole
python 03_DBinCSV.py              # → erstellt artikel.csv im Projektordner
python 04_DBausgabeFenster.py     # → Tkinter-Fenster mit Kunden-Tabelle
python 05_csv_to_xml.py           # → liest artikel.csv, erstellt artikel.xml
```

> `05_csv_to_xml.py` setzt voraus, dass `03_DBinCSV.py` vorher gelaufen ist.

---

### Option 1 – Tkinter-Hauptprogramm (Pflicht, lt. Lehrer)

```bash
python3 main.py
```

- Zwei getrennte Screens: **Login-Screen** → nach Anmelden → **Task-Screen**
- Login-Screen: zentrierte weiße Karte auf blauem Hintergrund (wie Browser-Login)
- Task-Screen: Sidebar mit Feature-Übersicht (✓ freigeschaltet / ✗ gesperrt), Tool-Auswahl und Ausgabe-Bereich
- SQL-Ausgabe wird tabellarisch formatiert (nicht als rohe Tupel)
- Roter „Abmelden"-Button führt zurück zum Login-Screen
- ESC: Vollbild verlassen
- `python 21_dropdown.py` startet dasselbe (Scaffold-Datei des Lehrers)

### Option 2 – Browser-GUI (Bonus)

```bash
python3 BrowserGUI/app.py
```

Dann im Browser öffnen: **http://localhost:5000**

- Gleicher Login (Abteilung + Passwort = Abteilungsname)
- CSV und XML werden direkt im Browser heruntergeladen (keine Dateien im Repo)
- Geschäftsführung sieht zusätzlich 3 interaktive Umsatz-Diagramme im Dashboard
- Zeigt wie dieselbe Aufgabe mit einem Web-Framework (Flask) gelöst werden kann

---

## Login-Zugangsdaten (Test)

| Abteilung | Passwort |
|---|---|
| Lager | `Lager` |
| Verwaltung | `Verwaltung` |
| Marketing | `Marketing` |
| Geschäftsführung | `Geschäftsführung` |

Das Passwort ist immer gleich dem Abteilungsnamen (lt. Aufgabenstellung).

> **Hinweis:** Dies ist kein echtes Authentifizierungssystem – Passwörter sind Klartext und entsprechen dem Abteilungsnamen. Das ist ein Lernbeispiel für RBAC (Role-Based Access Control), wie in der Aufgabenstellung vorgegeben.

---

## Rollen & Zugriffsrechte (RBAC)

| Abteilung | F2: SQL-Ausgabe | F3: CSV | F4: DB-Tabelle | F5: XML | Charts |
|---|:---:|:---:|:---:|:---:|:---:|
| Lager | ✓ | – | ✓ | – | – |
| Verwaltung | ✓ | ✓ | ✓ | – | – |
| Marketing | ✓ | – | ✓ | ✓ | – |
| Geschäftsführung | ✓ | ✓ | ✓ | ✓ | ✓ |

---

## Verwendete Bibliotheken

### Pflichtteil (nur erlaubte Bibliotheken)

| Datei | Bibliothek | Zweck |
|---|---|---|
| `01` – `04` | `mariadb` | Verbindung zur MariaDB-Datenbank |
| `03` | `csv` | Tabellendaten als CSV-Datei schreiben |
| `04`, `21_dropdown` | `tkinter` / `ttk` | GUI-Fenster und Widgets |
| `05` | `csv`, `xml.etree.ElementTree` | CSV lesen, XML-Datei erzeugen |

### Bonus (zusätzlich dokumentiert, frei wählbar)

| Datei | Bibliothek | Installation | Zweck |
|---|---|---|---|
| `BrowserGUI/app.py` | `flask` | `pip install flask` | Web-Framework: Routen, Sessions, Templates, Downloads |
| `BrowserGUI/templates/app.html` | `Plotly.js` | CDN (keine Installation) | Interaktive Diagramme im Browser |

---

## Zwei Varianten im Vergleich

| | Tkinter (`21_dropdown.py`) | Browser (`BrowserGUI/app.py`) |
|---|---|---|
| Start | `python 21_dropdown.py` | `python BrowserGUI/app.py` |
| Oberfläche | Desktop-Fenster (Vollbild) | Webbrowser |
| CSV-Export | Datei wird im Projektordner gespeichert | Download direkt im Browser |
| XML-Export | Setzt CSV-Datei voraus | Direkt aus DB, kein Zwischenschritt |
| CEO-Diagramme | – | 3 interaktive Charts (Plotly.js) |
| Komplexität | kurz, übersichtlich | vollständig, erweiterbar |

Der Tkinter-Ansatz folgt dem Codegerüst des Lehrers und bleibt bewusst kurz und gut erklärbar.
Der Browser-Bonus zeigt, wie die gleiche Aufgabe mit einem Web-Framework moderner gelöst werden kann.

---

## Begründung der Implementierungsentscheidungen

### 01 – ConnectionTest

| Frage | Antwort |
|---|---|
| Warum `try/except` statt direktem `mariadb.connect()`? | Ohne Fehlerbehandlung würde das Skript bei falschem Passwort oder ausgeschaltetem Server mit einem Traceback abstürzen. So wird der Fehler lesbar ausgegeben. |
| Warum `**DB_LOCAL`? | `**` entpackt das Dictionary zu einzelnen Keyword-Argumenten (`host=...`, `port=...`). Trennt Konfiguration (config.py) sauber vom Code. |
| Warum `dbc.ping()` zum Testen? | `ping()` sendet ein echtes Signal an den DB-Server und prüft, ob die Verbindung **jetzt** noch lebt – nicht nur ob das Verbindungsobjekt existiert. |
| Warum prüfen ob `dbc is None`? | Wenn der Verbindungsaufbau fehlschlug, ist `db = None`. Ohne Prüfung würde `None.ping()` einen `AttributeError` werfen. |
| Warum `mariadb` statt `mysql.connector`? | Laut PDF „01_Informationen" ist `mariadb` die einzig erlaubte DB-Bibliothek. Ist speziell für MariaDB-Server optimiert. |

---

### 02 – print_SQL_Ausgabe

| Frage | Antwort |
|---|---|
| Warum `fetchall()` statt `fetchone()` in einer Schleife? | `fetchall()` holt alle Ergebnisse auf einmal. Bei 20 Zeilen problemlos. Bei Millionen Zeilen wäre `fetchone()` speicherschonender. |
| Warum `cur.close()` im `finally`-Block? | Der Cursor wird auch bei einem Fehler geschlossen. Offene Cursor belegen DB-Ressourcen und können den Server belasten. |
| Warum `db` und `sql_Anweisung` außerhalb der Funktion? | So vorgegeben durch das Codegerüst der Lehrkraft. Eigentlich wäre Kapselung in der Funktion sauberer. |

---

### 03 – DBinCSV

| Frage | Antwort |
|---|---|
| Warum `;` als CSV-Trenner statt `,`? | Deutsche Excel/LibreOffice-Locale reserviert `,` als Dezimaltrennzeichen. Mit `,` würden Beträge wie „46,00" die Spaltenstruktur zerstören. |
| Warum `encoding="utf-8"` explizit angeben? | Ohne Angabe nutzt Python das OS-Default (Linux: UTF-8, Windows: cp1252). Unter Windows würden Umlaute als Mojibake erscheinen. |
| Warum `newline=""` beim Öffnen? | Verhindert dass Python und das CSV-Modul beide ein Zeilenende einfügen → sonst leere Zeilen zwischen Datensätzen (vor allem unter Windows). |
| Warum `cursor.description` für die Kopfzeile? | Dynamisch: funktioniert für jede Tabelle, ohne Spaltennamen hardzucoden. Ändert sich das Schema, passt sich der Export automatisch an. |
| Warum `mariadb` statt `mysql.connector` (wie im Codegerüst)? | Das Codegerüst enthält hier einen Widerspruch zur Aufgabenstellung. Korrektur ist im Datei-Header dokumentiert. |

---

### 04 – DBausgabeFenster

| Frage | Antwort |
|---|---|
| Warum `ttk.Treeview` statt `tk.Listbox`? | Listbox kann nur eine Spalte. Treeview unterstützt mehrere Spalten mit Headern – sieht aus wie eine Excel-Tabelle. |
| Warum `show="headings"`? | Tkinter zeigt standardmäßig eine zusätzliche Baumstruktur-Spalte „#0". `"headings"` blendet diese aus für eine reine Tabellenansicht. |
| Warum Verbindung in `read_from_database()` öffnen UND schließen? | Separation of Concerns: Die GUI-Funktion kümmert sich nicht um den DB-Lifecycle. Hält keine Verbindung unnötig offen. |
| Warum `mainloop()` ganz am Ende? | Startet die Event-Loop, die auf Klicks/Scrolls reagiert. Ohne sie öffnet sich das Fenster und schließt sich sofort wieder. |
| Warum dynamische Spalten aus `cursor.description`? | Tabellenname ist in einer Variable – Spalten passen sich automatisch an, ohne den GUI-Code anzufassen. |

---

### 05 – csv_to_xml

| Frage | Antwort |
|---|---|
| Warum `DictReader` statt `csv.reader`? | `DictReader` nutzt die erste Zeile (Header) automatisch als Spaltennamen. CSV-Zeile wird zu Dictionary `{spalte: wert}` – keine Spaltennamen hardzucodieren. |
| Warum `ET.indent()`? | Ohne wäre das XML eine einzige lange Zeile – technisch korrekt, aber für Menschen unlesbar. Verfügbar ab Python 3.9. |
| Warum `xml_declaration=True`? | Schreibt `<?xml version="1.0" encoding="utf-8"?>` ans Anfang. Best Practice – manche Parser verweigern XML ohne Deklaration. |
| Warum `ET.SubElement` statt `ET.Element`? | `SubElement` erstellt das Element und hängt es direkt an das Parent. Spart eine separate `parent.append()`-Zeile. |

---

### BrowserGUI – Flask Bonus

| Frage | Antwort |
|---|---|
| Warum Flask statt ein weiteres Tkinter-Programm? | Flask als Webframework zeigt einen anderen Architekturansatz: Routen statt Callbacks, Jinja2-Templates statt Widget-Code, HTTP statt Event-Loop. Guter Vergleich zum Pflichtteil. |
| Warum `io.BytesIO` / `io.StringIO` für CSV/XML? | In-Memory-Buffer: Es wird keine Datei auf dem Server gespeichert. Der Inhalt wird direkt als HTTP-Response gestreamt. Sauberer für Web-Anwendungen. |
| Warum `send_file()` mit `as_attachment=True`? | Erzwingt einen Browser-Download-Dialog statt die Datei im Browser anzuzeigen. `download_name` setzt den vorgeschlagenen Dateinamen. |
| Warum XML in BrowserGUI direkt aus DB (ohne CSV)? | Im Tkinter-Ansatz muss zuerst `03_DBinCSV.py` laufen. Im Browser entfällt diese Abhängigkeit – XML wird direkt aus der DB-Abfrage gebaut. Unabhängiger und robuster. |
| Warum Plotly.js via CDN (keine Installation)? | Kein `pip install` nötig, Browser lädt Plotly automatisch. Einzig erlaubt sind im Bonus frei wählbare Bibliotheken – Plotly.js ist rein frontend-seitig und braucht keine Python-Abhängigkeit. |
| Warum `sys.path.insert(0, ...)` in app.py? | `BrowserGUI/app.py` liegt in einem Unterordner. Ohne diesen Trick findet Python `config.py` im Root nicht. Ermöglicht `from config import DB_LOCAL`. |

---

### Cross-cutting Konzepte

| Konzept | Wo angewendet | Warum |
|---|---|---|
| **DRY** (Don't Repeat Yourself) | `config.py` für alle DB-Zugangsdaten | Passwort an einer Stelle ändern, wirkt überall. |
| **Separation of Concerns** | DB-Logik, GUI und Berechtigungen getrennt | Jede Funktion macht eine Sache – leichter zu erklären und zu warten. |
| **Defensive Programmierung** | `if dbc is None`, `try/finally` | Externe Ressourcen (DB, Dateien) immer absichern – nie annehmen, dass alles funktioniert. |
| **RBAC** (Role-Based Access Control) | `TOOLS`-Dict in `21_dropdown.py` und `BrowserGUI/app.py` | Industriestandard für Berechtigungen. Statt If-Else-Chaos eine zentrale Mapping-Tabelle. |
| **UTF-8 durchgängig** | DB-Verbindung, CSV-Export, XML-Ausgabe | Verhindert Umlaut-Probleme (`ü → ü`) über Systemgrenzen hinweg. |
