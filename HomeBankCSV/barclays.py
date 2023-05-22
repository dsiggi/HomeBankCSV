from .HomeBankCSV import HomeBankCSV
import openpyxl

class barclays(HomeBankCSV):
    CONV={
        "SEPERATOR": ',',
        "DATUM": 1,
        "EMPFÄNGER": 4,
        "TYP": None,
        "VWZ": 4,
        "KATEGORIE": None,
        "BETRAG": 3,
        "BETRAG_SEPERATOR": True,
        "BETRAG_UMRECHNEN": False,
        "ERSTE_ZEILE": 14,
        "CONVERT": True,
        "ENCODING": "utf-8"
    }

    def Convert2CSV(self):
        """
        Die Eingabedatei wird nach CSV gewandelt.
        In diesem Fall von XLSX zu CSV.
        """
        ## Excel Date öffnen
        xlsx = openpyxl.load_workbook(self.file)
        ## Auf aktuelles Blatt wechseln und die Spalten öffnen
        data = xlsx.active.rows
        csv=""

        for row in data:
            l = list(row)
            for i in range(len(l)):
                if str(l[i].value) == 'None':
                    col = '""'
                else:
                    if i == self.CONV["BETRAG"]:
                        ## Tausender Trennzeichen entfernen
                        col = '"' + str(l[i].value).replace(".", "") + '"'
                    else:
                        col = '"' + str(l[i].value) + '"'
                if i == len(l) - 1:
                    csv = csv + col
                else:
                    csv = csv + col + ','
            csv = csv + '\n'

        return csv

    def get_typ(self, val):
        return "1"
        