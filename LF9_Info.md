# LF9 – Heiner IT-Systems GmbH: Projekt-Übersicht & To-Do

> **Ziel in einem Satz:** Daten aus einer MariaDB-Datenbank holen und in 4 Formaten ausgeben (Konsole, CSV, GUI-Fenster, XML) – am Ende alles in einem Login-Programm mit Rollen vereinen.

---

## 1. Worum geht's? (Erklärung für Non-Techies)

Die fiktive Firma "Heiner IT-Systems" zieht ihre Datenbank um. Verschiedene Abteilungen (Lager, Verwaltung, Marketing, Geschäftsführung) brauchen die Daten in unterschiedlichen Formaten – manche wollen Excel-Tabellen (CSV), manche XML-Dateien, manche nur ein Fenster mit Übersicht.

Du baust **5 kleine Python-Programme**, die je eine Aufgabe lösen, plus **1 Hauptprogramm**, das alle vereint und je nach Login die richtigen Tools freischaltet.

---

## 2. Spielregeln (WICHTIG – Punkteverlust vermeiden!)

### ✅ Erlaubt im Pflichtteil (nur diese Bibliotheken!)

| Datei | Bibliothek | Status bei dir |
|---|---|---|
| `01_ConnectionTest` | `mariadb` | ✅ installiert (1.1.14) |
| `02_print_SQL_Ausgabe` | `mariadb` | ✅ |
| `03_DBinCSV` | `csv` | ✅ Python-Standard |
| `04_DBausgabeFenster` | `tkinter` | ⚠️ **fehlt** – `sudo pacman -S tk` |

**DB-GUI-Tool:** DBeaver (statt HeidiSQL) – `sudo pacman -S dbeaver`
| `05_csv_to_xml` | `csv` + `xml.etree.ElementTree` | ✅ Python-Standard |

### ❌ Nicht erlaubt im Pflichtteil
- **pandas** – kein `pd.read_sql()` oder `df.to_csv()`! Auch wenn's nur eine Zeile wäre.
- **sqlalchemy**, **lxml**, **openpyxl** etc.
- **PySide6** (das hast du installiert – wäre eigentlich Ersatz für tkinter, aber im Pflichtteil ist tkinter vorgeschrieben)

### ✅ Erlaubt in der Erweiterung (1.6 und 2.3 "Überraschung")
Hier darfst du jede Bibliothek nehmen – **aber im Code dokumentieren**:
```python
# Bibliothek: pandas
# Installation: pip3 install pandas
# Verwendungszweck: schnelle CSV-Generierung aus DataFrame
import pandas as pd
```

### Weitere Pflichten
- Vorgegebene **Dateinamen und Codegerüst** verwenden (`01_ConnectionTest`, `21_dropdown` etc.)
- **Jede Codezeile** bekommt einen `#`-Kommentar mit kurzer Erklärung
- Dokumentation als PDF + kommentierter Quellcode abgeben

---

## 3. Setup-Status auf deinem Omarchy-Notebook

### Schon erledigt ✅
- VS Code
- Python + `mariadb` Library + PySide6

### Noch offen – mach das zuerst:

```bash
# 1. DBeaver installieren (offizielles Repo, zieht Java automatisch mit)
sudo pacman -S dbeaver

# 2. tkinter installieren (für Aufgabe 1.4)
sudo pacman -S tk

# Test ob tkinter geht:
python -m tkinter   # Es sollte ein kleines Fenster aufpoppen

# 3. Lokale MariaDB installieren (erst lokal arbeiten, dann auf Server!)
sudo pacman -S mariadb
sudo mariadb-install-db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
sudo systemctl enable --now mariadb
sudo mysql_secure_installation   # Root-Passwort setzen (merken!)

# 4. DB lokal anlegen und SQL-Datei importieren
sudo mariadb -u root -p
> CREATE DATABASE heiner;
> quit
sudo mariadb -u root -p heiner < /pfad/zu/deiner.sql

# 5. In DBeaver Verbindung anlegen:
#    "New Database Connection" → MariaDB auswählen
#    Beim ersten Mal: Driver-Download bestätigen
#    Host: 127.0.0.1, Port: 3306, Database: heiner, User: root, Password: <dein lokales>
#    "Test Connection" → muss grün werden, dann "Finish"
```

> **Reihenfolge:** Erst lokal alles zum Laufen bringen, dann auf den Schul-Server umziehen. Das WLAN ist laut PDF unzuverlässig.

---

## 4. To-Do-Liste (Senior-Dev-Stil, alles in kurzen Files)

