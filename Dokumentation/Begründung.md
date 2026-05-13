# LF9 – Begründungs-Dokumentation der Quellcode-Entscheidungen

> Pro Datei eine Tabelle mit den "Warum X statt Y"-Begründungen.
> Hilfreich für die Projekt-Doku (1.7) und das mündliche Testat (7 individuelle Fragen).

---

## 1.1 – `01_ConnectionTest.py`

| Frage | Antwort |
|---|---|
| Warum `try/except` statt einfachem `mariadb.connect()`? | Ohne Fehlerbehandlung würde das Skript bei falschem Passwort oder ausgeschaltetem Server mit einem hässlichen Traceback abstürzen. So wird der Fehler aufgefangen und als lesbarer Text ausgegeben. |
| Warum der `**DB_LOCAL`-Sternoperator? | `**` packt das Dictionary aus, sodass `host="...", port=..., user="..."` als einzelne Keyword-Argumente an `connect()` übergeben werden. Saubere Trennung von Daten (config.py) und Code. |
| Warum `dbc.ping()` zum Testen statt nur die Existenz der Verbindung prüfen? | `ping()` sendet ein echtes Signal an den DB-Server. Das prüft, ob die Verbindung **gerade jetzt** noch lebt – die Verbindung könnte z.B. nach Timeout vom Server geschlossen worden sein. Pure Existenz von `db` reicht nicht. |
| Warum eine zentrale `config.py` statt Zugangsdaten direkt im Code? | DRY-Prinzip: Wenn das Passwort sich ändert, muss man es nur an EINER Stelle anpassen, nicht in 5 Dateien. Außerdem kann man `config.py` aus Git ausschließen, ohne den Code zu verlieren. |
| Warum `mariadb` und nicht `mysql.connector`? | Vorgabe aus PDF "01_Informationen". MariaDB-Bibliothek ist speziell für MariaDB-Server optimiert, während `mysql.connector` der MySQL-Konzern-Connector ist. |
| Warum prüfen, ob `dbc is None` ist, bevor `ping()` aufgerufen wird? | Wenn der Verbindungsaufbau im `try` fehlgeschlagen ist, ist `db = None`. Ohne diese Prüfung würde `None.ping()` einen `AttributeError` werfen. |

---

## 1.2 – `02_print_SQL_Ausgabe.py`

| Frage | Antwort |
|---|---|
| Warum `cursor.fetchall()` statt `fetchone()` in einer Schleife? | `fetchall()` holt alle Ergebnisse in einem Rutsch in den RAM. Bei 20 Zeilen problemlos. Bei Millionen Zeilen wäre `fetchone()` oder Iteration über den Cursor besser (weniger Speicher). |
| Warum `cur.close()` im `finally`-Block? | Damit der Cursor auch dann geschlossen wird, wenn die Query einen Fehler wirft. Sonst bleiben DB-Ressourcen offen – auf Dauer crasht der Server. |
| Warum `SELECT * FROM personal` statt einzelne Spalten? | Aufgabenstellung: "alle Mitarbeiter ausgeben". `*` ist hier richtig. In Produktivcode wäre explizit besser (klar dokumentiert, robust gegen Schema-Änderungen), aber für diese Aufgabe ist `*` korrekt. |
| Warum die Variable außerhalb der Funktion definieren (`db`, `sql_Anweisung`)? | So vorgegeben durch das Codegerüst der Lehrkraft. Eigentlich wäre es sauberer, alles in die Funktion zu kapseln. |
| Warum `print(zeile)` statt formatierte Ausgabe? | Aufgabenstellung verlangt die Roh-Tupel-Darstellung (siehe PDF-Screenshot). Spätere Formatierung passiert im GUI (Aufgabe 1.4). |

---

## 1.3 – `03_DBinCSV.py`

