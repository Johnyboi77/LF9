##### CSV-Datei in XML-Format umwandeln #####
# csv_to_xml.py
# Autor: Johny | Datum: 2026-05-18
# Zweck: artikel.csv (aus DBinCSV.py) in artikel.xml konvertieren
# Bibliothek: csv (Python-Standard) | xml.etree.ElementTree (Python-Standard)

import csv                                  # CSV-Modul aus Python-Standardbibliothek
import xml.etree.ElementTree as ET          # XML-Modul (ET = Kurzname für ElementTree)

def csv_to_xml(input_file, output_file):    # input_file = CSV-Quelldatei, output_file = XML-Ziel
    root = ET.Element("artikel_liste")      # Wurzel-Element der XML: <artikel_liste>
    with open(input_file, newline="", encoding="utf-8") as datei:  # utf-8 für Umlaute, newline='' für Konsistenz
        leser = csv.DictReader(datei, delimiter=";")  # ; als Trenner (wie in 03 geschrieben)
        for zeile in leser:                 # Jede CSV-Zeile = Dictionary {spalte: wert}
            eintrag = ET.SubElement(root, "artikel")  # Neues <artikel>-Element unter Wurzel
            for spalte, wert in zeile.items():        # Jede Spalte → eigenes XML-Unterelement
                ET.SubElement(eintrag, spalte).text = wert  # <Spaltenname>Wert</Spaltenname>
    baum = ET.ElementTree(root)             # ElementTree aus Wurzel-Element bauen
    ET.indent(baum, space="  ")             # Sauber einrücken für lesbares XML (Python 3.9+)
    baum.write(output_file, encoding="utf-8", xml_declaration=True)  # Mit <?xml ...?> Deklaration schreiben
    print(f"XML geschrieben: {output_file}")  # Erfolgsmeldung

csv_to_xml("artikel.csv", "artikel.xml")   # Eingabe artikel.csv → Ausgabe artikel.xml