> **Regel:** Jede Datei bleibt **unter 40 Zeilen**. Wenn länger – falsch gedacht.

### 🔧 Vorbereitung: Eine zentrale `config.py`

Damit du Zugangsdaten **nur einmal** schreibst (DRY-Prinzip):

```python
# config.py – zentrale DB-Konfiguration
DB_LOCAL = {                                  # Dictionary für lokale Verbindung
    "host": "127.0.0.1",                      # localhost
    "user": "root",                           # DB-User
    "password": "deinpasswort",               # Passwort hier eintragen
    "database": "heiner",                     # Name der Datenbank
    "port": 3306                              # Standard-MariaDB-Port
}
# DB_SERVER später für den Schul-Server (gleiche Struktur, andere IP)
```

Dann in jeder Datei nur: `from config import DB_LOCAL`

---

### ✅ 1.0 Quellcode-Dokumentation (parallel zu allem, 2h)
- Jede Codezeile bekommt einen `#`-Kommentar
- Datei-Header pro Datei: Autor, Datum, Zweck, genutzte Bibliotheken

### ✅ 1.1 `01_ConnectionTest.py` (2h) – ca. 10 Zeilen
**Was:** Nur prüfen, ob die Verbindung steht.
**Kern:** `mariadb.connect(**DB_LOCAL)` in `try/except`, bei Erfolg `print("Verbindung OK")`, am Ende `conn.close()`.

### ✅ 1.2 `02_print_SQL_Ausgabe.py` (1h) – ca. 15 Zeilen
**Was:** Alle Mitarbeiter aus `personal` auf Konsole ausgeben.
**Kern:** `cur.execute("SELECT * FROM personal")` → `for row in cur.fetchall(): print(row)`.

### ✅ 1.3 `03_DBinCSV.py` (2h) – ca. 20 Zeilen
**Was:** Tabelle `artikel` (Lagerbestand) in `artikel.csv` schreiben.
**Kern:**
```python
import csv                                    # CSV-Modul aus Standardlib
# ... Verbindung wie oben ...
cur.execute("SELECT * FROM artikel")          # Alle Artikel holen
headers = [d[0] for d in cur.description]     # Spaltennamen aus Cursor
with open("artikel.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")          # ; für Excel-DE
    w.writerow(headers)                       # Kopfzeile schreiben
    w.writerows(cur.fetchall())               # Datenzeilen schreiben
```

### ✅ 1.4 `04_DBausgabeFenster.py` (2h) – ca. 30 Zeilen
**Was:** Tabelle (z.B. `kunde`) in einem Fenster anzeigen.
**Kern:** `tkinter.ttk.Treeview` mit Spalten aus `cur.description`, eine `tree.insert()` Zeile pro Datensatz, `root.mainloop()`.

### ✅ 1.5 `05_csv_to_xml.py` (1h) – ca. 20 Zeilen
**Was:** Die `artikel.csv` aus 1.3 in `artikel.xml` umwandeln.
**Kern:**
```python
import csv                                    # CSV einlesen
import xml.etree.ElementTree as ET            # XML schreiben
root = ET.Element("artikel_liste")            # Wurzelelement
with open("artikel.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f, delimiter=";"):
        a = ET.SubElement(root, "artikel")    # <artikel>-Knoten
        for k, v in row.items():              # Pro Spalte ein Unterelement
            ET.SubElement(a, k).text = v
ET.ElementTree(root).write("artikel.xml", encoding="utf-8", xml_declaration=True)
```

### 🎁 1.6 Erweiterung (frei, Bonus-Punkte)
**Ideen, alle in 1 kleiner Datei machbar:**
- **XML im Browser ansehen:** Mini-HTTP-Server (`python -m http.server`) + XSL-Stylesheet für hübsche Darstellung
- **JSON-Export** zusätzlich (`json`-Modul, Standard)
- **Statistik-Dashboard** mit pandas + matplotlib (vergiss die Bibliotheks-Doku im Code nicht!)
- **Auto-Backup** der CSVs in ein Archiv (`shutil`, `zipfile`)

### ✅ 1.7 Projekt-Dokumentation (1h)
Eine Tabelle in der PDF/Word-Doku:

| Meilenstein | Geplante Zeit | Reale Zeit | Probleme / Lösungen |
|---|---|---|---|
| 1.1 ConnectionTest | 2h | | |
| ... | | | |

---

### 🚀 Hauptprogramm (Aufgabe 2)

Vorgegebenes Codegerüst: **`21_dropdown.py`** – das musst du erweitern.