| Frage | Antwort |
|---|---|
| Warum `mariadb` statt `mysql.connector` wie im Codegerüst? | Das Codegerüst enthält einen Widerspruch zur Aufgabenstellung. PDF "01_Informationen" listet `mariadb` als einzig erlaubte DB-Lib. Korrektur dokumentiert. |
| Warum `;` als CSV-Trenner statt `,`? | Deutsche Excel/LibreOffice-Locale erwartet `;`, weil `,` als Dezimaltrennzeichen reserviert ist. Mit `,` würden Beträge wie "46,00" die Spaltenstruktur kaputtmachen. |
| Warum `encoding="utf-8"` explizit angeben? | Ohne Angabe nutzt Python das OS-Default-Encoding (Linux: UTF-8, Windows: cp1252). Bei Windows-User würden Umlaute (ü, ä, ö, ß) als Mojibake erscheinen. |
| Warum `newline=""` beim Öffnen der CSV? | Verhindert dass Python und das CSV-Modul beide ein Zeilenende einfügen → sonst leere Zeilen zwischen den Datensätzen unter Windows. |
| Warum `cursor.description` für die Header-Zeile? | Dynamisch: Funktioniert für jede Tabelle, ohne Spaltennamen zu hardcoden. Wenn Schema sich ändert, passt sich der Export automatisch an. |
| Warum `f"SELECT * FROM {tabellec}"` (f-String) statt parametrisierte Query? | Tabellennamen können in SQL nicht parametrisiert werden (nur Werte). Da `tabellec` aus unserem eigenen Code kommt (kein User-Input), kein SQL-Injection-Risiko. |
| Warum `with open(...) as datei:` statt manuelles Schließen? | Context Manager schließt die Datei automatisch – auch bei Fehlern. Pythonischer und kürzer als `try/finally`. |
| Warum `writer.writerows(daten)` statt Schleife mit `writerow()`? | `writerows()` ist intern optimiert und kürzer. Macht dasselbe wie eine For-Schleife, nur in einer Zeile. |

---

## 1.4 – `04_DBausgabeFenster.py`

| Frage | Antwort |
|---|---|
| Warum `ttk.Treeview` statt `tk.Listbox`? | Listbox kann nur eine Spalte. Treeview unterstützt mehrere Spalten mit Headern – sieht aus wie eine Excel-Tabelle. Perfekt für tabellarische Daten. |
| Warum `show="headings"`? | Tkinter zeigt standardmäßig eine zusätzliche Spalte "#0" links für Baumstrukturen (Tree). Da wir eine reine Tabelle wollen, blendet `"headings"` diese Spalte aus. |
| Warum die DB-Verbindung in `read_from_database()` öffnen UND schließen, statt sie global zu halten? | Separation of Concerns: Die GUI-Funktion soll sich nicht um DB-Lifecycle kümmern. Plus: Wenn das Fenster lange offen ist, halten wir keine DB-Verbindung unnötig offen. |
| Warum `mainloop()` ganz am Ende? | Startet die Event-Loop, die auf Klicks/Scrolls reagiert. Ohne diese Zeile öffnet sich das Fenster und schließt sich sofort wieder. Blockiert das Skript, bis das Fenster geschlossen wird. |
| Warum dynamische Spalten aus `cursor.description`? | Tabelle ist in einer Variable austauschbar (z.B. `kunde` → `personal`). Spalten passen sich automatisch an, ohne dass jemand den GUI-Code anfassen muss. |
| Warum eine Scrollbar? | Treeview hat zwar internen Scroll, aber kein sichtbares Bedienelement. Bei 91 Kundenzeilen braucht der User die visuelle Scrollbar zur Orientierung. |
| Warum `fill="both", expand=True`? | Damit die Tabelle bei Fenstergrößen-Änderung mitwächst und nicht in der Ecke kleben bleibt. UX-Detail, das einen großen Unterschied macht. |
| Warum `ttk.Scrollbar` und nicht `tk.Scrollbar`? | `ttk` = "themed tk" sieht moderner aus und passt zum Treeview (auch `ttk`). Mischen von `tk` und `ttk` führt zu Style-Brüchen. |

---

## 1.5 – `05_csv_to_xml.py`

