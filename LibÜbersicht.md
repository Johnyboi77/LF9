# Bibliotheksübersicht – LF9 Projekt

## Pflichtteil

| Bibliothek | Vollständiger Name | Installation | Verwendungszweck | Eingesetzt in |
|---|---|---|---|---|
| mariadb | MariaDB Connector/Python | `pip3 install mariadb` | Verbindung zu MariaDB-Server aufbauen, SQL-Abfragen ausführen, Ergebniszeilen lesen | ConnectionTest.py, print_SQL_Ausgabe.py, DBinCSV.py, DBausgabeFenster.py |
| csv | csv (Python Standard Library) | keine – standardmäßig in Python enthalten | CSV-Dateien schreiben: Semikolon als Trenner, Spaltenüberschriften als erste Zeile, Datenzeilen aus DB-Ergebnis | DBinCSV.py |
| tkinter | tkinter (Python Standard GUI Library) | `sudo pacman -S tk` (Arch Linux) – standardmäßig in Python enthalten | Grafische Benutzeroberfläche: Fenster, Buttons, Dropdowns (Combobox), Treeview-Tabelle mit Scrollbar | DBausgabeFenster.py, main.py |
| xml.etree.ElementTree | xml.etree.ElementTree (Python Standard Library) | keine – standardmäßig in Python enthalten | XML-Dateien erzeugen und strukturieren: Wurzelelement `<artikel_liste>`, Unterelemente `<artikel>` pro Zeile | csv_to_xml.py |

---

## Bonusteil – BrowserGUI (Flask Web-App)

| Bibliothek | Vollständiger Name | Installation | Verwendungszweck |
|---|---|---|---|
| flask | Flask (Micro Web Framework für Python) | `pip install flask` | Web-Framework: HTTP-Routen definieren, Sessions für Login/Logout, HTML-Templates rendern, Datei-Downloads als Browser-Response senden |
| plotly.js | Plotly.js (JavaScript Charting Library) | keine – via CDN direkt im HTML eingebunden (`<script src="...">`) | Interaktive Diagramme im Browser für die Geschäftsführungs-Ansicht: Donut-Chart (Kunden-Umsatz), Balkendiagramm (Monatsumsatz 2025), horizontales Balkendiagramm (Top-10-Artikel) |
| mariadb | MariaDB Connector/Python | `pip3 install mariadb` (siehe Pflichtteil) | DB-Zugriff identisch zum Pflichtteil – Verbindung, SQL-Abfragen für alle 5 Features und die 3 CEO-Chart-APIs |
| csv, io, xml.etree.ElementTree, sys, pathlib, functools | Python Standard Library | keine – alle standardmäßig enthalten | CSV/XML in-memory erzeugen ohne Dateisystem (io.StringIO/BytesIO), sys.path für Root-Import aus Unterordner, Login-Decorator mit functools.wraps |
