import csv

class HomeBankCSV(object):
    """
    Dummy-Klasse für das konvertieren der CSV-Datei
    """

    # Konfiguration für die jeweilige Bank
    # Beispiele siehe: barclasy.py, bankofscotland.py, lbb.py, n26.py, old.py
    CONV={
        "SEPERATOR": ',',   # Seperator der in der Originaldatei verwendet wird
        "DATUM": 0, # Spalte in der sich das Datum befindet
        "EMPFÄNGER": 1, # Spalte in der sich der Empfänger befindet
        "TYP": 3, # Spalte in der sich der Typ der Transaktion befindet
        "VWZ": 4, # Spalte in der sich der Verwendungszweck befindet
        "KATEGORIE": 5, # Spalte in der sich die Kategorie befindet
        "BETRAG": 6,    # Spalte in der sich der Betrag befindet
        "BETRAG_SEPERATOR": False,  # Muss der Seperator des Betrags umgewandelt werden? Nötig wenn der Betrag im original durck ein Komma getrennt ist
        "BETRAG_UMRECHNEN": False,  # Muss der Betrag umgerechnet werden? Nötig wenn der Betrag positiv/negativ im original steht aber negativ/positiv sein sollte
        "ERSTE_ZEILE": 2,   # Erste Zeile mit Daten
        "CONVERT": None,    # Muss aus einem fremden Format (z.b. xlst) konvertiert werden? Hier wird das nötige python modul eingetragen
        "ENCODING": "utf-8" # Encoding mit dem die CSV-Datei geöffnet wird
    }

    def __init__(self, file: str):
        """
        Initalisieren der Klasse.
        file: Datei die eingelesen werden soll
        """
        self.file = file
        self.daten = ""
        self.new_csv = []
        self.line = 0
        self.encoding = self.CONV["ENCODING"]

        # Wenn CONVERT nicht None dann wird das passende modul als self.convert_module initalisiert
        # ansonsten wird die CSV-Datei geladen
        if self.CONV["CONVERT"] is not None:
            self.convert_module = __import__(self.CONV["CONVERT"])
            self.daten = self.Convert2CSV()
        else:
            with open(file, newline="", encoding=self.encoding) as openFile:
                # Die komplette Datei wird eingelesen und in einen String gespeichert
                for l in openFile:
                    self.daten = self.daten + l
                    
    def __iter__(self):
        return self

    def __next__(self):
        try:
            out = self.daten.splitlines()[self.line]
            self.line += 1
            return out
        except IndexError:
            self.line = 0
            raise StopIteration

    def Convert2CSV(self):
        """
        Funktion um fremde Formate nach CSV zu wandeln
        Wird in der jeweiligen Klasse der Bank definiert
        """
        return self.daten

    def string2csv(self):
        """
        Funktion die den erstellten String in eine Zeile für
        eine CSV-Datei konvertiert.
        """
        reader = csv.reader(self, delimiter=self.CONV["SEPERATOR"], quotechar='"')

        # Zeilen überspringen bis die erste Zeile mit Daten erreicht wird
        linenumber = 1
        for line in reader:
            if linenumber < self.CONV["ERSTE_ZEILE"]:
                linenumber += 1
                continue
            
            # Aufruf aller nötigen Funktionen zum Bilden der CSV-Datei
            # Aufbau der Zeilen:
            # [DATUM] [TYP] [INFO] [EMPFÄNGER] [VERWENDUNGSZWECK] [BETRAG] [KATEGORIE] [TAGS]
            self.new_csv.append([   self.get_date(line), \
                                    self.get_typ(line), \
                                    "", \
                                    self.get_empf(line), \
                                    self.get_vwz(line), \
                                    self.get_betrag(line), \
                                    self.get_kat(line), \
                                    ""])

    def get_typ(self, val):
        """ 
        Funktion um den Typ der Transaktion zu bestimmen.
        Wird in der Klasse der jeweiligen Bank definiert.
        """
        # Typ 0 = nichts
        # Typ 1 = Kreditkarte
        # Typ 2 = Scheck
        # Typ 3 = Bargeld
        # Typ 4 = Überweisung
        # Typ 6 = Debit-Karte
        # Typ 5 = ???
        # Typ 7 = Dauerauftrag
        # Typ 8 = Elektronische Zahlung
        # Typ 9 = Einzahlung
        # Typ 10 = Bankgebühr
        # Typ 11 = Lastschrift
        return str(0)

    def get_vwz(self, val):
        """
        Funktion die den Verwendungszweck zurück gibt
        val: Aktuelle Zeile als String
        """
        if self.CONV["VWZ"] is None:
            return ""
        else:
            return val[self.CONV["VWZ"]]

    def get_empf(self, val):
        """
        Funktion die den Empfänger zurück gibt
        val: Aktuelle Zeile als String
        """
        if self.CONV["EMPFÄNGER"] is None:
            return ""
        else:
            return val[self.CONV["EMPFÄNGER"]]

    def get_kat(self, val):
        """
        Funktion die die Kategorie zurück gibt
        val: Aktuelle Zeile als String
        """
        if self.CONV["KATEGORIE"] is None:
            return ""
        else:
            return val[self.CONV["KATEGORIE"]]

    def get_betrag(self, val):
        """
        Funktion die den Betrag wandelt und zurück gibt
        val: Aktuelle Zeile als String
        """
        betrag = val[self.CONV["BETRAG"]]
        if self.CONV["BETRAG_SEPERATOR"]:
            betrag = betrag.replace(",", ".")

        if self.CONV["BETRAG_UMRECHNEN"]:
            betrag = str(float(betrag) / -1.0)

        # Prüfe ob der Betrag nun 2 Punkte aufweist
        if betrag.count(".") > 1:
            betrag = betrag.replace(".", "", 1)  

        return betrag

    def get_date(self, val):
        """
        Wandelt das Datum in ein anderes Format um
        """
        return val[self.CONV["DATUM"]]

    def save(self, file):
        """
        Funktion die den CSV-String in eine Datei schreibt.
        file: Ausgabedatei als String
        """
        self.string2csv()
        with open(file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=";", quoting=csv.QUOTE_ALL)
            for line in self.new_csv:
                writer.writerow(line)