| Frage | Antwort |
|---|---|
| Warum `DictReader` statt `csv.reader`? | DictReader nutzt automatisch die erste Zeile (Header) als Spaltennamen. So müssen wir Spalten nicht hardcoden – CSV-Zeile wird zu Dictionary `{spalte: wert}`. |
| Warum `xml.etree.ElementTree` statt `lxml` oder `xmltodict`? | Standardbibliothek – kein `pip install` nötig. Vorgabe der Aufgabenstellung. Funktioniert für unsere Anforderung absolut ausreichend. |
| Was ist der Unterschied zwischen `ET.Element` und `ET.SubElement`? | `Element` erstellt ein eigenständiges Element ohne Parent. `SubElement` erstellt UND hängt es direkt an ein vorhandenes Parent-Element. Spart eine separate `parent.append()`-Zeile. |
| Warum `ET.indent()`? | Ohne wäre das XML in einer einzigen langen Zeile – technisch korrekt, aber für Menschen unlesbar. `indent()` fügt Zeilenumbrüche und Einrückungen ein (verfügbar ab Python 3.9). |
| Warum `xml_declaration=True`? | Schreibt die `<?xml version="1.0" encoding="utf-8"?>` Zeile am Anfang. Best Practice für valides XML, manche Parser verweigern XML ohne Deklaration. |
| Warum den Tag-Namen `artikel` und `artikel_liste` und nicht generisch `eintrag` und `daten`? | Selbsterklärende Tag-Namen machen die XML-Datei ohne Schema-Doku verständlich. "Sprich, was du tust" – wichtig wenn andere Systeme das XML konsumieren. |

---

## 1.6 – `06_Umsatz_Dashboard.py`

| Frage | Antwort |
|---|---|
| Warum **eine** `lade_daten(sql)`-Funktion statt 3 separater Funktionen? | DRY-Prinzip: Connect, Cursor, Execute, Fetch, Close ist für alle 3 Queries identisch. Code wird kompakter und Wartung leichter (z.B. Logging hinzufügen = 1× ändern). |
| Warum die SQL-Queries als Konstanten ganz oben in der Datei? | Trennung von Daten und Logik: SQL kann von einem DB-Spezialisten optimiert werden, ohne den GUI-Code anzufassen. Auch bessere Lesbarkeit – alle Queries auf einen Blick. |
| Warum `ZUGRIFFSBERECHTIGTE` als `set` statt als `list`? | `in`-Prüfung ist bei Sets O(1) statt O(n) bei Listen – schneller bei vielen Rollen. Zusätzlich: Duplikate sind in Sets unmöglich, was Bugs vorbeugt. |
| Warum `ttk.Notebook` (Tabs) statt 3 separate Buttons oder Fenster? | Standard-UX-Pattern für mehrere zusammengehörige Ansichten. Ein Fenster = übersichtlich, kein Fenster-Chaos. Tab-Wechsel ist intuitiver als Buttons. |
| Warum Donut-Style (`wedgeprops=dict(width=0.4)`) statt Vollkreis? | Modernere Optik. Außerdem: Im hohlen Zentrum könnte man optional die Gesamtsumme anzeigen. Vollkreis-Pies sind in Business-Dashboards "out". |
| Warum `FigureCanvasTkAgg`? | Brücke zwischen matplotlib (Renderer) und Tkinter (GUI-Framework). Ohne Adapter könnte matplotlib nur eigene Fenster aufmachen, nicht in unser Tkinter einbetten. |
| Warum `float(d[1])` bei den Umsätzen? | `mariadb` gibt `DECIMAL`-Werte als Python `decimal.Decimal` zurück. matplotlib kann nur `float` rendern. Konvertierung verhindert `TypeError`. |
| Warum `tight_layout()`? | Berechnet automatisch optimale Ränder, damit Labels nicht aus dem Diagramm rausragen oder sich überlappen. Spart manuelle `subplots_adjust()`-Frickelei. |
| Warum `invert_yaxis()` beim horizontalen Top-10-Balkendiagramm? | matplotlib zeichnet Y-Achse standardmäßig von unten nach oben. Top 1 würde unten landen → Lese-Intuition ist aber "von oben". Inversion korrigiert das. |
| Warum `ax.annotate()` mit Beträgen an den Balken statt nur Achsen-Labels? | Genaue Werte direkt am Balken, kein Augenmaß-Schätzen anhand der Skala nötig. Standard in Business-Reports (Tableau, PowerBI). |
| Warum `DATE_FORMAT(b.Bestelldatum, '%Y-%m')` statt `YEAR()` und `MONTH()` separat? | Ergibt einen einzelnen sortierbaren String wie `"1996-07"`. Bei getrennten Spalten müsste man im Python-Code nochmal zusammenpuzzeln und sortieren. |
| Warum "Top 5 + Sonstige" statt alle Kunden im Kreisdiagramm? | Bei 91 Kunden wären die Slices unleserlich klein. Top 5 + Sonstige ist die Standard-Aggregation für Pie-Charts in der Datenvisualisierung (z.B. Pareto-Prinzip 80/20). |
| Warum die SQL-Joins über 3 Tabellen (`kunde` → `bestellung` → `bestelldetails`)? | Der Umsatz ist erst aus `bestelldetails` (Anzahl × Preis × (1-Rabatt)) zu berechnen. Die Zuordnung zum Kunden geht aber nur über `bestellung` (die `KundenCode` enthält). |
| Warum `(1 - Rabatt)` und nicht `Rabatt`? | `Rabatt` ist als Anteil (z.B. 0.15 = 15%) gespeichert. Der bezahlte Betrag ist deshalb `Anzahl × Preis × (1 - 0.15) = 85% des Brutto`. |
| Warum `for widget in fenster.winfo_children(): widget.destroy()` beim Login-Erfolg? | Anstatt ein neues Fenster zu öffnen, "räumen" wir das aktuelle aus und befüllen es neu. Vermeidet Fenster-Chaos. |
| Warum `bind("<Return>", ...)` zusätzlich zum Login-Button? | Aufgabenstellung 2.1 verlangt explizit Enter-Bestätigung. Plus: UX – User erwarten Enter in Login-Feldern. |
| Warum `show="*"` beim Passwort-Feld? | Standard-Sicherheits-UX: Maskiert die Eingabe mit Sternchen. Verhindert "Shoulder Surfing". |
| Warum 3 Tabs statt aller Diagramme untereinander mit Scrollbar? | Tabs sind kognitiv leichter zu verarbeiten (eine Sache zur Zeit). Plus: jedes Diagramm kann die volle Fenstergröße nutzen. |
| Warum die Diagramm-Erstellung **innerhalb** der Tab-Funktion statt vorab im Hintergrund? | Lazy Loading: Diagramme werden erst gerendert, wenn der User den Tab öffnet → schnellere Initial-Anzeige. Aktuell sind alle gleich gerendert, aber Architektur erlaubt das Refactoring. |

