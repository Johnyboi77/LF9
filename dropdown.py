##### Dropdown-Konfiguration – Abteilungen, RBAC und Feature-Mapping #####
# dropdown.py
# Autor: Johny | Datum: 2026-05-19
# Zweck: Zentrale Stelle für alle Dropdown-Optionen und Zugriffsrechte (DRY-Prinzip)
#        Wird von main.py (Tkinter) und BrowserGUI/app.py (Flask) importiert

# Alle Abteilungen für das Login-Dropdown (lt. Codegerüst Hr. Ullmann)
mitarbeiter_options = ["Lager", "Verwaltung", "Marketing", "Geschäftsführung"]

# Abteilung → erlaubte Skript-Dateien (für Tkinter-Tool-Dropdown in main.py)
TOOLS = {
    "Lager":             ["print_SQL_Ausgabe.py", "DBausgabeFenster.py"],
    "Verwaltung":        ["print_SQL_Ausgabe.py", "DBinCSV.py", "DBausgabeFenster.py"],
    "Marketing":         ["print_SQL_Ausgabe.py", "DBausgabeFenster.py", "csv_to_xml.py"],
    "Geschäftsführung":  ["print_SQL_Ausgabe.py", "DBinCSV.py", "DBausgabeFenster.py", "csv_to_xml.py"],
}

# Alle Features mit Dateiname, Kurzname und Beschreibung (für Feature-Übersicht nach Login)
ALLE_FEATURES = [
    ("print_SQL_Ausgabe.py", "SQL-Ausgabe",  "Mitarbeiter anzeigen"),
    ("DBinCSV.py",           "CSV-Export",   "Artikel als CSV exportieren"),
    ("DBausgabeFenster.py",  "DB-Tabelle",   "Kunden im eigenen Fenster"),
    ("csv_to_xml.py",        "XML-Export",   "CSV in XML konvertieren"),
]

# Tools die ein eigenes Fenster öffnen – kein Textausgabe-Bereich in main.py nötig
FENSTER_TOOLS = {"DBausgabeFenster.py"}

# Mapping: Skript-Dateiname → Flask-Feature-Schlüssel (für BrowserGUI/app.py)
FILE_TO_FKEY = {
    "print_SQL_Ausgabe.py": "f2",
    "DBinCSV.py":           "f3",
    "DBausgabeFenster.py":  "f4",
    "csv_to_xml.py":        "f5",
}

# Abteilung → erlaubte Feature-Keys (aus TOOLS abgeleitet, für Flask-Routen in app.py)
TOOLS_WEB = {
    dept: [FILE_TO_FKEY[f] for f in files]
    for dept, files in TOOLS.items()
}
