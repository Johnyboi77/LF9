CREATE TABLE `artikel` (
  `ArtikelNr` int(2) NOT NULL,
  `Artikelname` varchar(36) DEFAULT NULL,
  `LieferantenNr` int(2) DEFAULT NULL,
  `KategorieNr` int(1) DEFAULT NULL,
  `Liefereinheit` varchar(20) DEFAULT NULL,
  `Einzelpreis` decimal(15,2) DEFAULT NULL,
  `Lagerbestand` int(3) DEFAULT NULL,
  `BestellteEinheiten` int(3) DEFAULT NULL,
  `Mindestbestand` int(2) DEFAULT NULL,
  `Auslaufartikel` int(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--Inserts artikel

CREATE TABLE `bestelldetails` (
  `BestellNr` int(5) NOT NULL,
  `ArtikelNr` int(2) NOT NULL,
  `Einzelpreis` decimal(15,2) DEFAULT NULL,
  `Anzahl` int(3) DEFAULT NULL,
  `Rabatt` decimal(2,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--Inserts bestelldetails

CREATE TABLE `bestellung` (
  `BestellNr` int(5) NOT NULL,
  `KundenCode` varchar(5) DEFAULT NULL,
  `PersonalNr` int(3) DEFAULT NULL,
  `Bestelldatum` date DEFAULT NULL,
  `Lieferdatum` date DEFAULT NULL,
  `Versanddatum` date DEFAULT NULL,
  `VersandUeber` int(2) DEFAULT NULL,
  `Frachtkosten` decimal(5,2) DEFAULT NULL,
  `Empfaenger` varchar(50) DEFAULT NULL,
  `Strasse` varchar(50) DEFAULT NULL,
  `Ort` varchar(50) DEFAULT NULL,
  `Region` varchar(50) DEFAULT NULL,
  `PLZ` varchar(20) DEFAULT NULL,
  `Bestimmungsland` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--Inserts bestellung


CREATE TABLE `kategorie` (
  `KategorieNr` int(3) NOT NULL,
  `Kategoriename` varchar(14) DEFAULT NULL,
  `Beschreibung` varchar(38) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--Inserts kategorie


CREATE TABLE `kunde` (
  `KundenCode` varchar(5) NOT NULL,
  `Firma` varchar(36) DEFAULT NULL,
  `Kontaktperson` varchar(23) DEFAULT NULL,
  `Position` varchar(26) DEFAULT NULL,
  `Strasse` varchar(46) DEFAULT NULL,
  `Ort` varchar(15) DEFAULT NULL,
  `Region` varchar(13) DEFAULT NULL,
  `PLZ` varchar(9) DEFAULT NULL,
  `Land` varchar(14) DEFAULT NULL,
  `Telefon` varchar(17) DEFAULT NULL,
  `Telefax` varchar(17) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--Inserts kunde


CREATE TABLE `lieferant` (
  `LieferantenNr` int(2) NOT NULL,
  `Firma` varchar(38) DEFAULT NULL,
  `Kontaktperson` varchar(27) DEFAULT NULL,
  `Position` varchar(30) DEFAULT NULL,
  `Strasse` varchar(46) DEFAULT NULL,
  `Ort` varchar(13) DEFAULT NULL,
  `Region` varchar(8) DEFAULT NULL,
  `PLZ` varchar(8) DEFAULT NULL,
  `Land` varchar(14) DEFAULT NULL,
  `Telefon` varchar(15) DEFAULT NULL,
  `Telefax` varchar(15) DEFAULT NULL,
  `Homepage` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--Inserts lieferant


CREATE TABLE `personal` (
  `PersonalNr` int(3) NOT NULL,
  `Nachname` varchar(15) DEFAULT NULL,
  `Vorname` varchar(15) DEFAULT NULL,
  `Position` varchar(35) DEFAULT NULL,
  `Anrede` varchar(4) DEFAULT NULL,
  `Geburtsdatum` date DEFAULT NULL,
  `Einstellung` date DEFAULT NULL,
  `Strasse` varchar(20) DEFAULT NULL,
  `Ort` varchar(15) DEFAULT NULL,
  `PLZ` varchar(10) DEFAULT NULL,
  `Land` varchar(1) DEFAULT NULL,
  `Telefonprivat` varchar(10) DEFAULT NULL,
  `Durchwahl` int(4) DEFAULT NULL,
  `Bemerkungen` varchar(10) DEFAULT NULL,
  `Vorgesetzt` varchar(3) DEFAULT NULL,
  `Gehalt` decimal(8,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--Inserts personal


CREATE TABLE `spediteur` (
  `SID` int(2) NOT NULL,
  `SpeditionName` varchar(50) DEFAULT NULL,
  `STelefon` varchar(25) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--Inserts spediteur


-- Indizes für die Tabelle `artikel`
--
ALTER TABLE `artikel`
  ADD PRIMARY KEY (`ArtikelNr`),
  ADD KEY `LieferantenNr` (`LieferantenNr`),
  ADD KEY `KategorieNr` (`KategorieNr`);

--
-- Indizes für die Tabelle `bestelldetails`
--
ALTER TABLE `bestelldetails`
  ADD PRIMARY KEY (`BestellNr`,`ArtikelNr`),
  ADD KEY `ArtikelNr` (`ArtikelNr`);

--
-- Indizes für die Tabelle `bestellung`
--
ALTER TABLE `bestellung`
  ADD PRIMARY KEY (`BestellNr`),
  ADD KEY `KundenCode` (`KundenCode`),
  ADD KEY `PersonalNr` (`PersonalNr`),
  ADD KEY `VersandUeber` (`VersandUeber`);

--
-- Indizes für die Tabelle `kategorie`
--
ALTER TABLE `kategorie`
  ADD PRIMARY KEY (`KategorieNr`);

--
-- Indizes für die Tabelle `kunde`
--
ALTER TABLE `kunde`
  ADD PRIMARY KEY (`KundenCode`);

--
-- Indizes für die Tabelle `lieferant`
--
ALTER TABLE `lieferant`
  ADD PRIMARY KEY (`LieferantenNr`);

--
-- Indizes für die Tabelle `personal`
--
ALTER TABLE `personal`
  ADD PRIMARY KEY (`PersonalNr`);

--
-- Indizes für die Tabelle `spediteur`
--
ALTER TABLE `spediteur`
  ADD PRIMARY KEY (`SID`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `artikel`
--
ALTER TABLE `artikel`
  MODIFY `ArtikelNr` int(2) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=81;
--
-- AUTO_INCREMENT für Tabelle `bestellung`
--
ALTER TABLE `bestellung`
  MODIFY `BestellNr` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11078;
--
-- AUTO_INCREMENT für Tabelle `kategorie`
--
ALTER TABLE `kategorie`
  MODIFY `KategorieNr` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT für Tabelle `lieferant`
--
ALTER TABLE `lieferant`
  MODIFY `LieferantenNr` int(2) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;
--
-- AUTO_INCREMENT für Tabelle `personal`
--
ALTER TABLE `personal`
  MODIFY `PersonalNr` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=106;
--
-- AUTO_INCREMENT für Tabelle `spediteur`
--
ALTER TABLE `spediteur`
  MODIFY `SID` int(2) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `artikel`
--
ALTER TABLE `artikel`
  ADD CONSTRAINT `artikel_ibfk_1` FOREIGN KEY (`LieferantenNr`) REFERENCES `lieferant` (`LieferantenNr`),
  ADD CONSTRAINT `artikel_ibfk_2` FOREIGN KEY (`KategorieNr`) REFERENCES `kategorie` (`KategorieNr`);

--
-- Constraints der Tabelle `bestelldetails`
--
ALTER TABLE `bestelldetails`
  ADD CONSTRAINT `bestelldetails_ibfk_1` FOREIGN KEY (`ArtikelNr`) REFERENCES `artikel` (`ArtikelNr`),
  ADD CONSTRAINT `bestelldetails_ibfk_2` FOREIGN KEY (`BestellNr`) REFERENCES `bestellung` (`BestellNr`);

--
-- Constraints der Tabelle `bestellung`
--
ALTER TABLE `bestellung`
  ADD CONSTRAINT `bestellung_ibfk_1` FOREIGN KEY (`KundenCode`) REFERENCES `kunde` (`KundenCode`),
  ADD CONSTRAINT `bestellung_ibfk_2` FOREIGN KEY (`PersonalNr`) REFERENCES `personal` (`PersonalNr`),
  ADD CONSTRAINT `bestellung_ibfk_3` FOREIGN KEY (`VersandUeber`) REFERENCES `spediteur` (`SID`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


