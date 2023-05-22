from .HomeBankCSV import HomeBankCSV
import xlrd

class bankofscotland(HomeBankCSV):
    CONV={
        "SEPERATOR": ',',
        "DATUM": 0,
        "EMPFÄNGER": None,
        "TYP": 2,
        "VWZ": 3,
        "KATEGORIE": None,
        "BETRAG": 4,
        "BETRAG_SEPERATOR": False,
        "BETRAG_UMRECHNEN": False,
        "ERSTE_ZEILE": 2,
        "CONVERT": True,
        "ENCODING": "utf-8"
    }

    def Convert2CSV(self):
        """
        Die Eingabedatei wird nach CSV gewandelt.
        In diesem Fall von XLS zu CSV.
        """
        ## Excel Date öffnen
        xls = xlrd.open_workbook(self.file)
        # Blatt öffnen
        sh = xls.sheet_by_index(0)
        csv = ""
        coll=0

        for row in range(sh.nrows):
            for col in range(sh.ncols):
                if coll == self.CONV["VWZ"]:
                    csv = csv + '"'
                    # Nur abarbeiten wenn auch ein VWZ vorhanden ist,
                    # ansonsten wird die Spalte abgeschloßen
                    if sh.cell_value(rowx=row, colx=col).splitlines():
                        for item in sh.cell_value(rowx=row, colx=col).splitlines():
                            csv = csv + item + " - "

                        csv = csv[:-3]
                    csv = csv + '"' + ","
                else:
                    csv = csv + '"' + str(sh.cell_value(rowx=row, colx=col)) + '"' + ','

                coll += 1

            csv = csv + "\n"
            coll = 0

        return csv

    def get_typ(self, val):
        """
        Wandeln des Typs der Transaktion
        """
        if val[self.CONV["TYP"]] == "Gutschrift":
            return "9"
        elif val[self.CONV["TYP"]] == "Überweisung":
            return "4"
        elif val[self.CONV["TYP"]] == "Zinsen":
            return "10"