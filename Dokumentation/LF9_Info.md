# LF9 – Heiner IT-Systems GmbH: Projekt-Übersicht

> **Ziel in einem Satz:** Daten aus einer MariaDB-Datenbank holen und in 4 Formaten ausgeben (Konsole, CSV, GUI-Fenster, XML) – vereint in einem Login-Programm mit Rollen.

---

## 1. Worum geht's?

Die fiktive Firma "Heiner IT-Systems" zieht ihre Datenbank um. Verschiedene Abteilungen (Lager, Verwaltung, Marketing, Geschäftsführung) brauchen die Daten in unterschiedlichen Formaten.

Das Projekt besteht aus **5 Pflicht-Dateien** + **1 Bonus** + **1 Hauptprogramm**:

| Datei | Aufgabe |
|---|---|
| `01_ConnectionTest.py` | Verbindung zur DB testen |
| `02_print_SQL_Ausgabe.py` | Mitarbeiter auf Konsole ausgeben |
| `03_DBinCSV.py` | Artikel-Tabelle als CSV exportieren |
| `04_DBausgabeFenster.py` | Kunden-Tabelle in Tkinter-Fenster zeigen |
| `05_csv_to_xml.py` | artikel.csv → artikel.xml konvertieren |
| `06_Bonus_Diagramme.py` | Umsatz-Dashboard (Erweiterung 1.6) |
| `21_dropdown.py` | Hauptprogramm: Flask-Web-App mit Login + RBAC |

---

## 2. Spielregeln (Bibliotheken)

### ✅ Erlaubt im Pflichtteil

| Datei | Bibliothek |
|---|---|
| `01_ConnectionTest.py` | `mariadb` |
| `02_print_SQL_Ausgabe.py` | `mariadb` |
| `03_DBinCSV.py` | `mariadb`, `csv` |
| `04_DBausgabeFenster.py` | `mariadb`, `tkinter` |
| `05_csv_to_xml.py` | `csv`, `xml.etree.ElementTree` |

### ❌ Nicht erlaubt im Pflichtteil
- **pandas**, **sqlalchemy**, **lxml**, **openpyxl**, **PySide6**

### ✅ Erlaubt in der Erweiterung (dokumentiert im Code)

| Datei | Bibliothek | Zweck |
|---|---|---|
| `06_Bonus_Diagramme.py` | `matplotlib` | 3 Diagramme (Kreis + 2x Balken) in Tkinter |
| `21_dropdown.py` | `flask` | Web-Framework für Browser-App |

---

## 3. Setup

```bash
# tkinter installieren (für 04 + 06)
sudo pacman -S tk

# MariaDB lokal starten
sudo systemctl start mariadb

# Flask installieren (für 21_dropdown.py)
pip install flask

# DB importieren
sudo mariadb -u root -p heiner < Datenbank/HeinerIT2025.sql
```

---

## 4. Datei-Übersicht mit Zeilenzahl-Ziel

> **Regel:** Jede Nicht-UI-Datei bleibt unter 40 Zeilen.

| Datei | Zeilen (aktuell) | Ziel |
|---|---|---|
| `config.py` | ~13 | ≤ 20 |
| `01_ConnectionTest.py` | ~28 | ≤ 30 |
| `02_print_SQL_Ausgabe.py` | ~30 | ≤ 30 |
| `03_DBinCSV.py` | ~38 | ≤ 40 |
| `04_DBausgabeFenster.py` | 40 | ≤ 40 |
| `05_csv_to_xml.py` | ~28 | ≤ 30 |
| `06_Bonus_Diagramme.py` | ~181 | Erweiterung – kein Limit |
| `21_dropdown.py` | ~140 | Erweiterung – kein Limit |
| `templates/login.html` | ~131 | UI – kein Limit |
| `templates/app.html` | ~420 | UI – kein Limit |

---

## 5. RBAC-Mapping (Hauptprogramm)