---

## Cross-cutting Konzepte (für die "7 individuellen Fragen" im Testat)

| Konzept | Wo angewendet | Warum sinnvoll |
|---|---|---|
| **DRY (Don't Repeat Yourself)** | `config.py`, `lade_daten(sql)` | Änderungen an einer Stelle propagieren überall. Weniger Bugs. |
| **Separation of Concerns** | DB-Logik vs. GUI vs. Berechtigung getrennt | Jede Funktion macht eine Sache → leichter zu testen und zu erweitern. |
| **Defensive Programmierung** | `if dbc is None`, `try/finally` | Nie davon ausgehen, dass alles funktioniert. Externer Ressourcen (DB, Dateien) immer absichern. |
| **RBAC (Role-Based Access Control)** | `ZUGRIFFSBERECHTIGTE` Set | Industriestandard für Berechtigungen (SAP, AD, AWS IAM). Statt If-Else-Chaos. |
| **Lazy vs. Eager Loading** | `fetchall()` (eager) vs. Cursor-Iteration (lazy) | Trade-off zwischen RAM-Verbrauch und Code-Klarheit. Bei kleinen Datenmengen ist eager okay. |
| **UTF-8 durchgängig** | DB-Charset, CSV, XML | Vermeidet "ü → ü"-Probleme über Systemgrenzen hinweg. |

---

## Quellen / Weiterführende Doku

- Python `csv`-Modul: https://docs.python.org/3/library/csv.html
- Python `xml.etree.ElementTree`: https://docs.python.org/3/library/xml.etree.elementtree.html
- MariaDB Python Connector: https://mariadb-corporation.github.io/mariadb-connector-python/
- Tkinter Treeview: https://docs.python.org/3/library/tkinter.ttk.html#treeview
- matplotlib Pie & Bar: https://matplotlib.org/stable/gallery/index.html