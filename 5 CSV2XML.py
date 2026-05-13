##### CSV-Datei in XML-Format umwandeln #####
# 05_csv_to_xml.py
import csv                                  # CSV-Modul aus Python-Standardbibliothek
import xml.etree.ElementTree as ET          # XML-Modul (ET = ElementTree, alias zur Lesbarkeit)

# Wandelt eine CSV-Datei in ein XML-Dokument um
def csv_to_xml(input_file, output_file):    # input_file = CSV, output_file = XML-Ziel
    root = ET.Element("artikel_liste")      # Wurzel-Element der XML <artikel_liste>
    # CSV öffnen: utf-8 für Umlaute, newline='' wegen Konsistenz beim Lesen
    with open(input_file, newline="", encoding="utf-8") as datei:
        leser = csv.DictReader(datei, delimiter=";")  # ; als Trenner (wie in 1.3 geschrieben)
        for zeile in leser:                 # Jede CSV-Zeile = ein Dictionary {spalte: wert}
            eintrag = ET.SubElement(root, "artikel")  # neues <artikel>-Element unter Wurzel
            for spalte, wert in zeile.items():  # Über alle Spalten der CSV-Zeile iterieren
                # Pro Spalte ein Unter-Element: <Spaltenname>Wert</Spaltenname>
                ET.SubElement(eintrag, spalte).text = wert
    baum = ET.ElementTree(root)             # ElementTree aus Wurzel-Element bauen
    ET.indent(baum, space="  ")             # Sauber einrücken für lesbares XML (Python 3.9+)
    # XML-Datei schreiben mit Deklaration <?xml version="1.0" encoding="utf-8"?>
    baum.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"XML geschrieben: {output_file}")  # Erfolgsmeldung

# Beispiel: CSV-Datei in XML konvertieren
csv_to_xml("artikel.csv", "artikel.xml")    # Eingabe artikel.csv, Ausgabe artikel.xml