#### 2.1 `create_dropdown_login` (2h)
- Dropdown mit den 4 Abteilungen: `["Lager", "Verwaltung", "Marketing", "Geschäftsführung"]`
- Passwort-Eingabefeld (Bestätigung mit Enter)
- Passwort = Abteilungsname (Klartext, ist so vorgegeben)

#### 2.2 `verfügbare_tools(mitarbeiter)` + `create_dropdown_tools(parent)` (2h)
Mapping im **Code** (nicht in DB!):

```python
TOOLS = {                                                     # Berechtigungs-Mapping
    "Lager":          ["print_SQL_Ausgabe", "DBausgabeFenster"],
    "Verwaltung":     ["print_SQL_Ausgabe", "DBinCSV", "DBausgabeFenster"],
    "Marketing":      ["print_SQL_Ausgabe", "DBausgabeFenster", "CSV_to_XML"],
    "Geschäftsführung": ["print_SQL_Ausgabe", "DBinCSV", "DBausgabeFenster", "CSV_to_XML"]
}
```

Zweites Dropdown zeigt nur die erlaubten Tools, Button "Ausführen" startet das gewählte Tool (per `subprocess.run(["python", "03_DBinCSV.py"])` oder per Import + Funktionsaufruf).

#### 2.3 Eigene Funktionalität "Überraschung" (2h, eigene Datei!)
**Ideen mit Wow-Effekt:**
- **Lagerbestand-Warnung:** Liste aller Artikel mit `Lagerbestand < Mindestbestand` → farbig im GUI
- **Bestellung erfassen:** Formular, das neuen Datensatz in `bestellung` schreibt
- **Umsatz-Chart:** Top 10 Kunden nach Bestellwert (matplotlib + Bibliotheks-Doku!)
- **Suchfunktion:** Volltext-Suche über alle Tabellen

---

## 5. Architektur-Tipps (Senior-Dev)

1. **Zentrale `config.py`** – DB-Daten nie hardcoden
2. **`db_utils.py`** mit einer Funktion `get_connection()` – spart Code in jeder Datei
3. **Spaltennamen dynamisch** aus `cursor.description` holen – nie als String-Liste hardcoden
4. **Encoding immer UTF-8** explizit angeben (Umlaute!)
5. **`try/except mariadb.Error`** mit klarer Fehlermeldung – nicht still failen
6. **Cursor und Connection schließen** (`finally`-Block oder `with`-Konstrukt mit Context Manager)
7. **Eine Datei = eine Aufgabe.** Wenn `04_DBausgabeFenster.py` > 40 Zeilen wird → GUI-Code in Funktionen aufteilen

---

## 6. Abgabe-Checkliste

- [ ] DBeaver läuft und ist mit lokaler DB verbunden
- [ ] tkinter funktioniert (`python -m tkinter`)
- [ ] Lokale MariaDB läuft, DB `heiner` importiert
- [ ] `config.py` mit lokalen Zugangsdaten erstellt
- [ ] `01_ConnectionTest.py` – Verbindung OK
- [ ] `02_print_SQL_Ausgabe.py` – Mitarbeiter erscheinen
- [ ] `03_DBinCSV.py` – CSV öffnet sich in Excel/LibreOffice
- [ ] `04_DBausgabeFenster.py` – Fenster zeigt Tabelle
- [ ] `05_csv_to_xml.py` – XML ist wohlgeformt
- [ ] `1.6` Erweiterung implementiert + dokumentiert
- [ ] `21_dropdown.py` – Login + Tool-Auswahl funktioniert
- [ ] `2.3` Eigene Funktionalität fertig + dokumentiert
- [ ] **Jede** Codezeile mit `#` kommentiert
- [ ] PDF-Dokumentation mit Zeit-Tabelle und Problemen
- [ ] Auf Schul-Server getestet (nicht nur lokal!)

---

## 7. Bewertung – wo holst du dir die 110%?

| Block | Max | Strategie |
|---|---|---|
| Pflichtteil (5 Files + Doku) | 27 P | Sauber, kurz, kommentiert |
| Hauptprogramm | 13 P | Codegerüst nicht verbiegen |
| **Überraschung 2.3** | **10 P** | **Hier kannst du glänzen – etwas Sichtbares!** |
| Testat (Vorführung + 7 Fragen) | 60 P | Jeder im Team muss jede Datei erklären können |

> **Pro-Tipp fürs Testat:** Sei sicher mit den Bibliotheks-Namen, dem Unterschied `fetchall()` vs. `fetchone()`, was `cursor.description` zurückgibt, und warum CSV `;` statt `,` benutzt (Excel-DE-Eigenheit). Das sind klassische "individuelle Fragen".