```python
TOOLS = {
    "Lager":             ["f2", "f4"],           # SQL + DB-Tabelle
    "Verwaltung":        ["f2", "f3", "f4"],     # + CSV-Export
    "Marketing":         ["f2", "f4", "f5"],     # + XML-Konvertierung
    "Geschäftsführung":  ["f2", "f3", "f4", "f5"],  # alle Features
}
# Passwort = Abteilungsname (lt. Aufgabenstellung)
```

Bonus-Diagramme (06): nur Geschäftsführung, Zugriff via separatem Tkinter-Login.

---

## 6. Architektur

```
LF9/
├── config.py                  ← DB-Zugangsdaten (DRY-Prinzip)
├── 01_ConnectionTest.py
├── 02_print_SQL_Ausgabe.py
├── 03_DBinCSV.py
├── 04_DBausgabeFenster.py
├── 05_csv_to_xml.py
├── 06_Bonus_Diagramme.py      ← Erweiterung 1.6 (matplotlib + tkinter)
├── 21_dropdown.py             ← Hauptprogramm (flask, startet auf :5000)
├── templates/
│   ├── login.html
│   └── app.html
└── Datenbank/
    └── HeinerIT2025.sql
```

**Wichtig:** `21_dropdown.py` ersetzt das vorgegebene tkinter-Dropdown durch eine Flask-Web-App. Die Bonus-Diagramme laufen weiterhin in `06_Bonus_Diagramme.py` als separates Tkinter-Fenster.

---

## 7. Starten

```bash
# Einzelne Pflicht-Dateien
python 01_ConnectionTest.py      # → "successful"
python 02_print_SQL_Ausgabe.py   # → Mitarbeiterliste
python 03_DBinCSV.py             # → artikel.csv erstellt
python 04_DBausgabeFenster.py    # → Tkinter-Fenster
python 05_csv_to_xml.py          # → artikel.xml erstellt

# Bonus-Diagramme
python 06_Bonus_Diagramme.py     # → Login, dann 3 Diagramme (nur GF)

# Hauptprogramm (Web-App)
python 21_dropdown.py            # → http://localhost:5000
```

---

## 8. Abgabe-Checkliste

- [ ] Lokale MariaDB läuft, DB `heiner` importiert
- [ ] `config.py` mit korrekten Zugangsdaten
- [ ] `01_ConnectionTest.py` → `successful`
- [ ] `02_print_SQL_Ausgabe.py` → Mitarbeiter erscheinen
- [ ] `03_DBinCSV.py` → CSV öffnet sich in LibreOffice
- [ ] `04_DBausgabeFenster.py` → Fenster zeigt Tabelle
- [ ] `05_csv_to_xml.py` → XML ist wohlgeformt
- [ ] `06_Bonus_Diagramme.py` → 3 Diagramme sichtbar (GF-Login)
- [ ] `21_dropdown.py` → Login + alle Features im Browser
- [ ] **Jede** Codezeile mit `#` kommentiert
- [ ] Bibliotheks-Dokumentation in `06` und `21_dropdown.py`
- [ ] PDF-Dokumentation mit Zeit-Tabelle

---

## 9. Bewertung

| Block | Max | Strategie |
|---|---|---|
| Pflichtteil (5 Files + Doku) | 27 P | Sauber, kurz, kommentiert |
| Hauptprogramm (`21_dropdown.py`) | 13 P | Codegerüst-Struktur beachten |
| **Überraschung** (`06_Bonus_Diagramme.py`) | **10 P** | **Sichtbar + erklärt** |
| Testat (Vorführung + 7 Fragen) | 60 P | Jede Datei erklären können |

> **Pro-Tipp fürs Testat:** Unterschied `fetchall()` vs. `fetchone()`, was `cursor.description` zurückgibt, warum CSV `;` statt `,` (Excel-DE), warum `newline=""` beim CSV-Schreiben, was `**DB_LOCAL` macht.
