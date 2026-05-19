##### Gemeinsame RBAC-Konfiguration – Dropdown-Menü und Zugriffsrechte #####
# dropdownmenu.py
# Autor: Johny | Datum: 2026-05-19
# Zweck: Zentrale Stelle für Abteilungen, Tools und Zugriffsrechte (DRY-Prinzip)
#        Wird von main.py (Tkinter) und BrowserGUI/app.py (Flask) importiert

# Alle Abteilungen für das Login-Dropdown (lt. Codegerüst Hr. Ullmann)
mitarbeiter_options = ["Lager", "Verwaltung", "Marketing", "Geschäftsführung"]

# Abteilung → erlaubte Skript-Dateien (für Tkinter-Tool-Dropdown in main.py)
TOOLS = {
    "Lager":             ["02_print_SQL_Ausgabe.py", "04_DBausgabeFenster.py"],
    "Verwaltung":        ["02_print_SQL_Ausgabe.py", "03_DBinCSV.py", "04_DBausgabeFenster.py"],
    "Marketing":         ["02_print_SQL_Ausgabe.py", "04_DBausgabeFenster.py", "05_csv_to_xml.py"],
    "Geschäftsführung":  ["02_print_SQL_Ausgabe.py", "03_DBinCSV.py", "04_DBausgabeFenster.py", "05_csv_to_xml.py"],
}

# Alle Features mit Dateiname, Kurzname und Beschreibung (für Feature-Übersicht nach Login)
ALLE_FEATURES = [
    ("02_print_SQL_Ausgabe.py", "SQL-Ausgabe",  "Mitarbeiter anzeigen"),
    ("03_DBinCSV.py",           "CSV-Export",   "Artikel als CSV exportieren"),
    ("04_DBausgabeFenster.py",  "DB-Tabelle",   "Kunden im eigenen Fenster"),
    ("05_csv_to_xml.py",        "XML-Export",   "CSV in XML konvertieren"),
]

# Tools die ein eigenes Fenster öffnen (04) – kein Text-Ausgabe-Bereich in main.py nötig
FENSTER_TOOLS = {"04_DBausgabeFenster.py"}

# Mapping: Skript-Dateiname → Flask-Feature-Schlüssel (für BrowserGUI/app.py)
FILE_TO_FKEY = {
    "02_print_SQL_Ausgabe.py": "f2",
    "03_DBinCSV.py":           "f3",
    "04_DBausgabeFenster.py":  "f4",
    "05_csv_to_xml.py":        "f5",
}

# Abteilung → erlaubte Feature-Keys (aus TOOLS abgeleitet, für Flask-Routen in app.py)
TOOLS_WEB = {
    dept: [FILE_TO_FKEY[f] for f in files]
    for dept, files in TOOLS.items()
}
