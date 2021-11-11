from .HomeBankCSV import HomeBankCSV

class lbb(HomeBankCSV):
    CONV={
        "SEPERATOR": ';',
        "DATUM": 1,
        "EMPFÄNGER": 3,
        "TYP": None,
        "VWZ": None,
        "KATEGORIE": 4,
        "BETRAG": 8,
        "BETRAG_SEPERATOR": True,
        "BETRAG_UMRECHNEN": True,
        "ERSTE_ZEILE": 3,
        "CONVERT": None,
        "ENCODING": "utf-8"
    }

    def get_typ(self, val):
        """
        Alle Transaktion sind "Kreditkarte"
        """
        return "1"
