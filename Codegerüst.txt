##### Verbindung zur Datenbank herstellen #####
## Codegerüst kam von Hr. Ullmann

# 01_ConnectionTest.py

import mariadb

# Connect to the MySQL database 
# - definiere hier die Verbindung zur Datenbank


# Die Methode pürft ob eine erfolgreiche Vebrindung zur Datenbank hergesetellt werden kann.
# Ausgabe: gibt succesfull oder fail als print-Ausgabe zurück
def testConnection(dbc):      #dbc steht für die Datenbankverbindung die überprüft werden soll
  # definieren sie hier die Tests und Ausgaben

# Aufruf der Methode zum Testen der Datenbankverbindung
testConnection(db)    

###################################

# 02_print_SQL_Ausgabe.py

import mariadb

# Connect to the MySQL database 
# - definiere hier die Verbindung zur Datenbank
db=

# definiere hier die SQl-Anweisung
sql_Anweisung= 

# gibt nach erfolgreicher Verbindung mit der Datenbank, die Sql-Abfrage zurück
def testprint(dbc, sql_Anweisungc):
    
testprint(db, sql_Anweisung)

# 03_DBinCSV.py

# from ConectionTest import *

### BIBs ###
import mysql.connector
import csv      # 

# MySQL Verbindung zur DB herstellen
db 

tabelle_to_csv(tabellec, dbs):
    
tabelle_to_csv(tabelle, db)

# 04_DBausgabeFenster.py

import tkinter as tk
from tkinter import ttk

#Daten auslesen 
def read_from_database():
    
# Tkinter-Setup
    
def darstellung_tabelle():

darstellung_tabelle()


# 05_csv_to_xml.py
import csv
import xml.etree.ElementTree as ET

def csv_to_xml(input_file, output_file):
    
# Beispiel: SSV-Datei in XML konvertieren
csv_to_xml("daten.csv", "xml_output.xml")


# 21_dropdown.py
import tkinter as tk
from tkinter import ttk #Grafik-Bib
import subprocess # Andere Pythonprgramme ausführen

mitarbeiter_options=["Lager", "Verwaltung", "Marketing", "Geschäftsführung"] # Nutzer Gruppenspezifisch für Login

